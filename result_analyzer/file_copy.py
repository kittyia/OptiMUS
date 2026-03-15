import os
import shutil


def copy_files():
    # 源目录和目标目录
    source_dir = "../data/nlp4lp"
    target_dir = "./results"

    # 确保目标目录存在
    os.makedirs(target_dir, exist_ok=True)

    # 遍历源目录下的所有子文件夹
    for folder_name in os.listdir(source_dir):
        folder_path = os.path.join(source_dir, folder_name)

        # 只处理目录
        if not os.path.isdir(folder_path):
            continue

        print(f"处理文件夹: {folder_name}")

        # 创建对应的目标子目录
        target_subdir = os.path.join(target_dir, folder_name)
        os.makedirs(target_subdir, exist_ok=True)

        # 复制 run_dev 文件夹
        run_dev_source = os.path.join(folder_path, "run_dev")
        if os.path.exists(run_dev_source):
            run_dev_target = os.path.join(target_subdir, "run_dev")
            shutil.copytree(run_dev_source, run_dev_target, dirs_exist_ok=True)
            print(f"  - 已复制: run_dev")
        else:
            print(f"  - 未找到: run_dev")

        # 复制 solution.json 文件
        solution_source = os.path.join(folder_path, "solution.json")
        if os.path.exists(solution_source):
            solution_target = os.path.join(target_subdir, "solution.json")
            shutil.copy2(solution_source, solution_target)  # copy2 保留文件元数据
            print(f"  - 已复制: solution.json")
        else:
            print(f"  - 未找到: solution.json")

    print(f"\n完成！文件已复制到 {target_dir}")


if __name__ == "__main__":
    copy_files()