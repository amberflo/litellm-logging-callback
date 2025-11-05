"""
This model provides pure functions that extract Amberflo Meter Events from
LiteLLM's Standard Logging Payload objects.
"""

from urllib.parse import urlparse

from .utils import get_env


_unknown = "unknown"
_global = "global"
_hosted_env = get_env("AFLO_HOSTED_ENV", _unknown)


def extract_events_from_log(log):
    # TODO consider metering errors
    if log["error_information"]["error_class"]:
        return

    metadata = log["metadata"]
    usage = metadata["usage_object"]

    request_id = log["id"]
    request_time_ms = round(log["startTime"] * 1000)
    request_duration_ms = round((log["endTime"] - log["startTime"]) * 1000)

    business_unit_id = metadata.get("user_api_key_team_alias") or _unknown

    provider, model = _resolve_provider_model(log)

    model_info = log["model_map_information"]["model_map_value"]

    sku = model_info["key"]
    platform = model_info["litellm_provider"]

    batch = "y" if log["hidden_params"]["batch_models"] else "n"

    usecase = log["call_type"]

    key_name = metadata.get("user_api_key_alias") or _unknown

    user = metadata.get("user_api_key_user_id") or _unknown

    region = _resolve_region(platform, log) or _global

    # (unit, quantity, type, cache)
    tokens = []

    if usage.get("prompt_tokens", 0) > 0:
        tokens.append(("token", usage["prompt_tokens"], "in", "n"))

    if usage.get("completion_tokens", 0) > 0:
        tokens.append(("token", usage["completion_tokens"], "out", "n"))

    dimensions = dict(
        # pricing dimensions
        sku=sku,
        tier="n",  # TODO
        cache="n",  # TODO
        batch=batch,
        # other dimensions
        business_unit_id=business_unit_id,
        hosted_env=_hosted_env,
        key_name=key_name,
        model=model,
        platform=platform,
        provider=provider,
        region=region,
        usecase=usecase,
        user=user,
    )

    base_event = {
        "meterTimeInMillis": request_time_ms,
        "uniqueId": request_id,
    }

    events = [
        {
            **base_event,
            "meterApiName": "llm_api_call",
            "meterValue": 1,
            "dimensions": dimensions,
        },
        {
            **base_event,
            "meterApiName": "llm_api_call_ms",
            "meterValue": request_duration_ms,
            "dimensions": dimensions,
        },
    ]

    for unit, quantity, in_out, cache in tokens:
        events.append(
            {
                **base_event,
                "meterApiName": _get_meter_name(unit),
                "meterValue": quantity,
                "dimensions": {**dimensions, "type": in_out, "cache": cache},
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
