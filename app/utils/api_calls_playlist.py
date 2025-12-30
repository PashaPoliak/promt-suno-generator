import requests
import time
import json

def make_playlist_api_calls():
    # Read playlist IDs from the file
    with open('playlist_ids.txt', 'r', encoding='utf-8') as file:
        playlist_ids = [line.strip() for line in file if line.strip()]
    
    base_url = "http://localhost:8000/api/v1/playlist/"
    
    for playlist_id in playlist_ids:
        url = base_url + playlist_id
        response = None
        try:
            response = requests.get(url)
            print(f"Playlist ID: {playlist_id}, Status Code: {response.status_code}")
            if response.status_code == 200:
                # Write response to a file
                with open(f"playlist_response_{playlist_id}.json", "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=2)
                print(f"Playlist response saved to playlist_response_{playlist_id}.json")
            else:
                print(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for playlist ID {playlist_id}: {e}")
        except UnicodeEncodeError as e:
            print(f"Unicode encoding error for playlist ID {playlist_id}: {e}")
            # Save to file instead
            if response is not None:
                try:
                    with open(f"playlist_response_{playlist_id}.json", "w", encoding="utf-8") as f:
                        json.dump(response.json(), f, ensure_ascii=False, indent=2)
                    print(f"Playlist response saved to playlist_response_{playlist_id}.json")
                except:
                    print("Could not save playlist response to file")
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(0.1)

if __name__ == "__main__":
    make_playlist_api_calls()