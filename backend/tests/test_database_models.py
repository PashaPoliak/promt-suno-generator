import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime
from uuid import UUID
from typing import cast

from models.database import Base, User, Category, Tag, PromptTemplate, PromptTemplateTag, GeneratedPrompt, FavoritePrompt


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Enable foreign key constraints for SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class TestUserModel:
    """Test the User database model"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_user_creation(self):
        """Test creating a user"""
        user = User(
            username="testuser"
        )
        
        self.session.add(user)
        self.session.commit()
        
        # Query the user from the database to ensure proper loading
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        assert retrieved_user is not None
        assert retrieved_user.id is not None
        user_username = retrieved_user.username  # Can be None
        user_username_value = cast(str, user_username) if user_username is not None else None
        assert user_username_value == "testuser"
        # username is optional, so check if it matches expected value when present
        if user_username is not None:
            user_username_value = cast(str, user_username)
            assert user_username_value == "testuser"
        assert retrieved_user.created_at is not None
        assert retrieved_user.updated_at is not None
    
    def test_user_creation_required_fields_only(self):
        """Test creating a user with only required fields"""
        user = User(
        )
        
        self.session.add(user)
        self.session.commit()
        
        # Query the user from the database to ensure proper loading
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        assert retrieved_user is not None
        assert retrieved_user.id is not None
        user_username = retrieved_user.username
        assert user_username is None
        assert retrieved_user.created_at is not None
    
    def test_user_unique_constraints(self):
        """Test that username is unique"""
        user1 = User(
            username="unique_user",
        )
        
        self.session.add(user1)
        self.session.commit()
        
        # Try to create another user with the same username
        user2 = User(
            username="unique_user",  # Same username as user1
        )
        
        self.session.add(user2)
        with pytest.raises(Exception):
            self.session.commit()


class TestCategoryModel:
    """Test the Category database model"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_category_creation(self):
        """Test creating a category"""
        category = Category(
            name="Test Category",
            description="A test category description"
        )
        
        self.session.add(category)
        self.session.commit()
        
        # Query the category from the database to ensure proper loading
        retrieved_category = self.session.query(Category).filter_by(id=category.id).first()
        assert retrieved_category is not None
        assert retrieved_category.id is not None
        # Type assertion to help Pylance understand the dynamic attributes
        # Use cast to help Pylance understand the types
        category_name = cast(str, retrieved_category.name)
        category_description = cast(str, retrieved_category.description)
        assert category_name == "Test Category"
        assert category_description == "A test category description"
        assert retrieved_category.created_at is not None
    
    def test_category_creation_required_fields_only(self):
        """Test creating a category with only required fields"""
        category = Category(
            name="Minimal Category"
        )
        
        self.session.add(category)
        self.session.commit()
        
        # Query the category from the database to ensure proper loading
        retrieved_category = self.session.query(Category).filter_by(id=category.id).first()
        assert retrieved_category is not None
        assert retrieved_category.id is not None
        category_name = cast(str, retrieved_category.name)
        category_description = retrieved_category.description  # This can be None
        assert category_name == "Minimal Category"
        assert category_description is None
        assert retrieved_category.created_at is not None


class TestTagModel:
    """Test the Tag database model"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_tag_creation(self):
        """Test creating a tag"""
        tag = Tag(
            name="Test Tag",
            description="A test tag description",
            tag_type="genre"
        )
        
        self.session.add(tag)
        self.session.commit()
        
        # Query the tag from the database to ensure proper loading
        retrieved_tag = self.session.query(Tag).filter_by(id=tag.id).first()
        assert retrieved_tag is not None
        assert retrieved_tag.id is not None
        tag_name = cast(str, retrieved_tag.name)
        tag_description = cast(str, retrieved_tag.description)
        tag_type = cast(str, retrieved_tag.tag_type)
        assert tag_name == "Test Tag"
        assert tag_description == "A test tag description"
        assert tag_type == "genre"
    
    def test_tag_creation_required_fields_only(self):
        """Test creating a tag with only required fields"""
        tag = Tag(
            name="Minimal Tag"
        )
        
        self.session.add(tag)
        self.session.commit()
        
        # Query the tag from the database to ensure proper loading
        retrieved_tag = self.session.query(Tag).filter_by(id=tag.id).first()
        assert retrieved_tag is not None
        assert retrieved_tag.id is not None
        tag_name = cast(str, retrieved_tag.name)
        tag_description = retrieved_tag.description
        tag_type = retrieved_tag.tag_type
        assert tag_name == "Minimal Tag"
        assert tag_description is None
        assert tag_type is None
    
    def test_tag_unique_name_constraint(self):
        """Test that tag names are unique"""
        tag1 = Tag(name="Unique Tag", tag_type="genre")
        
        self.session.add(tag1)
        self.session.commit()
        
        # Try to create another tag with the same name
        tag2 = Tag(name="Unique Tag", tag_type="mood")
        
        self.session.add(tag2)
        with pytest.raises(Exception):
            self.session.commit()


class TestPromptTemplateModel:
    """Test the PromptTemplate database model"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_prompt_template_creation(self):
        """Test creating a prompt template"""
        template = PromptTemplate(
            name="Test Template",
            description="A test template description",
            genre="pop",
            mood="energetic",
            style="vibrant",
            instruments="piano, guitar",
            voice_tags="smooth, powerful",
            lyrics_structure="verse-chorus-bridge",
            is_active=True
        )
        
        self.session.add(template)
        self.session.commit()
        
        # Query the template from the database to ensure proper loading
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        assert retrieved_template is not None
        assert retrieved_template.id is not None
        template_name = cast(str, retrieved_template.name)
        template_description = cast(str, retrieved_template.description)
        template_genre = cast(str, retrieved_template.genre)
        template_mood = cast(str, retrieved_template.mood)
        template_style = cast(str, retrieved_template.style)
        template_instruments = cast(str, retrieved_template.instruments)
        template_voice_tags = cast(str, retrieved_template.voice_tags)
        template_lyrics_structure = cast(str, retrieved_template.lyrics_structure)
        template_is_active = cast(bool, retrieved_template.is_active)
        assert template_name == "Test Template"
        assert template_description == "A test template description"
        assert template_genre == "pop"
        assert template_mood == "energetic"
        assert template_style == "vibrant"
        assert template_instruments == "piano, guitar"
        assert template_voice_tags == "smooth, powerful"
        assert template_lyrics_structure == "verse-chorus-bridge"
        assert template_is_active is True
        assert retrieved_template.created_at is not None
        assert retrieved_template.updated_at is not None
    
    def test_prompt_template_creation_required_fields_only(self):
        """Test creating a prompt template with only required fields"""
        template = PromptTemplate(
            name="Minimal Template"
        )
        
        self.session.add(template)
        self.session.commit()
        
        # Query the template from the database to ensure proper loading
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        assert retrieved_template is not None
        assert retrieved_template.id is not None
        template_name = cast(str, retrieved_template.name)
        template_description = retrieved_template.description
        template_genre = retrieved_template.genre
        template_mood = retrieved_template.mood
        template_style = retrieved_template.style
        template_instruments = retrieved_template.instruments
        template_voice_tags = retrieved_template.voice_tags
        template_lyrics_structure = retrieved_template.lyrics_structure
        template_is_active = cast(bool, retrieved_template.is_active)
        assert template_name == "Minimal Template"
        assert template_description is None
        assert template_genre is None
        assert template_mood is None
        assert template_style is None
        assert template_instruments is None
        assert template_voice_tags is None
        assert template_lyrics_structure is None
        assert template_is_active is True  # Default value
        assert retrieved_template.created_at is not None
        assert retrieved_template.updated_at is not None
    
    def test_prompt_template_default_values(self):
        """Test default values for prompt template"""
        template = PromptTemplate(
            name="Default Template"
        )
        
        self.session.add(template)
        self.session.commit()
        
        # Query the template from the database to ensure proper loading
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        assert retrieved_template is not None
        assert retrieved_template.is_active is True # Default value
        assert retrieved_template.created_at is not None
        assert retrieved_template.updated_at is not None


class TestPromptTemplateTagModel:
    """Test the PromptTemplateTag database model (junction table)"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_prompt_template_tag_creation(self):
        """Test creating a prompt template tag relationship"""
        # Create a template and a tag first
        template = PromptTemplate(name="Test Template", genre="pop")
        tag = Tag(name="Test Tag", tag_type="genre")
        
        self.session.add(template)
        self.session.add(tag)
        self.session.commit()
        
        # Create the relationship
        template_tag = PromptTemplateTag(
            template_id=template.id,
            tag_id=tag.id
        )
        
        self.session.add(template_tag)
        self.session.commit()
        
        # Query the relationship from the database to ensure proper loading
        retrieved_template_tag = self.session.query(PromptTemplateTag).filter_by(id=template_tag.id).first()
        assert retrieved_template_tag is not None
        assert retrieved_template_tag.id is not None
        template_tag_template_id = cast(UUID, retrieved_template_tag.template_id)
        template_tag_tag_id = cast(UUID, retrieved_template_tag.tag_id)
        template_id = cast(UUID, template.id)
        tag_id = cast(UUID, tag.id)
        assert template_tag_template_id == template_id
        assert template_tag_tag_id == tag_id
        assert retrieved_template_tag.created_at is not None
    
    def test_cascade_delete_template(self):
        """Test that deleting a template also deletes the relationships"""
        # Create a template and a tag
        template = PromptTemplate(name="Test Template", genre="pop")
        tag = Tag(name="Test Tag", tag_type="genre")
        
        self.session.add(template)
        self.session.add(tag)
        self.session.commit()
        
        # Create the relationship
        template_tag = PromptTemplateTag(
            template_id=template.id,
            tag_id=tag.id
        )
        
        self.session.add(template_tag)
        self.session.commit()
        
        # Verify the relationship exists
        assert self.session.query(PromptTemplateTag).count() == 1
        
        # Delete the template
        self.session.delete(template)
        self.session.commit()
        
        # The relationship should be deleted due to CASCADE
        remaining_relationships = self.session.query(PromptTemplateTag).count()
        assert remaining_relationships == 0


class TestGeneratedPromptModel:
    """Test the GeneratedPrompt database model"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_generated_prompt_creation(self):
        """Test creating a generated prompt"""
        prompt = GeneratedPrompt(
            prompt_text="Test prompt text, with multiple elements",
            parameters={"genre": "pop", "mood": "happy"},
            is_favorite=False,
            generation_result={"status": "success"}
        )
        
        self.session.add(prompt)
        self.session.commit()
        
        # Query the prompt from the database to ensure proper loading
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        assert retrieved_prompt is not None
        assert retrieved_prompt.id is not None
        prompt_text = cast(str, retrieved_prompt.prompt_text)
        prompt_parameters = retrieved_prompt.parameters
        prompt_is_favorite = cast(bool, retrieved_prompt.is_favorite)
        prompt_generation_result = retrieved_prompt.generation_result
        assert prompt_text == "Test prompt text, with multiple elements"
        # Compare JSON data carefully to avoid ColumnElement issues
        assert prompt_parameters is not None
        assert prompt_parameters.get("genre") == "pop"
        assert prompt_parameters.get("mood") == "happy"
        assert prompt_is_favorite is False
        assert prompt_generation_result is not None
        assert prompt_generation_result.get("status") == "success"
        assert retrieved_prompt.created_at is not None
    
    def test_generated_prompt_creation_required_fields_only(self):
        """Test creating a generated prompt with only required fields"""
        prompt = GeneratedPrompt(
            prompt_text="Minimal prompt text"
        )
        
        self.session.add(prompt)
        self.session.commit()
        
        # Query the prompt from the database to ensure proper loading
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        assert retrieved_prompt is not None
        assert retrieved_prompt.id is not None
        prompt_text = cast(str, retrieved_prompt.prompt_text)
        prompt_parameters = retrieved_prompt.parameters
        prompt_is_favorite = cast(bool, retrieved_prompt.is_favorite)
        prompt_generation_result = retrieved_prompt.generation_result
        assert prompt_text == "Minimal prompt text"
        assert prompt_parameters is None
        assert prompt_is_favorite is False  # Default value
        assert prompt_generation_result is None
        assert retrieved_prompt.created_at is not None
    
    def test_generated_prompt_default_values(self):
        """Test default values for generated prompt"""
        prompt = GeneratedPrompt(
            prompt_text="Default values test"
        )
        
        self.session.add(prompt)
        self.session.commit()
        
        # Query the prompt from the database to ensure proper loading
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        assert retrieved_prompt is not None
        assert retrieved_prompt.is_favorite is False  # Default value


class TestFavoritePromptModel:
    """Test the FavoritePrompt database model"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_favorite_prompt_creation(self):
        """Test creating a favorite prompt relationship"""
        # Create a user and a generated prompt first
        user = User(username="testuser")
        prompt = GeneratedPrompt(prompt_text="Test prompt")
        
        self.session.add(user)
        self.session.add(prompt)
        self.session.commit()
        
        # Create the favorite relationship
        favorite = FavoritePrompt(
            user_id=user.id,
            prompt_id=prompt.id
        )
        
        self.session.add(favorite)
        self.session.commit()
        
        # Query the favorite from the database to ensure proper loading
        retrieved_favorite = self.session.query(FavoritePrompt).filter_by(id=favorite.id).first()
        assert retrieved_favorite is not None
        assert retrieved_favorite.id is not None
        favorite_user_id = cast(UUID, retrieved_favorite.user_id)
        favorite_prompt_id = cast(UUID, retrieved_favorite.prompt_id)
        user_id = cast(UUID, user.id)
        prompt_id = cast(UUID, prompt.id)
        assert favorite_user_id == user_id
        assert favorite_prompt_id == prompt_id
        assert retrieved_favorite.created_at is not None
    
    def test_unique_constraint(self):
        """Test that a user can't favorite the same prompt twice"""
        # Create a user and a generated prompt
        user = User(username="testuser")
        prompt = GeneratedPrompt(prompt_text="Test prompt")
        
        self.session.add(user)
        self.session.add(prompt)
        self.session.commit()
        
        # Create the first favorite relationship
        favorite1 = FavoritePrompt(
            user_id=user.id,
            prompt_id=prompt.id
        )
        
        self.session.add(favorite1)
        self.session.commit()
        
        # Try to create a duplicate favorite relationship
        favorite2 = FavoritePrompt(
            user_id=user.id,
            prompt_id=prompt.id
        )
        
        self.session.add(favorite2)
        with pytest.raises(Exception):
            self.session.commit()


class TestModelRelationships:
    """Test the relationships between models"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_category_prompt_template_relationship(self):
        """Test the relationship between Category and PromptTemplate"""
        # Create a category
        category = Category(name="Test Category", description="A test category")
        self.session.add(category)
        self.session.commit()
        
        # Create a template associated with the category
        template = PromptTemplate(
            name="Template with Category",
            genre="pop",
            category_id=category.id
        )
        self.session.add(template)
        self.session.commit()
        
        # Verify the relationship
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        assert retrieved_template is not None
        template_category_id = cast(UUID, retrieved_template.category_id)
        category_id = cast(UUID, category.id)
        assert template_category_id == category_id
        
        retrieved_category = self.session.query(Category).filter_by(id=category.id).first()
        assert retrieved_category is not None # Make sure retrieved_category is not None before using its id
        templates_in_category = self.session.query(PromptTemplate).filter_by(category_id=retrieved_category.id).all()
        assert len(templates_in_category) == 1
        template_id = cast(UUID, templates_in_category[0].id)
        expected_template_id = cast(UUID, template.id)
        assert template_id == expected_template_id
    
    def test_user_generated_prompt_relationship(self):
        """Test the relationship between User and GeneratedPrompt"""
        # Create a user
        user = User(username="testuser")
        self.session.add(user)
        self.session.commit()
        
        # Create a generated prompt associated with the user
        prompt = GeneratedPrompt(
            prompt_text="User's prompt",
            user_id=user.id
        )
        self.session.add(prompt)
        self.session.commit()
        
        # Verify the relationship
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        assert retrieved_prompt is not None
        prompt_user_id = cast(UUID, retrieved_prompt.user_id)
        user_id = cast(UUID, user.id)
        assert prompt_user_id == user_id
        
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        assert retrieved_user is not None # Make sure retrieved_user is not None before using its id
        user_prompts = self.session.query(GeneratedPrompt).filter_by(user_id=retrieved_user.id).all()
        assert len(user_prompts) == 1
        user_prompt_id = cast(UUID, user_prompts[0].id)
        prompt_id = cast(UUID, prompt.id)
        assert user_prompt_id == prompt_id
    
    def test_user_favorite_prompt_relationship(self):
        """Test the relationship between User and FavoritePrompt"""
        # Create a user and a generated prompt
        user = User(username="testuser")
        prompt = GeneratedPrompt(prompt_text="Test prompt")
        self.session.add(user)
        self.session.add(prompt)
        self.session.commit()
        
        # Create a favorite relationship
        favorite = FavoritePrompt(
            user_id=user.id,
            prompt_id=prompt.id
        )
        self.session.add(favorite)
        self.session.commit()
        
        # Verify the relationships
        retrieved_favorite = self.session.query(FavoritePrompt).filter_by(id=favorite.id).first()
        assert retrieved_favorite is not None
        favorite_user_id = cast(UUID, retrieved_favorite.user_id)
        favorite_prompt_id = cast(UUID, retrieved_favorite.prompt_id)
        user_id = cast(UUID, user.id)
        prompt_id = cast(UUID, prompt.id)
        assert favorite_user_id == user_id
        assert favorite_prompt_id == prompt_id
        
        # Check that the prompt is accessible through the relationship
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        assert retrieved_prompt is not None


class TestDatabaseIntegrity:
    """Test database integrity constraints"""
    
    def setup_method(self):
        """Set up the test database"""
        Base.metadata.create_all(bind=engine)
        self.session = TestingSessionLocal()
    
    def teardown_method(self):
        """Clean up the test database"""
        self.session.close()
        Base.metadata.drop_all(bind=engine)
    
    def test_uuid_primary_keys(self):
        """Test that all primary keys are UUIDs"""
        # Create various entities
        user = User(username="testuser")
        category = Category(name="Test Category")
        tag = Tag(name="Test Tag")
        template = PromptTemplate(name="Test Template", genre="pop")
        prompt = GeneratedPrompt(prompt_text="Test prompt")
        
        self.session.add_all([user, category, tag, template, prompt])
        self.session.commit()
        
        # Query the entities to ensure proper loading
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        retrieved_category = self.session.query(Category).filter_by(id=category.id).first()
        retrieved_tag = self.session.query(Tag).filter_by(id=tag.id).first()
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        
        # Check that all IDs are valid UUIDs
        assert retrieved_user is not None  # Ensure object is not None before accessing id
        assert isinstance(retrieved_user.id, UUID)
        assert retrieved_category is not None  # Ensure object is not None before accessing id
        assert isinstance(retrieved_category.id, UUID)
        assert retrieved_tag is not None # Ensure object is not None before accessing id
        assert isinstance(retrieved_tag.id, UUID)
        assert retrieved_template is not None  # Ensure object is not None before accessing id
        assert isinstance(retrieved_template.id, UUID)
        assert retrieved_prompt is not None # Ensure object is not None before accessing id
        assert isinstance(retrieved_prompt.id, UUID)
    
    def test_timestamps_auto_set(self):
        """Test that timestamps are automatically set"""
        # Create entities
        user = User(username="testuser")
        category = Category(name="Test Category")
        tag = Tag(name="Test Tag")
        template = PromptTemplate(name="Test Template", genre="pop")
        prompt = GeneratedPrompt(prompt_text="Test prompt")
        
        self.session.add_all([user, category, tag, template, prompt])
        self.session.commit()
        
        # Query the entities to ensure proper loading
        retrieved_user = self.session.query(User).filter_by(id=user.id).first()
        retrieved_category = self.session.query(Category).filter_by(id=category.id).first()
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        
        # Check that timestamps are set
        assert retrieved_user is not None # Ensure object is not None before accessing timestamps
        assert retrieved_user.created_at is not None
        assert retrieved_user.updated_at is not None
        
        assert retrieved_category is not None  # Ensure object is not None before accessing timestamps
        assert retrieved_category.created_at is not None
        
        assert retrieved_template is not None  # Ensure object is not None before accessing timestamps
        assert retrieved_template.created_at is not None
        assert retrieved_template.updated_at is not None
        
        assert retrieved_prompt is not None  # Ensure object is not None before accessing timestamps
        assert retrieved_prompt.created_at is not None # GeneratedPrompt has created_at field
    
    def test_text_fields_can_be_none(self):
        """Test that text fields can be None"""
        template = PromptTemplate(
            name="Template with None fields",
            genre=None,
            mood=None,
            style=None,
            instruments=None,
            voice_tags=None,
            lyrics_structure=None
        )
        
        self.session.add(template)
        self.session.commit()
        
        # Query the template from the database to ensure proper loading
        retrieved_template = self.session.query(PromptTemplate).filter_by(id=template.id).first()
        assert retrieved_template is not None
        assert retrieved_template.genre is None
        assert retrieved_template.mood is None
        assert retrieved_template.style is None
        assert retrieved_template.instruments is None
        assert retrieved_template.voice_tags is None
        assert retrieved_template.lyrics_structure is None
    
    def test_json_fields_can_be_none(self):
        """Test that JSON fields can be None"""
        prompt = GeneratedPrompt(
            prompt_text="Test prompt",
            parameters=None,
            generation_result=None
        )
        
        self.session.add(prompt)
        self.session.commit()
        
        # Query the prompt from the database to ensure proper loading
        retrieved_prompt = self.session.query(GeneratedPrompt).filter_by(id=prompt.id).first()
        assert retrieved_prompt is not None
        assert retrieved_prompt.parameters is None
        assert retrieved_prompt.generation_result is None