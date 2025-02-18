import os
import json
import zipfile
import argparse
from src.analyze_project import analyze_project
from src.generate_migration_plan import generate_migration_plan
from src.create_output import create_output_files
import logging
import shutil

logging.basicConfig(level=logging.INFO)

# Define global paths
TEMP_PATH = "temp_extract"
OUTPUT_PATH = "output"


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
                    open(file_path, "w", encoding="utf-8").close()

    # Create root files
    root_files = project_structure.get("files", {}).get("root", [])
    for file in root_files:
        file_path = os.path.join(project_path, file)
        open(file_path, "w", encoding="utf-8").close()

    return project_path


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Migrate code between programming languages"
    )
    parser.add_argument(
        "input_zip", help="Path to the input zip file containing the source code"
    )
    parser.add_argument(
        "input_language", help="Source code language (e.g., php, python, java)"
    )
    parser.add_argument(
        "target_language",
        help="Target language to migrate to (e.g., node, python, java)",
    )
    args = parser.parse_args()

    try:
        # Clean up any existing directories
        for path in [TEMP_PATH, OUTPUT_PATH]:
            if os.path.exists(path):
                shutil.rmtree(path)
            os.makedirs(path)

        # Step 1: Extract and analyze the input project
        logging.info("Extracting the input project...")
        with zipfile.ZipFile(args.input_zip, "r") as zip_ref:
            zip_ref.extractall(TEMP_PATH)

        logging.info("Analyzing the input project...")
        project_analysis = analyze_project(TEMP_PATH, args.input_language)

        # Step 2: Generate project structure
        logging.info("Generating the migration plan...")
        migration_plan_text = generate_migration_plan(
            project_analysis,
            source_language=args.input_language,
            target_language=args.target_language,
        )

        # Validate and parse the migration plan
        try:
            migration_plan = json.loads(migration_plan_text)
            logging.info("Migration plan generated successfully")

            # Write migration plan to a file for inspection
            with open("migration_plan.json", "w", encoding="utf-8") as f:
                json.dump(migration_plan, f, indent=2)
            logging.info("Migration plan written to migration_plan.json")

            # Step 3: Generate output files
            logging.info("Creating output files...")
            create_output_files("migration_plan.json")
            logging.info(
                f"Migration completed successfully! Output is in the '{OUTPUT_PATH}' directory"
            )

        except json.JSONDecodeError:
            logging.error(f"Invalid migration plan JSON: {migration_plan_text}")
            with open("failed_migration_plan.txt", "w", encoding="utf-8") as f:
                f.write(migration_plan_text)
            logging.error("Raw response written to failed_migration_plan.txt")
            raise

    except Exception as e:
        logging.error(f"Error during migration: {str(e)}")
        raise
    finally:
        # Clean up temporary directory
        if os.path.exists(TEMP_PATH):
            shutil.rmtree(TEMP_PATH)


if __name__ == "__main__":
    main()
