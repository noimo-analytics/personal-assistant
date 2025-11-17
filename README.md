# Personal Assistant

An intelligent personal assistant powered by LangGraph and OpenAI, equipped with integrated tooling for web browsing, code execution, file management, and more. Features a self-evaluating workflow that ensures tasks are completed according to your success criteria.

## Key Features

- **Autonomous Task Completion**: Uses a worker-evaluator pattern to iteratively work on tasks until success criteria are met
- **Integrated Tooling**: Access to multiple tools for comprehensive task execution
- **Interactive Web UI**: Clean Gradio interface for easy interaction
- **Self-Evaluation**: Built-in evaluator that provides feedback and determines when tasks are complete

## Main Use Cases

The integrated tooling enables the assistant to handle complex, multi-step tasks autonomously:

### 1. **Web Research & Information Gathering**
   - Browse websites and extract information
   - Search the web using Google Serper API
   - Query Wikipedia for factual information
   - Navigate complex web applications

### 2. **Code Execution & Data Processing**
   - Run Python code in a REPL environment
   - Process data, perform calculations, and generate visualizations
   - Automate data analysis workflows

### 3. **File Management**
   - Create, read, write, and organize files in the `outputs/` directory
   - Generate reports, documents, and structured data files

### 4. **Notification & Communication**
   - Send push notifications via Pushover
   - Alert users when tasks are complete or require attention

### 5. **Google Calendar Manafer**
   - Add events to Google Calendar
   - List events from Google Calendar


### 6. **Complex Multi-Step Workflows**
   The assistant excels at combining these capabilities:
   - Research a topic online, compile findings into a document, and notify you
   - Scrape web data, process it with Python, and save results
   - Navigate web forms, extract information, and generate reports
   - Solve programming problems by researching, coding, testing, and documenting

## Setup Guide

### Prerequisites

- Python 3.12 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip
- API keys for required services (see Environment Variables)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/noimo-analytics/personal-assistant.git
   cd personal-assistant
   ```

2. **Install dependencies**

   Using uv (recommended):
   ```bash
   uv sync
   ```

3. **Install Playwright browsers**
   ```bash
   playwright install chromium
   ```

4. **Set up environment variables**

   Create a `.env` file in the `app_folder` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   PUSHOVER_TOKEN=your_pushover_token_here  
   PUSHOVER_USER=your_pushover_user_here    
   SERPER_API_KEY=your_serper_api_key_here  
   
   # LangSmith for observability and tracing
   # Enable tracing to monitor and debug your assistant's workflow
   LANGCHAIN_TRACING_V2=true
   LANGSMITH_ENDPOINT=https://eu.api.smith.langchain.com
   LANGCHAIN_API_KEY=your_langsmith_api_key_here
   LANGCHAIN_PROJECT=your_langchain_project_here
   # Google Calendar
   GOOGLE_TOKEN_PATH=token.json
   GOOGLE_CALENDAR_ID=primary
   # Timezone for RFC3339 formatting
   TIMEZONE_OFFSET=+05:30
   ```
5. **Configure Coolge Calendar**
   - **Enable the Calendar API** in Google Cloud Console.
   - Download your OAuth **client_secrets** file and save as `credentials.json` in the root.
   - Run `config.py` script to authorize and generate `token.json`

6. **Run the application**
   ```bash
   cd app_folder
   uv run app.py
   ```

   The application will launch in your default browser automatically.

## Usage

1. **Enter your request** in the message textbox (e.g., "Research the latest trends in AI and create a summary document")

2. **Define success criteria** (optional) to guide the assistant's evaluation:
   - Default: "The answer should be clear and accurate"
   - Example: "Provide a 500-word summary with at least 3 cited sources"

3. **Click "Go!"** or press Enter to submit

4. **Monitor progress**: The assistant will:
   - Work through the task using available tools
   - Self-evaluate against your success criteria
   - Iterate if the criteria aren't met
   - Ask for clarification if needed

5. **Reset** to start a new conversation at any time

## Architecture

The assistant uses a **LangGraph** workflow with three main components:

- **Worker Node**: Executes tasks using available tools
- **Tool Node**: Executes tool calls (web browsing, code execution, etc.)
- **Evaluator Node**: Assesses whether success criteria are met and provides feedback

The graph automatically routes between these nodes until the task is complete or user input is required.

## Project Structure

```
personal-assistant/
├── app_folder/
│   ├── app.py              # Gradio UI and main application entry point
│   ├── assistant.py        # Core Assistant class with LangGraph workflow
│   ├── assistant_tools.py  # Tool definitions (Playwright, Python REPL, etc.)
│   ├── outputs/            # Directory for generated files
│   ├── .env                # Environment variables
│   ├── token.json          # OAuth tokens (auto-generated)
├── config.py               # Generate token for Google Calendar intergration   
├── credentials.json        # OAuth client secrets
├── pyproject.toml          # Project dependencies and configuration
└── README.md               # This file
```

## Technologies

- **LangGraph**: Agent orchestration and workflow management
- **LangChain**: Tool integration and LLM interaction
- **LangSmith**: Observability and tracing platform (for debugging and monitoring)
- **OpenAI GPT-4o-mini**: Language model for reasoning and tool use
- **Gradio**: Web UI framework
- **Playwright**: Web browsing and automation
- **Python**: Runtime environment for code execution

## License

See LICENSE file for details.
