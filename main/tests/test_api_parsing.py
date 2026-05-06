import json
import sys
import os
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from main.services.api import fetch_playlist_from_suno

def test_api_parsing():
    """
    Test the API parsing logic with mocked Suno API response
    """
    print("Testing API parsing with mocked Suno response...")

    # Mock response data
    mock_response_data = {
        "id": "0e69bdd6-22ea-4c71-94a6-ff6e4203d7ff",
        "name": "Test Playlist",
        "playlist_clips": [
            {
                "clip": {
                    "id": "test-clip-id",
                    "title": "Test Song"
                }
            }
        ]
    }

    # Test the parsing function with the playlist ID
    playlist_id = "0e69bdd6-22ea-4c71-94a6-ff6e4203d7ff"

    try:
        with patch('main.services.api.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = mock_response_data
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            # Fetch the playlist using our service function
            playlist_data = fetch_playlist_from_suno(playlist_id)
        
        print("Successfully parsed playlist data:")
        print(json.dumps(playlist_data, indent=2))
        
        # Verify the structure of the parsed data
        assert "id" in playlist_data, "Missing 'id' field"
        assert "name" in playlist_data, "Missing 'name' field"
        assert "playlist_clips" in playlist_data, "Missing 'playlist_clips' field"
        
        print(f"\nPlaylist ID: {playlist_data['id']}")
        print(f"Playlist Name: {playlist_data['name']}")
        print(f"Number of clips: {len(playlist_data['playlist_clips'])}")

        # Check the first clip if it exists
        if playlist_data['playlist_clips']:
            first_clip = playlist_data['playlist_clips'][0]['clip'] if 'clip' in playlist_data['playlist_clips'][0] else playlist_data['playlist_clips'][0]
            print(f"First clip title: {first_clip.get('title', 'N/A')}")
            print(f"First clip ID: {first_clip.get('id', 'N/A')}")
        
        print("\nAll parsing tests passed!")
        
    except Exception as e:
        print(f"Error during parsing test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_parsing()