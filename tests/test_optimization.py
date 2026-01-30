import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.modules['bitsandbytes'] = MagicMock()
sys.modules['chromadb'] = MagicMock()

class TestOptimization(unittest.TestCase):

    @patch('src.heady_project.nlp_service.pipeline')
    @patch('src.heady_project.nlp_service.HuggingFacePipeline')
    @patch('src.heady_project.nlp_service.chromadb.Client')
    def test_nlp_service_initialization(self, mock_chroma, mock_hf_pipeline, mock_pipeline):
        mock_chroma.return_value.get_or_create_collection.return_value = MagicMock()
        mock_pipeline.return_value = MagicMock()

        from src.heady_project.nlp_service import NLPService
        service = NLPService()
        service.initialized = False
        service.initialize()

        self.assertTrue(service.initialized)
        mock_chroma.assert_called_once()
        self.assertEqual(mock_pipeline.call_count, 2)

    @patch('src.heady_project.nlp_service.pipeline')
    @patch('src.heady_project.nlp_service.HuggingFacePipeline')
    @patch('src.heady_project.nlp_service.chromadb.Client')
    @patch('src.heady_project.nlp_service.ChatGoogleGenerativeAI')
    def test_gemini_integration(self, mock_gemini, mock_chroma, mock_hf, mock_pipeline):
        # Mock dependencies to prevent real initialization failure
        mock_chroma.return_value.get_or_create_collection.return_value = MagicMock()
        mock_pipeline.return_value = MagicMock()

        from src.heady_project.nlp_service import NLPService
        service = NLPService()

        # Test without key
        with patch.dict(os.environ, {}, clear=True):
            service.initialized = False
            service.gemini_llm = None
            service.initialize()
            self.assertIsNone(service.gemini_llm)

        # Test with key
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'fake_key'}):
            service.initialized = False
            service.gemini_llm = None
            service.initialize()
            mock_gemini.assert_called_once()
            self.assertIsNotNone(service.gemini_llm)

if __name__ == '__main__':
    unittest.main()
