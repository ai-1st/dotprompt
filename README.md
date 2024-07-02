# DotPrompt

[AI-generated content notice: This README was produced by AI from a prompt and should not be edited directly.]

DotPrompt is a revolutionary approach to software development that explores the idea of generating code entirely through AI-driven prompts. This project, authored by Dmitry Degtyarev, aims to change the way we think about coding and version control.

## Table of Contents

- [Introduction](#introduction)
- [Key Concepts](#key-concepts)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Build and Deploy](#build-and-deploy)
- [To-Do List](#to-do-list)
- [License](#license)
- [Contact](#contact)

## Introduction

In traditional programming, code is built through a series of iterations, either by humans or AI. The resulting code doesn't reveal which prompts were used to build it, making it challenging to alter these prompts later. It's comparable to having a compiled binary without access to the source code.

DotPrompt proposes a radical idea: what if the code is 100% produced by AI, and humans only edit the prompts used by AI?

## Key Concepts

1. **`.prompt` files**: These files contain the prompts used to produce actual code files.
2. **Builder script**: A simple script that executes the `.prompt` files to generate the code.
3. **Self-generation**: The builder script itself can be generated from a `.prompt` file, allowing the generator to create itself.
4. **Multi-level abstraction**: `.prompt` files can be built from other `.prompt` files, enabling higher-level idea representation.
5. **Reverse engineering**: The potential to derive prompt files from existing source code.

## Features

- Generate code entirely from AI prompts
- Maintain a clear history of prompts used to create each file
- Enable easy modification of code by altering prompts
- Support for multi-level abstraction in prompt creation
- Potential for reverse engineering prompts from source code

## Installation

[Instructions for installing DotPrompt will be added here]

## Usage

[Instructions for using DotPrompt will be added here]

## Build and Deploy

To build and deploy DotPrompt to PyPI, follow these steps:

1. Ensure you have the `build` module installed:

```
pip install build
```

2. Navigate to the project root directory.

3. Build the project:

```
python -m build
```

This will create a `dist` directory with the built distributions.

4. Install `twine` if you haven't already:

```
pip install twine
```

5. Upload the distribution to PyPI:

```
twine upload dist/*
```

You will be prompted for your PyPI username and password.

## To-Do List

- Implement a templating engine for `.prompt` files to allow inclusion of other prompts and/or source files
- Add dependency graph analysis to the builder script for efficient prompt execution
- Develop the ability to produce multiple files from a single prompt (e.g., source code and unit tests)
- Implement functionality to run unit tests and make necessary changes based on error messages

## License

This project is licensed under the MIT License.

## Contact

For inquiries or suggestions, you can reach out to the author, Dmitry Degtyarev, via Twitter: [@Mitek99](https://twitter.com/Mitek99)