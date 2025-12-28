import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database.session import get_db
from models.database import Base
from backend.app.models.dtos import (
    PromptCreate, TemplateCreate, CategoryCreate, TagCreate,
    GenerateRequest
)


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create all tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db:
            db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestCompleteWorkflows:
    """Test complete end-to-end workflows based on documentation requirements"""
    
    def test_complete_prompt_generation_workflow(self):
        """Test the complete workflow of creating and generating prompts"""
        # Step 1: Create a category
        category_data = {
            "name": "Pop Music",
            "description": "Pop music category"
        }
        category_response = client.post("/api/v1/categories", json=category_data)
        assert category_response.status_code == 200
        category = category_response.json()
        category_id = category["id"]
        
        # Step 2: Create some tags
        tag_data = {
            "name": "upbeat",
            "tag_type": "mood"
        }
        tag_response = client.post("/api/v1/tags", json=tag_data)
        assert tag_response.status_code == 200
        tag = tag_response.json()
        tag_id = tag["id"]
        
        # Step 3: Create a template
        template_data = {
            "name": "Pop Template",
            "genre": "pop",
            "mood": "upbeat",
            "style": "vibrant",
            "instruments": "piano, guitar, drums",
            "category_id": category_id
        }
        template_response = client.post("/api/v1/templates", json=template_data)
        assert template_response.status_code == 200
        template = template_response.json()
        template_id = template["id"]
        
        # Step 4: Generate a prompt using the template
        generate_request = {
            "genre": "pop",
            "mood": "upbeat",
            "style": "vibrant",
            "instruments": "piano, guitar, drums",
            "custom_elements": {"tempo": "120 BPM"}
        }
        generate_response = client.post("/api/v1/prompts/generate", json=generate_request)
        assert generate_response.status_code == 200
        generated_prompt = generate_response.json()
        
        # Step 5: Verify the prompt was created correctly
        assert "id" in generated_prompt
        assert "prompt_text" in generated_prompt
        assert "pop, upbeat, vibrant, piano, guitar, drums, 120 BPM" in generated_prompt["prompt_text"]
        
        # Step 6: Create a prompt directly
        prompt_data = {
            "genre": "rock",
            "mood": "energetic",
            "style": "aggressive",
            "instruments": "guitar, bass, drums"
        }
        prompt_response = client.post("/api/v1/prompts", json=prompt_data)
        assert prompt_response.status_code == 200
        created_prompt = prompt_response.json()
        
        # Step 7: Verify the prompt was created
        assert "id" in created_prompt
        assert created_prompt["prompt_text"] == "rock, energetic, aggressive, guitar, bass, drums"
        
        # Step 8: Retrieve all prompts to confirm both were created
        all_prompts_response = client.get("/api/v1/prompts")
        assert all_prompts_response.status_code == 200
        all_prompts = all_prompts_response.json()
        assert len(all_prompts) == 2
    
    def test_template_based_generation_workflow(self):
        """Test workflow using templates for prompt generation"""
        # Create a template
        template_data = {
            "name": "Jazz Template",
            "genre": "jazz",
            "mood": "smooth",
            "style": "sultry",
            "instruments": "saxophone, piano, double bass"
        }
        template_response = client.post("/api/v1/templates", json=template_data)
        assert template_response.status_code == 200
        template = template_response.json()
        template_id = template["id"]
        
        # Retrieve the template to confirm it was created
        get_template_response = client.get(f"/api/v1/templates/{template_id}")
        assert get_template_response.status_code == 200
        retrieved_template = get_template_response.json()
        assert retrieved_template["name"] == "Jazz Template"
        assert retrieved_template["genre"] == "jazz"
        
        # Generate a prompt using the template as inspiration
        generate_request = {
            "genre": "jazz",
            "mood": "smooth",
            "style": "sultry",
            "instruments": "saxophone, piano, double bass, brushes on drums"
        }
        generate_response = client.post("/api/v1/prompts/generate", json=generate_request)
        assert generate_response.status_code == 200
        generated_prompt = generate_response.json()
        
        assert "id" in generated_prompt
        assert "jazz" in generated_prompt["prompt_text"]
        assert "smooth" in generated_prompt["prompt_text"]
        assert "sultry" in generated_prompt["prompt_text"]
    
    def test_multigenre_combination_workflow(self):
        """Test workflow for combining multiple genres as mentioned in docs"""
        # Generate a fusion prompt
        fusion_request = {
            "genre": "jazz",
            "mood": "hip-hop",
            "style": "energetic"
        }
        fusion_response = client.post("/api/v1/prompts/combine", json=fusion_request)
        assert fusion_response.status_code == 200
        fusion_result = fusion_response.json()
        
        assert "combined_prompt" in fusion_result
        assert "jazz-hip-hop" in fusion_result["combined_prompt"]
        assert "energetic" in fusion_result["combined_prompt"]
        assert "fusion" in fusion_result["combined_prompt"]
    
    def test_artist_inspired_workflow(self):
        """Test workflow for artist-inspired prompts as mentioned in docs"""
        # Create a prompt inspired by Adele as mentioned in docs
        adele_inspired = {
            "genre": "soul",
            "mood": "emotional",
            "style": "torch-lounge",
            "voice_tags": "female vocals"
        }
        generate_response = client.post("/api/v1/prompts/generate", json=adele_inspired)
        assert generate_response.status_code == 200
        generated_prompt = generate_response.json()
        
        assert "id" in generated_prompt
        assert "soul" in generated_prompt["prompt_text"]
        assert "emotional" in generated_prompt["prompt_text"]
        assert "torch-lounge" in generated_prompt["prompt_text"]
        assert "female vocals" in generated_prompt["prompt_text"]
    
    def test_time_period_themed_workflow(self):
        """Test workflow for time period themed prompts as mentioned in docs"""
        # Create an 80s inspired prompt as mentioned in docs
        eighties_inspired = {
            "genre": "synthwave",
            "mood": "nostalgic",
            "instruments": "synthesizers",
            "custom_text": "1980s influence, 80s futurism, Analog warmth"
        }
        generate_response = client.post("/api/v1/prompts/generate", json=eighties_inspired)
        assert generate_response.status_code == 200
        generated_prompt = generate_response.json()
        
        assert "id" in generated_prompt
        assert "synthwave" in generated_prompt["prompt_text"]
        assert "nostalgic" in generated_prompt["prompt_text"]
        assert "synthesizers" in generated_prompt["prompt_text"]
        assert "1980s influence" in generated_prompt["prompt_text"]
    
    def test_batch_generation_workflow(self):
        """Test workflow for batch generation of multiple prompts"""
        # Create multiple generation requests
        batch_requests = [
            {
                "genre": "pop",
                "mood": "happy",
                "instruments": "synthesizer, drums"
            },
            {
                "genre": "rock",
                "mood": "aggressive",
                "instruments": "guitar, bass"
            },
            {
                "genre": "jazz",
                "mood": "smooth",
                "instruments": "piano, saxophone"
            }
        ]
        
        batch_response = client.post("/api/v1/prompts/generate/batch", json=batch_requests)
        assert batch_response.status_code == 200
        batch_results = batch_response.json()
        
        assert len(batch_results) == 3
        
        # Verify each prompt was generated correctly
        prompt_texts = [result["prompt_text"] for result in batch_results]
        assert any("pop, happy" in text for text in prompt_texts)
        assert any("rock, aggressive" in text for text in prompt_texts)
        assert any("jazz, smooth" in text for text in prompt_texts)
    
    def test_cultural_influence_workflow(self):
        """Test workflow for cultural influence prompts as mentioned in docs"""
        # Create a prompt with Indian classical influence as mentioned in docs
        cultural_prompt = {
            "genre": "ambient",
            "mood": "reflective",
            "instruments": "sitar",
            "custom_text": "Indian classical influence, Urban meditation, Lo-fi textures"
        }
        generate_response = client.post("/api/v1/prompts/generate", json=cultural_prompt)
        assert generate_response.status_code == 200
        generated_prompt = generate_response.json()
        
        assert "id" in generated_prompt
        assert "ambient" in generated_prompt["prompt_text"]
        assert "reflective" in generated_prompt["prompt_text"]
        assert "sitar" in generated_prompt["prompt_text"]
        assert "Indian classical influence" in generated_prompt["prompt_text"]
    
    def test_emotional_arc_workflow(self):
        """Test workflow for emotional arc prompts as mentioned in docs"""
        # Create a cinematic prompt with emotional journey as mentioned in docs
        emotional_arc = {
            "genre": "cinematic",
            "mood": "triumphant",
            "instruments": "strings",
            "custom_text": "Emotional journey from despair to victory, Dynamic shifts"
        }
        generate_response = client.post("/api/v1/prompts/generate", json=emotional_arc)
        assert generate_response.status_code == 200
        generated_prompt = generate_response.json()
        
        assert "id" in generated_prompt
        assert "cinematic" in generated_prompt["prompt_text"]
        assert "triumphant" in generated_prompt["prompt_text"]
        assert "strings" in generated_prompt["prompt_text"]
        assert "Emotional journey from despair to victory" in generated_prompt["prompt_text"]


class TestAdvancedFeaturesIntegration:
    """Test integration of advanced features"""
    
    def test_prompt_extension_workflow(self):
        """Test extending an existing prompt"""
        # Extend a basic prompt with additional elements
        extend_request = {
            "genre": "classical",
            "mood": "peaceful",
            "instruments": "piano, strings",
            "custom_elements": {"tempo": "60 BPM", "key": "C Major"}
        }
        extend_response = client.post("/api/v1/prompts/extend", json=extend_request)
        assert extend_response.status_code == 200
        extended_result = extend_response.json()
        
        assert "extended_prompt" in extended_result
        assert "classical" in extended_result["extended_prompt"]
        assert "peaceful" in extended_result["extended_prompt"]
        assert "piano, strings" in extended_result["extended_prompt"]
        assert "60 BPM" in extended_result["extended_prompt"]
        assert "C Major" in extended_result["extended_prompt"]
    
    def test_validation_integration(self):
        """Test validation integration in the workflow"""
        # Validate a well-formed prompt
        valid_prompt = {
            "genre": "electronic",
            "mood": "energetic",
            "style": "dynamic",
            "instruments": "synthesizer, drums",
            "voice_tags": "robotic"
        }
        validate_response = client.post("/api/v1/prompts/validate", json=valid_prompt)
        assert validate_response.status_code == 200
        validation_result = validate_response.json()
        
        assert validation_result["is_valid"] is True
        assert len(validation_result["errors"]) == 0
        
        # Validate a problematic prompt
        problematic_prompt = {
            "genre": "a",  # Too short
            "mood": "b"    # Too short
        }
        validate_response2 = client.post("/api/v1/prompts/validate", json=problematic_prompt)
        assert validate_response2.status_code == 200
        validation_result2 = validate_response2.json()
        
        assert validation_result2["is_valid"] is False
        assert len(validation_result2["errors"]) > 0
    
    def test_tag_based_workflow(self):
        """Test workflow using tags for organization"""
        # Create several tags
        tags_to_create = [
            {"name": "upbeat", "tag_type": "mood"},
            {"name": "guitar", "tag_type": "instrument"},
            {"name": "vocal", "tag_type": "style"}
        ]
        
        tag_ids = []
        for tag_data in tags_to_create:
            tag_response = client.post("/api/v1/tags", json=tag_data)
            assert tag_response.status_code == 200
            tag = tag_response.json()
            tag_ids.append(tag["id"])
        
        # Search for tags
        search_response = client.get("/api/v1/tags/search?name=beat")
        assert search_response.status_code == 200
        search_results = search_response.json()
        assert len(search_results) >= 1
        assert any("upbeat" in tag["name"] for tag in search_results)
    
    def test_category_based_organization(self):
        """Test workflow using categories for organization"""
        # Create categories
        categories = [
            {"name": "Electronic", "description": "Electronic music prompts"},
            {"name": "Rock", "description": "Rock music prompts"},
            {"name": "Jazz", "description": "Jazz music prompts"}
        ]
        
        category_ids = []
        for cat_data in categories:
            cat_response = client.post("/api/v1/categories", json=cat_data)
            assert cat_response.status_code == 200
            category = cat_response.json()
            category_ids.append(category["id"])
        
        # Create templates in different categories
        for i, cat_id in enumerate(category_ids):
            template_data = {
                "name": f"Template {i}",
                "genre": ["electronic", "rock", "jazz"][i],
                "mood": ["energetic", "aggressive", "smooth"][i],
                "category_id": cat_id
            }
            template_response = client.post("/api/v1/templates", json=template_data)
            assert template_response.status_code == 200
        
        # Retrieve templates by category
        for i, cat_id in enumerate(category_ids):
            cat_templates_response = client.get(f"/api/v1/templates/?genre={['electronic', 'rock', 'jazz'][i]}")
            assert cat_templates_response.status_code == 200
            cat_templates = cat_templates_response.json()
            assert len(cat_templates) >= 1