import json
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.api import fetch_playlist_from_suno

def test_api_parsing():
    """
    Test the API parsing logic with the actual Suno API response
    """
    print("Testing API parsing with actual Suno response...")
    
    # Test the parsing function with the playlist ID
    playlist_id = "0e69bdd6-22ea-4c71-94a6-ff6e4203d7ff"
    
    try:
        # Fetch the playlist using our service function
        playlist_data = fetch_playlist_from_suno(playlist_id)
        
        print("Successfully parsed playlist data:")
        print(json.dumps(playlist_data, indent=2))
        
        # Verify the structure of the parsed data
        assert "id" in playlist_data, "Missing 'id' field"
        assert "name" in playlist_data, "Missing 'name' field"
        assert "clips" in playlist_data, "Missing 'clips' field"
        assert "description" in playlist_data, "Missing 'description' field"
        
        print(f"\nPlaylist ID: {playlist_data['id']}")
        print(f"Playlist Name: {playlist_data['name']}")
        print(f"Number of clips: {len(playlist_data['clips'])}")
        print(f"Description: {playlist_data['description']}")
        
        # Check the first clip if it exists
        if playlist_data['clips']:
            first_clip = playlist_data['clips'][0]['clip'] if 'clip' in playlist_data['clips'][0] else playlist_data['clips'][0]
            print(f"First clip title: {first_clip.get('title', 'N/A')}")
            print(f"First clip ID: {first_clip.get('id', 'N/A')}")
        
        print("\nAll parsing tests passed!")
        
    except Exception as e:
        print(f"Error during parsing test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_parsing()