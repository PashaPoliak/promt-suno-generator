import json
import os
from pathlib import Path

def extract_ids_from_profiles():
    profiles_dir = Path("app/json/profiles")
    playlist_ids = set()
    clip_ids = set()
    
    for json_file in profiles_dir.glob("*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                
                if 'playlists' in data:
                    for playlist in data['playlists']:
                        if 'id' in playlist:
                            playlist_ids.add(playlist['id'])
                
                if 'clips' in data:
                    for clip in data['clips']:
                        if 'id' in clip:
                            clip_ids.add(clip['id'])
                
                if 'playlists' in data:
                    for playlist in data['playlists']:
                        if 'clips' in playlist:
                            for clip in playlist['clips']:
                                if 'id' in clip:
                                    clip_ids.add(clip['id'])
                                    
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {json_file}")
    
    with open("../json/playlist_ids.txt", "w", encoding="utf-8") as f:
        for playlist_id in sorted(playlist_ids):
            f.write(f"{playlist_id}\n")
    
    with open("../json/clip_ids.txt", "w", encoding="utf-8") as f:
        for clip_id in sorted(clip_ids):
            f.write(f"{clip_id}\n")
    
    print(f"Extracted {len(playlist_ids)} unique playlist IDs")
    print(f"Extracted {len(clip_ids)} unique clip IDs")
    print("Playlist IDs saved to playlist_ids.txt")
    print("Clip IDs saved to clip_ids.txt")

if __name__ == "__main__":
    extract_ids_from_profiles()
