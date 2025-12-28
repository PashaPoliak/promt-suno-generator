import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime
from unittest.mock import AsyncMock, patch

from models.database import Base, GeneratedPrompt, PromptTemplate, Category, Tag
from backend.app.models.dtos import PromptCreate, TemplateCreate, CategoryCreate, TagCreate, GenerateRequest
from services.prompt_service import PromptService
from services.template_service import TemplateService
from services.category_service import CategoryService
from services.tag_service import TagService
from utils.prompt_generator import PromptGenerator

# Separate class for non-async tests to avoid pytest-asyncio warnings
class TestPromptGeneratorUnit:
    """Test the prompt generator utility in unit tests"""
    
    def test_generate_prompt_text_with_all_fields(self):
        """Test generating prompt text with all fields"""
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

# Configure pytest-asyncio for the test file
pytestmark = pytest.mark.asyncio


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestPromptService:
    """Test the prompt service layer functionality"""
    
    @pytest.fixture
    def db_session(self):
        """Create a test database session"""
        Base.metadata.create_all(bind=engine)
        session = TestingSessionLocal()
        yield session
        session.close()
        Base.metadata.drop_all(bind=engine)
    
    async def test_get_prompts_empty(self, db_session):
        """Test getting prompts when none exist"""
        prompts = await PromptService.get_prompts(db_session)
        assert prompts == []
    
    async def test_get_prompts_with_pagination(self, db_session):
        """Test getting prompts with pagination"""
        # Create some test prompts
        for i in range(5):
            prompt_data = PromptCreate(
                genre=f"genre_{i}",
                mood=f"mood_{i}"
            )
            await PromptService.create_prompt(db_session, prompt_data)
        
        # Test pagination
        prompts = await PromptService.get_prompts(db_session, skip=0, limit=2)
        assert len(prompts) == 2
        
        prompts = await PromptService.get_prompts(db_session, skip=2, limit=2)
        assert len(prompts) == 2
    
    async def test_create_prompt(self, db_session):
        """Test creating a new prompt"""
        prompt_data = PromptCreate(
            genre="pop",
            mood="energetic",
            style="vibrant",
            instruments="piano, guitar",
            voice_tags="smooth, powerful",
            lyrics_structure="verse-chorus-bridge",
            custom_text="Additional custom elements"
        )
        
        result = await PromptService.create_prompt(db_session, prompt_data)
        
        assert result.id is not None
        assert result.prompt_text == "pop, energetic, vibrant, piano, guitar, smooth, powerful, verse-chorus-bridge, Additional custom elements"
        assert result.parameters is not None
        assert result.created_at is not None
    
    async def test_create_prompt_partial_data(self, db_session):
        """Test creating a prompt with partial data"""
        prompt_data = PromptCreate(
            genre="rock",
            mood="intense"
        )
        
        result = await PromptService.create_prompt(db_session, prompt_data)
        
        assert result.id is not None
        assert result.prompt_text == "rock, intense"
    
    async def test_create_prompt_empty(self, db_session):
        """Test creating a prompt with no data"""
        prompt_data = PromptCreate()
        
        result = await PromptService.create_prompt(db_session, prompt_data)
        
        assert result.id is not None
        assert result.prompt_text == ""
    
    async def test_get_prompt_by_id_found(self, db_session):
        """Test getting a prompt by ID that exists"""
        # Create a prompt first
        prompt_data = PromptCreate(
            genre="jazz",
            mood="smooth"
        )
        created_prompt = await PromptService.create_prompt(db_session, prompt_data)
        
        # Get the prompt by ID
        result = await PromptService.get_prompt(db_session, created_prompt.id)
        
        assert result is not None
        assert result.id == created_prompt.id
        assert result.prompt_text == "jazz, smooth"
    
    async def test_get_prompt_by_id_not_found(self, db_session):
        """Test getting a prompt by ID that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await PromptService.get_prompt(db_session, fake_id)
        
        assert result is None
    
    async def test_generate_prompt(self, db_session):
        """Test generating a prompt with the generate endpoint"""
        generate_request = GenerateRequest(
            genre="electronic",
            mood="energetic",
            style="dynamic",
            instruments="synthesizer, drums",
            voice_tags="robotic, futuristic",
            lyrics_structure="verse-chorus",
            custom_elements={"tempo": "120 BPM", "key": "C Major"}
        )
        
        result = await PromptService.generate_prompt(db_session, generate_request)
        
        assert result.id is not None
        assert result.prompt_text == "electronic, energetic, dynamic, synthesizer, drums, robotic, futuristic, verse-chorus, 120 BPM, C Major"
        assert result.parameters_used is not None
        assert result.validation_result is not None
    
    async def test_generate_prompts_batch(self, db_session):
        """Test generating multiple prompts in batch"""
        requests = [
            GenerateRequest(genre="pop", mood="happy"),
            GenerateRequest(genre="rock", mood="intense")
        ]
        
        results = await PromptService.generate_prompts_batch(db_session, requests)
        
        assert len(results) == 2
        assert all(result.id is not None for result in results)
        prompt_texts = [result.prompt_text for result in results]
        assert "pop, happy" in prompt_texts
        assert "rock, intense" in prompt_texts
    
    async def test_update_prompt_found(self, db_session):
        """Test updating an existing prompt"""
        # Create a prompt first
        prompt_data = PromptCreate(
            genre="classical",
            mood="peaceful"
        )
        created_prompt = await PromptService.create_prompt(db_session, prompt_data)
        
        # Update the prompt
        updated_data = PromptCreate(
            genre="blues",
            mood="melancholic",
            style="soulful"
        )
        result = await PromptService.update_prompt(db_session, created_prompt.id, updated_data)
        
        assert result is not None
        assert result.id == created_prompt.id
        assert result.prompt_text == "blues, melancholic, soulful"
    
    async def test_update_prompt_not_found(self, db_session):
        """Test updating a prompt that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        updated_data = PromptCreate(
            genre="blues",
            mood="melancholic"
        )
        
        result = await PromptService.update_prompt(db_session, fake_id, updated_data)
        
        assert result is None
    
    async def test_delete_prompt_found(self, db_session):
        """Test deleting an existing prompt"""
        # Create a prompt first
        prompt_data = PromptCreate(
            genre="hip-hop",
            mood="energetic"
        )
        created_prompt = await PromptService.create_prompt(db_session, prompt_data)
        
        # Delete the prompt
        result = await PromptService.delete_prompt(db_session, created_prompt.id)
        
        assert result is True
        
        # Verify it's gone
        retrieved = await PromptService.get_prompt(db_session, created_prompt.id)
        assert retrieved is None
    
    async def test_delete_prompt_not_found(self, db_session):
        """Test deleting a prompt that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await PromptService.delete_prompt(db_session, fake_id)
        
        assert result is False


class TestTemplateService:
    """Test the template service layer functionality"""
    
    @pytest.fixture
    def db_session(self):
        """Create a test database session"""
        Base.metadata.create_all(bind=engine)
        session = TestingSessionLocal()
        yield session
        session.close()
        Base.metadata.drop_all(bind=engine)
    
    async def test_get_templates_empty(self, db_session):
        """Test getting templates when none exist"""
        templates = await TemplateService.get_templates(db_session)
        assert templates == []
    
    async def test_get_templates_with_pagination(self, db_session):
        """Test getting templates with pagination"""
        # Create some test templates
        for i in range(5):
            template_data = TemplateCreate(
                name=f"Template {i}",
                genre=f"genre_{i}",
                mood=f"mood_{i}"
            )
            await TemplateService.create_template(db_session, template_data)
        
        # Test pagination
        templates = await TemplateService.get_templates(db_session, skip=0, limit=2)
        assert len(templates) == 2
        
        templates = await TemplateService.get_templates(db_session, skip=2, limit=2)
        assert len(templates) == 2
    
    async def test_get_templates_with_filters(self, db_session):
        """Test getting templates with filters"""
        # Create test templates
        template1 = TemplateCreate(name="Pop Template", genre="pop", mood="happy")
        template2 = TemplateCreate(name="Rock Template", genre="rock", mood="intense")
        await TemplateService.create_template(db_session, template1)
        await TemplateService.create_template(db_session, template2)
        
        # Test genre filter
        templates = await TemplateService.get_templates(db_session, genre="pop")
        assert len(templates) == 1
        assert templates[0].name == "Pop Template"
        
        # Test mood filter
        templates = await TemplateService.get_templates(db_session, mood="intense")
        assert len(templates) == 1
        assert templates[0].name == "Rock Template"
    
    async def test_create_template(self, db_session):
        """Test creating a new template"""
        template_data = TemplateCreate(
            name="Test Template",
            description="A test template",
            genre="pop",
            mood="energetic",
            style="vibrant",
            instruments="piano, guitar",
            voice_tags="smooth, powerful",
            lyrics_structure="verse-chorus-bridge"
        )
        
        result = await TemplateService.create_template(db_session, template_data)
        
        assert result.id is not None
        assert result.name == "Test Template"
        assert result.genre == "pop"
        assert result.mood == "energetic"
        assert result.style == "vibrant"
    
    async def test_get_template_by_id_found(self, db_session):
        """Test getting a template by ID that exists"""
        # Create a template first
        template_data = TemplateCreate(
            name="Test Template",
            genre="jazz",
            mood="smooth"
        )
        created_template = await TemplateService.create_template(db_session, template_data)
        
        # Get the template by ID
        result = await TemplateService.get_template(db_session, created_template.id)
        
        assert result is not None
        assert result.id == created_template.id
        assert result.name == "Test Template"
        assert result.genre == "jazz"
    
    async def test_get_template_by_id_not_found(self, db_session):
        """Test getting a template by ID that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await TemplateService.get_template(db_session, fake_id)
        
        assert result is None
    
    async def test_update_template_found(self, db_session):
        """Test updating an existing template"""
        # Create a template first
        template_data = TemplateCreate(
            name="Test Template",
            genre="classical",
            mood="peaceful"
        )
        created_template = await TemplateService.create_template(db_session, template_data)
        
        # Update the template
        updated_data = TemplateCreate(
            name="Updated Template",
            genre="blues",
            mood="melancholic",
            style="soulful"
        )
        result = await TemplateService.update_template(db_session, created_template.id, updated_data)
        
        assert result is not None
        assert result.id == created_template.id
        assert result.name == "Updated Template"
        assert result.genre == "blues"
        assert result.mood == "melancholic"
        assert result.style == "soulful"
    
    async def test_update_template_not_found(self, db_session):
        """Test updating a template that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        updated_data = TemplateCreate(
            name="Updated Template",
            genre="blues",
            mood="melancholic"
        )
        
        result = await TemplateService.update_template(db_session, fake_id, updated_data)
        
        assert result is None
    
    async def test_delete_template_found(self, db_session):
        """Test deleting an existing template"""
        # Create a template first
        template_data = TemplateCreate(
            name="Test Template",
            genre="hip-hop",
            mood="energetic"
        )
        created_template = await TemplateService.create_template(db_session, template_data)
        
        # Delete the template
        result = await TemplateService.delete_template(db_session, created_template.id)
        
        assert result is True
        
        # Verify it's gone
        retrieved = await TemplateService.get_template(db_session, created_template.id)
        assert retrieved is None
    
    async def test_delete_template_not_found(self, db_session):
        """Test deleting a template that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await TemplateService.delete_template(db_session, fake_id)
        
        assert result is False


class TestCategoryService:
    """Test the category service layer functionality"""
    
    @pytest.fixture
    def db_session(self):
        """Create a test database session"""
        Base.metadata.create_all(bind=engine)
        session = TestingSessionLocal()
        yield session
        session.close()
        Base.metadata.drop_all(bind=engine)
    
    async def test_get_categories_empty(self, db_session):
        """Test getting categories when none exist"""
        categories = await CategoryService.get_categories(db_session)
        assert categories == []
    
    async def test_get_categories_with_pagination(self, db_session):
        """Test getting categories with pagination"""
        # Create some test categories
        for i in range(5):
            category_data = CategoryCreate(
                name=f"Category {i}",
                description=f"Description {i}"
            )
            await CategoryService.create_category(db_session, category_data)
        
        # Test pagination
        categories = await CategoryService.get_categories(db_session, skip=0, limit=2)
        assert len(categories) == 2
        
        categories = await CategoryService.get_categories(db_session, skip=2, limit=2)
        assert len(categories) == 2
    
    async def test_get_categories_with_filter(self, db_session):
        """Test getting categories with name filter"""
        # Create test categories
        category1 = CategoryCreate(name="Music", description="Music category")
        category2 = CategoryCreate(name="Art", description="Art category")
        await CategoryService.create_category(db_session, category1)
        await CategoryService.create_category(db_session, category2)
        
        # Test name filter
        categories = await CategoryService.get_categories(db_session, name="Music")
        assert len(categories) == 1
        assert categories[0].name == "Music"
    
    async def test_create_category(self, db_session):
        """Test creating a new category"""
        category_data = CategoryCreate(
            name="Test Category",
            description="A test category"
        )
        
        result = await CategoryService.create_category(db_session, category_data)
        
        assert result.id is not None
        assert result.name == "Test Category"
        assert result.description == "A test category"
    
    async def test_get_category_by_id_found(self, db_session):
        """Test getting a category by ID that exists"""
        # Create a category first
        category_data = CategoryCreate(
            name="Test Category",
            description="A test category"
        )
        created_category = await CategoryService.create_category(db_session, category_data)
        
        # Get the category by ID
        result = await CategoryService.get_category(db_session, created_category.id)
        
        assert result is not None
        assert result.id == created_category.id
        assert result.name == "Test Category"
    
    async def test_get_category_by_id_not_found(self, db_session):
        """Test getting a category by ID that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await CategoryService.get_category(db_session, fake_id)
        
        assert result is None
    
    async def test_update_category_found(self, db_session):
        """Test updating an existing category"""
        # Create a category first
        category_data = CategoryCreate(
            name="Test Category",
            description="A test category"
        )
        created_category = await CategoryService.create_category(db_session, category_data)
        
        # Update the category
        updated_data = CategoryCreate(
            name="Updated Category",
            description="An updated category"
        )
        result = await CategoryService.update_category(db_session, created_category.id, updated_data)
        
        assert result is not None
        assert result.id == created_category.id
        assert result.name == "Updated Category"
        assert result.description == "An updated category"
    
    async def test_update_category_not_found(self, db_session):
        """Test updating a category that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        updated_data = CategoryCreate(
            name="Updated Category",
            description="An updated category"
        )
        
        result = await CategoryService.update_category(db_session, fake_id, updated_data)
        
        assert result is None
    
    async def test_delete_category_found(self, db_session):
        """Test deleting an existing category"""
        # Create a category first
        category_data = CategoryCreate(
            name="Test Category",
            description="A test category"
        )
        created_category = await CategoryService.create_category(db_session, category_data)
        
        # Delete the category
        result = await CategoryService.delete_category(db_session, created_category.id)
        
        assert result is True
        
        # Verify it's gone
        retrieved = await CategoryService.get_category(db_session, created_category.id)
        assert retrieved is None
    
    async def test_delete_category_not_found(self, db_session):
        """Test deleting a category that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await CategoryService.delete_category(db_session, fake_id)
        
        assert result is False


class TestTagService:
    """Test the tag service layer functionality"""
    
    @pytest.fixture
    def db_session(self):
        """Create a test database session"""
        Base.metadata.create_all(bind=engine)
        session = TestingSessionLocal()
        yield session
        session.close()
        Base.metadata.drop_all(bind=engine)
    
    async def test_get_tags_empty(self, db_session):
        """Test getting tags when none exist"""
        tags = await TagService.get_tags(db_session)
        assert tags == []
    
    async def test_get_tags_with_pagination(self, db_session):
        """Test getting tags with pagination"""
        # Create some test tags
        for i in range(5):
            tag_data = TagCreate(
                name=f"Tag {i}",
                tag_type="genre"
            )
            await TagService.create_tag(db_session, tag_data)
        
        # Test pagination
        tags = await TagService.get_tags(db_session, skip=0, limit=2)
        assert len(tags) == 2
        
        tags = await TagService.get_tags(db_session, skip=2, limit=2)
        assert len(tags) == 2
    
    async def test_get_tags_with_filters(self, db_session):
        """Test getting tags with filters"""
        # Create test tags
        tag1 = TagCreate(name="Rock", tag_type="genre")
        tag2 = TagCreate(name="Happy", tag_type="mood")
        await TagService.create_tag(db_session, tag1)
        await TagService.create_tag(db_session, tag2)
        
        # Test tag_type filter
        tags = await TagService.get_tags(db_session, tag_type="genre")
        assert len(tags) == 1
        assert tags[0].name == "Rock"
        
        # Test name filter
        tags = await TagService.get_tags(db_session, name="Happy")
        assert len(tags) == 1
        assert tags[0].name == "Happy"
    
    async def test_create_tag(self, db_session):
        """Test creating a new tag"""
        tag_data = TagCreate(
            name="Test Tag",
            description="A test tag",
            tag_type="genre"
        )
        
        result = await TagService.create_tag(db_session, tag_data)
        
        assert result.id is not None
        assert result.name == "Test Tag"
        assert result.description == "A test tag"
        assert result.tag_type == "genre"
    
    async def test_get_tag_by_id_found(self, db_session):
        """Test getting a tag by ID that exists"""
        # Create a tag first
        tag_data = TagCreate(
            name="Test Tag",
            tag_type="mood"
        )
        created_tag = await TagService.create_tag(db_session, tag_data)
        
        # Get the tag by ID
        result = await TagService.get_tag(db_session, created_tag.id)
        
        assert result is not None
        assert result.id == created_tag.id
        assert result.name == "Test Tag"
    
    async def test_get_tag_by_id_not_found(self, db_session):
        """Test getting a tag by ID that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await TagService.get_tag(db_session, fake_id)
        
        assert result is None
    
    async def test_update_tag_found(self, db_session):
        """Test updating an existing tag"""
        # Create a tag first
        tag_data = TagCreate(
            name="Test Tag",
            tag_type="style"
        )
        created_tag = await TagService.create_tag(db_session, tag_data)
        
        # Update the tag
        updated_data = TagCreate(
            name="Updated Tag",
            description="An updated tag",
            tag_type="instrument"
        )
        result = await TagService.update_tag(db_session, created_tag.id, updated_data)
        
        assert result is not None
        assert result.id == created_tag.id
        assert result.name == "Updated Tag"
        assert result.tag_type == "instrument"
    
    async def test_update_tag_not_found(self, db_session):
        """Test updating a tag that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        updated_data = TagCreate(
            name="Updated Tag",
            tag_type="instrument"
        )
        
        result = await TagService.update_tag(db_session, fake_id, updated_data)
        
        assert result is None
    
    async def test_delete_tag_found(self, db_session):
        """Test deleting an existing tag"""
        # Create a tag first
        tag_data = TagCreate(
            name="Test Tag",
            tag_type="voice"
        )
        created_tag = await TagService.create_tag(db_session, tag_data)
        
        # Delete the tag
        result = await TagService.delete_tag(db_session, created_tag.id)
        
        assert result is True
        
        # Verify it's gone
        retrieved = await TagService.get_tag(db_session, created_tag.id)
        assert retrieved is None
    
    async def test_delete_tag_not_found(self, db_session):
        """Test deleting a tag that doesn't exist"""
        from uuid import UUID
        fake_id = UUID("12345678-1234-5678-9012-123456789012")
        
        result = await TagService.delete_tag(db_session, fake_id)
        
        assert result is False
    
    async def test_search_tags(self, db_session):
        """Test searching for tags"""
        # Create test tags
        tag1 = TagCreate(name="Rock", tag_type="genre")
        tag2 = TagCreate(name="Jazz", tag_type="genre")
        tag3 = TagCreate(name="Happy", tag_type="mood")
        await TagService.create_tag(db_session, tag1)
        await TagService.create_tag(db_session, tag2)
        await TagService.create_tag(db_session, tag3)
        
        # Search for tags containing "R"
        results = await TagService.search_tags(db_session, "R")
        assert len(results) >= 1
        assert any("Rock" in tag.name for tag in results)
        
        # Search for genre tags containing "J"
        results = await TagService.search_tags(db_session, "J", tag_type="genre")
        assert len(results) >= 1
        assert all(tag.tag_type == "genre" for tag in results)
        assert any("Jazz" in tag.name for tag in results)


# Separate class for non-async tests to avoid pytest-asyncio warnings
class TestPromptGeneratorIntegration:
    """Test the prompt generator utility in integration with services"""
    
    def test_generate_prompt_text_with_all_fields(self):
        """Test generating prompt text with all fields"""
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