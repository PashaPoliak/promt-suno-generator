export interface PromptCreate {
  genre?: string;
  mood?: string;
  style?: string;
  instruments?: string;
  voice_tags?: string;
  lyrics_structure?: string;
  custom_text?: string;
}

export interface PromptResponse {
  id: string;
  prompt_text: string;
  parameters?: Record<string, any>;
  created_at: string;
  generation_result?: Record<string, any>;
}

export interface TemplateResponse {
  id: string;
  name: string;
  description?: string;
  genre?: string;
  mood?: string;
  style?: string;
  instruments?: string;
  voice_tags?: string;
  lyrics_structure?: string;
  created_at: string;
  is_active: boolean;
  tags: string[];
}

export interface GenerateRequest {
  genre?: string;
  mood?: string;
  style?: string;
  instruments?: string;
  voice_tags?: string;
  lyrics_structure?: string;
  custom_elements?: Record<string, any>;
}

export interface GenerateResponse {
  id: string;
  prompt_text: string;
  generated_at: string;
  parameters_used: Record<string, any>;
  validation_result: {
    is_valid: boolean;
    errors: string[];
    warnings: string[];
    suggestions: string[];
  };
}


export interface TemplateCreate {
  name: string;
  description?: string;
  genre?: string;
  mood?: string;
  style?: string;
  instruments?: string;
  voice_tags?: string;
  lyrics_structure?: string;
  is_active?: boolean;
}


export interface TemplateResponse {
  id: string;
  name: string;
  description?: string;
  genre?: string;
  mood?: string;
  style?: string;
  instruments?: string;
  voice_tags?: string;
  lyrics_structure?: string;
  created_at: string;
  is_active: boolean;
  tags: string[];
}


export interface TagCreate {
  name: string;
  description?: string;
  tag_type?: string;
}


export interface TagResponse {
  id: string;
  name: string;
  description?: string;
  tag_type?: string;
  created_at: string;
}


export interface CategoryCreate {
  name: string;
  description?: string;
}


export interface CategoryResponse {
  id: string;
  name: string;
  description?: string;
  created_at: string;
}