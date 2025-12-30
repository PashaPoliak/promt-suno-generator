from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from models.entities import GeneratedPrompt, PromptTemplate
from models.prompt import PromptResponse, PromptCreate, GenerateRequest, GenerateResponse
from utils.prompt_generator import PromptGenerator


class PromptService:
    @staticmethod
    async def get_prompts(db: Session, skip: int = 0, limit: int = 100) -> List[PromptResponse]:
        prompts = db.query(GeneratedPrompt).offset(skip).limit(limit).all()
        return [
            PromptResponse.model_validate(prompt)
            for prompt in prompts
        ]

    @staticmethod
    async def create_prompt(db: Session, prompt: PromptCreate) -> PromptResponse:
        # Generate prompt_text if not provided
        if prompt.prompt_text is None or prompt.prompt_text == "":
            prompt_text = PromptGenerator.generate_prompt_text(prompt)
        else:
            prompt_text = prompt.prompt_text
        
        db_prompt = GeneratedPrompt(
            prompt_text=prompt_text,
            parameters=prompt.dict(),
            is_favorite=prompt.is_favorite,
            generation_result=prompt.generation_result
        )
        
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        
        return PromptResponse.model_validate(db_prompt)

    @staticmethod
    async def get_prompt(db: Session, prompt_id: str) -> Optional[PromptResponse]:
        prompt = db.query(GeneratedPrompt).filter(GeneratedPrompt.id == prompt_id).first()
        if prompt:
            return PromptResponse.model_validate(prompt)
        return None

    @staticmethod
    async def generate_prompt(db: Session, request: GenerateRequest) -> GenerateResponse:
        prompt_text = PromptGenerator.generate_prompt_from_request(request)
        
        db_prompt = GeneratedPrompt(
            prompt_text=prompt_text,
            parameters=request.dict()
        )
        
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        validation_result = {
            "is_valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        return GenerateResponse(
            id=str(db_prompt.id),
            prompt_text=str(db_prompt.prompt_text or ""),
            generated_at=datetime.utcnow(),
            parameters_used=request.dict(),
            validation_result=validation_result
        )

    @staticmethod
    async def generate_prompts_batch(db: Session, requests: List[GenerateRequest]) -> List[GenerateResponse]:
        responses = []
        for request in requests:
            response = await PromptService.generate_prompt(db, request)
            responses.append(response)
        return responses

    @staticmethod
    async def update_prompt(db: Session, prompt_id: str, prompt: PromptCreate) -> Optional[PromptResponse]:
        db_prompt = db.query(GeneratedPrompt).filter(GeneratedPrompt.id == prompt_id).first()
        if not db_prompt:
            return None
        
        # Update fields
        # Generate prompt_text if not provided
        if prompt.prompt_text is None or prompt.prompt_text == "":
            prompt_text = PromptGenerator.generate_prompt_text(prompt)
        else:
            prompt_text = prompt.prompt_text
        
        setattr(db_prompt, 'prompt_text', prompt_text)
        setattr(db_prompt, 'parameters', prompt.dict())
        setattr(db_prompt, 'is_favorite', prompt.is_favorite)
        
        db.commit()
        db.refresh(db_prompt)
        
        return PromptResponse.model_validate(db_prompt)

    @staticmethod
    async def delete_prompt(db: Session, prompt_id: str) -> bool:
        db_prompt = db.query(GeneratedPrompt).filter(GeneratedPrompt.id == prompt_id).first()
        if not db_prompt:
            return False
        
        db.delete(db_prompt)
        db.commit()
        return True