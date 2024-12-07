# App Service for Python Apps

Deploying the `python-api-app` using Azure App Service, following workflows from the [Microsoft Learn Quickstart Guide](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python).

## Using the Azure Portal

Create an empty App Service from within the Azure portal, choosing to export an ARM template and parameters file (see the `iac` directory).

### Deploy the App as a ZIP File

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

Next, create a ZIP file for the app:

```text
zip -r python-api.zip $(realpath ../python-api-app) -x '*/.*' '*/__pycache__*'
```

And deploy!

```text
az webapp deploy \
    --resource-group az900-app-service-python \
    --name az900-app-service-python \
    --src-path python-api.zip
```
