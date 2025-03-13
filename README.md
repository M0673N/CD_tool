TODO: Add propper documentation

Example test for the webhook endpoint:
```
curl -k -X POST \
  https://127.0.0.1:8000/webhook/ \
  -H 'Content-Type: application/json' \
  -d '{"username": "tool_user", "password": "pppp1234", "command": "CD"}'
```

Example test for the schedule endpoint:
```
curl -k -X POST \
  https://127.0.0.1:8000/webhook/schedule \
  -H 'Content-Type: application/json' \
  -d '{"username": "tool_user", "password": "pppp1234", "command": "CD", "hour": 23, "minute": 45}'
```

### Using the -k flag disables SSL/TLS certificate verification, which can expose your connection to man-in-the-middle (MITM) attacks. Use it for testing only