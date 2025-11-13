"""
This model provides pure functions that extract Amberflo Meter Events from
LiteLLM's Standard Logging Payload objects.
"""

import re
from urllib.parse import urlparse

from .utils import get_env


_unknown = "unknown"
_global = "global"
_n = "n"
_hosted_env = get_env("AFLO_HOSTED_ENV", _unknown)


def extract_events_from_log(log):
    metadata = log["metadata"]
    usage = metadata["usage_object"]

    request_id = log["id"]
    request_time_ms = round(log["startTime"] * 1000)
    request_duration_ms = round((log["endTime"] - log["startTime"]) * 1000)

    business_unit_id = _get_business_unit_id(metadata) or _unknown

    provider, model = _resolve_provider_model(log)

    model_info = log["model_map_information"]["model_map_value"]

    if model_info:
        sku = model_info["key"]
        platform = model_info["litellm_provider"]
    else:
        # happens on error scenarios
        sku = _unknown
        platform = _unknown

    batch = "y" if log["hidden_params"]["batch_models"] else _n

    usecase = log["call_type"]

    key_name = metadata.get("user_api_key_alias") or _unknown

    user = metadata.get("user_api_key_user_id") or _unknown

    region = _resolve_region(platform, log) or _global

    ## ERRORS
    error_details = _extract_error_details(log["error_information"])

    error_code = error_details["code"] if error_details else _n

    ## TOKENS (unit, quantity, type, cache)
    # TODO implement "cache"
    # TODO implement units other than "token"
    tokens = []

    if usage.get("prompt_tokens", 0) > 0:
        tokens.append(("token", usage["prompt_tokens"], "in", _n))

    if usage.get("completion_tokens", 0) > 0:
        tokens.append(("token", usage["completion_tokens"], "out", _n))

    # TODO implement "tier"
    tier = _n

    pricing_dimensions = {
        "sku": sku,
        "tier": tier,
        "batch": batch,
    }

    dimensions = {
        "business_unit_id": business_unit_id,
        "hosted_env": _hosted_env,
        "key_name": key_name,
        "model": model,
        "platform": platform,
        "provider": provider,
        "region": region,
        "usecase": usecase,
        "user": user,
    }

    base_event = {
        "meterTimeInMillis": request_time_ms,
        "uniqueId": request_id,
    }

    events = [
        {
            **base_event,
            "meterApiName": "llm_api_call",
            "meterValue": 1,
            "dimensions": { **dimensions, **pricing_dimensions, "error_code": error_code }
        },
        {
            **base_event,
            "meterApiName": "llm_api_call_ms",
            "meterValue": request_duration_ms,
            "dimensions": { **dimensions, **pricing_dimensions, "error_code": error_code }
        },
    ]

    for unit, quantity, in_out, cache in tokens:
        events.append(
            {
                **base_event,
                "meterApiName": _get_meter_name(unit),
                "meterValue": quantity,
                "dimensions": { **dimensions, **pricing_dimensions, "type": in_out, "cache": cache },
            }
        )

    if error_details:
        events.append(
            {
                **base_event,
                "meterApiName": "llm_error_details",
                "meterValue": 1,
                "dimensions": { **dimensions, **error_details }
            }
        )

    return events


def _resolve_region(platform, log):
    if platform == "bedrock":
        return _get_api_base_domain_part(log, 1)

    # TODO test these
    if platform in ("azure", "google"):
        return _get_api_base_domain_part(log, 0)

    return None


def _get_business_unit_id(metadata):
    """
    We support two conventions:
    1. Set the `business_unit_id` as a custom metadata in the User or Team objects.
    2. Set the Team ID to be the `business_unit_id`
    """
    buid = metadata.get("user_api_key_auth_metadata", {}).get("business_unit_id")
    return buid or metadata.get("user_api_key_team_id")


def _get_api_base_domain_part(log, index):
    api_base = log["api_base"]

    if api_base:
        hostname = urlparse(api_base).hostname
        if hostname:
            parts = hostname.split(".")
            return parts[index]

    return None


def _resolve_provider_model(log):
    provider, model = log["custom_llm_provider"], log["model"]

    if provider != "openai" and "." in model:
        provider, model = model.split(".", 1)

    return provider, model


def _get_meter_name(unit):
    if unit == "query":
        unit = "queries"

    elif unit == "token":
        unit = "text_token"

    return f"llm_{unit}s"


_openai_429_error_regex = r"Rate limit reached .* on .*\(([^:]+)\): Limit (\d+)"

_litellm_429_error_regex = (
    r"Rate limit exceeded for (\w+):.+Limit type: (\w+).+Current limit: (\d+)"
)


def _extract_error_details(error_info):
    if not error_info["error_class"]:
        return None

    error = {
        "class": error_info["error_class"],
        "code": error_info["error_code"],
    }

    if error["code"] == "429":
        message = error_info["error_message"]

        if error_info["llm_provider"] == "openai":
            match = re.search(_openai_429_error_regex, message)
            if match:
                error["subject"] = "provider"
                error["rate"] = match.group(1).lower()
                error["limit"] = match.group(2)

        else:
            match = re.search(_litellm_429_error_regex, message)
            if match:
                error["subject"] = match.group(1)

                limit_type = match.group(2)
                error["rate"] = "rpm" if limit_type == "requests" else "tpm"

                error["limit"] = match.group(3)

    return error
