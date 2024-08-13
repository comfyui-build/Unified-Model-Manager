import argparse
import glob
import json
import os

base_cache_dir = "/chenyudata/umm/cache"
config_dir = "/chenyudata/Unified-Model-Manager/umm"


class ModelContent:
    def __init__(self, cache=None, sha256=None, size=None, comfyui_path=None, sdwebui_path=None, download=None,
                 **kwargs):
        self.type = type
        self.cache = cache
        self.sha256 = sha256
        self.size = size
        self.comfyui_path = comfyui_path
        self.sdwebui_path = sdwebui_path
        self.download = download

    def __str__(self):
        return f"ModelContent(cache={self.cache}, sha256={self.sha256}, size={self.size}, comfyui_path={self.comfyui_path}, sdwebui_path={self.sdwebui_path}, download={self.download})"


def general_link(is_comfyui=False, app_base_dir=None):
    # 读取目录文件
    json_files = glob.glob(os.path.join(config_dir, '*.json'))
    for content_file in json_files:
        with open(content_file, 'r', encoding='utf-8') as file:
            # Load the content of the JSON file
            json_array = json.load(file)
            # 将 JSON 数组中的每个元素转换为 ModelContent 对象
            for item in json_array:
                obj = ModelContent(**item)
                if obj.cache is None or ((is_comfyui and obj.comfyui_path is None) or obj.sdwebui_path is None):
                    continue
                if is_comfyui:
                    target_dir = os.path.join(app_base_dir, obj.comfyui_path)
                    source = os.path.join(base_cache_dir, obj.cache)
                    link = os.path.join(app_base_dir, obj.comfyui_path)
                    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
                    if not os.path.exists(link):
                        os.symlink(source, link)
                elif obj.sdwebui_path:
                    target_dir = os.path.join(app_base_dir, obj.sdwebui_path)
                    source = os.path.join(base_cache_dir, obj.cache)
                    link = os.path.join(app_base_dir, obj.sdwebui_path)
                    os.makedirs(os.path.dirname(target_dir), exist_ok=True)
                    if not os.path.exists(link):
                        os.symlink(source, link)


def main():
    parser = argparse.ArgumentParser(description='auth general links.')
    parser.add_argument('--app_base_dir', type=str, help='App Base Dir. ex:/root/ComfyUI')
    parser.add_argument('--is_comfyui', action='store_true', help='Generate comfyui link')
    general_link(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
