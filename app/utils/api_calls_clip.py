import requests
import time

def make_clip_api_calls():
    with open('clip_ids.txt', 'r', encoding='utf-8') as file:
        clip_ids = [line.strip() for line in file if line.strip()]
    
    base_url = "http://localhost:8000/api/v1/clip/"
    
    for clip_id in clip_ids:
        url = base_url + clip_id
        response = None
        try:
            response = requests.get(url)
            print(f"Clip ID: {clip_id}, Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for clip ID {clip_id}: {e}")
        except UnicodeEncodeError as e:
            print(f"Unicode encoding error for clip ID {clip_id}: {e}")
            # Save to file instead
        
            
if __name__ == "__main__":
    make_clip_api_calls()