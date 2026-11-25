# AI Platform Gateway: Pydantic and Request Validation

**Learning level:** Beginner (designed for a 15-year-old)

This project is a small AI gateway built with FastAPI. It receives API requests, checks that the data is safe and correct, and sends back structured responses.

An AI gateway is like a security desk and control room between a user and several AI companies:

```text
User or app
    |
    |  HTTP request with JSON
    v
FastAPI gateway
    |
    |  Pydantic validates the JSON
    v
AI request service
    |
    |  Finds model and checks provider
    v
Structured JSON response
```

Today, the gateway does not contact a real AI model. It simulates the response so we can safely practice backend validation.

## What this lesson teaches

- What Pydantic is and why FastAPI uses it
- How to require fields and set default values
- How to limit numbers and text lengths
- How to create optional fields
- How to write custom validation rules
- How to validate nested JSON
- How to use response models
- How to test an API in Swagger UI
- What 400 and 422 HTTP status codes mean

---

## Quick start

### 1. Open the project

From this folder, activate the existing virtual environment:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

The main dependencies are:

- **FastAPI** - creates the web API
- **Pydantic** - validates Python objects and JSON data
- **Uvicorn** - runs the web server

### 3. Start the API

```powershell
fastapi dev main.py
```

Then open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- Application home: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`

Stop the server with **Ctrl+C**.

---

## Project files

```text
AIPlatformGateway_03/
├── main.py                 # Creates the FastAPI application
├── api/
│   └── endpoints.py        # API routes and HTTP responses
├── config/
│   └── models_config.py    # Available models and providers
├── schemas/
│   └── request_schema.py   # Pydantic input and output models
├── services/
│   └── model_service.py    # Request processing and validation logic
├── requirements.txt        # Python dependencies
└── README.md               # This guide
```

### main.py

This creates the application, adds routes, and defines the title, description, and version.

### api/endpoints.py

This receives HTTP requests and decides what response to return.

### schemas/request_schema.py

This describes the shape and rules for incoming and outgoing data.

### services/model_service.py

This contains the main business logic, such as finding a model and checking its provider.

### config/models_config.py

This stores the models available in the current lesson.

---

## Understanding Pydantic

Pydantic validates data using Python type annotations.

```python
from pydantic import BaseModel

class AIRequest(BaseModel):
    model: str
    prompt: str
    max_tokens: int
```

This means:

- `model` must be text
- `prompt` must be text
- `max_tokens` must be an integer

Pydantic is useful because it performs repetitive validation automatically. FastAPI combines Pydantic with HTTP route definitions to create a well-documented API.

### BaseModel

`BaseModel` is the base for creating a Pydantic data model.

```python
class AIRequest(BaseModel):
    model: str
```

### Field

`Field` adds rules and extra information to a field.

```python
prompt: str = Field(
    ...,
    min_length=5,
    max_length=10000,
    description="Prompt submitted by the user"
)
```

- `...` means the field is required
- `min_length=5` requires at least 5 characters
- `max_length=10000` allows at most 10,000 characters

### Default values

```python
max_tokens: int = 500
```

If the request omits `max_tokens`, Pydantic uses `500`.

### Number ranges

```python
temperature: float = Field(
    default=0.7,
    ge=0.0,
    le=2.0
)
```

- `ge` means greater than or equal to
- `le` means less than or equal to
- Temperature must therefore be from `0.0` through `2.0`

Temperature controls output variation. A lower value usually gives more predictable text; a higher value allows more variation.

### Optional fields

```python
provider: str | None = None
```

This field may contain text or `None`. Because it has a default, it can also be omitted.

### Literal values

```python
provider: Literal["OpenAI", "Anthropic", "Google"] | None = None
```

`Literal` means the value must be one of the named choices.

---

## Custom validation

A custom validator lets us add a rule that Pydantic cannot express with an ordinary type alone.

```python
@field_validator("prompt")
@classmethod
def validate_prompt(cls, value):
    cleaned_value = value.strip()

    if not cleaned_value:
        raise ValueError("Prompt cannot contain only spaces")

    return cleaned_value
```

The `.strip()` method removes spaces at the beginning and end of the text.

For example, this prompt is invalid:

```json
{
  "model": "gpt-4o",
  "prompt": "     "
}
```

The validator cleans the value and rejects it when nothing remains.

---

## Request and response models

### AIRequest

`AIRequest` describes the JSON accepted by `POST /requests`.

| Field | Example | Rules |
|---|---|---|
| `model` | `"gpt-4o"` | Required text, 3-100 characters |
| `prompt` | `"Explain AI engineering"` | Required text, 5-10,000 characters |
| `max_tokens` | `500` | Integer from 1 to 4000 |
| `temperature` | `0.7` | Number from 0.0 to 2.0 |
| `provider` | `"OpenAI"` | Optional: OpenAI, Anthropic, or Google |
| `stream` | `false` | Boolean; defaults to `false` |

### AIResponse

`AIResponse` describes what `POST /requests` returns:

- A unique request ID
- The model name
- A success status
- Estimated input tokens
- Estimated output tokens
- Total estimated tokens
- A result message
- The model provider

### response_model

FastAPI can convert the Python result into safe, predictable JSON:

```python
@router.post("/requests", response_model=AIResponse)
def create_ai_request(request: AIRequest):
    ...
```

`response_model=AIResponse` means the API will use `AIResponse` as the public output format.

---

## Nested JSON

Complex APIs often group related settings.

```json
{
  "model": "gpt-4o",
  "prompt": "Explain AI Platform Engineering",
  "generation": {
    "max_tokens": 1000,
    "temperature": 0.5
  },
  "metadata": {
    "user_id": "user_101",
    "application": "AI Gateway"
  }
}
```

A nested Pydantic model checks the generation object:

```python
class GenerationConfig(BaseModel):
    max_tokens: int = Field(default=500, ge=1, le=4000)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class AdvancedAIRequest(BaseModel):
    model: str
    prompt: str
    generation: GenerationConfig
    metadata: dict[str, str] = Field(default_factory=dict)
```

`GenerationConfig` is reused inside `AdvancedAIRequest`. `metadata: dict[str, str]` means each key and value must be text.

`default_factory=dict` creates a separate empty dictionary when metadata is omitted. This prevents multiple objects from accidentally sharing mutable default data.

---

## Provider and model validation

The gateway knows these example models:

| Model | Provider |
|---|---|
| `gpt-4o` | OpenAI |
| `claude-3-5-sonnet` | Anthropic |
| `gemini-2.0-flash` | Google |

The service first checks whether the model exists. It then compares the requested provider with the provider in the model configuration.

```json
{
  "model": "gpt-4o",
  "provider": "Google",
  "prompt": "Explain AI engineering"
}
```

This is rejected because `gpt-4o` belongs to OpenAI, not Google.

---

## API endpoints

| Method | URL | Purpose |
|---|---|---|
| GET | `/` | Show a welcome message |
| GET | `/health` | Confirm the service is healthy |
| GET | `/models` | List all available models |
| GET | `/models/{model_id}` | Get one model |
| POST | `/requests` | Validate and simulate an AI request |
| POST | `/requests/validate` | Check a prompt and count its characters |

### HTTP status codes

| Code | Name | Meaning here |
|---:|---|---|
| 200 | OK | The request worked |
| 400 | Bad Request | The request is understood but conflicts with application rules |
| 404 | Not Found | The requested model does not exist |
| 422 | Unprocessable Entity | Pydantic validation rejected the request data |

---

## Test in Swagger

Open `http://127.0.0.1:8000/docs`, select an endpoint, choose **Try it out**, enter JSON, and select **Execute**.

### Test 1: valid request

```json
{
  "model": "gpt-4o",
  "prompt": "Explain AI Platform Engineering",
  "max_tokens": 500,
  "temperature": 0.7,
  "provider": "OpenAI",
  "stream": false
}
```

Expected: `200 OK`, with a response containing `request_id`, token counts, and `provider`.

The token counts are only simulations. The gateway estimates input tokens by splitting the prompt into words. It does not use a real tokenizer or call an AI model.

### Test 2: invalid temperature

```json
{
  "model": "gpt-4o",
  "prompt": "Explain AI Platform Engineering",
  "temperature": 5
}
```

Expected: `422 Unprocessable Entity`, because temperature must be from `0.0` to `2.0`.

### Test 3: provider mismatch

```json
{
  "model": "gpt-4o",
  "prompt": "Explain AI Platform Engineering",
  "provider": "Google"
}
```

Expected: `400 Bad Request`.

### Test 4: empty prompt

```json
{
  "model": "gpt-4o",
  "prompt": "     "
}
```

Expected: `422 Unprocessable Entity`.

### Test 5: prompt validation

Request to `POST /requests/validate`:

```json
{
  "prompt": "Explain AI Platform Engineering"
}
```

Example response:

```json
{
  "valid": true,
  "prompt_length": 32,
  "message": "Prompt validation successful"
}
```

---

## Important terms

| Term | Simple meaning |
|---|---|
| Schema | A description of expected data |
| Validation | Checking whether data follows the rules |
| BaseModel | Pydantic's base class for data models |
| Field | Adds rules or metadata to a field |
| Custom validator | An application-specific validation rule |
| Optional field | A field that may be omitted or use `None` |
| Nested model | A Pydantic model used inside another model |
| Response model | Defines the shape and type of API output |
| Serialization | Converts Python objects into JSON |
| Deserialization | Converts JSON into Python objects |
| Type annotation | A label saying what type a value should have |

---

## Practice assignments

Try these changes yourself.

### 1. Add top_p

Add this field to `AIRequest`:

```python
top_p: float = Field(
    default=1.0,
    ge=0.0,
    le=1.0
)
```

Test that `top_p: 1.5` is rejected.

### 2. Strengthen prompt validation

The prompt validator already strips whitespace and rejects an all-space prompt. Try adding it to `PromptValidationRequest` too, so every prompt entry uses the same rule.

### 3. Filter models by provider

Create:

```text
GET /models/provider/{provider_name}
```

It should return only models whose `provider` value matches `provider_name`.

Use `AVAILABLE_MODELS` and filter its values, for example:

```python
[model for model in AVAILABLE_MODELS.values()
 if model["provider"] == provider_name]
```

Choose the expected behavior for an unknown provider and test it.

---

## Interview questions

### 1. What is Pydantic?

Pydantic validates and structures Python data using type annotations.

### 2. Why does FastAPI use Pydantic?

FastAPI uses Pydantic to validate request bodies, generate API documentation, and shape responses.

### 3. What is the difference between `BaseModel` and `Field`?

`BaseModel` creates a data model. `Field` adds constraints and configuration to an individual field.

### 4. What is a custom field validator?

It is a function that checks or transforms a field according to a custom application rule.

### 5. What is a nested Pydantic model?

It is a model used as a field inside another model.

### 6. What is the difference between 400 and 422?

`400` means a validly structured request conflicts with application logic. `422` means Pydantic found invalid request data.

### 7. What does `response_model` do?

It tells FastAPI which Pydantic model defines the public response structure.

### 8. What is the difference between `str | None = None` and `str`?

`str | None = None` allows text or no value. `str` is required and must be text.

---

## Completion checklist

- [ ] I understand `BaseModel`
- [ ] I understand required fields and default values
- [ ] I understand optional fields
- [ ] I can use `Field` constraints
- [ ] I can explain `ge` and `le`
- [ ] I understand custom field validators
- [ ] I understand nested Pydantic models
- [ ] I know the difference between 400 and 422
- [ ] I tested a valid request in Swagger
- [ ] I tested invalid temperature
- [ ] I tested a provider mismatch
- [ ] I tested an empty prompt
- [ ] I tested `POST /requests/validate`
- [ ] I answered the interview questions
- [ ] I completed the practice assignments

## What comes next

Day 12 adds a real database. SQL and SQLAlchemy will let the gateway save AI requests and retrieve request history instead of keeping information only in memory.
