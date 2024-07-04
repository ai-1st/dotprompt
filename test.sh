#!/bin/bash

# This file was produced by https://github.com/ai-1st/dotprompt and shouldn't be edited directly.

# Test case 1: Basic usage
echo "Test case 1: Basic usage"
python3.12 -m dotprompt_cli.gen test/README.md.prompt

# Test case 2: Recursive processing
echo "Test case 2: Recursive processing"
python3.12 -m dotprompt_cli.gen test/README.md.prompt --recursive

# Test case 3: Generate from scratch
echo "Test case 3: Generate from scratch"
python3.12 -m dotprompt_cli.gen test/README.md.prompt --from-scratch

# Test case 4: Using a different provider
echo "Test case 4: Using a different provider"
python3.12 -m dotprompt_cli.gen test/README.md.prompt --provider anthropic

# Test case 5: Using a different model
echo "Test case 5: Using a different model"
python3.12 -m dotprompt_cli.gen test/README.md.prompt --model anthropic.claude-3-sonnet-20240229-v1:0

# Test case 6: Combining options
echo "Test case 6: Combining options"
python3.12 -m dotprompt_cli.gen test/README.md.prompt --recursive --from-scratch --provider bedrock --model anthropic.claude-3-5-sonnet-20240620-v1:0

# Test case 7: Invalid file (no .prompt extension)
echo "Test case 7: Invalid file (no .prompt extension)"
python3.12 -m dotprompt_cli.gen test/invalid_file.txt

# Test case 8: Non-existent file
echo "Test case 8: Non-existent file"
python3.12 -m dotprompt_cli.gen test/non_existent_file.prompt

echo "All test cases completed."