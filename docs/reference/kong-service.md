## Kong Configuration File Explanation
The kong-config.json file defines Kong services, routes, and plugins for the Kong Injector to apply to a Kong API Gateway instance. This file is usually stored in a ConfigMap that is mounted to the Kong Injector.  
# Basic Structure
The configuration file follows this general structure:

```json
{
  "services": [
    {
      "name": "example-service",
      "url": "http://example-backend:8080",
      "routes": [
        {
          "name": "example-route",
          "paths": ["/api"],
          "plugins": [
            {
              "name": "key-auth",
              "config": {
                "key_names": ["api-key"]
              }
            }
          ]
        }
      ],
      "plugins": [
        {
          "name": "rate-limiting",
          "config": {
            "second": 5
          }
        }
      ]
    }
  ]
}
```

## Examples
Adding a Service
```json
{
  "services": [
    {
      "name": "user-service",
      "url": "http://user-backend:3000",
      "protocol": "http",
      "connect_timeout": 60000,
      "read_timeout": 60000,
      "write_timeout": 60000
    }
  ]
}
```

Adding a Route to a Service

```json
{
  "services": [
    {
      "name": "user-service",
      "url": "http://user-backend:3000",
      "routes": [
        {
          "name": "user-api-route",
          "paths": ["/users", "/users/(?:[^/]+)"],
          "methods": ["GET", "POST"],
          "strip_path": false,
          "preserve_host": true
        }
      ]
    }
  ]
}
```

Adding a Plugin to a Route
```json
{
  "services": [
    {
      "name": "user-service",
      "url": "http://user-backend:3000",
      "routes": [
        {
          "name": "user-api-route",
          "paths": ["/users"],
          "plugins": [
            {
              "name": "key-auth",
              "config": {
                "key_names": ["api-key"],
                "hide_credentials": true
              }
            }
          ]
        }
      ]
    }
  ]
}
```