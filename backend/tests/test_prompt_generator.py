import pytest
from utils.prompt_generator import PromptGenerator


class TestPromptGenerator:
    def test_generate_prompt_text_with_all_fields(self):
        """Test generating prompt text with all fields filled"""
        from backend.app.models.dtos import PromptCreate
        
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
        from backend.app.models.dtos import PromptCreate
        
        prompt_data = PromptCreate(
            genre="rock",
            mood="intense"
        )
        
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = "rock, intense"
        assert result == expected

    def test_generate_prompt_text_empty(self):
        """Test generating prompt text with no fields filled"""
        from backend.app.models.dtos import PromptCreate
        
        prompt_data = PromptCreate()
        result = PromptGenerator.generate_prompt_text(prompt_data)
        expected = ""
        assert result == expected

    def test_generate_prompt_from_request_with_all_fields(self):
        """Test generating prompt from request with all fields"""
        from backend.app.models.dtos import GenerateRequest
        
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