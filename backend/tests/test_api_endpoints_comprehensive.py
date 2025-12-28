from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database.session import get_db
from models.database import Base


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
    """Comprehensive tests for prompt endpoints"""
    
    def test_create_prompt_with_all_fields(self):
        """Test creating a prompt with all fields"""
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
    
    def test_create_prompt_with_partial_data(self):
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
    
    def test_create_prompt_empty(self):
        """Test creating a prompt with no data"""
        prompt_data = {}
        
        response = client.post("/api/v1/prompts", json=prompt_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["prompt_text"] == ""
    
    def test_get_prompts_pagination(self):
        """Test getting prompts with pagination"""
        # Create multiple prompts first
        for i in range(5):
            prompt_data = {
                "genre": f"genre_{i}",
                "mood": f"mood_{i}"
            }
            client.post("/api/v1/prompts", json=prompt_data)
        
        # Test pagination
        response = client.get("/api/v1/prompts?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_get_prompt_by_id(self):
        """Test getting a specific prompt by ID"""
        # Create a prompt first
        prompt_data = {
            "genre": "jazz",
            "mood": "smooth"
        }
        create_response = client.post("/api/v1/prompts", json=prompt_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        prompt_id = created_data["id"]
        
        # Get the prompt by ID
        response = client.get(f"/api/v1/prompts/{prompt_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == prompt_id
        assert data["prompt_text"] == "jazz, smooth"
    
    def test_get_prompt_by_id_not_found(self):
        """Test getting a prompt with invalid ID"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.get(f"/api/v1/prompts/{invalid_id}")
        assert response.status_code == 404
    
    def test_update_prompt(self):
        """Test updating an existing prompt"""
        # Create a prompt first
        prompt_data = {
            "genre": "classical",
            "mood": "peaceful"
        }
        create_response = client.post("/api/v1/prompts", json=prompt_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        prompt_id = created_data["id"]
        
        # Update the prompt
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
        """Test updating a prompt that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "genre": "blues",
            "mood": "melancholic"
        }
        response = client.put(f"/api/v1/prompts/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_prompt(self):
        """Test deleting an existing prompt"""
        # Create a prompt first
        prompt_data = {
            "genre": "hip-hop",
            "mood": "energetic"
        }
        create_response = client.post("/api/v1/prompts", json=prompt_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        prompt_id = created_data["id"]
        
        # Delete the prompt
        response = client.delete(f"/api/v1/prompts/{prompt_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Prompt deleted successfully"}
    
    def test_delete_prompt_not_found(self):
        """Test deleting a prompt that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/prompts/{invalid_id}")
        assert response.status_code == 404


class TestTemplateEndpoints:
    """Comprehensive tests for template endpoints"""
    
    def test_create_template_with_all_fields(self):
        """Test creating a template with all fields"""
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
    
    def test_create_template_with_required_fields_only(self):
        """Test creating a template with only required fields"""
        template_data = {
            "name": "Minimal Template"
        }
        
        response = client.post("/api/v1/templates", json=template_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Minimal Template"
        assert data["genre"] is None
    
    def test_get_templates_pagination(self):
        """Test getting templates with pagination"""
        # Create multiple templates first
        for i in range(5):
            template_data = {
                "name": f"Template {i}",
                "genre": f"genre_{i}",
                "mood": f"mood_{i}"
            }
            client.post("/api/v1/templates", json=template_data)
        
        # Test pagination
        response = client.get("/api/v1/templates?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_get_templates_with_filters(self):
        """Test getting templates with filters"""
        # Create test templates
        template1 = {"name": "Pop Template", "genre": "pop", "mood": "happy"}
        template2 = {"name": "Rock Template", "genre": "rock", "mood": "intense"}
        client.post("/api/v1/templates", json=template1)
        client.post("/api/v1/templates", json=template2)
        
        # Test genre filter
        response = client.get("/api/v1/templates?genre=pop")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(template["name"] == "Pop Template" for template in data)
    
    def test_get_template_by_id(self):
        """Test getting a specific template by ID"""
        # Create a template first
        template_data = {
            "name": "Test Template",
            "genre": "jazz",
            "mood": "smooth"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Get the template by ID
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
        # Create a template first
        template_data = {
            "name": "Test Template",
            "genre": "classical",
            "mood": "peaceful"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Update the template
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
        """Test updating a template that doesn't exist"""
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
        # Create a template first
        template_data = {
            "name": "Test Template",
            "genre": "hip-hop",
            "mood": "energetic"
        }
        create_response = client.post("/api/v1/templates", json=template_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        template_id = created_data["id"]
        
        # Delete the template
        response = client.delete(f"/api/v1/templates/{template_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Template deleted successfully"}
    
    def test_delete_template_not_found(self):
        """Test deleting a template that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/templates/{invalid_id}")
        assert response.status_code == 404


class TestCategoryEndpoints:
    """Comprehensive tests for category endpoints"""
    
    def test_create_category(self):
        """Test creating a category"""
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        
        response = client.post("/api/v1/categories", json=category_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Test Category"
    
    def test_get_categories_pagination(self):
        """Test getting categories with pagination"""
        # Create multiple categories first
        for i in range(5):
            category_data = {
                "name": f"Category {i}",
                "description": f"Description {i}"
            }
            client.post("/api/v1/categories", json=category_data)
        
        # Test pagination
        response = client.get("/api/v1/categories?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_get_categories_with_filter(self):
        """Test getting categories with name filter"""
        # Create test categories
        category1 = {"name": "Music", "description": "Music category"}
        category2 = {"name": "Art", "description": "Art category"}
        client.post("/api/v1/categories", json=category1)
        client.post("/api/v1/categories", json=category2)
        
        # Test name filter
        response = client.get("/api/v1/categories?name=Music")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(category["name"] == "Music" for category in data)
    
    def test_get_category_by_id(self):
        """Test getting a specific category by ID"""
        # Create a category first
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        create_response = client.post("/api/v1/categories", json=category_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        category_id = created_data["id"]
        
        # Get the category by ID
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
        # Create a category first
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        create_response = client.post("/api/v1/categories", json=category_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        category_id = created_data["id"]
        
        # Update the category
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
        """Test updating a category that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "name": "Updated Category",
            "description": "An updated category"
        }
        response = client.put(f"/api/v1/categories/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_category(self):
        """Test deleting an existing category"""
        # Create a category first
        category_data = {
            "name": "Test Category",
            "description": "A test category"
        }
        create_response = client.post("/api/v1/categories", json=category_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        category_id = created_data["id"]
        
        # Delete the category
        response = client.delete(f"/api/v1/categories/{category_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Category deleted successfully"}
    
    def test_delete_category_not_found(self):
        """Test deleting a category that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/categories/{invalid_id}")
        assert response.status_code == 404


class TestTagEndpoints:
    """Comprehensive tests for tag endpoints"""
    
    def test_create_tag(self):
        """Test creating a tag"""
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
    
    def test_create_tag_required_fields_only(self):
        """Test creating a tag with only required fields"""
        tag_data = {
            "name": "Minimal Tag"
        }
        
        response = client.post("/api/v1/tags", json=tag_data)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert data["name"] == "Minimal Tag"
        assert data["tag_type"] is None
    
    def test_get_tags_pagination(self):
        """Test getting tags with pagination"""
        # Create multiple tags first
        for i in range(5):
            tag_data = {
                "name": f"Tag {i}",
                "tag_type": "genre"
            }
            client.post("/api/v1/tags", json=tag_data)
        
        # Test pagination
        response = client.get("/api/v1/tags?skip=0&limit=2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_get_tags_with_filters(self):
        """Test getting tags with filters"""
        # Create test tags
        tag1 = {"name": "Rock", "tag_type": "genre"}
        tag2 = {"name": "Happy", "tag_type": "mood"}
        client.post("/api/v1/tags", json=tag1)
        client.post("/api/v1/tags", json=tag2)
        
        # Test tag_type filter
        response = client.get("/api/v1/tags?tag_type=genre")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(tag["name"] == "Rock" for tag in data)
        
        # Test name filter
        response = client.get("/api/v1/tags?name=Happy")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert any(tag["name"] == "Happy" for tag in data)
    
    def test_get_tag_by_id(self):
        """Test getting a specific tag by ID"""
        # Create a tag first
        tag_data = {
            "name": "Test Tag",
            "tag_type": "mood"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        tag_id = created_data["id"]
        
        # Get the tag by ID
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
        # Create a tag first
        tag_data = {
            "name": "Test Tag",
            "tag_type": "style"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        tag_id = created_data["id"]
        
        # Update the tag
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
        """Test updating a tag that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        updated_data = {
            "name": "Updated Tag",
            "tag_type": "instrument"
        }
        response = client.put(f"/api/v1/tags/{invalid_id}", json=updated_data)
        assert response.status_code == 404
    
    def test_delete_tag(self):
        """Test deleting an existing tag"""
        # Create a tag first
        tag_data = {
            "name": "Test Tag",
            "tag_type": "voice"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        created_data = create_response.json()
        tag_id = created_data["id"]
        
        # Delete the tag
        response = client.delete(f"/api/v1/tags/{tag_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Tag deleted successfully"}
    
    def test_delete_tag_not_found(self):
        """Test deleting a tag that doesn't exist"""
        invalid_id = "12345678-1234-5678-9012-123456789012"
        response = client.delete(f"/api/v1/tags/{invalid_id}")
        assert response.status_code == 404
    
    def test_search_tags(self):
        """Test searching for tags"""
        # Create test tags
        tag_data = {
            "name": "Rock",
            "tag_type": "genre",
            "description": "Rock music tag"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        
        # Search for tags
        response = client.get("/api/v1/tags/search?name=Roc")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert any("Rock" in tag["name"] for tag in data)
    
    def test_search_tags_with_type(self):
        """Test searching for tags with type filter"""
        # Create test tags
        tag_data = {
            "name": "Jazz",
            "tag_type": "genre"
        }
        create_response = client.post("/api/v1/tags", json=tag_data)
        assert create_response.status_code == 200
        
        # Search for tags with type filter
        response = client.get("/api/v1/tags/search?name=Jaz&tag_type=genre")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert all(tag["tag_type"] == "genre" for tag in data)


class TestGenerationEndpoints:
    """Comprehensive tests for generation endpoints"""
    
    def test_generate_prompt_with_all_fields(self):
        """Test generating a prompt with all fields"""
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