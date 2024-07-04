# DotPrompt

DotPrompt is an innovative project that explores a radical approach to programming where code is 100% produced by AI, and humans only edit the prompts used to generate the code.

## Table of Contents

- [Introduction](#introduction)
- [Key Concepts](#key-concepts)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [To-Do List](#to-do-list)
- [License](#license)
- [Contact](#contact)

## Introduction

In traditional programming, code is built through a series of iterations, where each iteration is done by a human or by AI. The resulting code doesn't reveal which prompts were used to build it, making it challenging to alter these prompts later. It's similar to having a compiled binary without the source code and continuing to work on the compiled binary.

DotPrompt introduces a novel concept: what if the code is entirely produced by AI, and humans only edit the prompts used by AI?

## Key Concepts

1. **`.prompt` files**: These files contain the prompts used to produce actual code files.
2. **Builder script**: A simple script that executes the `.prompt` files to generate the code.
3. **Self-generation**: The builder script itself can be generated from a `.prompt` file, allowing the generator to generate itself.
4. **Multi-level abstraction**: `.prompt` files can be built from other `.prompt` files, enabling higher-level ideas to be expressed in `program.prompt.prompt` files.
5. **Reverse engineering**: The possibility to derive prompt files from existing source code.

## Features

- Generate code files from `.prompt` files
- Support for recursive processing of directories
- Ability to skip directive processing
- Option to process dependencies for `@raw` directives
- Customizable LLM provider and model selection

## Installation

To install DotPrompt, use the following command:

```
pip3 install dotprompt-cli
```

## Usage

The DotPrompt CLI supports the following options:

```
Usage: dotprompt [OPTIONS] INPUT_PATH

Options:
  --skip-directives        Skip processing of @raw and @prompt directives
  --dependencies           Process dependencies for @raw directives
  --recursive              Process folder recursively
  --provider [bedrock|anthropic]
                           LLM provider (default: bedrock)
  --model TEXT             LLM model (default: anthropic.claude-3-5-sonnet-20240620-v1:0)
  --help                   Show this message and exit
```

### Arguments:

- `INPUT_PATH`: Path to the input `.prompt` file or directory (when using `--recursive`)

### Options:

- `--skip-directives`: If set, skips processing of `@raw` and `@prompt` directives in the input files.
- `--dependencies`: If set, processes dependencies for `@raw` directives.
- `--recursive`: If set, processes the input folder recursively. The input path must be a directory when using this option.
- `--provider`: Specifies the LLM provider. Can be either `bedrock` or `anthropic`. Default is `bedrock`.
- `--model`: Specifies the LLM model to use. Default is `anthropic.claude-3-5-sonnet-20240620-v1:0`.

### Examples:

1. Process a single `.prompt` file:
   ```
   dotprompt path/to/file.prompt
   ```

2. Process a directory recursively:
   ```
   dotprompt --recursive path/to/directory
   ```

3. Use a specific provider and model:
   ```
   dotprompt --provider anthropic --model claude-2 path/to/file.prompt
   ```

4. Skip directive processing:
   ```
   dotprompt --skip-directives path/to/file.prompt
   ```

5. Process dependencies for `@raw` directives:
   ```
   dotprompt --dependencies path/to/file.prompt
   ```

## To-Do List

- Implement the ability to produce several files from one prompt, which could be especially useful when generating both code and unit tests.
- Add functionality to run unit tests and check if the generated code runs correctly. If not, make necessary changes based on the exception/error messages.

## License

This project is licensed under the MIT License.

## Contact

For more information or to get in touch with the author, Dmitry Degtyarev, please visit [https://twitter.com/Mitek99](https://twitter.com/Mitek99).