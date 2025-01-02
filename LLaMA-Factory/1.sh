curl -X 'POST' \
  'http://localhost:8083/v1/chat/completions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "string",
  "messages": [
    {
      "role": "user",
      "content": "你是什么模型",
      "tool_calls": [
        {
          "id": "string",
          "type": "function",
          "function": {
            "name": "string",
            "arguments": "string"
          }
        }
      ]
    }
  ],
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "string",
        "description": "string",
        "parameters": {}
      }
    }
  ],
  "do_sample": true,
  "temperature": 0,
  "top_p": 0,
  "n": 1,
  "max_tokens": 0,
  "stop": "string",
  "stream": false
}'