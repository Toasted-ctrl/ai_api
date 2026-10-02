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
        mock_tool_1 = MagicMock()
        mock_tool_2 = MagicMock()
        mock_tools = [mock_tool_1, mock_tool_2]

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
                first_call_connections = mock_client_class.call_args_list[0][1]['connections']
                assert first_call_connections == {
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

    async def test_includes_web_search_when_enabled(self):
        """Test that web search tools are included and filtered when enabled."""
        mcp_id = uuid.uuid4()

        mock_session = MagicMock()
        mock_regular_tool = MagicMock()
        mock_regular_tool.name = 'regular_tool'
        mock_firecrawl_map = MagicMock()
        mock_firecrawl_map.name = 'firecrawl_map'
        mock_firecrawl_scrape = MagicMock()
        mock_firecrawl_scrape.name = 'firecrawl_scrape'
        mock_firecrawl_crawl = MagicMock()
        mock_firecrawl_crawl.name = 'firecrawl_crawl'
        mock_other_tool = MagicMock()
        mock_other_tool.name = 'other_tool'

        with patch('tools.mcp_tools.get_mcp_by_id') as mock_get_mcp:
            with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
                with patch('tools.mcp_tools.config') as mock_config:
                    mock_get_mcp.side_effect = [
                        MCPConfig(id=mcp_id, name='search', url='http://search', transport='stdio')
                    ]
                    mock_config.WEB_SEARCH_URL = 'http://web-search'
                    mock_config.WEB_SEARCH_TRANSPORT = 'sse'

                    mock_client = MagicMock()
                    # First call: regular MCPs, second call: web search
                    mock_client.get_tools = AsyncMock(side_effect=[
                        [mock_regular_tool],
                        [mock_firecrawl_map, mock_firecrawl_scrape, mock_firecrawl_crawl, mock_other_tool]
                    ])
                    mock_client_class.return_value = mock_client

                    result = await get_mcp_tools(
                        session=mock_session,
                        mcp_ids=[mcp_id],
                        web_search=True
                    )

                    # Should include regular tool and filtered web search tools
                    assert mock_regular_tool in result
                    assert mock_firecrawl_map in result
                    assert mock_firecrawl_scrape in result
                    assert mock_firecrawl_crawl in result
                    assert mock_other_tool not in result
                    assert len(result) == 4

    async def test_excludes_web_search_when_disabled(self):
        """Test that web search is not included when disabled."""
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
                # Should only have one client call (for regular MCPs)
                assert mock_client_class.call_count == 1
                connections = mock_client_class.call_args_list[0][1]['connections']
                assert 'Web Search' not in connections

    async def test_filters_web_search_tools_to_firecrawl_only(self):
        """Test that only allowed Firecrawl tools are returned from web search."""
        mock_session = MagicMock()
        mock_firecrawl_map = MagicMock()
        mock_firecrawl_map.name = 'firecrawl_map'
        mock_firecrawl_scrape = MagicMock()
        mock_firecrawl_scrape.name = 'firecrawl_scrape'
        mock_firecrawl_crawl = MagicMock()
        mock_firecrawl_crawl.name = 'firecrawl_crawl'
        mock_other_tool = MagicMock()
        mock_other_tool.name = 'some_other_tool'

        with patch('tools.mcp_tools.MultiServerMCPClient') as mock_client_class:
            with patch('tools.mcp_tools.config') as mock_config:
                mock_config.WEB_SEARCH_URL = 'http://web-search'
                mock_config.WEB_SEARCH_TRANSPORT = 'sse'

                mock_client = MagicMock()
                # Only web search client is called
                mock_client.get_tools = AsyncMock(return_value=[
                    mock_firecrawl_map, mock_firecrawl_scrape, mock_firecrawl_crawl, mock_other_tool
                ])
                mock_client_class.return_value = mock_client

                result = await get_mcp_tools(session=mock_session, mcp_ids=[], web_search=True)

                assert mock_firecrawl_map in result
                assert mock_firecrawl_scrape in result
                assert mock_firecrawl_crawl in result
                assert mock_other_tool not in result
                assert len(result) == 3

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

                    # asyncio.gather is called once for fetching MCPs by ID
                    assert mock_gather.call_count >= 1
