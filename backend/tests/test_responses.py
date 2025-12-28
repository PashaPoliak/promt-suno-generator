import requests
import pytest

profiles_URL = "https://studio-api.prod.suno.com/api/profiles/fotballpiraten"
profiles_LOCAL_URL = "http://localhost:8000/api/v1/profiles/fotballpiraten"

playlist_URL = "https://studio-api.prod.suno.com/api/playlist/7ec624f7-9a8d-4a9c-84a6-33132901e1cc"
playlist_LOCAL_URL = "http://localhost:8000/api/v1/playlist/7ec624f7-9a8d-4a9c-84a6-33132901e1cc"

def fetch(url, params=None):
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def diff_dict(d1, d2, path=""):
    diffs = []
    keys = set(d1.keys()) | set(d2.keys())
    for k in keys:
        new_path = f"{path}.{k}" if path else k
        if k not in d1:
            diffs.append(f"Missing in first: {new_path}")
        elif k not in d2:
            diffs.append(f"Missing in second: {new_path}")
        else:
            v1, v2 = d1[k], d2[k]
            if isinstance(v1, dict) and isinstance(v2, dict):
                diffs.extend(diff_dict(v1, v2, new_path))
            elif isinstance(v1, list) and isinstance(v2, list):
                min_len = min(len(v1), len(v2))
                for i in range(min_len):
                    if isinstance(v1[i], dict) and isinstance(v2[i], dict):
                        diffs.extend(diff_dict(v1[i], v2[i], f"{new_path}[{i}]"))
                    elif v1[i] != v2[i]:
                        diffs.append(f"Value mismatch at {new_path}[{i}]: {v1[i]} != {v2[i]}")
                if len(v1) != len(v2):
                    diffs.append(f"List length mismatch at {new_path}: {len(v1)} != {len(v2)}")
            elif v1 != v2:
                diffs.append(f"Value mismatch at {new_path}: {v1} != {v2}")
    return diffs

@pytest.mark.parametrize("url_prod,url_local,params", [
    (profiles_URL, profiles_LOCAL_URL, {"playlists_sort_by": "upvote_count", "clips_sort_by": "created_at"}),
    (playlist_URL, playlist_LOCAL_URL, None)
])
def test_compare_responses(url_prod, url_local, params):
    prod = fetch(url_prod, params=params)
    local = fetch(url_local, params=params)
    diffs = diff_dict(prod, local)
    assert diffs == [], f"Differences found between {url_prod} and {url_local}: {diffs}"
