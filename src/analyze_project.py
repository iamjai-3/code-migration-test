import os
import anthropic
import logging
from tqdm import tqdm


def analyze_project(project_path, input_language):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key)

    project_analysis = {
        "files": [],
        "dependencies": [],
        "structure": {},
        "sourceLanguage": input_language,
    }

    # Iterate through project files and analyze them
    context = ""
    for root, dirs, files in os.walk(project_path):
        for file in tqdm(files, desc="Analyzing files"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8") as input_file:
                    code_content = input_file.read()
            except UnicodeDecodeError:
                logging.warning(f"Skipping binary file: {file_path}")
                continue

            # Prepare the payload for the API request
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=5000,
                system=f"""You are a code analysis expert specializing in {input_language}.
                Analyze the code and provide a detailed summary including:
                1. Main functionality and purpose
                2. Dependencies and imports used
                3. Key classes, functions, and their relationships
                4. External services or APIs used
                5. Data structures and patterns
                Be thorough but concise. Focus on elements that will be important for code migration.""",
                messages=[
                    {
                        "role": "user",
                        "content": f"{context}\nAnalyze the following {input_language} code:\n\n{code_content}",
                    }
                ],
            )
            analysis = response.content[0].text
            context += analysis + "\n"

            # Store the analysis result
            project_analysis["files"].append(
                {"file_path": file_path, "analysis": analysis}
            )
            logging.info(f"Analyzed {file_path}")

            # Store the file structure
            relative_path = os.path.relpath(file_path, project_path)
            project_analysis["structure"][relative_path] = ""

    return project_analysis
