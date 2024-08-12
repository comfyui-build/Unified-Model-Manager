import requests
import re
import json
from tqdm.auto import tqdm
import argparse

def get_sha256(url_orign):
    try:
        url = url_orign.replace('resolve/main', 'blob/main')
        response = requests.get(url)

        if response.status_code == 200:
            pattern = r'<li><strong>SHA256:</strong>\s*([0-9a-fA-F]+)</li>'
            match = re.search(pattern, response.text)

            if match:
                sha256_value = match.group(1).strip()
                return sha256_value
            else:
                print("SHA256 value not found.")
        else:
            print(f"Failed to retrieve the file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_json_sha256(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for d in tqdm(data):
        if not d['sha256']:
            d['sha256'] = get_sha256(d['download'])

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    parser = argparse.ArgumentParser(description='Update JSON file with SHA256 values.')
    parser.add_argument('file_path', type=str, help='Path to the JSON file')
    args = parser.parse_args()

    update_json_sha256(args.file_path)

if __name__ == '__main__':
    main()
