## API

### Controller (`vvecon.qt.api.Controller`)

Class variables:
```python
base: str = os.environ.get('API_URL', 'http://127.0.0.1:8000')
api: str = NotImplemented
refreshUrl: str = f"{base}/api/v1/auth/token/refresh"
```

Methods:
```python
def generateUrl(self, endpoint: str) -> str

@staticmethod
def returnError(res) -> Error

@staticmethod
def returnJson(res) -> dict | Error

def request(self, method: str, endpoint: str, data: dict | None = None, params: dict | None = None,
            authorized: bool = False, retry: bool = True) -> tuple[dict | Error, int]

def post(self, endpoint: str, data: dict | None = None, **kwargs)
def get(self, endpoint: str, params: dict | None = None, **kwargs)
def put(self, endpoint: str, data: dict | None = None, **kwargs)
```

Auth:
- When `authorized=True`, adds `Authorization: Bearer <ACCESS_TOKEN>` using `Settings.get('ACCESS_TOKEN')`.
- On 400/401/403 (and `authorized=True`), posts to `refreshUrl` with `REFRESH_TOKEN`, then retries once.


