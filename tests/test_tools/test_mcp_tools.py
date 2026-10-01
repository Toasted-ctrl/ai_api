import pytest
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

from tools.mcp_tools import get_mcp_tools
from database.mcps import MCPConfig


pytestmark = pytest.mark.asyncio


class TestGetMcpTools:

    async def test_returns_tools_from_multiple_mcps(self):
        """Test fetching tools from multiple MCP configurations."""
        mcp_id_1 = uuid.uuid4()
        mcp_id_2 = uuid.uuid4()

        mock_session = MagicMock()
        mock_tools = [MagicMock(), MagicMock()]

        with patch('tools.mcp_tools.get_mcp_by_id') as mock_get_mcp:
            with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
                mock_get_mcp.side_effect = [
                    MCPConfig(id=mcp_id_1, name='search', url='http://search', transport='stdio'),
                    MCPConfig(id=mcp_id_2, name='files', url='http://files', transport='sse')
                ]
                mock_client = MagicMock()
                mock_client.get_tools = AsyncMock(return_value=mock_tools)
                mock_client_class.return_value = mock_client

                result = await get_mcp_tools(session=mock_session, mcp_ids=[mcp_id_1, mcp_id_2])

                assert result == mock_tools
                assert mock_client_class.call_args[1]['connections'] == {
                    'search': {'url': 'http://search/mcp', 'transport': 'stdio'},
                    'files': {'url': 'http://files/mcp', 'transport': 'sse'}
                }

    async def test_returns_empty_tools_with_no_mcps(self):
        """Test that empty mcp_ids returns empty tools list."""
        mock_session = MagicMock()
        mock_tools = []

        with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_tools = AsyncMock(return_value=mock_tools)
            mock_client_class.return_value = mock_client

            result = await get_mcp_tools(session=mock_session, mcp_ids=[])

            assert result == mock_tools
            assert mock_client_class.call_args[1]['connections'] == {}

    async def test_includes_web_search_when_enabled(self):
        """Test that web search connection is added when enabled."""
        mcp_id = uuid.uuid4()

        mock_session = MagicMock()
        mock_tools = [MagicMock()]

        with patch('tools.mcp_tools.get_mcp_by_id') as mock_get_mcp:
            with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
                with patch('tools.mcp_tools.config') as mock_config:
                    mock_get_mcp.side_effect = [
                        MCPConfig(id=mcp_id, name='search', url='http://search', transport='stdio')
                    ]
                    mock_config.WEB_SEARCH_URL = 'http://web-search'
                    mock_config.WEB_SEARCH_TRANSPORT = 'sse'

                    mock_client = MagicMock()
                    mock_client.get_tools = AsyncMock(return_value=mock_tools)
                    mock_client_class.return_value = mock_client

                    result = await get_mcp_tools(
                        session=mock_session,
                        mcp_ids=[mcp_id],
                        web_search=True
                    )

                    assert result == mock_tools
                    connections = mock_client_class.call_args[1]['connections']
                    assert connections['search'] == {'url': 'http://search/mcp', 'transport': 'stdio'}
                    assert connections['Web Search'] == {'url': 'http://web-search', 'transport': 'sse'}

    async def test_excludes_web_search_when_disabled(self):
        """Test that web search is not included by default."""
        mcp_id = uuid.uuid4()

        mock_session = MagicMock()
        mock_tools = [MagicMock()]

        with patch('tools.mcp_tools.get_mcp_by_id') as mock_get_mcp:
            with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
                mock_get_mcp.side_effect = [
                    MCPConfig(id=mcp_id, name='search', url='http://search', transport='stdio')
                ]

                mock_client = MagicMock()
                mock_client.get_tools = AsyncMock(return_value=mock_tools)
                mock_client_class.return_value = mock_client

                result = await get_mcp_tools(session=mock_session, mcp_ids=[mcp_id], web_search=False)

                assert result == mock_tools
                connections = mock_client_class.call_args[1]['connections']
                assert 'Web Search' not in connections

    async def test_handles_missing_mcp(self):
        """Test that ValueError is raised when an MCP is not found."""
        mcp_id = uuid.uuid4()

        mock_session = MagicMock()

        with patch('tools.mcp_tools.get_mcp_by_id') as mock_get_mcp:
            mock_get_mcp.side_effect = ValueError("MCP with ID")

            with pytest.raises(ValueError):
                await get_mcp_tools(session=mock_session, mcp_ids=[mcp_id])

    async def test_fetches_mcps_in_parallel(self):
        """Test that MCPs are fetched in parallel using asyncio.gather."""
        mcp_id_1 = uuid.uuid4()
        mcp_id_2 = uuid.uuid4()

        mock_session = MagicMock()
        mock_tools = []

        with patch('tools.mcp_tools.get_mcp_by_id') as mock_get_mcp:
            with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
                with patch('tools.mcp_tools.asyncio.gather', wraps=__import__('asyncio').gather) as mock_gather:
                    mock_get_mcp.side_effect = [
                        MCPConfig(id=mcp_id_1, name='search', url='http://search', transport='stdio'),
                        MCPConfig(id=mcp_id_2, name='files', url='http://files', transport='sse')
                    ]

                    mock_client = MagicMock()
                    mock_client.get_tools = AsyncMock(return_value=mock_tools)
                    mock_client_class.return_value = mock_client

                    await get_mcp_tools(session=mock_session, mcp_ids=[mcp_id_1, mcp_id_2])

                    mock_gather.assert_called_once()
