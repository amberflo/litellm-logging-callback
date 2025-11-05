#!/bin/bash
#
# This script contains sample API calls to LiteLLM, in order to test a variety
# of scenarios regarding the Amberflo meter events capture.
#
# The goal is twofold:
# - to help produce the standard log objects JSONs in the ./resources/
# - to serve as a manual end-to-end test scenario.

API_KEY='...'

call() {
    local method="$1"
    shift
    local path="$1"
    shift

    echo "$method /$path"

    curl -s -X "$method" "http://localhost:4000/$path" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $API_KEY" \
        "$@" | jq
}

# list models available for this key
call GET 'v1/models'

# invalid model
call POST 'v1/chat/completions' -d '{ "model": "gpt-4", "messages": [{"role": "user", "content": "Say hello in French"}] }'

# openai text completion
call POST 'v1/chat/completions' -d '{ "model": "gpt-4o", "messages": [{"role": "user", "content": "Say hello in French"}] }'

# openai text embeddings
call POST 'v1/embeddings' -d '{ "model": "text-embedding-ada-002", "input": "The quick brown fox jumps over the lazy dog" }'

# bedrock text completion
call POST 'v1/chat/completions' -d '{ "model": "anthropic.claude-3-5-haiku-20241022-v1:0", "messages": [{"role": "user", "content": "Say hello in Japanese"}] }'

# anthropic text completion
call POST 'v1/chat/completions' -d '{ "model": "anthropic.claude-3-5-sonnet-20241022-v2:0", "messages": [{"role": "user", "content": "Say hello in German"}] }'

# amazon titan embeddings
call POST 'v1/embeddings' -d '{ "model": "amazon.titan-embed-text-v2:0", "input": "The quick brown fox jumps over the lazy dog" }'
