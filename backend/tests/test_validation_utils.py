import pytest
from utils.validators import PromptValidator
from utils.prompt_generator import PromptGenerator
from backend.app.models.dtos import PromptCreate, GenerateRequest


class TestPromptValidator:
    """Test the prompt validation utility functions"""
    
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


class TestPromptGenerator:
    """Test the prompt generation utility functions"""
    
    def test_generate_prompt_text_with_all_fields(self):
        """Test generating prompt text with all fields filled"""
        prompt_data = PromptCreate(
            genre="pop",
            mood="energetic",
            style="vibrant",
            instruments="piano, guitar",
            voice_tags="smooth, powerful",
            lyrics_structure="verse-chorus-bridge",
            custom_text="Additional custom elements"
        )
        
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = "pop, energetic, vibrant, piano, guitar, smooth, powerful, verse-chorus-bridge, Additional custom elements"
        assert result == expected

    def test_generate_prompt_text_with_some_fields(self):
        """Test generating prompt text with some fields filled"""
        prompt_data = PromptCreate(
            genre="rock",
            mood="intense"
        )
        
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = "rock, intense"
        assert result == expected

    def test_generate_prompt_text_empty(self):
        """Test generating prompt text with no fields filled"""
        prompt_data = PromptCreate()
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = ""
        assert result == expected

    def test_generate_prompt_from_request_with_all_fields(self):
        """Test generating prompt from request with all fields"""
        request = GenerateRequest(
            genre="electronic",
            mood="energetic",
            style="dynamic",
            instruments="synthesizer, drums",
            voice_tags="robotic, futuristic",
            lyrics_structure="verse-chorus",
            custom_elements={"tempo": "120 BPM", "key": "C Major"}
        )
        
        result = PromptGenerator.generate_prompt_from_request(request)
        expected = "electronic, energetic, dynamic, synthesizer, drums, robotic, futuristic, verse-chorus, 120 BPM, C Major"
        assert result == expected

    def test_generate_fusion_prompt(self):
        """Test generating a fusion prompt"""
        result = PromptGenerator.generate_fusion_prompt("jazz", "hip-hop", "energetic", "smooth")
        expected = "jazz-hip-hop, energetic, smooth, fusion, blend, combination"
        assert result == expected

    def test_generate_fusion_prompt_without_optional_params(self):
        """Test generating a fusion prompt without optional parameters"""
        result = PromptGenerator.generate_fusion_prompt("rock", "classical")
        expected = "rock-classical, fusion, blend, combination"
        assert result == expected

    def test_generate_voice_tag_prompt(self):
        """Test generating a voice tag prompt"""
        result = PromptGenerator.generate_voice_tag_prompt(["smooth", "powerful"])
        expected = "smooth, powerful, vocal manipulation, voice style"
        assert result == expected

    def test_generate_voice_tag_prompt_empty(self):
        """Test generating a voice tag prompt with empty list"""
        result = PromptGenerator.generate_voice_tag_prompt([])
        expected = ""
        assert result == expected

    def test_generate_instrumental_prompt(self):
        """Test generating an instrumental prompt"""
        result = PromptGenerator.generate_instrumental_prompt(["piano", "guitar"])
        expected = "piano, guitar, instrumental, musical arrangement"
        assert result == expected

    def test_generate_instrumental_prompt_empty(self):
        """Test generating an instrumental prompt with empty list"""
        result = PromptGenerator.generate_instrumental_prompt([])
        expected = ""
        assert result == expected
    
    def test_generate_prompt_text_with_none_values(self):
        """Test generating prompt text with None values"""
        prompt_data = PromptCreate(
            genre=None,
            mood="energetic",
            style=None,
            instruments="piano",
            voice_tags=None
        )
        
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = "energetic, piano"
        assert result == expected
    
    def test_generate_prompt_text_with_empty_string_values(self):
        """Test generating prompt text with empty string values"""
        prompt_data = PromptCreate(
            genre="",
            mood="energetic",
            style="",
            instruments="piano",
            voice_tags=""
        )
        
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = "energetic, piano"
        assert result == expected


class TestAdvancedValidationFeatures:
    """Test advanced validation features based on documentation requirements"""
    
    def test_validate_combination_styles(self):
        """Test validation for combination styles as mentioned in docs"""
        prompt_data = {
            "genre": "jazztronica",
            "mood": "groovy",
            "instruments": "electric piano",
            "custom_text": "Urban nightlife, Crisp and clean production, Jazz and electronica fusion"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_time_period_themes(self):
        """Test validation for time period themes as mentioned in docs"""
        prompt_data = {
            "genre": "synthwave",
            "mood": "nostalgic",
            "instruments": "synthesizers",
            "custom_text": "1980s influence, 80s futurism, Analog warmth"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_artist_inspired_prompts(self):
        """Test validation for artist-inspired prompts as mentioned in docs"""
        prompt_data = {
            "genre": "soul",
            "mood": "emotional",
            "style": "torch-lounge",
            "voice_tags": "female vocals"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_multigenre_combinations(self):
        """Test validation for multi-genre combinations as mentioned in docs"""
        prompt_data = {
            "genre": "jazz, blues, dubstep, acapella",
            "custom_text": "Blending multiple genres to create a hybrid"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_cultural_influences(self):
        """Test validation for cultural influences as mentioned in docs"""
        prompt_data = {
            "genre": "ambient",
            "mood": "reflective",
            "instruments": "sitar",
            "custom_text": "Indian classical influence, Urban meditation, Lo-fi textures"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_emotional_arc_prompts(self):
        """Test validation for emotional arc prompts as mentioned in docs"""
        prompt_data = {
            "genre": "cinematic",
            "mood": "triumphant",
            "instruments": "strings",
            "custom_text": "Emotional journey from despair to victory, Dynamic shifts"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_environmental_soundscapes(self):
        """Test validation for environmental soundscapes as mentioned in docs"""
        prompt_data = {
            "genre": "chillout",
            "mood": "calm",
            "instruments": "acoustic guitar",
            "custom_text": "Evening solitude, Rainfall and distant thunder, Reverb-drenched"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_rhythm_variations(self):
        """Test validation for rhythm variations as mentioned in docs"""
        prompt_data = {
            "genre": "experimental",
            "mood": "unsettling",
            "instruments": "percussion",
            "custom_text": "Time distortion, Polyrhythmic layers, Constantly shifting tempos"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_instrument_combinations(self):
        """Test validation for instrument combinations as mentioned in docs"""
        prompt_data = {
            "genre": "folk",
            "mood": "introspective",
            "instruments": "banjo and synthesizer",
            "custom_text": "Rural futurism, Minimalist, Acoustic and electronic blend"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_harmony_complexity(self):
        """Test validation for harmony complexity as mentioned in docs"""
        prompt_data = {
            "genre": "jazz",
            "mood": "complex",
            "instruments": "piano",
            "custom_text": "Inner conflict, Layered harmonies, Dissonant and unresolved chords"
        }
        
        result = PromptValidator.validate_prompt_elements(prompt_data)
        
        assert result["is_valid"] is True
        assert len(result["errors"]) == 0