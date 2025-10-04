## API Controller

`vvecon.qt.api.Controller` is a minimal HTTP helper around `requests`.

Features:
- Base URL from `API_URL` env (default `http://127.0.0.1:8000`)
- Per-controller `api` prefix
- JSON requests with optional bearer auth via `Settings`
- Refresh retry for 401/403 via `refreshUrl`

### Subclassing
```python
from vvecon.qt.api import Controller

class Users(Controller):
    api = 'api/v1/users'

svc = Users()
data, status = svc.get('')         # GET /api/v1/users
data, status = svc.get('42')       # GET /api/v1/users/42
resp, status = svc.post('', {"name": "Ada"}, authorized=True)
```

### Auth tokens
When `authorized=True`, the controller sends `Authorization: Bearer <ACCESS_TOKEN>` using:
```python
from vvecon.qt.util import Settings

Settings.set('ACCESS_TOKEN', '<jwt>')
Settings.set('REFRESH_TOKEN', '<jwt>')
```

If a 400/401/403 occurs and `authorized=True`, it attempts a refresh by POSTing to `refreshUrl` and retries once.

Return values are `(json_or_Error, status_code)`. `Error` is `vvecon.qt.models.Error` for non-2xx.

Notes:
- TLS verification is disabled (`verify=False`). Adjust as needed for production.
- `timeout=10` seconds by default.


