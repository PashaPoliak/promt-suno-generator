https://studio-api.prod.suno.com/api/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at&include_hooks=true
https://studio-api.prod.suno.com/api/playlist/574c5144-2eb5-44e1-9333-3add06c84006
https://studio-api.prod.suno.com/api/clip/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b
https://studio-api.prod.suno.com/api/clip/3084c7bb-5260-4f94-b799-6faaa53528d0


http://localhost:8000/api/v1/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at

http://localhost:8000/api/v1/playlist/574c5144-2eb5-44e1-9333-3add06c84006
http://localhost:8000/api/v1/clip/d057f1e9-ba96-41e9-a0d9-c21370ed7f9b
http://localhost:8000/api/v1/clip/3084c7bb-5260-4f94-b799-6faaa53528d0

run setup_sample_data.py
run server 8000
check DB
https://studio-api.prod.suno.com/api/profiles/fotballpiraten?playlists_sort_by=upvote_count&clips_sort_by=created_at
check  not empty http://localhost:8000/api/v1/profiles
check  not empty http://localhost:8000/api/v1/profiles/fotballpiraten
check  not empty http://localhost:8000/api/v1/profiles/c0af00fb-7f80-4984-82ac-a22cc08e7b7f

Updated the to-do list
Analyze existing documentation and API structure for Suno prompt generation
Design backend architecture with Python for prompt generation logic
Design frontend architecture with React for user interface
Plan database schema for storing prompt templates and user data
Create API endpoints for prompt generation and management
Develop React components for prompt creation interface
Implement prompt validation and testing mechanisms
Create detailed implementation plan with testing strategy
Design frontend architecture with React for user interface
Plan database schema for storing prompt templates and user data
Create API endpoints for prompt generation and management
Develop React components for prompt creation interface
Implement prompt validation and testing mechanisms
Plan security measures and authentication for the application
Create detailed implementation plan with testing strategy

design a Python-based backend + framework architecture for the Suno prompt generator application. This architecture will focus on generating, managing, and validating Suno music prompts based on the documentation analysis.

Core Components:
Prompt Generation Engine - Core logic for creating various types of Suno prompts
Template Management System - Store and manage prompt templates
API Layer - RESTful endpoints for frontend communication
Data Model Layer - Define data structures for prompts and templates
Validation Engine - Validate prompts against Suno requirements
Utility Functions - Helper functions for prompt manipulation
Tech Stack:
Python
Web framework for API endpoints
Data validation and settings management
H2/PostgreSQL - Database storage
Pytest - Testing framework

Key Features:
Prompt Generation Interface:

Multi-step form for creating prompts + lyric 
Genre selection with visual categories
Style and mood combination tools
Voice tag selection
Real-time prompt preview
Template System:

Browse pre-built prompt templates
Filter by genre, mood, style
Save and favorite custom templates
Advanced Editing:

Text editor with syntax highlighting
Prompt history and comparison
User Experience:
