import os
import json
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
import logging
from tqdm import tqdm

# Function to analyze the input project
# This function should use the Anthropics API to understand the project structure and logic

def analyze_project(project_path):
    api_key = os.getenv('ANTHROPIC_API_KEY')  # Get API key from environment variable
    client = anthropic.Anthropic(api_key=api_key)
    
    project_analysis = {
        'files': [],
        'dependencies': [],
        'structure': {}
    }
    
    # Iterate through project files and analyze them
    context = ''
    for root, dirs, files in os.walk(project_path):
        for file in tqdm(files, desc='Analyzing files'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as input_file:
                code_content = input_file.read()
            
            # Prepare the payload for the API request
            response = client.messages.create(
                model='claude-3-5-sonnet-20241022',
                max_tokens=5000,
                messages=[{
                    'role': 'user',
                    'content': f'{context}\nAnalyze the following PHP code and provide a summary:\n\n{code_content}',
                }]
            )
            analysis = response.content[0].text
            context += analysis + '\n'
            
            # Store the analysis result
            project_analysis['files'].append({
                'file_path': file_path,
                'analysis': analysis
            })
            logging.info(f'Analyzed {file_path}')
            
            # Store the file structure
            relative_path = os.path.relpath(file_path, project_path)
            project_analysis['structure'][relative_path] = ''
            
    return project_analysis
