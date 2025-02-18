import os
import json
import anthropic
import logging
from tqdm import tqdm

# Function to translate the code using the Anthropics API
# This function should translate the code without losing its context


def translate_code(migration_plan_text, target_language):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    migration_plan = json.loads(migration_plan_text)
    project_structure = migration_plan["projectStructure"]
    code_conversion = migration_plan["codeConversion"]

    # Create package.json with dependencies
    root_dir = project_structure["root"].lstrip("/")
    package_json = {
        "name": root_dir,
        "version": "1.0.0",
        "dependencies": {dep: "*" for dep in migration_plan["dependencies"]},
    }
    with open(os.path.join("output", root_dir, "package.json"), "w") as f:
        json.dump(package_json, f, indent=2)

    # Process each file in the code conversion mapping
    for source_file, target_info in tqdm(
        code_conversion.items(), desc="Converting files"
    ):
        if not isinstance(target_info, dict):
            logging.error(f"Invalid target info for {source_file}: {target_info}")
            continue

        target_file = target_info.get("target")
        if not target_file:
            logging.error(f"Missing target field for {source_file}")
            continue

        source_code = target_info.get("code")
        if not source_code:
            # Try to read the source code from the original file
            try:
                # Remove any 'output' prefix from the path if it exists
                actual_path = source_file.replace("output/", "").replace("output\\", "")
                with open(actual_path, "r", encoding="utf-8") as f:
                    source_code = f.read()
            except Exception as e:
                logging.error(f"Could not read source file {source_file}: {str(e)}")
                continue

        try:
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8000,
                system="You are a code conversion expert. Convert the provided PHP code to the target language. Return only the converted code, no explanations.",
                messages=[
                    {
                        "role": "user",
                        "content": f"Convert this PHP code to {target_language}:\n\n{source_code}",
                    }
                ],
            )
            converted_code = response.content[0].text

            # Write the converted code to the target file
            target_path = os.path.join("output", root_dir, target_file)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(converted_code)

            logging.info(f"Converted {source_file} -> {target_file}")

        except Exception as e:
            logging.error(f"Error converting {source_file}: {str(e)}")
            continue
