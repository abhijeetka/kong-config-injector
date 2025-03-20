# Kong Injector Helm Chart

### Overview

The Kong Injector is a Kubernetes admission controller responsible for injecting Kong configuration into workloads. It ensures that services are automatically configured with Kong settings stored in a ConfigMap named kong-config.

#### Installation

To install the Kong Injector Helm chart, run:

```helm upgrade --install kong-injector ./kong-injector-chart  -n kong ```

Ensure that the kong-config ConfigMap exists before deployment:

``` kubectl get configmap kong-config -n <namespace> ```

If it does not exist, create it:

``` kubectl create configmap kong-config  --from-file=kong.yaml -n <namespace> ```

#### How It Works

It reads a configmap named kong-config and creates configuration as per the json file.

#### Uninstalling

To remove the Kong Injector, run:

``` helm uninstall kong-injector ```

#### Troubleshooting

If the injector is not modifying pods, check the webhook logs:

``` kubectl logs -l app=kong-injector -n <namespace> ```

Ensure the kong-config ConfigMap exists and is correctly formatted.

For further assistance, refer to the official Kong documentation or reach out to support.
