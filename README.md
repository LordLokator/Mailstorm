# Text-based LLM Task Scaffold

This repository contains the initial scaffold for a text-based LLM project, prepared as part of a one-week interview assignment. The focus is on setting up a clean, reproducible development environment and a modular project structure for rapid prototyping and experimentation.

---

## Project Structure

```
.
├── Blueprint.md
├── config.py
├── control.py
├── data
│   └── content.zip
├── data_transformers
│   ├── date_handling.py
│   ├── email_handling.py
│   ├── __init__.py
│   ├── role_handling.py
│   └── sanitize_pipeline.py
├── helpers.py
├── json_handler.py
├── logs
├── main.py
├── outputs
│   └── summary.json
├── prompts.py
├── README.md
├── resources.md
├── setup.sh
└── tests
    └── test_helpers.py
```

---


## Setup

To initialize the project environment:

```bash
chmod +x setup.sh
./setup.sh
```

This will:

Create or reuse a local .venv virtual environment

Install dependencies from requirements.txt

Create a secure artifacts/logs directory for logging

---

## Running the Project

After setup:

```bash
source .venv/bin/activate
python main.py
```

---

## Notes

### Choice of logger

I've been using loguru for over a year, and I prefer its simplicity and usability over other loggers.