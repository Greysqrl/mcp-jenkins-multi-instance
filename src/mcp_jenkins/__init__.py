import asyncio
import os
import sys
from collections.abc import Coroutine

import click
from loguru import logger

try:
    from mcp_jenkins.xdg import get_data_dir

    LOG_DIR = get_data_dir()
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger.add(LOG_DIR / "log.log", rotation="10 MB")
except Exception as e:  # noqa: BLE001
    logger.error(f"Failed to set up logger directory: {e}")


@click.command()
@click.option("--jenkins-url", required=False)
@click.option("--jenkins-username", required=False)
@click.option("--jenkins-password", required=False)
@click.option("--jenkins-timeout", default=5)
@click.option(
    "--jenkins-verify-ssl/--no-jenkins-verify-ssl",
    default=True,
    help="Whether to verify SSL certificates, default is True",
)
@click.option(
    "--read-only",
    default=False,
    is_flag=True,
    help="Whether to run in read-only mode, default is False",
)
@click.option(
    "--tool-regex",
    default="",
    help="(Deprecated) Regex pattern to enable specific tools",
)
@click.option(
    "--jenkins-session-singleton/--no-jenkins-session-singleton",
    default=True,
    help="In the same session, does it share the Jenkins request instance, "
    "significantly reducing the number of instantiations and crumb requests",
)
@click.option(
    "--config-file",
    type=click.Path(exists=False),
    default="~/.config/mcp-jenkins/instances.yaml",
    help="Path to multi-instance YAML config file (e.g. ~/.config/mcp-jenkins/instances.yaml)",
)
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse", "streamable-http"]),
    default="stdio",
)
@click.option(
    "--host",
    default="0.0.0.0",
    help="Host to bind to for SSE or Streamable HTTP transport",
)  # noqa: S104
@click.option(
    "--port",
    default=9887,
    help="Port to listen on for SSE or Streamable HTTP transport",
)
def main(
    jenkins_url: str,
    jenkins_username: str,
    jenkins_password: str,
    jenkins_timeout: int,
    jenkins_verify_ssl: bool,  # noqa: FBT001
    read_only: bool,  # noqa: FBT001
    tool_regex: str,
    jenkins_session_singleton: bool,  # noqa: FBT001
    config_file: str | None,
    transport: str,
    host: str,
    port: int,
) -> None:
    if config_file:
        os.environ["MCP_JENKINS_CONFIG"] = str(config_file)
    if jenkins_url:
        os.environ["jenkins_url"] = jenkins_url
    if jenkins_username:
        os.environ["jenkins_username"] = jenkins_username
    if jenkins_password:
        os.environ["jenkins_password"] = jenkins_password

    os.environ["jenkins_timeout"] = str(jenkins_timeout)
    os.environ["jenkins_verify_ssl"] = str(jenkins_verify_ssl).lower()
    os.environ["jenkins_session_singleton"] = str(jenkins_session_singleton).lower()

    from mcp_jenkins.server import mcp

    if read_only:
        mcp.enable(tags={"read"}, only=True)

    if tool_regex:
        logger.warning(
            "The [--tool-regex] option is deprecated and will be removed in future versions."
        )

    def _run_with_loop_factory(coro: Coroutine) -> None:
        if sys.platform == "win32":
            with asyncio.Runner(loop_factory=asyncio.SelectorEventLoop) as runner:
                return runner.run(coro)
        else:
            return asyncio.run(coro)

    if transport == "stdio":
        _run_with_loop_factory(mcp.run_async(transport=transport))
    elif transport in ("sse", "streamable-http"):
        _run_with_loop_factory(mcp.run_async(transport=transport, host=host, port=port))


if __name__ == "__main__":
    main()
