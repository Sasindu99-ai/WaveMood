## Env

### Env (`vvecon.qt.env.Env`)
```python
Env(mode: EnvMode, **kwargs)
set(key: str, value) -> None  # sets attribute and os.environ
get(key: str)
init() -> None  # exports all attributes to os.environ
```

### EnvManager (`vvecon.qt.env.EnvManager`)
```python
EnvManager(envs: list[Env] | None = None, default=EnvMode.DEBUG)
set_env(env: Env) -> None
get_env() -> Env
get(key: str)
current() -> Env
init() -> None
```


