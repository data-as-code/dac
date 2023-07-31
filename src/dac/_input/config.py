import pydantic

print("here")
print(pydantic.__version__)
if pydantic.__version__ >= "2.0.0":
    print("yeah")
    from dac._input._config_pydantic_v2 import PackConfig  # noqa: F401 # type: ignore
elif pydantic.__version__ >= "1.0.0":
    print("d'oh")
    from dac._input._config_pydantic_v1 import PackConfig  # noqa: F401
else:
    raise RuntimeError(f"Unsupported pydantic version: {pydantic.__version__}")
