import requests
import time
import json

def make_api_calls():
    # Read handles from the file
    with open('handles.txt', 'r', encoding='utf-8') as file:
        handles = [line.strip() for line in file if line.strip()]
    
    base_url = "http://localhost:8000/api/v1/profiles/"
    
    for handle in handles:
        url = base_url + handle
        response = None
        try:
            response = requests.get(url)
            print(f"Handle: {handle}, Status Code: {response.status_code}")
            if response.status_code == 200:
                # Write response to a file instead of printing to console to avoid encoding issues
                with open(f"response_{handle}.json", "w", encoding="utf-8") as f:
                    json.dump(response.json(), f, ensure_ascii=False, indent=2)
                print(f"Response saved to response_{handle}.json")
            else:
                print(f"Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed for handle {handle}: {e}")
        except UnicodeEncodeError as e:
            print(f"Unicode encoding error for handle {handle}: {e}")
            # Save to file instead
            if response is not None:
                try:
                    with open(f"response_{handle}.json", "w", encoding="utf-8") as f:
                        json.dump(response.json(), f, ensure_ascii=False, indent=2)
                    print(f"Response saved to response_{handle}.json")
                except:
                    print("Could not save response to file")
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(0.1)

if __name__ == "__main__":
    make_api_calls()