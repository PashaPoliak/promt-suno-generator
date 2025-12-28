import React, { useState, useEffect } from 'react';
import { getAllTemplates, createTemplate, updateTemplate, deleteTemplate } from '../services/api';
import { TemplateResponse, TemplateCreate } from '../types';

const TemplateLibrary: React.FC = () => {
  const [templates, setTemplates] = useState<TemplateResponse[]>([]);
  const [loading, setLoading] = useState(true);
 const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<TemplateResponse | null>(null);
  const [formData, setFormData] = useState<TemplateCreate>({
    name: '',
    description: '',
    genre: '',
    mood: '',
    style: '',
    instruments: '',
    voice_tags: '',
    lyrics_structure: '',
    is_active: true
  });

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const response = await getAllTemplates();
      setTemplates(response);
    } catch (err) {
      setError('Failed to fetch templates');
      console.error('Error fetching templates:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingTemplate) {
        await updateTemplate(editingTemplate.id, formData);
      } else {
        await createTemplate(formData);
      }
      setFormData({
        name: '',
        description: '',
        genre: '',
        mood: '',
        style: '',
        instruments: '',
        voice_tags: '',
        lyrics_structure: '',
        is_active: true
      });
      setShowForm(false);
      setEditingTemplate(null);
      fetchTemplates();
    } catch (err) {
      setError('Failed to save template');
      console.error('Error saving template:', err);
    }
  };

  const handleEdit = (template: TemplateResponse) => {
    setEditingTemplate(template);
    setFormData({
      name: template.name,
      description: template.description || '',
      genre: template.genre || '',
      mood: template.mood || '',
      style: template.style || '',
      instruments: template.instruments || '',
      voice_tags: template.voice_tags || '',
      lyrics_structure: template.lyrics_structure || '',
      is_active: template.is_active
    });
    setShowForm(true);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this template?')) {
      try {
        await deleteTemplate(id);
        fetchTemplates();
      } catch (err) {
        setError('Failed to delete template');
        console.error('Error deleting template:', err);
      }
    }
 };

  const handleNewTemplate = () => {
    setEditingTemplate(null);
    setFormData({
      name: '',
      description: '',
      genre: '',
      mood: '',
      style: '',
      instruments: '',
      voice_tags: '',
      lyrics_structure: '',
      is_active: true
    });
    setShowForm(true);
  };

  if (loading) return <div className="text-center py-8">Loading templates...</div>;
  if (error) return <div className="text-center py-8 text-red-600">{error}</div>;

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Template Library</h1>
        <button
          onClick={handleNewTemplate}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-60 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Create Template
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200 mb-8">
          <h2 className="text-lg font-semibold mb-4">
            {editingTemplate ? 'Edit Template' : 'Create New Template'}
          </h2>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
                  Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              <div>
                <label htmlFor="genre" className="block text-sm font-medium text-gray-700 mb-1">
                  Genre
                </label>
                <input
                  type="text"
                  id="genre"
                  name="genre"
                  value={formData.genre}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-50 focus:border-indigo-500"
                />
              </div>
              <div>
                <label htmlFor="mood" className="block text-sm font-medium text-gray-700 mb-1">
                  Mood
                </label>
                <input
                  type="text"
                  id="mood"
                  name="mood"
                  value={formData.mood}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-50 focus:border-indigo-500"
                />
              </div>
              <div>
                <label htmlFor="style" className="block text-sm font-medium text-gray-700 mb-1">
                  Style
                </label>
                <input
                  type="text"
                  id="style"
                  name="style"
                  value={formData.style}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              <div>
                <label htmlFor="instruments" className="block text-sm font-medium text-gray-700 mb-1">
                  Instruments
                </label>
                <input
                  type="text"
                  id="instruments"
                  name="instruments"
                  value={formData.instruments}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
              <div>
                <label htmlFor="voice_tags" className="block text-sm font-medium text-gray-700 mb-1">
                  Voice Tags
                </label>
                <input
                  type="text"
                  id="voice_tags"
                  name="voice_tags"
                  value={formData.voice_tags}
                  onChange={handleInputChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                />
              </div>
            </div>
            <div>
              <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div>
              <label htmlFor="lyrics_structure" className="block text-sm font-medium text-gray-700 mb-1">
                Lyrics Structure
              </label>
              <input
                type="text"
                id="lyrics_structure"
                name="lyrics_structure"
                value={formData.lyrics_structure}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
              />
            </div>
            <div className="flex items-center">
              <input
                type="checkbox"
                id="is_active"
                name="is_active"
                checked={formData.is_active}
                onChange={(e) => setFormData(prev => ({ ...prev, is_active: e.target.checked }))}
                className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label htmlFor="is_active" className="ml-2 block text-sm text-gray-900">
                Active
              </label>
            </div>
            <div className="flex space-x-3">
              <button
                type="submit"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-60 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                {editingTemplate ? 'Update' : 'Create'}
              </button>
              <button
                type="button"
                onClick={() => {
                  setShowForm(false);
                  setEditingTemplate(null);
                }}
                className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {templates.map(template => (
          <div key={template.id} className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <div className="flex justify-between items-start">
              <h3 className="text-lg font-semibold text-gray-800">{template.name}</h3>
              <div className="flex space-x-2">
                <button
                  onClick={() => handleEdit(template)}
                  className="text-indigo-600 hover:text-indigo-900"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(template.id)}
                  className="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </div>
            {template.description && (
              <p className="mt-2 text-gray-600">{template.description}</p>
            )}
            <div className="mt-4 space-y-1">
              {template.genre && (
                <div className="text-sm text-gray-500">
                  <span className="font-medium">Genre:</span> {template.genre}
                </div>
              )}
              {template.mood && (
                <div className="text-sm text-gray-500">
                  <span className="font-medium">Mood:</span> {template.mood}
                </div>
              )}
              {template.style && (
                <div className="text-sm text-gray-500">
                  <span className="font-medium">Style:</span> {template.style}
                </div>
              )}
              {template.instruments && (
                <div className="text-sm text-gray-500">
                  <span className="font-medium">Instruments:</span> {template.instruments}
                </div>
              )}
              {template.voice_tags && (
                <div className="text-sm text-gray-500">
                  <span className="font-medium">Voice Tags:</span> {template.voice_tags}
                </div>
              )}
            </div>
            <div className="mt-4">
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                template.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
              }`}>
                {template.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TemplateLibrary;