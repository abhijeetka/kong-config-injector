## Prerequisites (`docs/getting-started/prerequisites.md`)

```markdown
# Prerequisites

Before installing Kong Injector, ensure that you have the following prerequisites:

## Kong API Gateway

You must have a running Kong API Gateway instance with the Admin API accessible from the Kubernetes cluster where you'll deploy Kong Injector.

- Kong version: 2.x or higher recommended
- Admin API must be accessible (by default on port 8001)

## Kubernetes

- Kubernetes cluster (version 1.16+)
- kubectl configured to interact with your cluster
- Helm 3.x (for Helm chart installation)

## Permissions

The service account used by Kong Injector needs permissions to:

- Access the Kong Admin API
- Read ConfigMaps in its namespace (for the kong-service.json configuration)

## Network Access

Kong Injector needs network access to:

- Kong Admin API (typically at `http://<kong-admin-service>:8001`)
- Kubernetes API server

## JSON Configuration

Prepare your `kong-service.json` file that defines the services, routes, and plugins you want to configure in Kong. See the [Kong Service JSON Reference](../reference/kong-service-json.md) for details on the file format.