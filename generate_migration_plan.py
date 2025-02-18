import json
import os
import anthropic
import logging
import time

# Function to generate the migration plan using streaming API
# This function should create a file-folder structure tree and list dependencies for the target language


def generate_migration_plan(project_analysis, target_language, max_retries=3):
    api_key = os.getenv("ANTHROPIC_API_KEY")  # Get API key from environment variable
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare the payload for the API request
    context = ""
    for file_info in project_analysis["files"]:
        file_path = file_info["file_path"]
        analysis = file_info["analysis"]
        context += analysis + "\n"

    migration_plan_text = ""
    retries = 0
    while retries < max_retries:
        try:
            with client.messages.stream(
                max_tokens=8000,
                messages=[
                    {
                        "role": "user",
                        "content": f"{context}\nGenerate a migration plan for converting the above PHP project to a Node.js (Express) project. Include the file-folder structure and dependencies which will be directly converted into files. Ensure all code snippets are converted to Node.js (Express). The output should be a valid JSON with camelCase keys which will be parsed into python dictionary",
                    }
                ],
                model="claude-3-5-sonnet-20241022",
            ) as stream:
                for text in stream.text_stream:
                    migration_plan_text += text
            break  # Exit the loop if successful
        except Exception as e:
            logging.error(f"Error generating migration plan: {e}")
            retries += 1
            time.sleep(2**retries)  # Exponential backoff

    if retries == max_retries:
        raise Exception("Failed to generate migration plan after maximum retries")

    # Print the response content for debugging
    # print(f'Migration plan response: {migration_plan_text}')

    return migration_plan_text


# Function to parse the migration plan


def parse_migration_plan(migration_plan_text):
    print(migration_plan_text)
    # Extract JSON substring from the migration plan text and parse it
    start = migration_plan_text.find("{")
    end = migration_plan_text.rfind("}") + 1
    if start == -1 or end == 0:
        raise ValueError("No JSON object found in the migration plan text")
    json_str = migration_plan_text[start:end]
    return json.loads(json_str)


# Function to write the migration plan to files


def write_migration_plan_to_files(migration_plan, output_dir):
    for file_path, file_content in migration_plan.items():
        full_path = os.path.join(output_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as file:
            file.write(file_content)
