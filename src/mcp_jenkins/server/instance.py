from fastmcp import Context

from mcp_jenkins.server import mcp


@mcp.tool(tags=["read"])
async def list_instances(ctx: Context) -> dict:
    """List all configured Jenkins instances and the default.

    Returns:
        A dict with 'instances' (list of instance names) and 'default' (the default instance name).
        Returns an empty result if multi-instance mode is not configured.
    """
    instances = ctx.request_context.lifespan_context.instances
    if not instances:
        return {"instances": [], "default": None}

    return {
        "instances": list(instances.instances.keys()),
        "default": instances.default,
    }
