from typing import List, Dict, Any, Optional
from models.prompt import PromptCreate, GenerateRequest


class PromptGenerator:
    @staticmethod
    def generate_prompt_text(prompt_data: PromptCreate) -> str:
        elements = []
        
        if prompt_data.genre:
            elements.append(prompt_data.genre)
        if prompt_data.mood:
            elements.append(prompt_data.mood)
        if prompt_data.style:
            elements.append(prompt_data.style)
        if prompt_data.instruments:
            elements.append(prompt_data.instruments)
        if prompt_data.voice_tags:
            elements.append(prompt_data.voice_tags)
        if prompt_data.lyrics_structure:
            elements.append(prompt_data.lyrics_structure)
        if prompt_data.custom_text:
            elements.append(prompt_data.custom_text)
        
        return ", ".join(elements)

    @staticmethod
    def generate_prompt_from_request(request: GenerateRequest) -> str:
        elements = []
        
        if request.genre:
            elements.append(request.genre)
        if request.mood:
            elements.append(request.mood)
        if request.style:
            elements.append(request.style)
        if request.instruments:
            elements.append(request.instruments)
        if request.voice_tags:
            elements.append(request.voice_tags)
        if request.lyrics_structure:
            elements.append(request.lyrics_structure)
        
        if request.custom_elements:
            for key, value in request.custom_elements.items():
                if isinstance(value, str):
                    elements.append(value)
                else:
                    elements.append(str(value))
        
        return ", ".join(elements)

    @staticmethod
    def generate_fusion_prompt(genre1: str, genre2: str, mood: Optional[str] = None, style: Optional[str] = None) -> str:
        elements = [f"{genre1}-{genre2}"]
        
        if mood:
            elements.append(mood)
        if style:
            elements.append(style)
        
        elements.extend([
            "fusion",
            "blend",
            "combination"
        ])
        
        return ", ".join(elements)

    @staticmethod
    def generate_voice_tag_prompt(voice_tags: List[str]) -> str:
        if not voice_tags:
            return ""
        
        elements = []
        elements.extend(voice_tags)
        
        elements.append("vocal manipulation")
        elements.append("voice style")
        
        return ", ".join(elements)

    @staticmethod
    def generate_instrumental_prompt(instruments: List[str]) -> str:
        if not instruments:
            return ""
        
        elements = instruments
        elements.append("instrumental")
        elements.append("musical arrangement")
        
        return ", ".join(elements)