# Kong Config Injector

Kong Config Injector is a tool designed to automatically configure Kong API Gateway in Kubernetes environments. It reads service configurations from a JSON file provided via ConfigMap and sets up routes, services, and plugins in Kong using its Admin API.

## Overview

The Kong Config Injector helps DevOps teams and developers manage Kong API Gateway configurations as code. Instead of manually configuring services and routes through Kong's Admin API, you can define your desired configuration in a structured JSON file and let the injector handle the rest.

**Key features:**

- Define Kong services, routes, and plugins as code
- Automatically sync configurations to Kong API Gateway
- Kubernetes native deployment with Helm
- Support for multiple services and routes
- Configurable plugin settings

## How It Works

1. You define your Kong configuration in a JSON file (`kong-service.json`)
2. The JSON file is mounted into the injector via a Kubernetes ConfigMap
3. The injector communicates with Kong's Admin API to create/update services, routes, and plugins
4. Configuration changes are automatically detected and applied

## Quick Start


# Add the Helm repository
```
helm repo add kong-injector https://abhijeetka.github.io/kong-injector
```

# Install Kong Injector
```
helm install kong-injector kong-injector/kong-injector \
  --set env.kongAdminUrl=kong-admin-service \
  --set env.kongAdminPort=8001 \
  --set env.kongNamespace=kong
```