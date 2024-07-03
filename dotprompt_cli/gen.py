# This file was produced by AI from a prompt and shouldn't be edited directly.

import click
import os
import re
import sys
from typing import List, Dict
from .models import llm_invoke

def process_directives(content: str, file_path: str, skip_directives: bool, dependencies: bool, processed_files: Dict[str, str]) -> str:
    if skip_directives:
        return content

    def replace_directive(match):
        directive, path = match.groups()
        full_path = os.path.normpath(os.path.join(os.path.dirname(file_path), path))
        
        if directive == 'raw':
            if dependencies and os.path.exists(full_path + '.prompt'):
                process_file(full_path + '.prompt', skip_directives, dependencies, processed_files)
            with open(full_path, 'r') as f:
                return f.read()
        elif directive == 'prompt':
            return process_file(full_path, skip_directives, dependencies, processed_files)

    pattern = r'@(raw|prompt)\((.*?)\)'
    return re.sub(pattern, replace_directive, content)

def process_file(file_path: str, skip_directives: bool, dependencies: bool, processed_files: Dict[str, str]) -> str:
    if file_path in processed_files:
        if processed_files[file_path] is None:
            raise click.ClickException(f"Circular dependency detected: {file_path}")
        return processed_files[file_path]

    processed_files[file_path] = None  # Mark as being processed
    click.echo(f"Processing file: {file_path}")

    with open(file_path, 'r') as f:
        content = f.read()

    processed_content = process_directives(content, file_path, skip_directives, dependencies, processed_files)
    processed_files[file_path] = processed_content
    return processed_content

def generate_code(prompt: str, provider: str, model: str) -> str:
    system_message = "Output just the file content, nothing else. Do not print any introductory text before the code. Do not enclose the code in triple quotes. Include a comment in the code saying that this file was produced by AI from a prompt and shouldn't be edited directly, unless generating json or other file formats that don't support comments."
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": "Hello world in python"},
        {"role": "assistant", "content": "print('Hello world')"},
        {"role": "user", "content": prompt}
    ]
    return llm_invoke(provider, model, messages)

def process_folder(folder_path: str, skip_directives: bool, dependencies: bool, provider: str, model: str) -> None:
    processed_files = {}
    for root, dirs, files in os.walk(folder_path):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file.endswith('.prompt'):
                file_path = os.path.join(root, file)
                try:
                    prompt = process_file(file_path, skip_directives, dependencies, processed_files)
                    code = generate_code(prompt, provider, model)
                    output_file = file_path[:-7]  # Remove '.prompt' suffix
                    with open(output_file, 'w') as f:
                        f.write(code)
                    click.echo(f"Generated code saved to: {output_file}")
                except click.ClickException as e:
                    click.echo(f"Error processing {file_path}: {str(e)}", err=True)

@click.command()
@click.argument('input_path')
@click.option('--skip-directives', is_flag=True, help='Skip processing of @raw and @prompt directives')
@click.option('--dependencies', is_flag=True, help='Process dependencies for @raw directives')
@click.option('--recursive', is_flag=True, help='Process folder recursively')
@click.option('--provider', default='bedrock', type=click.Choice(['bedrock', 'anthropic']), help='LLM provider')
@click.option('--model', default='anthropic.claude-3-5-sonnet-20240620-v1:0', help='LLM model')
def main(input_path: str, skip_directives: bool, dependencies: bool, recursive: bool, provider: str, model: str) -> None:
    if recursive:
        if not os.path.isdir(input_path):
            raise click.ClickException("Input path must be a directory when using --recursive option")
        process_folder(input_path, skip_directives, dependencies, provider, model)
    else:
        if not input_path.endswith('.prompt'):
            raise click.ClickException("Input file must have .prompt extension")
        processed_files = {}
        prompt = process_file(input_path, skip_directives, dependencies, processed_files)
        code = generate_code(prompt, provider, model)
        output_file = input_path[:-7]  # Remove '.prompt' suffix
        with open(output_file, 'w') as f:
            f.write(code)
        click.echo(f"Generated code saved to: {output_file}")

if __name__ == '__main__':
    main()