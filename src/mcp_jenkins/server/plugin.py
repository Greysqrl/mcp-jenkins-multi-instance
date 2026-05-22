from fastmcp import Context

from mcp_jenkins.core.lifespan import jenkins
from mcp_jenkins.server import mcp


@mcp.tool(tags={"read"})
async def get_all_plugins(
    ctx: Context, depth: int = 2, instance: str | None = None
) -> list[dict]:
    """Get all installed plugins from Jenkins

    Args:
        depth: The depth of the information to retrieve. Default is 2 (includes dependencies).
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of all installed plugins
    """
    return jenkins(ctx, instance=instance).get_plugins(depth=depth)


@mcp.tool(tags={"read"})
async def get_plugin(
    ctx: Context, short_name: str, depth: int = 2, instance: str | None = None
) -> dict | None:
    """Get a specific plugin from Jenkins

    Contains detailed information about the plugin, including dependencies when depth >= 2.

    Args:
        short_name: The short name of the plugin
        depth: The depth of the information to retrieve. Default is 2 (includes dependencies).
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        The plugin details, or None if not found
    """
    return jenkins(ctx, instance=instance).get_plugin(
        short_name=short_name, depth=depth
    )


@mcp.tool(tags={"read"})
async def get_plugins_with_problems(
    ctx: Context, instance: str | None = None
) -> list[dict]:
    """Get all plugins with problems from Jenkins

    These are plugins that have issues such as missing dependencies,
    incompatible versions, core version mismatch, or other configuration problems.

    Args:
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of plugins with problems
    """
    return jenkins(ctx, instance=instance).get_plugins_with_problems()


@mcp.tool(tags={"read"})
async def get_plugins_with_backup(
    ctx: Context, depth: int = 0, instance: str | None = None
) -> list[dict]:
    """Get plugins that can be downgraded

    Returns plugins that have a backupVersion and can be rolled back.

    Args:
        depth: The depth of the information to retrieve. Default is 0.
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of plugins that can be downgraded
    """
    return jenkins(ctx, instance=instance).get_plugins_with_backup(depth=depth)


@mcp.tool(tags={"read"})
async def get_plugins_with_updates(
    ctx: Context, depth: int = 0, instance: str | None = None
) -> list[dict]:
    """Get plugins that have available updates

    Args:
        depth: The depth of the information to retrieve. Default is 0.
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of plugins with available updates
    """
    return jenkins(ctx, instance=instance).get_plugins_with_updates(depth=depth)


@mcp.tool(tags={"read"})
async def get_plugin_dependency_graph(
    ctx: Context, short_name: str, instance: str | None = None
) -> dict:
    """Get dependency graph for a specific plugin in Graphviz format

    Recursively analyzes dependencies down to leaf nodes.
    Returns nodes and edges that can be used to generate a dependency graph.

    Args:
        short_name: The short name of the plugin to analyze
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A dictionary with 'nodes' and 'edges' for Graphviz rendering
    """
    return jenkins(ctx, instance=instance).get_plugin_dependency_graph(
        short_name=short_name
    )
