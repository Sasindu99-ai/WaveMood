## Environment

`vvecon.qt.env.Env` and `EnvManager` manage runtime variables and export them to `os.environ`.

### Define environments
```python
from vvecon.qt.enums import EnvMode
from vvecon.qt.env import Env, EnvManager

env = EnvManager([
    Env(EnvMode.DEBUG,  ENVIRONMENT='development', API_URL='http://127.0.0.1:8000'),
    Env(EnvMode.RELEASE, ENVIRONMENT='production',  API_URL='https://api.example.com'),
], default=EnvMode.DEBUG)

env.init()  # exports to os.environ
```

### Access
```python
from vvecon.qt.env import EnvManager

api = EnvManager.get('API_URL')
```

`Env.set(key, value)` also sets `os.environ[key]` on `init()`; booleans are lowercased; other values are stringified.


