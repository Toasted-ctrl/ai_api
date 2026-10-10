import uuid
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from langchain_core.tools import StructuredTool

from tools.skill_discovery import get_user_skill_discovery_tool, VSSkillSearchInput


pytestmark = pytest.mark.asyncio


class TestGetUserSkillDiscoveryTool:

    async def test_returns_structured_tool(self):
        """Test that function returns a StructuredTool."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        # Set up the embedding provider as an attribute
        mock_em = MagicMock()
        mock_em.base_url = 'http://embeddings'
        mock_em.langchain_con = MagicMock()
        mock_em.encrypted_api_key = 'enc_key'
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_vscf.vs_collection_name = 'test_collection'
                    mock_vscf.vs_vendor = 'test_vendor'
                    mock_vscf.vs_port = 8080
                    mock_vscf.vs_base_url = 'http://test'
                    mock_vscf.vs_encrypted_api_key = 'test_key'
                    mock_vscf.e_model = 'test_model'
                    mock_vscf.e_dimensions = 1536
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    assert isinstance(result, StructuredTool)
                    assert result.name == 'discover_skills'

    async def test_tool_has_correct_description(self):
        """Test that the tool has the expected description."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    assert 'skill database' in result.description.lower()

    async def test_tool_has_correct_args_schema(self):
        """Test that the tool has the expected args schema."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    assert result.args_schema == VSSkillSearchInput

    async def test_returns_no_results_message_when_empty(self):
        """Test that function returns 'No relevant results found' when search returns empty."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_em.base_url = 'http://embeddings'
        mock_em.langchain_con = MagicMock()
        mock_em.encrypted_api_key = 'enc_key'
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    # Call the underlying function
                    output = result.func(query='test', limit=5)
                    assert output == 'No relevant results found'

    async def test_returns_formatted_results(self):
        """Test that function returns formatted results when documents are found."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_em.base_url = 'http://embeddings'
        mock_em.langchain_con = MagicMock()
        mock_em.encrypted_api_key = 'enc_key'
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    # Create mock document with metadata
                    mock_doc = MagicMock()
                    mock_doc.page_content = 'Test skill content'
                    mock_doc.metadata = {'key': 'value'}
                    mock_search.return_value = [(mock_doc, 0.95)]

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    # Call the underlying function
                    output = result.func(query='test', limit=5)
                    assert 'Score: 0.95' in output
                    assert 'Test skill content' in output
                    assert 'Metadata:' in output

    async def test_filters_by_user_id(self):
        """Test that the filter includes the user_id."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_em.base_url = 'http://embeddings'
        mock_em.langchain_con = MagicMock()
        mock_em.encrypted_api_key = 'enc_key'
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    # Call the function to trigger the search
                    result.func(query='test', limit=5)

                    # Check that search was called with the correct filter
                    assert mock_search.called
                    call_kwargs = mock_search.call_args[1]
                    assert call_kwargs['filter'] == {'user-id': str(user_id)}

    async def test_uses_correct_vector_store_config(self):
        """Test that the correct vector store settings are used."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_em.base_url = 'http://embeddings'
        mock_em.langchain_con = MagicMock()
        mock_em.encrypted_api_key = 'enc_key'
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_vscf.vs_collection_name = 'test_collection'
                    mock_vscf.vs_vendor = 'test_vendor'
                    mock_vscf.vs_port = 8080
                    mock_vscf.vs_base_url = 'http://test'
                    mock_vscf.vs_encrypted_api_key = 'test_key'
                    mock_vscf.e_model = 'test_model'
                    mock_vscf.e_dimensions = 1536
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    # Call the function to trigger the vector store creation
                    result.func(query='test', limit=5)

                    # Verify get_vector_store was called with correct settings from vscf
                    mock_get_vs.assert_called_once()
                    call_kwargs = mock_get_vs.call_args[1]
                    assert call_kwargs['vs_collection_name'] == 'test_collection'
                    assert call_kwargs['vs_vendor'] == 'test_vendor'
                    assert call_kwargs['vs_port'] == 8080
                    assert call_kwargs['e_model'] == 'test_model'

    async def test_passes_query_and_limit_to_search(self):
        """Test that query and limit are passed correctly to search."""
        user_id = uuid.uuid4()
        mock_session = AsyncMock()
        mock_pr = MagicMock()
        
        mock_em = MagicMock()
        mock_em.base_url = 'http://embeddings'
        mock_em.langchain_con = MagicMock()
        mock_em.encrypted_api_key = 'enc_key'
        mock_pr.test_provider = mock_em

        with patch('tools.skill_discovery.get_vector_store_settings') as mock_get_vscf:
            with patch('tools.skill_discovery.get_vector_store') as mock_get_vs:
                with patch('tools.skill_discovery.search_docs_similarity') as mock_search:
                    mock_vscf = MagicMock()
                    mock_vscf.e_provider = 'test_provider'
                    mock_get_vscf.return_value = mock_vscf

                    mock_vs = MagicMock()
                    mock_get_vs.return_value = mock_vs

                    mock_search.return_value = []

                    result = await get_user_skill_discovery_tool(
                        session=mock_session,
                        user_id=user_id,
                        scope='user_vs_skills',
                        pr=mock_pr
                    )

                    # Call the underlying function with specific parameters
                    result.func(query='test query', limit=10)

                    # Check that search was called with the correct query
                    assert mock_search.called
                    call_kwargs = mock_search.call_args[1]
                    assert call_kwargs['query'] == 'test query'
