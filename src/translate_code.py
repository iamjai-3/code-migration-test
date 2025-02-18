import os
import json
import anthropic
import logging
from tqdm import tqdm


def translate_code(migration_plan_text, target_language):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    migration_plan = json.loads(migration_plan_text)
    project_structure = migration_plan["projectStructure"]
    code_conversion = migration_plan["codeConversion"]
    source_language = migration_plan.get("sourceLanguage", "Unknown")

    root_dir = project_structure["root"].lstrip("/")

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
            try:
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
                system=f"""You are a code conversion expert. Convert the provided {source_language} code to {target_language}. 
                Follow these rules:
                1. Return only the converted code, no explanations
                2. Preserve all functionality exactly
                3. Keep the same code structure where possible
                4. Maintain all comments and documentation
                5. Use idiomatic patterns in the target language
                6. Handle language-specific features appropriately""",
                messages=[
                    {
                        "role": "user",
                        "content": f"Convert this {source_language} code to {target_language}:\n\n{source_code}",
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
