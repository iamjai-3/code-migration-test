import os
import json
import anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
import logging
from tqdm import tqdm

# Function to translate the code using the Anthropics API
# This function should translate the code without losing its context

def translate_code(migration_plan_text, target_language):
    api_key = os.getenv('ANTHROPIC_API_KEY')  # Get API key from environment variable
    client = anthropic.Anthropic(api_key=api_key)
    
    # Parse the migration plan text into a structured format
    migration_plan = json.loads(migration_plan_text)
    
    context = ''
    for file_info in tqdm(migration_plan['structure']['files'], desc='Translating files'):
        file_path = file_info['file_path']
        # Read the content of the file to be translated
        with open(file_path, 'r') as input_file:
            code_content = input_file.read()
        
        # Prepare the payload for the API request
        response = client.messages.create(
            model='claude-3-5-sonnet-20241022',
            max_tokens=8000,
            messages=[{
                'role': 'user',
                'content': f'{context}\nTranslate the following PHP code to {target_language} code:\n\n{code_content}',
            }]
        )
        translated_code = response.content[0].text
        context += translated_code + '\n'
        
        # Write the translated code to the output file
        output_file_path = os.path.join(migration_plan['structure']['root'], file_path)
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, 'w') as output_file:
            output_file.write(translated_code)
        logging.info(f'Translated {file_path}')
