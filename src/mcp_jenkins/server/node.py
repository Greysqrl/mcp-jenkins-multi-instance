from fastmcp import Context

from mcp_jenkins.core.lifespan import jenkins
from mcp_jenkins.server import mcp


@mcp.tool(tags=["read"])
async def get_all_nodes(ctx: Context, instance: str | None = None) -> list[dict]:
    """Get all nodes from Jenkins

    Args:
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of all nodes
    """
    return [
        node.model_dump(exclude={"executors"})
        for node in jenkins(ctx, instance=instance).get_nodes(depth=0)
    ]


@mcp.tool(tags=["read"])
async def get_node(ctx: Context, name: str, instance: str | None = None) -> dict:
    """Get a specific node from Jenkins

    Contains executor about the node.

    Args:
        name: The name of the node
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The node
    """
    return (
        jenkins(ctx, instance=instance)
        .get_node(name=name, depth=2)
        .model_dump(exclude_none=True)
    )


@mcp.tool(tags=["read"])
async def get_node_config(ctx: Context, name: str, instance: str | None = None) -> str:
    """Get node config from Jenkins

    Args:
        name: The name of the node
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The config of the node
    """
    return jenkins(ctx, instance=instance).get_node_config(name=name)


@mcp.tool(tags=["write"])
async def set_node_config(
    ctx: Context, name: str, config_xml: str, instance: str | None = None
) -> None:
    """Set specific node config in Jenkins

    Args:
        name: The name of the node
        config_xml: The config XML of the node
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.
    """
    jenkins(ctx, instance=instance).set_node_config(name=name, config_xml=config_xml)
