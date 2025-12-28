import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add the backend directory to the Python path to resolve import issues
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main import app
from database.session import get_db
from models.database import Base
from backend.models.dtos import (
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


class TestPromptEndpoints:
    """Test the prompt-related API endpoints"""
    
    def test_create_prompt(self):
        """Test creating a new prompt"""
        prompt_data = {
            "genre": "pop",
            "mood": "energetic",
            "style": "vibrant",
            "instruments": "piano, guitar",
            "voice_tags": "smooth, powerful",
            "lyrics_structure": "verse-chorus-bridge",
            "custom_text": "Additional custom elements"
        }
        
        response = client.post("/api/v1/prompts", json=prompt_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["prompt_text"] == "pop, energetic, vibrant, piano, guitar, smooth, powerful, verse-chorus-bridge, Additional custom elements"
        assert "created_at" in data
    
    def test_create_prompt_partial_data(self):
        """Test creating a prompt with partial data"""
        prompt_data = {
            "genre": "rock",
            "mood": "intense"
        }
        
        response = client.post("/api/v1/prompts", json=prompt_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["prompt_text"] == "rock, intense"
    
    def test_get_prompts(self):
        """Test getting all prompts"""
        response = client.get("/api/v1/prompts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_prompts_with_pagination(self):
        """Test getting prompts with pagination"""
        response = client.get("/api/v1/prompts?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_prompt_by_id(self):
        """Test getting a specific prompt by ID"""
        # First create a prompt
        prompt_data = {
            "genre": "electronic",
            "mood": "upbeat"
        }
        create_response = client.post("/api/v1/prompts", json=prompt_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        prompt_id = created_data["id"]
        
        # Then get it by ID
        response = client.get(f"/api/v1/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
        assert data["prompt_text"] == "electronic, upbeat"
    
    def test_get_prompt_by_id_not_found(self):
        """Test getting a prompt with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.get(f"/api/v1/prompts/{invalid_id}")
        assert response.status_code == 404
    
    def test_update_prompt(self):
        """Test updating an existing prompt"""
        # First create a prompt
        prompt_data = {
            "genre": "jazz",
            "mood": "smooth"
        }
        create_response = client.post("/api/v1/prompts", json=prompt_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        prompt_id = created_data["id"]
        
        # Then update it
        updated_data = {
            "genre": "blues",
            "mood": "melancholic",
            "style": "soulful"
        }
        response = client.put(f"/api/v1/prompts/{prompt_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
        assert data["prompt_text"] == "blues, melancholic, soulful"
    
    def test_update_prompt_not_found(self):
        """Test updating a prompt with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "genre": "blues",
            "mood": "melancholic"
        }
        response = client.put(f"/api/v1/prompts/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_prompt(self):
        """Test deleting an existing prompt"""
        # First create a prompt
        prompt_data = {
            "genre": "classical",
            "mood": "peaceful"
        }
        create_response = client.post("/api/v1/prompts", json=prompt_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        prompt_id = created_data["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/prompts/{prompt_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Prompt deleted successfully"}
    
    def test_delete_prompt_not_found(self):
        """Test deleting a prompt with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/prompts/{invalid_id}")
        assert response.status_code == 404


class TestTemplateEndpoints:
    """Test the template-related API endpoints"""
    
    def test_create_template(self):
        """Test creating a new template"""
        template_data = {
            "name": "Test Template",
            "description": "A test template",
            "genre": "pop",
            "mood": "energetic",
            "style": "vibrant",
            "instruments": "piano, guitar",
            "voice_tags": "smooth, powerful",
            "lyrics_structure": "verse-chorus-bridge"
        }
        
        response = client.post("/api/v1/templates", json=template_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Template"
        assert data["genre"] == "pop"
    
    def test_get_templates(self):
        """Test getting all templates"""
        response = client.get("/api/v1/templates")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_templates_with_pagination(self):
        """Test getting templates with pagination"""
        response = client.get("/api/v1/templates?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_template_by_id(self):
        """Test getting a specific template by ID"""
        # First create a template
        template_data = {
            "name": "Test Template",
            "genre": "rock",
            "mood": "intense"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Then get it by ID
        response = client.get(f"/api/v1/templates/{template_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == template_id
        assert data["name"] == "Test Template"
    
    def test_get_template_by_id_not_found(self):
        """Test getting a template with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.get(f"/api/v1/templates/{invalid_id}")
        assert response.status_code == 404
    
    def test_update_template(self):
        """Test updating an existing template"""
        # First create a template
        template_data = {
            "name": "Test Template",
            "genre": "jazz",
            "mood": "smooth"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Then update it
        updated_data = {
            "name": "Updated Template",
            "genre": "blues",
            "mood": "melancholic",
            "style": "soulful"
        }
        response = client.put(f"/api/v1/templates/{template_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == template_id
        assert data["name"] == "Updated Template"
        assert data["genre"] == "blues"
    
    def test_update_template_not_found(self):
        """Test updating a template with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "name": "Updated Template",
            "genre": "blues",
            "mood": "melancholic"
        }
        response = client.put(f"/api/v1/templates/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_template(self):
        """Test deleting an existing template"""
        # First create a template
        template_data = {
            "name": "Test Template",
            "genre": "classical",
            "mood": "peaceful"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/templates/{template_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Template deleted successfully"}
    
    def test_delete_template_not_found(self):
        """Test deleting a template with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/templates/{invalid_id}")
        assert response.status_code == 404


class TestCategoryEndpoints:
    """Test the category-related API endpoints"""
    
    def test_create_category(self):
        """Test creating a new category"""
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        
        response = client.post("/api/v1/categories", json=category_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Category"
    
    def test_get_categories(self):
        """Test getting all categories"""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_categories_with_pagination(self):
        """Test getting categories with pagination"""
        response = client.get("/api/v1/categories?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_categories_with_filter(self):
        """Test getting categories with name filter"""
        response = client.get("/api/v1/categories?name=Test")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_category_by_id(self):
        """Test getting a specific category by ID"""
        # First create a category
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        create_response = client.post("/api/v1/categories", json=category_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        category_id = created_data["id"]
        
        # Then get it by ID
        response = client.get(f"/api/v1/categories/{category_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == "Test Category"
    
    def test_get_category_by_id_not_found(self):
        """Test getting a category with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.get(f"/api/v1/categories/{invalid_id}")
        assert response.status_code == 404
    
    def test_update_category(self):
        """Test updating an existing category"""
        # First create a category
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        create_response = client.post("/api/v1/categories", json=category_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        category_id = created_data["id"]
        
        # Then update it
        updated_data = {
            "name": "Updated Category",
            "description": "An updated category"
        }
        response = client.put(f"/api/v1/categories/{category_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == category_id
        assert data["name"] == "Updated Category"
    
    def test_update_category_not_found(self):
        """Test updating a category with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "name": "Updated Category",
            "description": "An updated category"
        }
        response = client.put(f"/api/v1/categories/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_category(self):
        """Test deleting an existing category"""
        # First create a category
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        create_response = client.post("/api/v1/categories", json=category_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        category_id = created_data["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/categories/{category_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Category deleted successfully"}
    
    def test_delete_category_not_found(self):
        """Test deleting a category with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/categories/{invalid_id}")
        assert response.status_code == 404


class TestTagEndpoints:
    """Test the tag-related API endpoints"""
    
    def test_create_tag(self):
        """Test creating a new tag"""
        tag_data = {
            "name": "Test Tag",
            "description": "A test tag",
            "tag_type": "genre"
        }
        
        response = client.post("/api/v1/tags", json=tag_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Tag"
        assert data["tag_type"] == "genre"
    
    def test_get_tags(self):
        """Test getting all tags"""
        response = client.get("/api/v1/tags")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_tags_with_pagination(self):
        """Test getting tags with pagination"""
        response = client.get("/api/v1/tags?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_tags_with_filters(self):
        """Test getting tags with filters"""
        response = client.get("/api/v1/tags?tag_type=genre&name=Test")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_tag_by_id(self):
        """Test getting a specific tag by ID"""
        # First create a tag
        tag_data = {
            "name": "Test Tag",
            "tag_type": "mood"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        tag_id = created_data["id"]
        
        # Then get it by ID
        response = client.get(f"/api/v1/tags/{tag_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tag_id
        assert data["name"] == "Test Tag"
    
    def test_get_tag_by_id_not_found(self):
        """Test getting a tag with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.get(f"/api/v1/tags/{invalid_id}")
        assert response.status_code == 404
    
    def test_update_tag(self):
        """Test updating an existing tag"""
        # First create a tag
        tag_data = {
            "name": "Test Tag",
            "tag_type": "style"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        tag_id = created_data["id"]
        
        # Then update it
        updated_data = {
            "name": "Updated Tag",
            "description": "An updated tag",
            "tag_type": "instrument"
        }
        response = client.put(f"/api/v1/tags/{tag_id}", json=updated_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == tag_id
        assert data["name"] == "Updated Tag"
        assert data["tag_type"] == "instrument"
    
    def test_update_tag_not_found(self):
        """Test updating a tag with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "name": "Updated Tag",
            "tag_type": "instrument"
        }
        response = client.put(f"/api/v1/tags/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_tag(self):
        """Test deleting an existing tag"""
        # First create a tag
        tag_data = {
            "name": "Test Tag",
            "tag_type": "voice"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        tag_id = created_data["id"]
        
        # Then delete it
        response = client.delete(f"/api/v1/tags/{tag_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Tag deleted successfully"}
    
    def test_delete_tag_not_found(self):
        """Test deleting a tag with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/tags/{invalid_id}")
        assert response.status_code == 404
    
    def test_search_tags(self):
        """Test searching for tags"""
        # First create a tag
        tag_data = {
            "name": "Rock",
            "tag_type": "genre"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        
        # Then search for it
        response = client.get("/api/v1/tags/search?name=Rock")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any(tag["name"] == "Rock" for tag in data)
    
    def test_search_tags_with_type(self):
        """Test searching for tags with type filter"""
        # First create a tag
        tag_data = {
            "name": "Jazz",
            "tag_type": "genre"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        
        # Then search for it with type filter
        response = client.get("/api/v1/tags/search?name=Jazz&tag_type=genre")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all(tag["tag_type"] == "genre" for tag in data)


class TestGenerationEndpoints:
    """Test the prompt generation API endpoints"""
    
    def test_generate_prompt(self):
        """Test generating a new prompt"""
        generate_data = {
            "genre": "electronic",
            "mood": "energetic",
            "style": "dynamic",
            "instruments": "synthesizer, drums",
            "voice_tags": "robotic, futuristic",
            "lyrics_structure": "verse-chorus",
            "custom_elements": {"tempo": "120 BPM", "key": "C Major"}
        }
        
        response = client.post("/api/v1/generate", json=generate_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "prompt_text" in data
        assert "generated_at" in data
        assert "parameters_used" in data
        assert "validation_result" in data
        assert data["prompt_text"] == "electronic, energetic, dynamic, synthesizer, drums, robotic, futuristic, verse-chorus, 120 BPM, C Major"
    
    def test_generate_prompt_partial_data(self):
        """Test generating a prompt with partial data"""
        generate_data = {
            "genre": "rock",
            "mood": "intense"
        }
        
        response = client.post("/api/v1/generate", json=generate_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["prompt_text"] == "rock, intense"
    
    def test_generate_prompts_batch(self):
        """Test generating multiple prompts in batch"""
        batch_data = [
            {
                "genre": "pop",
                "mood": "happy"
            },
            {
                "genre": "jazz",
                "mood": "smooth"
            }
        ]
        
        response = client.post("/api/v1/generate/batch", json=batch_data)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert all("id" in item and "prompt_text" in item for item in data)
        # Check that both prompts were generated correctly
        prompt_texts = [item["prompt_text"] for item in data]
        assert "pop, happy" in prompt_texts
        assert "jazz, smooth" in prompt_texts
    
    def test_validate_prompt(self):
        """Test validating a prompt without generating it"""
        validate_data = {
            "genre": "pop",
            "mood": "energetic",
            "style": "vibrant",
            "instruments": "piano, guitar",
            "voice_tags": "smooth, powerful"
        }
        
        response = client.post("/api/v1/validate", json=validate_data)
        assert response.status_code == 200
        data = response.json()
        assert "is_valid" in data
        assert "errors" in data
        assert "warnings" in data
        assert data["is_valid"] is True
        assert isinstance(data["errors"], list)
        assert isinstance(data["warnings"], list)
    
    def test_combine_prompts(self):
        """Test combining multiple prompt elements"""
        combine_data = {
            "genre": "jazz",
            "mood": "hip-hop",
            "style": "energetic"
        }
        
        response = client.post("/api/v1/combine", json=combine_data)
        assert response.status_code == 200
        data = response.json()
        assert "combined_prompt" in data
        # The combined prompt should follow the fusion format
        assert "jazz-hip-hop" in data["combined_prompt"]
        assert "energetic" in data["combined_prompt"]
        assert "fusion" in data["combined_prompt"]
    
    def test_extend_prompt(self):
        """Test extending an existing prompt"""
        extend_data = {
            "genre": "classical",
            "mood": "peaceful",
            "instruments": "piano, strings",
            "custom_elements": {"tempo": "60 BPM"}
        }
        
        response = client.post("/api/v1/extend", json=extend_data)
        assert response.status_code == 200
        data = response.json()
        assert "extended_prompt" in data
        assert "classical" in data["extended_prompt"]
        assert "peaceful" in data["extended_prompt"]
        assert "piano, strings" in data["extended_prompt"]
        assert "60 BPM" in data["extended_prompt"]


class TestTemplateInPrompts:
    """Test using templates in prompt generation"""
    
    def test_get_templates_from_prompts_endpoint(self):
        """Test getting templates through the prompts endpoint"""
        response = client.get("/api/v1/prompts/templates/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_templates_with_filters_from_prompts_endpoint(self):
        """Test getting templates with filters through the prompts endpoint"""
        response = client.get("/api/v1/prompts/templates/?genre=pop&mood=energetic")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_template_by_id_from_prompts_endpoint(self):
        """Test getting a specific template by ID through the prompts endpoint"""
        # First create a template
        template_data = {
            "name": "Test Template",
            "genre": "rock",
            "mood": "intense"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Then get it through the prompts endpoint
        response = client.get(f"/api/v1/prompts/templates/{template_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == template_id
        assert data["name"] == "Test Template"