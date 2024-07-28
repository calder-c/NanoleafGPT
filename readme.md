# NanoleafGPT

This project enables you to control Nanoleaf lights using ChatGPT. You can issue text prompts to control what is shown on your lights. This project uses Python built-in libraries, there is no requirements except both Nanoleaf and OpenAI keys. Please refer to the [Nanoleaf API Guide](#https://nanoleaf.me/en-GB/newsroom/blogs/4435/) for info on how to obtain your device's API key.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)


## Introduction

The Nanoleaf Control with ChatGPT project bridges the gap between smart lighting and advanced AI communication. By leveraging the capabilities of ChatGPT, users can interact with their Nanoleaf lights by prompting the AI to display colors and patterns.

## Installation

Follow these steps to set up the project and start controlling your Nanoleaf lights with ChatGPT:

### Prerequisites

- Python 3.7 or higher
- Nanoleaf API access token (use authhelper.py to obtain this)
- OpenAI API key for ChatGPT access

### Steps
    

1. **Set up environment variables**:
    
    **Linux/Mac**
    
    Open the terminal in the project directory, and run:
    ```plaintext
    export NANOLEAF_IP=<your light's IP>
    export NANOLEAF_KEY=<your nanoleaf key obtained with authhelper.py>
    export API_KEY=<your openai key>
    ```
    **Windows**
    
    Open Command Prompt in the project directory, and run:
    ```plaintext
    SET NANOLEAF_IP=<your light's IP>
    SET NANOLEAF_KEY=<your nanoleaf key obtained with authhelper.py>
    SET API_KEY=<your openai key>
    ```

2. **Run the application demo**:
    ```bash
    python3 nanoleaf.py
    ```

## Usage

Once the installation is complete, you can start using the application to control your Nanoleaf lights via ChatGPT. Here are some example prompts you can use:

- **A red to blue gradient**:
    ```plaintext
    A red to blue gradient, with red on top and blue on the bottom.
    ```

- **Change the color to green**:
    ```plaintext
    All green
    ```

- **A rainbow**:
    ```plaintext
    Make a full rainbow, red at the top, violet at the bottom
    ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


Thank you for using the NanoleafGPT project! Please credit the author of this project if you plan to use this in other projects.
