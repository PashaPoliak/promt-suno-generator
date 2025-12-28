from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
import uuid
from datetime import datetime

from models.database import GeneratedPrompt, PromptTemplate
from backend.app.models.dtos import PromptCreate, PromptResponse, GenerateRequest, GenerateResponse
from utils.prompt_generator import PromptGenerator


class PromptService:
    @staticmethod
    async def get_prompts(db: Session, skip: int = 0, limit: int = 100) -> List[PromptResponse]:
        prompts = db.query(GeneratedPrompt).offset(skip).limit(limit).all()
        return [
            PromptResponse(
                id=prompt.id,
                prompt_text=prompt.prompt_text,
                parameters=prompt.parameters,
                created_at=prompt.created_at,
                generation_result=prompt.generation_result
            )
            for prompt in prompts
        ]

    @staticmethod
    async def create_prompt(db: Session, prompt: PromptCreate) -> PromptResponse:
        prompt_text = PromptGenerator.generate_prompt_text(prompt)
        
        db_prompt = GeneratedPrompt(
            prompt_text=prompt_text,
            parameters=prompt.dict()
        )
        
        db.add(db_prompt)
        db.commit()
        db.refresh(db_prompt)
        
        return PromptResponse(
            id=db_prompt.id,
            prompt_text=db_prompt.prompt_text,
            parameters=db_prompt.parameters,
            created_at=db_prompt.created_at,
            generation_result=db_prompt.generation_result
        )

    @staticmethod
    async def get_prompt(db: Session, prompt_id: UUID) -> Optional[PromptResponse]:
        prompt = db.query(GeneratedPrompt).filter(GeneratedPrompt.id == prompt_id).first()
        if prompt:
            return PromptResponse(
                id=prompt.id,
                prompt_text=prompt.prompt_text,
                parameters=prompt.parameters,
                created_at=prompt.created_at,
                generation_result=prompt.generation_result
            )
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
        
        return GenerateResponse(
            id=db_prompt.id,
            prompt_text=db_prompt.prompt_text,
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
    async def update_prompt(db: Session, prompt_id: UUID, prompt: PromptCreate) -> Optional[PromptResponse]:
        db_prompt = db.query(GeneratedPrompt).filter(GeneratedPrompt.id == prompt_id).first()
        if not db_prompt:
            return None
        
        # Update fields
        prompt_text = PromptGenerator.generate_prompt_text(prompt)
        db_prompt.prompt_text = prompt_text
        db_prompt.parameters = prompt.dict()
        
        db.commit()
        db.refresh(db_prompt)
        
        return PromptResponse(
            id=db_prompt.id,
            prompt_text=db_prompt.prompt_text,
            parameters=db_prompt.parameters,
            created_at=db_prompt.created_at,
            generation_result=db_prompt.generation_result
        )

    @staticmethod
    async def delete_prompt(db: Session, prompt_id: UUID) -> bool:
        db_prompt = db.query(GeneratedPrompt).filter(GeneratedPrompt.id == prompt_id).first()
        if not db_prompt:
            return False
        
        db.delete(db_prompt)
        db.commit()
        return True