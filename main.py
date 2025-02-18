import os
import json
import zipfile
from analyze_project import analyze_project
from generate_migration_plan import generate_migration_plan
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_folder_structure(project_structure, base_path):
    """Create folders and files based on project structure"""
    # Create root directory
    root_dir = project_structure["root"].lstrip("/")
    project_path = os.path.join(base_path, root_dir)
    os.makedirs(project_path, exist_ok=True)

    # Create folders and their files
    folders = project_structure.get("folders", {})
    for folder, subfolders in folders.items():
        for subfolder, files in subfolders.items():
            folder_path = os.path.join(project_path, folder, subfolder)
            os.makedirs(folder_path, exist_ok=True)

            # Create empty files
            if isinstance(files, list):
                for file in files:
                    file_path = os.path.join(folder_path, file)
                    open(file_path, "w").close()

    # Create root files
    root_files = project_structure.get("files", {}).get("root", [])
    for file in root_files:
        file_path = os.path.join(project_path, file)
        open(file_path, "w").close()

    return project_path


def write_code_files(code_conversion, project_structure, project_path):
    """Write code to files based on code conversion mapping"""
    # Create a mapping of filenames to their full paths
    file_paths = {}

    # Map files from folders structure
    folders = project_structure.get("folders", {})
    for folder, subfolders in folders.items():
        for subfolder, files in subfolders.items():
            if isinstance(files, list):
                for file in files:
                    file_paths[file] = os.path.join(
                        project_path, folder, subfolder, file
                    )

    # Map root files
    root_files = project_structure.get("files", {}).get("root", [])
    for file in root_files:
        file_paths[file] = os.path.join(project_path, file)

    # Write code files using the path mapping
    for file_name, content in code_conversion.items():
        if not isinstance(content, dict):
            # Direct code content
            file_path = file_paths.get(file_name, os.path.join(project_path, file_name))
            with open(file_path, "w") as f:
                f.write(content.strip())
            continue

        # Get the target file path
        target_file = content.get("newFile", file_name)
        file_path = file_paths.get(target_file, os.path.join(project_path, target_file))

        if "to" in content:
            # Handle direct conversion
            with open(file_path, "w") as f:
                f.write(content["to"].strip())

        elif "code" in content:
            # Handle files with direct code
            with open(file_path, "w") as f:
                f.write(content["code"].strip())

        elif "methods" in content:
            # Handle files with multiple methods
            methods_content = []
            for method_code in content["methods"].values():
                methods_content.append(method_code.strip())

            # Get imports from the content if available
            imports = content.get("imports", [])
            imports_text = "\n".join(imports) if imports else ""

            # Get exports from the content if available
            exports = content.get("exports", list(content["methods"].keys()))

            # Format the file content
            file_content = f"""{imports_text}

{"\n\n".join(methods_content)}

module.exports = {{
    {",\n    ".join(exports)}
}};"""

            with open(file_path, "w") as f:
                f.write(file_content)


def generate_config_files(project_structure, dependencies, project_path):
    """Generate configuration files based on project structure"""
    root_files = project_structure.get("files", {}).get("root", [])

    if "package.json" in root_files:
        package_json = {
            "name": os.path.basename(project_path),
            "version": "1.0.0",
            "description": "Migrated Node.js application",
            "main": "server.js",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js",
                "test": "jest",
            },
            "dependencies": dependencies.get("primary", {}),
            "devDependencies": dependencies.get("dev", {}),
        }
        with open(os.path.join(project_path, "package.json"), "w") as f:
            json.dump(package_json, f, indent=2)

    if ".env" in root_files:
        env_content = """PORT=3000
NODE_ENV=development"""
        with open(os.path.join(project_path, ".env"), "w") as f:
            f.write(env_content)

    if ".gitignore" in root_files:
        gitignore_content = """node_modules/
.env
coverage/
.DS_Store"""
        with open(os.path.join(project_path, ".gitignore"), "w") as f:
            f.write(gitignore_content)


# Define the input and output paths
input_zip_path = "Php.zip"
output_path = "output"

try:
    # Step 1: Extract the input project
    logging.info("Extracting the input project...")
    with zipfile.ZipFile(input_zip_path, "r") as zip_ref:
        zip_ref.extractall(output_path)

    # Step 2: Analyze the input project
    logging.info("Analyzing the input project...")
    project_analysis = analyze_project(output_path)

    # Step 3: Generate and parse the migration plan
    logging.info("Generating the migration plan...")
    migration_plan_text = generate_migration_plan(
        project_analysis, target_language="node"
    )

    print(migration_plan_text)
    migration_plan = json.loads(migration_plan_text)

    # Step 4: Create project structure
    # logging.info("Creating project structure...")
    # project_structure = migration_plan["migrationPlan"]["projectStructure"]
    # project_path = create_folder_structure(project_structure, output_path)

    # # Step 5: Write code files
    # logging.info("Writing code files...")
    # write_code_files(
    #     migration_plan["migrationPlan"]["codeConversion"],
    #     project_structure,
    #     project_path,
    # )

    # # Step 6: Generate configuration files
    # logging.info("Generating configuration files...")
    # generate_config_files(
    #     project_structure, migration_plan["migrationPlan"]["dependencies"], project_path
    # )

    # logging.info("Migration completed successfully!")
    # logging.info(f"Project created at: {project_path}")
    # logging.info("\nTo start the project:")
    # logging.info(f"1. cd {project_path}")
    # logging.info("2. npm install")
    # logging.info("3. npm run dev")

except Exception as e:
    logging.error(f"Error during migration: {str(e)}")
    raise
