from unittest.mock import patch, MagicMock
import rag_service.embed as embed_mod

def test_embed_texts_calls_client_with_document_type():
	fake_client= MagicMock()
	fake_client.embed.return_value= MagicMock(embeddings=[[0.1,0.2,0.3]])
	with patch.object(embed_mod,"_client",None), patch("rag_service.embed.voyageai.Client",return_value=fake_client):
		result= embed_mod.embed_texts(["hello world"])
	assert result== [[0.1,0.2,0.3]]
	fake_client.embed.assert_called_once()
	_,kwargs= fake_client.embed.call_args
	assert kwargs["input_type"]== "document"

def test_embed_query_uses_query_input_type():
	fake_client= MagicMock()
	fake_client.embed.return_value= MagicMock(embeddings=[[0.5,0.5]])
	with patch.object(embed_mod,"_client",None), patch("rag_service.embed.voyageai.Client",return_value=fake_client):
		result= embed_mod.embed_query("why did it drop")
	assert result== [0.5,0.5]
	_,kwargs= fake_client.embed.call_args
	assert kwargs["input_type"]== "query"

def test_get_client_only_constructs_once():
	fake_client= MagicMock()
	with patch.object(embed_mod,"_client",None), patch("rag_service.embed.voyageai.Client",return_value=fake_client) as ctor:
		embed_mod.get_client()
		embed_mod.get_client()
	ctor.assert_called_once()