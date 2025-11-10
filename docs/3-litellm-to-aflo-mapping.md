
# LiteLLM Log to Amberflo Meter Event Mapping

This document defines the mapping logic from LiteLLM standardized log entries to Amberflo meter events.

## Overview

LiteLLM generates standardized log entries that contain detailed usage information. These logs are transformed into Amberflo meter events with specific dimensions and values to enable precise billing and analytics.

## Core Mapping Logic

### Token-Based Meters

#### Completion/Output Tokens (Type: "out")
All completion tokens map to meter dimension `"type": "out"`

| LiteLLM Log Path | Amberflo Meter API Name | Unit | Description |
|------------------|-------------------------|------|-------------|
| `metadata.usage_object.completion_tokens_details.audio_tokens` | `llm_audio_tokens` | tokens | Audio output tokens |
| `metadata.usage_object.completion_tokens_details.reasoning_tokens` | `llm_reasoning_tokens` | tokens | Reasoning/thinking tokens |
| `metadata.usage_object.completion_tokens_details.text_tokens` | `llm_text_tokens` | tokens | Text output tokens |
| `metadata.usage_object.completion_tokens_details.citation_tokens` | `llm_citation_tokens` | tokens | Citation tokens |
| `metadata.usage_object.completion_tokens_details.image_tokens` | `llm_image_tokens` | tokens | Image generation tokens |

#### Prompt/Input Tokens (Type: "in")
All prompt tokens map to meter dimension `"type": "in"`

| LiteLLM Log Path | Amberflo Meter API Name | Unit | Description |
|------------------|-------------------------|------|-------------|
| `metadata.usage_object.prompt_tokens_details.audio_tokens` | `llm_audio_tokens` | tokens | Audio input tokens |
| `metadata.usage_object.prompt_tokens_details.text_tokens` | `llm_text_tokens` | tokens | Text input tokens |
| `metadata.usage_object.prompt_tokens_details.image_tokens` | `llm_image_tokens` | tokens | Image processing tokens |

### Time-Based Meters

| LiteLLM Log Path | Amberflo Meter API Name | Unit | Description |
|------------------|-------------------------|------|-------------|
| `endTime - startTime` (calculated) | `llm_seconds` | seconds | Total request duration |
| Audio processing duration | `llm_audio_seconds` | seconds | Audio processing time |
| Video processing duration | `llm_video_seconds` | seconds | Video processing time |

### Request/Count-Based Meters

| LiteLLM Log Path | Amberflo Meter API Name | Unit | Description |
|------------------|-------------------------|------|-------------|
| Per request (always 1) | `llm_requests` | requests | Request count |

### Other Metrics

| LiteLLM Log Path | Amberflo Meter API Name | Unit | Description |
|------------------|-------------------------|------|-------------|
| Character count | `llm_characters` | characters | Character usage |
| Image dimensions | `llm_pixels` | pixels | Image pixel count |

## Dimension Mapping

### `business_unit_id`

This Business Unit ID value is taken from the custom Team metadata, `business_unit_id`, exposed in the log field `metadata.user_api_key_auth_metadata`. This can be set when editting the Team in the LiteLLM UI.

If this metadata is not set, then the Team ID, exposed in the log field `metadata.user_api_key_team_id`, is used).

### Core Dimensions

| LiteLLM Log Field | Amberflo Dimension | Description |
|-------------------|-------------------|-------------|
| `call_type` | `usecase` | API endpoint type (acompletion, aembedding, etc.) |
| `custom_llm_provider` | `platform` | Provider name (openai, anthropic, bedrock, etc.) |
| `model` | `model` | Model identifier |
| `model_map_information.model_map_key` | `sku` | Specific model SKU/version identifier |
| `user` | `user` | End user identifier |
| `metadata.user_api_key_alias` | `keyName` | API key name |

### Token Type Dimension

| Token Source | Type Dimension Value |
|--------------|---------------------|
| `completion_tokens_details.*` | `"out"` |
| `prompt_tokens_details.*` | `"in"` |

### Additional Dimensions

| Dimension | Possible Values | Source |
|-----------|----------------|--------|
| `provider` | Various | Environment/platform identifier |
| `batch` | `"y"`, `"n"` | Whether request was batched |
| `hostedEnv` | Environment name | Deployment environment |
| `region` | AWS/Azure regions | Extracted from API base URL |
| `type` | `"in"`, `"out"` | Token direction (see above) |
| `tier` | `"flex"`, `"priority"`, `"n"` | tier level |
| `cache` | `"r"`, `"c"`, `"n"` | Cache usage status |

## Example Transformation

### Input LiteLLM Log
```json
{
  "request_id": "req-123",
  "call_type": "acompletion",
  "custom_llm_provider": "openai",
  "model": "gpt-4o",
  "startTime": 1728691389.851645,
  "endTime": 1728691391.922394,
  "metadata": {
    "user_api_key_team_alias": "engineering",
    "user_api_key_alias": "prod-key",
    "usage_object": {
      "completion_tokens_details": {
        "audio_tokens": 150,
        "text_tokens": 45
      },
      "prompt_tokens_details": {
        "text_tokens": 120
      }
    }
  }
}
```

### Output Amberflo Meter Events
```json
[
  {
    "uniqueId": "req-123",
    "meterApiName": "llm_audio_tokens",
    "meterValue": 150,
    "meterTimeInMillis": 1728691391922,
    "dimensions": {
      "business_unit_id": "engineering",
      "provider": "openai",
      "model": "gpt-4o",
      "usecase": "acompletion",
      "keyName": "prod-key",
      "type": "out"
    }
  },
  {
    "uniqueId": "req-123",
    "meterApiName": "llm_text_tokens",
    "meterValue": 45,
    "meterTimeInMillis": 1728691391922,
    "dimensions": {
      "business_unit_id": "engineering",
      "provider": "openai",
      "model": "gpt-4o",
      "usecase": "acompletion",
      "keyName": "prod-key",
      "type": "out"
    }
  },
  {
    "uniqueId": "req-123",
    "meterApiName": "llm_text_tokens",
    "meterValue": 120,
    "meterTimeInMillis": 1728691389851,
    "dimensions": {
      "business_unit_id": "engineering",
      "provider": "openai",
      "model": "gpt-4o",
      "usecase": "acompletion",
      "keyName": "prod-key",
      "type": "in"
    }
  }
]
```
