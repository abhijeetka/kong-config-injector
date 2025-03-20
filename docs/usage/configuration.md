## Configuration (`docs/usage/configuration.md`)

Kong Injector is configured using a combination of Helm chart values and a JSON configuration file. This page provides an overview of the configuration options available in Kong Injector.
# Configuring Kong Injector

Kong Injector is primarily configured through:

1. Helm chart values when deploying
2. The `kong-service.json` file in the ConfigMap

## Helm Configuration

When installing Kong Injector via Helm, you can configure various aspects of the deployment:

```bash
helm install kong-injector kong-injector/kong-injector \
  --set env.kongAdminUrl=kong-admin-service \
  --set env.kongAdminPort=8001 \
  --set env.kongNamespace=kong \
  --set replicaCount=2 \
  -n <your-namespace>
```
