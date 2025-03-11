TODO: Add propper documentation

Example test for the webhook endpoint:
```
curl -X POST \
  http://127.0.0.1:8000/webhook/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "tool_user", "password": "pppp1234", "command": "CD"}'
```

Example test for the schedule endpoint:
```
curl -X POST \
  http://127.0.0.1:8000/webhook/schedule \
  -H 'Content-Type: application/json' \
  -d '{"username": "tool_user", "password": "pppp1234", "command": "CD", "hour": 23, "minute": 45}'
```