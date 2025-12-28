import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { GenerateRequest } from '../../types';

const promptSchema = z.object({
  genre: z.string().optional(),
  mood: z.string().optional(),
  style: z.string().optional(),
  instruments: z.string().optional(),
  voice_tags: z.string().optional(),
  lyrics_structure: z.string().optional(),
});

interface PromptFormProps {
  onSubmit: (data: GenerateRequest) => void;
}

const PromptForm: React.FC<PromptFormProps> = ({ onSubmit }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<GenerateRequest>({
    resolver: zodResolver(promptSchema),
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFormSubmit = async (data: GenerateRequest) => {
    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } finally {
      setIsSubmitting(false);
    }
 };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label htmlFor="genre" className="block text-sm font-medium text-gray-700 mb-1">
            Genre
          </label>
          <input
            id="genre"
            {...register('genre')}
            type="text"
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., pop, rock, jazz"
          />
          {errors.genre && (
            <p className="mt-1 text-sm text-red-600">{errors.genre.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="mood" className="block text-sm font-medium text-gray-700 mb-1">
            Mood
          </label>
          <input
            id="mood"
            {...register('mood')}
            type="text"
            className="w-full px-3 py-2 border border-gray-30 rounded-md shadow-sm focus:outline-none focus:ring-indigo-50 focus:border-indigo-500"
            placeholder="e.g., energetic, melancholic, uplifting"
          />
          {errors.mood && (
            <p className="mt-1 text-sm text-red-600">{errors.mood.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="style" className="block text-sm font-medium text-gray-700 mb-1">
            Style
          </label>
          <input
            id="style"
            {...register('style')}
            type="text"
            className="w-full px-3 py-2 border border-gray-30 rounded-md shadow-sm focus:outline-none focus:ring-indigo-50 focus:border-indigo-500"
            placeholder="e.g., vibrant, dynamic, smooth"
          />
          {errors.style && (
            <p className="mt-1 text-sm text-red-600">{errors.style.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="instruments" className="block text-sm font-medium text-gray-700 mb-1">
            Instruments
          </label>
          <input
            id="instruments"
            {...register('instruments')}
            type="text"
            className="w-full px-3 py-2 border border-gray-30 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., piano, guitar, drums"
          />
          {errors.instruments && (
            <p className="mt-1 text-sm text-red-600">{errors.instruments.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="voice_tags" className="block text-sm font-medium text-gray-700 mb-1">
            Voice Tags
          </label>
          <input
            id="voice_tags"
            {...register('voice_tags')}
            type="text"
            className="w-full px-3 py-2 border border-gray-30 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., smooth, powerful, airy"
          />
          {errors.voice_tags && (
            <p className="mt-1 text-sm text-red-600">{errors.voice_tags.message}</p>
          )}
        </div>

        <div>
          <label htmlFor="lyrics_structure" className="block text-sm font-medium text-gray-700 mb-1">
            Lyrics Structure
          </label>
          <input
            id="lyrics_structure"
            {...register('lyrics_structure')}
            type="text"
            className="w-full px-3 py-2 border border-gray-30 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="e.g., verse-chorus-bridge"
          />
          {errors.lyrics_structure && (
            <p className="mt-1 text-sm text-red-600">{errors.lyrics_structure.message}</p>
          )}
        </div>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isSubmitting}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isSubmitting ? 'Generating...' : 'Generate Prompt'}
        </button>
      </div>
    </form>
  );
};

export default PromptForm;