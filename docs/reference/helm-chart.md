## Helm Chart Reference (`docs/reference/helm-chart.md`)

```markdown
# Helm Chart Reference

The Kong Injector Helm chart provides a Kubernetes-native way to deploy and manage the Kong Injector application. This page describes all the configuration options available in the chart.

## Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of Kong Injector replicas | `1` |
| `image.repository` | Container image repository | `abhijeetka/kong-injector` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `image.tag` | Image tag | `v1.0.0` |
| `imagePullSecrets` | Image pull secrets | `[]` |
| `nameOverride` | Override the name of the chart | `""` |
| `fullnameOverride` | Override the full name of the chart | `""` |
| `env.kongAdminUrl` | Kong Admin API URL | `kong-cp-kong-admin` |
| `env.kongAdminPort` | Kong Admin API port | `8001` |
| `env.kongNamespace` | Namespace where Kong is deployed | `kong` |
| `serviceAccount.create` | Create a service account | `true` |
| `serviceAccount.annotations` | Service account annotations | `{}` |
| `serviceAccount.name` | Service account name | `kong-injector` |
| `podAnnotations` | Pod annotations | `{}` |
| `podSecurityContext` | Pod security context | `{}` |
| `securityContext` | Container security context | `{}` |
| `service.type` | Service type | `ClusterIP` |
| `service.port` | Service port | `80` |
| `configMap.name` | Name of the ConfigMap containing Kong configuration | `kong-config` |
| `configMap.mountPath` | Path where the ConfigMap is mounted | `/opt/kong` |
| `configMap.readOnly` | Whether the ConfigMap is mounted read-only | `true` |
| `resources` | CPU/Memory resource requests/limits | `{}` |

## Example: values.yaml

```yaml
replicaCount: 1

image:
  repository: abhijeetka/kong-injector
  pullPolicy: IfNotPresent
  tag: "v1.0.0"

env:
  kongAdminUrl: kong-admin
  kongAdminPort: 8001
  kongNamespace: kong-system

serviceAccount:
  create: true
  name: kong-injector

configMap:
  name: kong-config
  mountPath: "/opt/kong"
  readOnly: true

resources:
  limits:
    cpu: 200m
    memory: 256Mi
  requests:
    cpu: 100m
    memory: 128Mi