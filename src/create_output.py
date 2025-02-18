import os
import json


def append_to_file(file_path, code):
    """Append code to an existing file"""
    with open(file_path, "r") as f:
        content = f.read().strip()

    # Check if code already exists in file
    if code.strip() in content:
        return

    with open(file_path, "a") as f:
        # Add newlines for separation
        if content:
            f.write("\n\n")
        f.write(code)


def clean_directory(root_dir):
    if os.path.exists(root_dir):
        print(f"Directory {root_dir} already exists. Cleaning...")
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


def create_folder_structure(root_dir, folders):
    for folder_path in folders:
        full_path = os.path.join(root_dir, folder_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")


def create_code_file(root_dir, target, code):
    target_path = os.path.join(root_dir, target)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    if os.path.exists(target_path):
        append_to_file(target_path, code)
        print(f"Appended to file: {target_path}")
    else:
        with open(target_path, "w") as f:
            f.write(code)
        print(f"Created file: {target_path}")


def create_output_files(migration_plan_path):
    with open(migration_plan_path, "r") as f:
        plan = json.load(f)

    root_dir = plan["projectStructure"]["root"]
    clean_directory(root_dir)
    create_folder_structure(root_dir, plan["projectStructure"]["folders"])

    for source, info in plan["codeConversion"].items():
        if isinstance(info, dict) and "target" in info and "code" in info:
            create_code_file(root_dir, info["target"], info["code"])


if __name__ == "__main__":
    create_output_files("migration_plan.json")
