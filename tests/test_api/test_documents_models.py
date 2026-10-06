"""
Tests for the API models in the documents module.
"""

import uuid
import pytest
from pydantic import ValidationError

from iom.skills import PayloadCreateSkill, ResponseCreateSkill
from iom.vector_store import PayloadSaveDocuments, PayloadSearchDocuments, ResponseSavedDocuments
from iom.documents import Document, ResponseDocuments, ResponseDeleteDocument
from iom.vector_embedding import PayloadSingleVectorEmbedding, ResponseSingleVectorEmbedding


class TestSkillsModels:
    """Tests for the skills Pydantic models."""

    def test_payload_create_skill_valid(self):
        """Test that valid payload is accepted."""
        payload = PayloadCreateSkill(
            name="test_skill",
            description="A test skill description",
            skill_text="def test_skill(): pass",
            parameters_schema={"type": "object"}
        )
        
        assert payload.name == "test_skill"
        assert payload.description == "A test skill description"
        assert payload.skill_text == "def test_skill(): pass"
        assert payload.parameters_schema == {"type": "object"}

    def test_payload_create_skill_missing_required_fields(self):
        """Test that missing required fields raise validation errors."""
        # Test missing name
        with pytest.raises(ValidationError) as exc_info:
            PayloadCreateSkill(
                description="A test skill description",
                skill_text="def test_skill(): pass"
            )
        assert "name" in str(exc_info.value)

        # Test missing description
        with pytest.raises(ValidationError) as exc_info:
            PayloadCreateSkill(
                name="test_skill",
                skill_text="def test_skill(): pass"
            )
        assert "description" in str(exc_info.value)

        # Test missing skill_text
        with pytest.raises(ValidationError) as exc_info:
            PayloadCreateSkill(
                name="test_skill",
                description="A test skill description"
            )
        assert "skill_text" in str(exc_info.value)

    def test_payload_create_skill_optional_parameters_schema(self):
        """Test that parameters_schema is optional."""
        payload = PayloadCreateSkill(
            name="test_skill",
            description="A test skill description",
            skill_text="def test_skill(): pass"
        )
        
        assert payload.parameters_schema is None

    def test_response_create_skill_valid(self):
        """Test that valid response is created."""
        skill_id = uuid.uuid4()
        response = ResponseCreateSkill(
            skill_id=skill_id,
            name="test_skill",
            message="Skill created successfully"
        )
        
        assert response.skill_id == skill_id
        assert response.name == "test_skill"
        assert response.message == "Skill created successfully"


class TestVectorStoreModels:
    """Tests for the vector store Pydantic models."""

    def test_payload_save_documents_valid(self):
        """Test that valid PayloadSaveDocuments is accepted."""
        payload = PayloadSaveDocuments(
            texts=["test document 1", "test document 2"],
            metadatas=[
                {"document_name": "doc1"},
                {"document_name": "doc2"}
            ]
        )
        
        assert len(payload.texts) == 2
        assert len(payload.metadatas) == 2
        assert payload.metadatas[0].document_name == "doc1"

    def test_payload_save_documents_empty_lists(self):
        """Test that empty lists are accepted."""
        payload = PayloadSaveDocuments(texts=[], metadatas=[])
        
        assert len(payload.texts) == 0
        assert len(payload.metadatas) == 0

    def test_payload_search_documents_valid(self):
        """Test that valid PayloadSearchDocuments is accepted."""
        payload = PayloadSearchDocuments(query="test search query")
        
        assert payload.query == "test search query"

    def test_response_saved_documents_valid(self):
        """Test that valid ResponseSavedDocuments is accepted."""
        doc_id = uuid.uuid4()
        response = ResponseSavedDocuments(added_documents=[doc_id, uuid.uuid4()])
        
        assert len(response.added_documents) == 2
        assert response.added_documents[0] == doc_id


class TestDocumentsModels:
    """Tests for the documents Pydantic models."""

    def test_document_model_valid(self):
        """Test that valid Document model is accepted."""
        doc_id = uuid.uuid4()
        doc = Document(name="test_doc", id=doc_id)
        
        assert doc.name == "test_doc"
        assert doc.id == doc_id

    def test_response_documents_valid(self):
        """Test that valid ResponseDocuments is accepted."""
        doc_id = uuid.uuid4()
        response = ResponseDocuments(
            documents_scope="user_vs_files",
            documents=[
                {"name": "doc1", "id": str(uuid.uuid4())},
                {"name": "doc2", "id": str(uuid.uuid4())}
            ]
        )
        
        assert response.documents_scope == "user_vs_files"
        assert len(response.documents) == 2

    def test_response_delete_document_valid(self):
        """Test that valid ResponseDeleteDocument is accepted."""
        doc_id = uuid.uuid4()
        response = ResponseDeleteDocument(id=doc_id, is_deleted=True)
        
        assert response.id == doc_id
        assert response.is_deleted is True

    def test_response_delete_document_false(self):
        """Test ResponseDeleteDocument with is_deleted=False."""
        doc_id = uuid.uuid4()
        response = ResponseDeleteDocument(id=doc_id, is_deleted=False)
        
        assert response.id == doc_id
        assert response.is_deleted is False


class TestVectorEmbeddingModels:
    """Tests for the vector embedding Pydantic models."""

    def test_payload_single_vector_embedding_valid(self):
        """Test that valid PayloadSingleVectorEmbedding is accepted."""
        payload = PayloadSingleVectorEmbedding(
            prompt="test prompt",
            provider="openai",
            model="text-embedding-3-small",
            dimensions=1536
        )
        
        assert payload.prompt == "test prompt"
        assert payload.provider == "openai"
        assert payload.model == "text-embedding-3-small"
        assert payload.dimensions == 1536

    def test_response_single_vector_embedding_valid(self):
        """Test that valid ResponseSingleVectorEmbedding is accepted."""
        embedding = [0.1, 0.2, 0.3] * 512  # 1536-dimensional embedding
        response = ResponseSingleVectorEmbedding(
            prompt="test prompt",
            provider="openai",
            model="text-embedding-3-small",
            dimensions=1536,
            embedding=embedding
        )
        
        assert response.prompt == "test prompt"
        assert response.provider == "openai"
        assert response.model == "text-embedding-3-small"
        assert response.dimensions == 1536
        assert len(response.embedding) == 1536