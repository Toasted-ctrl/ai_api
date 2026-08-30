from langchain_core.documents import Document
import uuid

from vs.save_docs import (
    _chunker,
    _prep_docs_personal_data,
    _normalize_texts,
    _sanitize_metadata
)


class TestChunker:

    def test_chunker_small_text(self):

        text = """
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
        Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """

        chunks = _chunker(text=text)
        assert isinstance(chunks, list)
        assert len(chunks) == 1


    def test_chunker_large_text(self):

        text = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """

        chunks = _chunker(text=text)
        assert isinstance(chunks, list)
        assert len(chunks) == 2


class TestPrepDocsPersonalData:

    def test_single_chunk(self):
        metadata = {"user_id": str(uuid.uuid4())}
        text = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """
        doc = _prep_docs_personal_data(texts=[text], metadatas=[metadata])
        assert isinstance(doc, list)
        assert isinstance(doc[0], Document)
        assert len(doc) == 1


    def test_multiple_chunks(self):

        metadata = {"user_id": str(uuid.uuid4())}
        text = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """

        docs = _prep_docs_personal_data(texts=[text], metadatas=[metadata])
        doc1 = docs[0]
        doc2 = docs[1]

        assert len(docs) == 2
        assert isinstance(docs, list)
        assert isinstance(doc1, Document)
        assert isinstance(doc2, Document)
        assert doc1.id != doc2.id
        assert doc1.metadata['chunk_id'] != doc2.metadata['chunk_id']
        assert doc1.metadata['document_hash'] == doc2.metadata['document_hash']
        assert doc1.metadata['user_id'] == doc2.metadata['user_id']


    def test_multiple_documents(self):

        metadata = {"user_id": str(uuid.uuid4())}
        text1 = """
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """

        text2 = """
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
        """

        docs = _prep_docs_personal_data(texts=[text1, text2], metadatas=[metadata, metadata])
        doc1 = docs[0]
        doc2 = docs[1]

        assert len(docs) == 2
        assert isinstance(docs, list)
        assert isinstance(doc1, Document)
        assert isinstance(doc2, Document)
        assert doc1.id != doc2.id
        assert doc1.metadata['chunk_id'] == doc2.metadata['chunk_id']
        assert doc1.metadata['document_hash'] != doc2.metadata['document_hash']
        assert doc1.metadata['user_id'] == doc2.metadata['user_id']


class TestNormalizeTexts:

    def test_text_unchanged(self):
        text = "This is an example text."
        result = _normalize_texts(texts=[text])

        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert len(result) == 1
        assert result[0] == text


    def test_remove_trailing_leading_spaces(self):
        text = "    This is an example text    "
        result = _normalize_texts(texts=[text])
        
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert len(result) == 1
        assert result[0] == "This is an example text"


    def test_remove_unnecessary_middle_spaces(self):
        text = "This      is an example text"
        result = _normalize_texts(texts=[text])
                
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert len(result) == 1
        assert result[0] == "This is an example text"


    def test_remove_additional_linebreaks(self):
        text = "This is \n\n\n\n an example text"
        result = _normalize_texts(texts=[text])
                        
        assert isinstance(result, list)
        assert isinstance(result[0], str)
        assert len(result) == 1
        assert result[0] == "This is\n\nan example text"


class TestSanitizeMetadata:

    def test_no_uuid(self):
        metadata = {
            "user": "test_user"
        }

        result = _sanitize_metadata(metadatas=[metadata])

        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert len(result) == 1
        assert result[0] == metadata


    def test_convert_uuid(self):
        metadata = {
            "user_id": uuid.uuid4()
        }

        result = _sanitize_metadata(metadatas=[metadata])
        
        assert isinstance(result, list)
        assert isinstance(result[0], dict)
        assert len(result) == 1
        assert result[0]['user_id'] == str(metadata['user_id'])