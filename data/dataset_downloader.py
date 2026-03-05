from datasets import load_dataset
import shutil
import os

# 加载数据集（会从缓存读取，不用重新下载）
dataset = load_dataset("udell-lab/NLP4LP")

# 设置你想保存的路径
save_path = "NLP4LP_original_format"  # 你可以修改这个路径

# 创建目录
os.makedirs(save_path, exist_ok=True)

# 或者保存为 JSON 格式（方便查看）
dataset['test'].to_json(f"{save_path}/test.json")
dataset['validation'].to_json(f"{save_path}/validation.json")