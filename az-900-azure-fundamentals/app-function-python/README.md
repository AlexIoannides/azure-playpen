# Azure Function Apps for Serverless Compute

This guide loosely follows the [Microsoft Learn Quickstart Guide](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=macos%2Cbash%2Cazure-cli%2Cbrowser) for deploying a Python function that handles HTTP requests.

## Install Azure Functions Core Tools

In order to be able to test Azure Function apps we need a framework for mocking how Azure will handle them. We've opted to use the CLI tools, but there are other tools available (e.g., VS Code plugins). The advantage of using CLI tools is that they could, hypothetically, be used in a CI pipeline. To the tool for macOS:

```text
brew tap azure/functions
brew install azure-functions-core-tools@4
```

For other OSs refer to the [docs](https://learn.microsoft.com/en-us/azure/azure-functions/create-first-function-cli-python?tabs=linux%2Cbash%2Cazure-cli%2Cbrowser#install-the-azure-functions-core-tools).

## Develop the Function

We're going to use [uv](https://docs.astral.sh/uv/) for managing Python dependencies. Start by initialising a uv managed Python app:

```text
uv init --app
uv sync
uv add azure-functions
rm hello.py
```

Now initialise an Azure Python app:

```text
uv run func init --python
```
And add an HTTP endpoint:

```text
uv run func new --name HttpExample --template "HTTP trigger" --authlevel "ANONYMOUS"
```

We can start the test suite using:

```text
uv run func start
```

And test the endpoint with:

```text
$ curl http://localhost:7071/api/HttpExample\?name\=foo
Hello, foo. This HTTP triggered function executed successfully.
```

## Deploy the Function

Start by creating a resource group:

```text
az group create \
    --name az900-function-app-rg \
    --location "UK South"
```

Create a storage account:

```text
az storage account create \
    --name az900functionapp \
    --location "UK South" \
    --resource-group az900-function-app-rg \
    --sku "Standard_LRS"
```

Create an empty function app:

```text
az functionapp create \
    --resource-group az900-function-app-rg \
    --consumption-plan-location uksouth \
    --runtime python \
    --runtime-version 3.11 \
    --functions-version 4 \
    --name az900-http-endpoint \
    --os-type linux \
    --storage-account az900functionapp
```

Synchronise the uv managed requests with the `requirements.txt` file:

```text
uv export --format requirements-txt --no-hashes > requirements.txt
```

And now deploy the app:

```text
func azure functionapp publish az900-http-endpoint
```

Where the output will include the URI - confirm that it works as expected:

```text
$ curl -s https://az900-http-endpoint.azurewebsites.net/api/httpexample\?name\=foo
Hello, foo. This HTTP triggered function executed successfully.
```

Be sure to explore this in the Azure portal as there are several helpful features for debugging and monitoring.

## Cleanup

```text
az group delete --name az900-function-app-rg
```
