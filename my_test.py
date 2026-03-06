# test_main_import.py
import sys

print(f"Python: {sys.executable}")

try:
    print("1. 导入 os...")
    import os

    print("✅ os 导入成功")

    print("2. 导入 time...")
    import time

    print("✅ time 导入成功")

    print("3. 导入 json...")
    import json

    print("✅ json 导入成功")

    print("4. 导入 argparse...")
    import argparse

    print("✅ argparse 导入成功")

    print("5. 导入 rag.rag_utils...")
    from rag.rag_utils import RAGMode

    print("✅ rag.rag_utils 导入成功")

    print("6. 导入 dotenv...")
    from dotenv import load_dotenv

    print("✅ dotenv 导入成功")

    print("\n🎉 所有导入成功！")

except Exception as e:
    print(f"\n❌ 导入失败: {e}")
    import traceback

    traceback.print_exc()

    print("\n检查 sys.path:")
    for i, p in enumerate(sys.path):
        print(f"  {i}: {p}")