import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generatePrompt = async (data: any) => {
  const response = await api.post('/generate', data);
  return response.data;
};

export const getPrompts = async (params?: any) => {
  const response = await api.get('/prompts', { params });
  return response.data;
};

export const getPrompt = async (id: string) => {
  const response = await api.get(`/prompts/${id}`);
  return response.data;
};

export const createPrompt = async (data: any) => {
  const response = await api.post('/prompts', data);
  return response.data;
};

export const getTemplates = async (params?: any) => {
  const response = await api.get('/prompts/templates', { params });
  return response.data;
};

export const getTemplate = async (id: string) => {
  const response = await api.get(`/prompts/templates/${id}`);
  return response.data;
};

export const validatePrompt = async (data: any) => {
  const response = await api.post('/validate', data);
  return response.data;
};

export default api;


// Template API functions
export const getAllTemplates = async (params?: any) => {
  const response = await api.get('/prompts/templates', { params });
  return response.data;
};


export const getSingleTemplate = async (id: string) => {
  const response = await api.get(`/prompts/templates/${id}`);
  return response.data;
};


export const createTemplate = async (data: any) => {
  const response = await api.post('/prompts/templates', data);
  return response.data;
};


export const updateTemplate = async (id: string, data: any) => {
 const response = await api.put(`/prompts/templates/${id}`, data);
  return response.data;
};


export const deleteTemplate = async (id: string) => {
  const response = await api.delete(`/prompts/templates/${id}`);
  return response.data;
};


// Tag API functions
export const getAllTags = async (params?: any) => {
  const response = await api.get('/tags', { params });
  return response.data;
};


export const getSingleTag = async (id: string) => {
  const response = await api.get(`/tags/${id}`);
 return response.data;
};


export const createTag = async (data: any) => {
  const response = await api.post('/tags', data);
  return response.data;
};


export const updateTag = async (id: string, data: any) => {
  const response = await api.put(`/tags/${id}`, data);
  return response.data;
};


export const deleteTag = async (id: string) => {
  const response = await api.delete(`/tags/${id}`);
 return response.data;
};


// Category API functions
export const getAllCategories = async (params?: any) => {
  const response = await api.get('/categories', { params });
  return response.data;
};


export const getSingleCategory = async (id: string) => {
  const response = await api.get(`/categories/${id}`);
  return response.data;
};


export const createCategory = async (data: any) => {
  const response = await api.post('/categories', data);
  return response.data;
};


export const updateCategory = async (id: string, data: any) => {
  const response = await api.put(`/categories/${id}`, data);
  return response.data;
};


export const deleteCategory = async (id: string) => {
  const response = await api.delete(`/categories/${id}`);
  return response.data;
};


// Additional generation functions
export const combinePrompts = async (data: any) => {
  const response = await api.post('/prompts/combine', data);
  return response.data;
};


export const extendPrompt = async (data: any) => {
  const response = await api.post('/prompts/extend', data);
  return response.data;
};


// Prompt management functions
export const deletePrompt = async (id: string) => {
  const response = await api.delete(`/prompts/${id}`);
  return response.data;
};