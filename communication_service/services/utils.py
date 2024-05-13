import hazelcast
import json


def get_config(consul_client, config_name):
    """
    Retrieve the configuration from Consul for the given config_name.

    Args:
        consul_client (Consul): The Consul client object.
        config_name (str): The name of the configuration to retrieve.

    Returns:
        dict: The configuration as a dictionary, or None if no valid configuration is found.
    """
    index, hazelcast_config = consul_client.kv.get(config_name)

    if hazelcast_config and "Value" in hazelcast_config:
        hazelcast_config = json.loads(hazelcast_config["Value"].decode().replace("\'", "\""))
    else:
        print(f"Warning: No valid configuration found for {config_name}.")
        return None

    return hazelcast_config


def get_client(hazelcast_config):
    """
    Get a Hazelcast client based on the provided configuration.

    Args:
        hazelcast_config (dict): The Hazelcast configuration containing the cluster name, cluster members, and lifecycle listeners.

    Returns:
        hazelcast.HazelcastClient: The Hazelcast client instance.

    Raises:
        ValueError: If the hazelcast_config is None or invalid.

    """
    if hazelcast_config is None:
        raise ValueError("Invalid or missing Hazelcast configuration.")

    print("Hazelcast Configuration:", hazelcast_config)
    client = hazelcast.HazelcastClient(
        cluster_name=hazelcast_config["cluster_name"],
        cluster_members=hazelcast_config["cluster_members"],
        lifecycle_listeners=[
            lambda state: print("Lifecycle event >>>", state),
        ]
    )
    return client