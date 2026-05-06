import httpx
import json

def test_suno_playlist_api():
    """
    Test script to verify the Suno playlist API endpoint works correctly
    """
    # The playlist ID from the original request
    playlist_id = "0e69bdd6-22ea-4c71-94a6-ff6e4203d7ff"
    base_url = "http://localhost:8000/api/v1/playlists"

    print(f"Testing Suno playlist API with playlist ID: {playlist_id}")
    
    try:
        # Make a request to the API to fetch and save the playlist
        response = httpx.get(f"{base_url}/suno-playlist/{playlist_id}")
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Successfully fetched and saved playlist data:")
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
    except httpx.ConnectError:
        print("Error: Could not connect to the API. Make sure the FastAPI server is running.")
    except httpx.RequestError as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response")


def test_local_playlist_api():
    """
    Test script to verify the local Suno playlist API endpoint works correctly
    """
    # The playlist ID from the original request
    playlist_id = "0e69bdd6-22ea-4c71-94a6-ff6e4203d7ff"
    base_url = "http://localhost:8000/api/v1/playlists"

    print(f"Testing local Suno playlist API with playlist ID: {playlist_id}")
    
    try:
        # Make a request to the API to get the playlist from local database
        response = httpx.get(f"{base_url}/suno-playlist/{playlist_id}/local")
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Successfully fetched playlist from local database:")
            print(json.dumps(data, indent=2))
        elif response.status_code == 404:
            print("Playlist not found in local database")
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
    except httpx.ConnectError:
        print("Error: Could not connect to the API. Make sure the FastAPI server is running.")
    except httpx.RequestError as e:
        print(f"Error making request: {e}")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON response")


if __name__ == "__main__":
    print("Testing Suno Playlist API...")
    test_suno_playlist_api()
    print("\n" + "="*50 + "\n")
    test_local_playlist_api()