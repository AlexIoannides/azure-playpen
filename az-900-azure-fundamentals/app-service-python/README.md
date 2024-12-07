# Deploying a Simple Web API

With a single endpoint at `"/"` that return a heatbeat - e.g.,

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
