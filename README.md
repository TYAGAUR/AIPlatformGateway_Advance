# AI Platform Gateway

## What is this project?

This is a small practice project for learning how a web API works. Think of an API as a
restaurant:

- A client (like a website) places an order by sending a request.
- The API is the counter that receives the order.
- The service checks the order and prepares a response.
- The client gets the response back as JSON.

This project can show a list of example AI models and accept a pretend AI request.
**It does not connect to OpenAI, Anthropic, or Google, and it does not generate a real
AI answer.** It only simulates the request and estimates token counts.

## What you need

- Python installed on your computer
- PowerShell (the terminal included with Windows)

## Set up and run it

Open PowerShell in this project folder, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

The first command creates a project-only Python environment called `.venv`. The second
installs the packages listed in [requirements.txt](requirements.txt). The last command
starts the development server. Keep that terminal open while using the API; press
**Ctrl+C** there to stop it.

If `.venv` already exists, you can skip the first command. Using the Python executable
inside `.venv` keeps the packages and server command in the right environment, so
PowerShell does not have to find a separate `fastapi` command on your PATH.

Open the interactive API page at **http://127.0.0.1:8000/docs**. You can try the
endpoints there without writing another program.

## Try the endpoints

| Method | URL | What it does |
| --- | --- | --- |
| `GET` | `/` | Shows a welcome message. |
| `GET` | `/health` | Reports whether the app is running. |
| `GET` | `/models` | Lists all example models. |
| `GET` | `/models/gpt-4o` | Shows one model. Replace `gpt-4o` with another model ID to look it up. |
| `POST` | `/requests` | Sends a pretend AI request and receives a simulated result. |

For `POST /requests`, choose **Try it out** on the docs page and send this JSON:

```json
{
  "model": "gpt-4o",
  "prompt": "Explain AI",
  "max_tokens": 100
}
```

You should get a response shaped like this (the request ID will be different each time):

```json
{
  "request_id": "req_a1b2c3d4",
  "model": "gpt-4o",
  "status": "success",
  "input_tokens": 2,
  "output_tokens": 3,
  "total_tokens": 5,
  "message": "AI request processed successfully (simulation)"
}
```

The token numbers are simple estimates made by this project, not the real token counts
of an AI provider.

## How a request travels through the code

1. FastAPI receives the web request at a route in [api/endpoints.py](api/endpoints.py).
2. For `POST /requests`, Pydantic checks the incoming JSON against
   [schemas/request_schema.py](schemas/request_schema.py).
3. The route asks [services/model_service.py](services/model_service.py) to handle
   the request.
4. The service checks the model list in [config/models_config.py](config/models_config.py),
   estimates token counts, and builds a response.
5. FastAPI sends that response back as JSON.

Keeping routes, data rules, service logic, and configuration in separate files makes
the project easier to understand and change.

## Project map

```text
main.py                    Creates the FastAPI app and adds the routes
api/endpoints.py           Defines the URLs and what happens for each one
schemas/request_schema.py  Describes and validates request/response data
services/model_service.py  Contains the simulated request logic
config/models_config.py    Stores the example model list
requirements.txt           Lists the Python packages the project needs
```

## A few useful ideas

- **GET** usually asks to read information, like the model list.
- **POST** usually sends information to be processed, like a prompt.
- **JSON** is a text format for sending organized data, using keys and values.
- A **route** is a method and URL that the API knows how to handle.
- A **schema** is a set of rules for what data is allowed.
- A **virtual environment** keeps this project's Python packages separate from other
  projects on your computer.

The request schema requires a model and a non-empty prompt. `max_tokens` defaults to
500 and must be between 1 and 4000. An unknown model returns **404 Not Found**; invalid
request data returns **422 Unprocessable Entity**.

## Beginner experiments

1. Open `/models` in the docs and find the model IDs.
2. Try `/models/not-a-real-model` and notice the 404 response.
3. Send an empty prompt or set `max_tokens` to `5000` and notice the validation error.
4. Add another example model in `config/models_config.py` and try looking it up.
5. Read the endpoint and service files to see how the request moves through the app.
