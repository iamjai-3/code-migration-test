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


def create_output_files(migration_plan_path):
    # Read migration plan
    with open(migration_plan_path, "r") as f:
        plan = json.load(f)

    # Get project root
    root_dir = plan["projectStructure"]["root"]
    if os.path.exists(root_dir):
        print(f"Directory {root_dir} already exists. Cleaning...")
        for root, dirs, files in os.walk(root_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

    # Create folder structure
    for folder_path in plan["projectStructure"]["folders"]:
        full_path = os.path.join(root_dir, folder_path)
        os.makedirs(full_path, exist_ok=True)
        print(f"Created directory: {full_path}")

    # Create code files
    for source, info in plan["codeConversion"].items():
        if isinstance(info, dict) and "target" in info and "code" in info:
            target_path = os.path.join(root_dir, info["target"])
            os.makedirs(os.path.dirname(target_path), exist_ok=True)

            if os.path.exists(target_path):
                append_to_file(target_path, info["code"])
                print(f"Appended to file: {target_path}")
            else:
                with open(target_path, "w") as f:
                    f.write(info["code"])
                print(f"Created file: {target_path}")


if __name__ == "__main__":
    create_output_files("migration_plan.json")
