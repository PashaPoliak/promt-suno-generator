import axios from 'axios';
import {
  GenerateRequest,
  GenerateResponse,
  PromptCreate,
  PromptResponse,
  TemplateCreate,
  TemplateResponse,
  TagCreate,
  TagResponse,
  CategoryCreate,
  CategoryResponse
} from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generatePrompt = async (data: GenerateRequest) => {
  const response = await api.post('/generate', data);
  return response.data as GenerateResponse;
};

export const getPrompts = async (params?: any) => {
  const response = await api.get<PromptResponse[]>('/prompts', { params });
  return response.data;
};

export const getPrompt = async (id: string) => {
  const response = await api.get<PromptResponse>(`/prompts/${id}`);
  return response.data;
};

export const createPrompt = async (data: PromptCreate) => {
  const response = await api.post<PromptResponse>('/prompts', data);
  return response.data;
};

export const getTemplates = async (params?: any) => {
  const response = await api.get<TemplateResponse[]>('/prompts/templates', { params });
  return response.data;
};

export const getTemplate = async (id: string) => {
  const response = await api.get<TemplateResponse>(`/prompts/templates/${id}`);
  return response.data;
};

export const validatePrompt = async (data: GenerateRequest) => {
  const response = await api.post('/validate', data);
  return response.data;
};

export default api;


// Template API functions
export const getAllTemplates = async (params?: any) => {
  const response = await api.get<TemplateResponse[]>('/prompts/templates', { params });
  return response.data;
};


export const getSingleTemplate = async (id: string) => {
  const response = await api.get<TemplateResponse>(`/prompts/templates/${id}`);
  return response.data;
};


export const createTemplate = async (data: TemplateCreate) => {
  const response = await api.post<TemplateResponse>('/prompts/templates', data);
  return response.data;
};


export const updateTemplate = async (id: string, data: TemplateCreate) => {
 const response = await api.put<TemplateResponse>(`/prompts/templates/${id}`, data);
  return response.data;
};


export const deleteTemplate = async (id: string) => {
  const response = await api.delete(`/prompts/templates/${id}`);
  return response.data;
};


// Tag API functions
export const getAllTags = async (params?: any) => {
  const response = await api.get<TagResponse[]>('/tags', { params });
  return response.data;
};


export const getSingleTag = async (id: string) => {
  const response = await api.get<TagResponse>(`/tags/${id}`);
  return response.data;
};


export const createTag = async (data: TagCreate) => {
  const response = await api.post<TagResponse>('/tags', data);
  return response.data;
};


export const updateTag = async (id: string, data: TagCreate) => {
  const response = await api.put<TagResponse>(`/tags/${id}`, data);
  return response.data;
};


export const deleteTag = async (id: string) => {
  const response = await api.delete(`/tags/${id}`);
 return response.data;
};


// Category API functions
export const getAllCategories = async (params?: any) => {
  const response = await api.get<CategoryResponse[]>('/categories', { params });
  return response.data;
};


export const getSingleCategory = async (id: string) => {
  const response = await api.get<CategoryResponse>(`/categories/${id}`);
  return response.data;
};


export const createCategory = async (data: CategoryCreate) => {
  const response = await api.post<CategoryResponse>('/categories', data);
  return response.data;
};


export const updateCategory = async (id: string, data: CategoryCreate) => {
  const response = await api.put<CategoryResponse>(`/categories/${id}`, data);
  return response.data;
};


export const deleteCategory = async (id: string) => {
  const response = await api.delete(`/categories/${id}`);
  return response.data;
};


// Additional generation functions
export const combinePrompts = async (data: GenerateRequest) => {
  const response = await api.post('/prompts/combine', data);
  return response.data;
};


export const extendPrompt = async (data: GenerateRequest) => {
  const response = await api.post('/prompts/extend', data);
  return response.data;
};


// Prompt management functions
export const deletePrompt = async (id: string) => {
  const response = await api.delete(`/prompts/${id}`);
  return response.data;
};

// User API functions
export const getUsers = async (params?: any) => {
  const response = await api.get('/users', { params });
  return response.data;
};

export const getUser = async (id: string) => {
  const response = await api.get(`/users/${id}`);
  return response.data;
};

// Playlist API functions
export const getPlaylists = async (params?: any) => {
  const response = await api.get('/playlist', { params });
  return response.data;
};

export const getPlaylist = async (id: string) => {
  const response = await api.get(`/playlist/${id}`);
  return response.data;
};

// Clip API functions
export const getClips = async (params?: any) => {
  const response = await api.get('/clip', { params });
  return response.data;
};

export const getClip = async (id: string) => {
  const response = await api.get(`/clip/${id}`);
  return response.data;
};