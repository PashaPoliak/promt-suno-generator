from typing import Dict, List, Any, Optional


class PromptValidator:
    @staticmethod
    def validate_prompt_elements(prompt_data: Dict[str, Any]) -> Dict[str, Any]:
        errors = []
        warnings = []
        suggestions = []
        
        # Check for required elements
        if not any([
            prompt_data.get('genre'),
            prompt_data.get('mood'),
            prompt_data.get('style'),
            prompt_data.get('instruments'),
            prompt_data.get('voice_tags')
        ]):
            warnings.append("At least one of genre, mood, style, instruments, or voice_tags should be specified")
        
        # Validate specific elements
        genre = prompt_data.get('genre')
        if genre:
            if len(genre) < 2:
                errors.append("genre should be at least 2 characters long")
            if len(genre) > 50:
                errors.append("genre should not exceed 50 characters")
        
        mood = prompt_data.get('mood')
        if mood:
            if len(mood) < 2:
                errors.append("mood should be at least 2 characters long")
            if len(mood) > 50:
                errors.append("mood should not exceed 50 characters")
        
        style = prompt_data.get('style')
        if style:
            if len(style) < 2:
                errors.append("style should be at least 2 characters long")
            if len(style) > 50:
                errors.append("style should not exceed 50 characters")
        
        # Check total prompt length if all elements were combined
        all_elements = []
        for key in ['genre', 'mood', 'style', 'instruments', 'voice_tags', 'lyrics_structure', 'custom_text']:
            value = prompt_data.get(key)
            if value:
                all_elements.append(str(value))
        
        combined_length = len(", ".join(all_elements))
        if combined_length > 200:
            warnings.append("Combined prompt length exceeds 200 characters, which may affect generation quality")
        
        # Generate suggestions
        if not prompt_data.get('instruments'):
            suggestions.append("Consider adding specific instruments to better control the sound")
        
        if not prompt_data.get('voice_tags'):
            suggestions.append("Consider adding voice tags for vocal characteristics")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }

    @staticmethod
    def validate_prompt_text(prompt_text: Optional[str]) -> Dict[str, Any]:
        errors = []
        warnings = []
        suggestions = []
        
        if not prompt_text or len(prompt_text.strip()) == 0:
            errors.append("prompt text cannot be empty")
            return {
                "is_valid": len(errors) == 0,
                "errors": errors,
                "warnings": warnings,
                "suggestions": suggestions
            }
        
        if len(prompt_text) > 500:
            errors.append("prompt text exceeds 500 characters")
        
        if len(prompt_text) > 300:
            warnings.append("Prompt text is quite long, consider shortening for better results")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions
        }