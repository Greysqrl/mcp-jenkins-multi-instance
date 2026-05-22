from fastmcp import Context

from mcp_jenkins.core.lifespan import jenkins
from mcp_jenkins.server import mcp


@mcp.tool(tags=["read"])
async def get_all_views(ctx: Context, instance: str | None = None) -> list[dict]:
    """Get all top-level views from Jenkins.

    Args:
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A list of views with their name and URL.
    """
    return jenkins(ctx, instance=instance).get_views()


@mcp.tool(tags=["read"])
async def get_view(
    ctx: Context, view_path: str, depth: int = 0, instance: str | None = None
) -> dict:
    """Get a Jenkins view by path, returning its jobs and/or nested sub-views.

    Views can be nested up to multiple levels deep. Use "/" to separate levels
    in the path. If the view contains sub-views instead of jobs, the response
    will include their names so you can drill down further.

    Args:
        view_path: View path using "/" to separate levels.
                   Examples: "All", "frontend", "frontend/nightly".
                   Spaces and special characters in view names are handled automatically.
        depth: Depth of detail to retrieve for each job. Default is 0.
        instance: Name of the Jenkins instance to target. If omitted, uses the configured default.

    Returns:
        A dict with the view's name, jobs list, and/or nested views.
    """
    return jenkins(ctx, instance=instance).get_view(view_path=view_path, depth=depth)
