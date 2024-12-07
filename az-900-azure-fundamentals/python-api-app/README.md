# A Simple Web API

To be used for testing various deployment options. This defines an app with a single route at `"/"` that returns a heatbeat - e.g.,

```text
{
  "timestamp": "2024-12-07T12:55:12.933",
  "message": "I am healthy."
}
```

## Test the App

Dependencies managed using [uv](https://docs.astral.sh/uv/) - start by setting-up the environment:

```text
uv sync
```

Run the API:

```text
uv run app.py
```

Then test it:

```text
$ curl -s http://localhost:8000 | jq
{
  "timestamp": "2024-12-07T12:55:12.933",
  "message": "I am healthy."
}
```

## Generate a `requirements.txt` File

This is required by Azure for customising an app's local Python environment so that it has the required dependencies.

```text
uv export --format requirements-txt --no-hashes > requirements.txt
```

## Startup Script

For use with some deployment options. Make sure this is executable,

```text
chmod +x startup.sh
```

And then to run from within the uv managed environment,

```text
uv run ./startup.sh
```
