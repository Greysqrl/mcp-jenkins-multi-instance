import pytest

from mcp_jenkins.core.config import JenkinsInstanceConfig, MultiInstanceConfig
from mcp_jenkins.server import instance


@pytest.mark.asyncio
async def test_list_instances_multi_mode(mocker):
    multi_config = MultiInstanceConfig(
        default="prod",
        instances={
            "prod": JenkinsInstanceConfig(
                url="http://prod.example.com", username="u", password="p"
            ),
            "dev": JenkinsInstanceConfig(
                url="http://dev.example.com", username="u2", password="p2"
            ),
        },
    )

    ctx = mocker.Mock()
    ctx.request_context.lifespan_context.instances = multi_config

    result = await instance.list_instances(ctx)
    assert result["default"] == "prod"
    assert set(result["instances"]) == {"prod", "dev"}


@pytest.mark.asyncio
async def test_list_instances_legacy_mode(mocker):
    ctx = mocker.Mock()
    ctx.request_context.lifespan_context.instances = None

    result = await instance.list_instances(ctx)
    assert result == {"instances": [], "default": None}
