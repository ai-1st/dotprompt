# This file was produced by AI from a prompt and shouldn't be edited directly.

import os
import click
from .models import llm_invoke

def process_include_directives(file_content, file_path, recursive=False, processed_files=None):
    if processed_files is None:
        processed_files = set()

    lines = file_content.split('\n')
    result = []
    
    for line in lines:
        if line.strip().startswith('@include('):
            include_file = line.strip()[9:-1]
            include_path = os.path.join(os.path.dirname(file_path), include_file)
            
            if include_path in processed_files:
                print(f"Warning: Circular dependency detected for {include_path}")
                continue
            
            processed_files.add(include_path)
            
            if recursive and os.path.exists(include_path + '.prompt'):
                print(f"Regenerating {include_path} from prompt")
                process_file(include_path + '.prompt', recursive=True, processed_files=processed_files)
            
            if os.path.exists(include_path):
                print(f"Including {include_path}")
                with open(include_path, 'r') as f:
                    included_content = f.read()
                included_content = process_include_directives(included_content, include_path, recursive, processed_files)
                result.extend(included_content.split('\n'))
            else:
                print(f"Warning: Included file {include_path} not found")
        else:
            result.append(line)
    
    return '\n'.join(result)

def generate_code(prompt, existing_content, provider, model):
    system_message = """
    Make only the necessary changes to the existing file:
    <existing_file>{}</existing_file>
    Important! Output just the naked file content, without any 
    introductory text or enclosing the code in triple quotes. 
    Include a comment in the code saying that this file was produced by https://github.com/ai-1st/dotprompt 
    and shouldn't be edited directly.
    """.format(existing_content)

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Hello world in python"},
        {"role": "assistant", "content": "print('Hello world')"},
        {"role": "user", "content": prompt}
    ]

    return llm_invoke(provider=provider, model=model, messages=messages)

def process_file(input_file, recursive=False, from_scratch=False, provider='bedrock', model='anthropic.claude-3-5-sonnet-20240620-v1:0', processed_files=None):
    if not input_file.endswith('.prompt'):
        print(f"Error: Input file {input_file} must have .prompt suffix")
        return

    output_file = input_file[:-7]  # Remove .prompt suffix
    print(f"Processing {input_file}")

    with open(input_file, 'r') as f:
        prompt_content = f.read()

    prompt_content = process_include_directives(prompt_content, input_file, recursive, processed_files)

    existing_content = ''
    if not from_scratch and os.path.exists(output_file):
        with open(output_file, 'r') as f:
            existing_content = f.read()

    generated_code = generate_code(prompt_content, existing_content, provider, model)

    with open(output_file, 'w') as f:
        f.write(generated_code)

    print(f"Generated {output_file}")

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--recursive', is_flag=True, help='Recursively process included files')
@click.option('--from-scratch', is_flag=True, help='Generate code from scratch, ignoring existing output file')
@click.option('--provider', default='bedrock', help='LLM provider (bedrock or anthropic)')
@click.option('--model', default='anthropic.claude-3-5-sonnet-20240620-v1:0', help='LLM model')
def main(input_file, recursive, from_scratch, provider, model):
    """
    CLI application to process prompt files and generate code.

    This application takes a prompt file stored in the local filesystem and produces a raw code file,
    stored along with the prompt. The prompt files have a ".prompt" suffix.

    Usage:
    python script.py input_file.prompt [OPTIONS]

    Options:
    --recursive      Process included files recursively
    --from-scratch   Generate code from scratch, ignoring existing output file
    --provider       LLM provider (bedrock or anthropic)
    --model          LLM model to use
    """
    process_file(input_file, recursive, from_scratch, provider, model)

if __name__ == '__main__':
    main()