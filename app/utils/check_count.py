import sys
import os
from pathlib import Path
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from config.settings import settings

DATABASE_URL = "postgresql://admin:AFttyzTL6nzF7A4myOEFlFMazQ7dVefg@dpg-d5bf6otactks73ft9310-a.oregon-postgres.render.com/suno"

engine = create_engine(DATABASE_URL)

def check_profile_count(table):
    with engine.connect() as conn:
        result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
        count = result.scalar()
        print(f'{table} count: {count}')
        return count

def count_json_files(directory):
    dir_path = Path(f"app/json/{directory}")
    if not dir_path.exists():
        print(f"Directory {directory} does not exist, returning 0")
        return 0
    
    json_files = list(dir_path.glob("*.json"))
    count = 0
    for json_file in json_files:
        with open(json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    count += len(data)
                else:
                    count += 1
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {json_file}")
                continue
    print(f"JSON {directory} count: {count}")
    return count

if __name__ == "__main__":
    tables = ['profiles', 'playlists', 'clips']
    
    for table, json_dir in zip(tables, tables):
        db_count = check_profile_count(table)
        json_count = count_json_files(json_dir)
        if db_count == json_count:
            print(f"[OK] {table}: DB({db_count}) == JSON({json_count})")
        else:
            print(f"[ERROR] {table}: DB({db_count}) != JSON({json_count})")