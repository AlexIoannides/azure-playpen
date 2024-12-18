# App Service for Python Apps

Deploying the `python-api-app` using Azure App Service, following workflows from the [Microsoft Learn Quickstart Guide](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python).

## Using the Azure Portal

Create an empty App Service from within the Azure portal, choosing to export an ARM template and parameters file before creation (see the `iac` directory and [Redeploying with ARM Templates](#redeploying-with-arm-templates)).

### Deploy the App as a Zip File

Enable build automation:

```text
az webapp config appsettings set \
    --resource-group az900-app-service-python \
    --name az900-app-service-python \
    --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

This can also be set in the portal by browsing to `Settings --> Environment Variables` and setting `SCM_DO_BUILD_DURING_DEPLOYMENT` to `true`.

Then, configure the startup script:

```text
az webapp config set \
    --resource-group az900-app-service-python \
    --name az900-app-service-python \
    --startup-file "startup.sh"
```

This can also be set in the portal by browsing to `Settings --> Configuration` and setting `Startup Command` to `startup.sh`.

Next, create a zip file for the app:

```text
cd ../python-api-app &&\
    zip -r python-api.zip . -x '.??*' '__pycache__/*' &&\
    mv python-api.zip ../app-service-python/python-api.zip &&\
    cd ../app-service-python
```

And deploy!

```text
az webapp deploy \
    --resource-group az900-app-service-python \
    --name az900-app-service-python \
    --src-path python-api.zip
```

### Testing the Service

```text
$ curl -sL http://az900-app-service-python-ecc3hbczfpfhgvcp.uksouth-01.azurewebsites.net | jq
{
  "timestamp": "2024-12-07T16:50:25.737",
  "message": "I am healthy."
}
```

Where the `-L` flag follows redirects.

### Accessing Logs

Configure logging to the local filesystem:

```text
az webapp log config \
    --resource-group az900-app-service-python \
    --name az900-app-service-python \
    --web-server-logging filesystem
```

Stream logs (albeit with a lag):

```text
az webapp log tail \
    --resource-group az900-app-service-python \
    --name az900-app-service-python
```

**Note: the VS Code plugin for Azure provides direct access to a lot of these, as does the portal.**

### Clean Up

```text
az group delete --name az900-app-service-python
```

## Redeploying with ARM Templates

First of all create a new resource group:

```text
az group create \
  --name az900-app-service-python \
  --location 'UK South'
```

Then we can deploy the template:

```text
az deployment group create \
    --resource-group az900-app-service-python \
    --template-file iac/app-template.json \
    --parameters iac/app.parameters.json
```

**Note: you will need to modify the resource group name, subscription ID and region as they are parameters for the template.**

## Configuring CI

When first creating the App Service in the portal you are asked if you want to configure Continuous Integration (CI) and Continuous Deployment (CD). One of the options is to authenticate to GitHub and then allow Azure to inject a GitHub Actions workflow (and the appropriate secrets) to build the zip file in one job and deploy it in another. This can also be configured after initial setup in `Deployment --> Deployment Center`.

In my opinion, this is a useful starting point but will likely need to be modified to fit the DevOps best practices in use within a particular team. Also, I'd prefer it if GitHub didn't add and remove files from my repo - it's probably better to use the automatically generated workflow as a guide, but to recreate the zip file build-and-push manually, which would require getting the Azure CLI tool in a GitHub action and authenticating, etc. - e.g.,

```yaml
name: Azure CLI Example
on:
  push:
    branches:
      - main

jobs:
  azure-cli:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Run Azure CLI command
        run: |
          az account show
```

Where `secrets.AZURE_CREDENTIALS` are those for a dedicated Azure service principle. See the [github.com/Azure/login](https://github.com/Azure/login) for more information and examples.
