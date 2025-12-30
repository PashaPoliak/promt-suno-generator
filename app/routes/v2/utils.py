import json
from pathlib import Path
from typing import Optional

from config.logging_config import get_logger
logger = get_logger(__name__)

def read_json_file(file_path: str) -> Optional[dict]:
    path = Path(file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

def read_json_from_folder(folder_path: str, page: int = 0, size: int = 25) -> list:
    all_json_files = []
    path = Path(folder_path)
    json_files = list(path.glob("*.json"))
    start_index = page * size
    end_index = start_index + size
    paginated_files = json_files[start_index:end_index]
    try:
        for json_file in paginated_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    all_json_files.append(json.load(f))
            except json.JSONDecodeError:
                continue
    except Exception as e:
        logger.error(f"Error reading folder {folder_path}: {e}")
    
    return all_json_files
