import structlog
import os
import sys
import json
import requests

REQUIRED_KONG_ENV_VARS = ["KONG_ADMIN_URL", "KONG_ADMIN_PORT", "KONG_NAMESPACE"]
# for local to work.
#KONG_SERVICE_CONFIG = "kong-injector/config/kong-config.json"
KONG_SERVICE_CONFIG = "/opt/kong/kong-config.json"
HEADERS = {
    "Content-Type": "application/json",
    "accept": "application/json"
}
KONG_ADMIN_URL = None
KONG_ADMIN_PORT = None
KONG_NAMESPACE = None
BASE_URL = None


def check_env_variables(REQUIRED_KONG_ENV_VARS):
    """Check if all required environment variables are set."""
    missing_vars = [var for var in REQUIRED_KONG_ENV_VARS if not os.getenv(var)]

    if missing_vars:
        logging.info(f"Error: Missing environment variables: {', '.join(missing_vars)}", file=sys.stderr)
        sys.exit(1)  # Exit with error code 1

    print("All required environment variables are available and we can proceed.")


def setup_global_variables():
    global KONG_ADMIN_URL, KONG_ADMIN_PORT, KONG_NAMESPACE, BASE_URL
    KONG_ADMIN_URL = os.getenv(REQUIRED_KONG_ENV_VARS[0])
    KONG_ADMIN_PORT = os.getenv(REQUIRED_KONG_ENV_VARS[1])
    KONG_NAMESPACE = os.getenv(REQUIRED_KONG_ENV_VARS[2])
    BASE_URL = f"http://{KONG_ADMIN_URL}.{KONG_NAMESPACE}:{KONG_ADMIN_PORT}"
    # for local to work
    #BASE_URL = f"http://{KONG_ADMIN_URL}:{KONG_ADMIN_PORT}"


def check_kong_config():
    config_path = os.path.join(os.getcwd(), KONG_SERVICE_CONFIG)
    if not os.path.exists(config_path):
        logger.info(f"Error: Configuration file '{KONG_SERVICE_CONFIG}' not found in {os.getcwd()}")
        sys.exit(1)
    else:
        logger.info(f"Successfully read configuration file '{KONG_SERVICE_CONFIG}' file from {os.getcwd()}")


def test_kong_connection():
    logger.info("Testing Connection to Kong Admin Server")
    try:
        response = requests.get(f"{BASE_URL}/status", headers=HEADERS)
        # Fix the logging statements
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())
        if response.status_code == 200:
            logger.info(f"Successfully Connected to Kong Admin Server")
        else:
            logger.info(f"Failed Connecting to Kong Admin Server.. ")
            logger.info(f"Exit")
            exit(1)
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))
        exit(1)


def read_kong_config(KONG_SERVICE_CONFIG):
    try:
        config_path = os.path.join(os.getcwd(), KONG_SERVICE_CONFIG)
        with open(config_path, 'r') as file:
            kong_config = file.read()
            logger.info(f"Successfully read Kong configuration from {config_path}")
            return kong_config
    except FileNotFoundError:
        logger.error(f"Error: Could not find Kong configuration file at {config_path}")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Error: Permission denied when trying to read {config_path}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: Failed to read Kong configuration file: {str(e)}")
        sys.exit(1)


def get_kong_route_plugin(route_name, plugin_info):
    logger.info(
        f"Checking if plugin is already configured for route: {route_name} with plugin : {plugin_info['name']}..")
    try:
        response = requests.get(f"{BASE_URL}/routes/{route_name}/pluginss", headers=HEADERS)
        # Fix the logging statements
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())
        if response.status_code == 200:
            if plugin_info['name'] in response.json():
                logger.info(f"Plugin already configured, Patching the plugin with latest configuration")
                return response.json()
            else:
                logger.info(f"Plugin not found with name {plugin_info['name']} in route {route_name}")
                return response.json()
        else:
            logger.info(f"Seems, no response from server, Creating the plugin configuration for route {route_name}")
            return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))


def create_kong_route_plugin(route_name, plugin):
    logger.info(f"creating kong plugin for route {route_name} and plugin {plugin['name']}..")
    payload = plugin
    try:
        # check if kong route plugin already present
        plugin_status = get_kong_route_plugin(route_name, plugin)
        if "id" in plugin_status:
            # This specifies that the plugin present for the route
            logger.info("Plugin %s with id %s already present for route, Patching Plugin.. ", plugin_status['name'],
                        plugin_status['id'])
            response = requests.put(f"{BASE_URL}/routes/{route_name}/plugins/{plugin_status['id`']}", json=payload, headers=HEADERS)
            response.raise_for_status()
        else:
            logger.info("plugin not present and creating it.")
            response = requests.post(f"{BASE_URL}/routes/{route_name}/plugins", json=payload, headers=HEADERS)
            response.raise_for_status()
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))


def create_kong_service(service_info):
    logger.info(f"creating kong service {service_info['name']}..")
    payload = {
        "name": service_info["name"],
        "retries": service_info['retries'],
        "protocol": service_info['protocol'],
        "host": service_info['host'],
        "port": service_info['port'],
        "connect_timeout": service_info['connect_timeout'],
        "write_timeout": service_info['write_timeout'],
        "read_timeout": service_info['read_timeout'],
        "enabled": service_info['enabled']
    }
    try:
        # check if service already present
        service_status = get_kong_service(service_info['name'])
        if "id" in service_status:
            # This specifies that the service is present and we need to get routes
            logger.info("Service %s with id %s already present, Patching service ", service_status['name'],
                        service_status['id'])
            response = requests.patch(f"{BASE_URL}/services/{service_info['name']}", json=payload, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        else:
            logger.info("Service not present and creating it.")
            response = requests.post(f"{BASE_URL}/services", json=payload, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))
        return {}


def get_kong_service(service_name):
    logger.info("Inside get kong service")
    try:
        response = requests.get(f"{BASE_URL}/services/{service_name}", headers=HEADERS)

        # Fix the logging statements
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())

        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))
        return {}


def get_kong_route(route_name, service_name):
    logger.info("Inside get kong route")
    try:
        response = requests.get(f"{BASE_URL}/services/{service_name}/routes/{route_name}", headers=HEADERS)
        # Fix the logging statements
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))
        return {}


def create_kong_route(service_id, service_name, route):
    logger.info(f"creating kong route for service {service_name} and route {route['name']}..")
    payload = {
        "name": route["name"],
        "protocols": route['protocols'],
        "paths": route['paths'],
        "path_handling": route['path_handling'],
        "methods": route['methods'],
        "preserve_host": route['preserve_host'],
        "https_redirect_status_code": route['https_redirect_status_code'],
        "service": {
            "id": service_id
        }
    }
    try:
        # check if service already present
        route_status = get_kong_route(route['name'], service_name)
        if "id" in route_status:
            # This specifies that the service is present and we need to get routes
            logger.info("Route %s with id %s already present, Patching Route.. ", route_status['name'],
                        route_status['id'])
            response = requests.put(f"{BASE_URL}/services/{service_name}/routes/{route_status['name']}", json=payload,
                                    headers=HEADERS)
            response.raise_for_status()
            return response.json()
        else:
            logger.info("Route not present and creating it.")
            response = requests.post(f"{BASE_URL}/services/{service_name}/routes", json=payload, headers=HEADERS)
            response.raise_for_status()
            return response.json()
        logger.info("Response Status Code: %d", response.status_code)
        logger.info("Response JSON: %s", response.json())
    except requests.exceptions.RequestException as e:
        logger.error("Error occurred: %s", str(e))
        return {}


def inject_kong_config():
    kong_config = json.loads(read_kong_config(KONG_SERVICE_CONFIG))

    # Loop through each service in the configuration
    for service in kong_config.get('services', []):
        try:
            service_name = service.get('name')
            logger.info(f"Processing service: {service_name}")
            service_info = create_kong_service(service)
            if any(service.get('routes')):
                routes = service.get('routes')
                for route in routes:
                    logger.info(f"Processing route: {route['name']}")
                    route_info = create_kong_route(service_info['id'], service_info['name'], route)
                    if any(route.get('plugins')):
                        logger.info(f"Processing Plugins for route: {route_info['name']} with id {route_info['id']}")
                        plugins = route.get('plugins')
                        for plugin in plugins:
                            logger.info(f"Processing Plugin: {plugin['name']}")
                            create_kong_route_plugin(route_info['name'], plugin)

        except Exception as e:
            logger.error(f"Error processing service {service_name}: {str(e)}")
            #continue


if __name__ == "__main__":
    logger = structlog.get_logger()
    check_env_variables(REQUIRED_KONG_ENV_VARS)
    check_kong_config()
    setup_global_variables()
    test_kong_connection()
    inject_kong_config()
