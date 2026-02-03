# Locator Healer Agent

A FastAPI-based service that extracts locators from UI element lists using Google Gemini 2.5 Pro.

## Features

- FastAPI REST API for locator extraction
- Integration with Google Gemini 2.5 Pro
- Configurable LLM parameters via environment variables
- Request/response validation using Pydantic
- Health check endpoint

## Project Structure

```
.
├── main.py           # FastAPI application and endpoints
├── config.py         # Configuration and environment variables
├── utils/
│   └── llm.py       # Gemini API integration
├── requirements.txt  # Python dependencies
├── .env.example     # Example environment variables
└── README.md        # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the project root by copying `.env.example`:

```bash
cp .env.example .env
```

Then update `.env` with your actual Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.5-pro
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=1024
LLM_TOP_P=0.9
LLM_TOP_K=40
DEBUG=True
```

### 3. Run the Application

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Documentation

Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

### Health Check
- **GET** `/health`
  - Returns the health status of the service

### Extract Locator
- **POST** `/extract-locator`
  
  **Request Body:**
  ```json
  {
    "element_list": {
      "element1": {
        "type": "button",
        "text": "Login",
        "xpath": "//button[text()='Login']",
        "css": "button.login-btn"
      }
    },
    "logical_name": "LoginButton"
  }
  ```

  **Response:**
  ```json
  {
    "logical_name": "LoginButton",
    "locator": "//button[text()='Login']",
    "status": "success"
  }
  ```

## Configuration

LLM parameters can be configured via environment variables:

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `GEMINI_MODEL`: Model to use (default: `gemini-2.5-pro`)
- `LLM_TEMPERATURE`: Controls randomness (0.0-1.0, default: 0.7)
- `LLM_MAX_TOKENS`: Max tokens in response (default: 1024)
- `LLM_TOP_P`: Nucleus sampling parameter (default: 0.9)
- `LLM_TOP_K`: Top-k sampling parameter (default: 40)
- `DEBUG`: Enable debug mode (default: True)

## Example Usage

```python
import requests
import json

url = "http://localhost:8000/extract-locator"

payload = {
    "element_list": {
        "components": [
            {
                "id": "login_btn",
                "type": "button",
                "text": "Login",
                "xpath": "//button[@id='login_btn']"
            },
            {
                "id": "email_input",
                "type": "input",
                "placeholder": "Enter email",
                "xpath": "//input[@id='email_input']"
            }
        ]
    },
    "logical_name": "LoginButton"
}

response = requests.post(url, json=payload)
print(response.json())
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- google-generativeai
- python-dotenv
- pydantic

## License

MIT
