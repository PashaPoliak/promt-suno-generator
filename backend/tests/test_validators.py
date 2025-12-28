import pytest
from utils.validators import PromptValidator


class TestPromptValidator:
    def test_validate_prompt_elements_with_valid_data(self):
        """Test validation with valid prompt elements"""
        prompt_data = {
            "genre": "pop",
            "mood": "energetic",
            "style": "vibrant",
            "instruments": "piano, guitar",
            "voice_tags": "smooth, powerful"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0

    def test_validate_prompt_elements_missing_required_fields(self):
        """Test validation with missing required fields"""
        prompt_data = {
            "custom_text": "some custom text"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True  # Not invalid, just has warnings
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "at least one of genre, mood, style, instruments, or voice_tags should be specified" in result["warnings"][0].lower()

    def test_validate_prompt_elements_invalid_genre_length(self):
        """Test validation with invalid genre length"""
        prompt_data = {
            "genre": "a",  # Too short
            "mood": "energetic"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "genre should be at least 2 characters long" in result["errors"][0]

    def test_validate_prompt_elements_excessive_genre_length(self):
        """Test validation with excessive genre length"""
        prompt_data = {
            "genre": "a" * 51,  # Too long
            "mood": "energetic"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "genre should not exceed 50 characters" in result["errors"][0]

    def test_validate_prompt_elements_invalid_mood_length(self):
        """Test validation with invalid mood length"""
        prompt_data = {
            "genre": "pop",
            "mood": "a" # Too short
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "mood should be at least 2 characters long" in result["errors"][0]

    def test_validate_prompt_elements_invalid_style_length(self):
        """Test validation with invalid style length"""
        prompt_data = {
            "genre": "pop",
            "mood": "energetic",
            "style": "a"  # Too short
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "style should be at least 2 characters long" in result["errors"][0]

    def test_validate_prompt_elements_excessive_prompt_length(self):
        """Test validation with excessive combined prompt length"""
        prompt_data = {
            "genre": "pop",
            "mood": "energetic",
            "style": "vibrant",
            "instruments": "piano, guitar, drums, bass, synthesizer, violin, cello, flute, clarinet, saxophone",
            "voice_tags": "smooth, powerful, airy, breathy, crisp, deep, gritty, warm, raw, sharp, muffled, bright, mellow, raspy, clear, thin, dense"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "combined prompt length exceeds 200 characters" in result["warnings"][0].lower()

    def test_validate_prompt_text_valid(self):
        """Test validation with valid prompt text"""
        prompt_text = "pop, energetic, vibrant, piano, guitar"
        
        result = PromptValidator.validate_prompt_text(prompt_text)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 0

    def test_validate_prompt_text_empty(self):
        """Test validation with empty prompt text"""
        prompt_text = ""
        
        result = PromptValidator.validate_prompt_text(prompt_text)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "prompt text cannot be empty" in result["errors"][0]

    def test_validate_prompt_text_none(self):
        """Test validation with None prompt text"""
        prompt_text = None
        
        result = PromptValidator.validate_prompt_text(prompt_text)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "prompt text cannot be empty" in result["errors"][0]

    def test_validate_prompt_text_excessive_length(self):
        """Test validation with excessive prompt text length"""
        prompt_text = "a" * 501  # Too long
        
        result = PromptValidator.validate_prompt_text(prompt_text)
        
        assert result["is_valid"] is False
        assert len(result["errors"]) == 1
        assert "prompt text exceeds 500 characters" in result["errors"][0]

    def test_validate_prompt_text_long_warning(self):
        """Test validation with long prompt text that generates warning"""
        prompt_text = "a" * 301  # Long but not too long
        
        result = PromptValidator.validate_prompt_text(prompt_text)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert len(result["warnings"]) == 1
        assert "prompt text is quite long" in result["warnings"][0].lower()