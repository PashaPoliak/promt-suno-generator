import { api } from "../api/client";
import { 
 ClipDTO, 
  PlaylistDTO, 
  ProfileDTO, 
  UserDTO 
} from "../api/types";

export const fetchClips = async (): Promise<ClipDTO[]> => {
  const response = await api.get<ClipDTO[]>("/api/v1/clips");
  return response.data;
};

export const fetchClipById = async (id: string): Promise<ClipDTO> => {
 const response = await api.get<ClipDTO>(`/api/v1/clips/${id}`);
  return response.data;
};

export const fetchPlaylists = async (): Promise<PlaylistDTO[]> => {
  const response = await api.get<PlaylistDTO[]>("/api/v1/playlists");
  return response.data;
};

export const fetchPlaylistById = async (id: string): Promise<PlaylistDTO> => {
  const response = await api.get<PlaylistDTO>(`/api/v1/playlists/${id}`);
  return response.data;
};

export const fetchProfiles = async (): Promise<ProfileDTO[]> => {
  const response = await api.get<ProfileDTO[]>("/api/v1/profiles");
  return response.data;
};

export const fetchProfileById = async (id: string): Promise<ProfileDTO> => {
  const response = await api.get<ProfileDTO>(`/api/v1/profiles/${id}`);
  return response.data;
};

export const fetchUsers = async (): Promise<UserDTO[]> => {
  const response = await api.get<UserDTO[]>("/api/v1/users");
  return response.data;
};

export const fetchUserById = async (id: string): Promise<UserDTO> => {
  const response = await api.get<UserDTO>(`/api/v1/users/${id}`);
  return response.data;
};

