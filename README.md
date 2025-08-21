# Mailstorm: LLM powered QBR assistant tool

This project implements a proof-of-concept automated system that analyzes project emails to generate a Portfolio Health Report for Directors. It highlights unresolved tasks, risks, and inconsistencies requiring attention.

This PoC ingests a zip file with corporate e-mail conversations as .txt files, and outputs a json formatted "Portfolio Health Report".

The project uses llama3.1:8b for inference, which can be changed in config.py to any model available on [Ollama](https://ollama.com/library).


---

## Project Structure

```
.
├── Blueprint.md            # my main report
├── config.py               # LLM related objects, constants
├── control.py              # an Enum to make control more readable
├── data
│   └── content.zip
├── data_transformers           # Text transformation / cleaning
│   ├── date_handling.py        # Make dates more LLM ingestable
│   ├── email_handling.py       # remove email addresses (redundant data)
│   ├── __init__.py             # expose only sanitize_pipeline from this module
│   ├── role_handling.py        # add roles after names for more context information
│   └── sanitize_pipeline.py    # interface that accepts a .zip path and returns the cleaned mails
├── helpers.py              # basic file parsers
├── json_handler.py         # handles json report writing
├── logs                    # loguru logger saves here
├── main.py                 # entrypoint
├── outputs                 # output report is saved here as a .json file.
│   └── summary.json
├── prompts.py              # Holds objects, strings related to prompting
├── README.md
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

Create logs directory to hold logging artifacts.

---

## Running the Project

After setup:

```bash
source .venv/bin/activate
python main.py --chunking_strategy none
```

main.py accepts manual, automatic or none as chunking strategies.
This is elaborated in Blueprint.md.

---

## Notes

### Output

After a successful run of main.py, a report will be generated in `./outputs`. \
If the LLM gave a structured output, the PoC will parse it and save it as a `.json` object. \
If the model was unable to generate a properly formed output, the output will still be saved as a raw text file.

An example json output:
```
{
  "unresolved_high_priority_action_items": [
    {
      "description": "Gábor's question about callback URL handling in Barion's API documentation",
      "assignee": "Barion's support team",
      "time_elapsed": "14 days"
    },
    ...
  ],
  "emerging_risks_blockers": [
    {
      "description": "Potential issue with callback URL handling in Barion's V2 API",
      "impact": "high",
      "suggested_action": "Verify the correct method for transactionId return"
    },
    ...
  ]
}
```

### LLM model

For rapid prototyping and because I'm more familiar with local hosted LLMs, \
I used `Llama3.2:1b` (while iterating) and later `llama3.1:8b` (while testing prompts). \
While I used llm.invoke as the interface for inference, I'm aware of ainvoke, an async version of invoke;\
this should be used rather than sync calls in production to save time and resources.

I found the latter capable of following structured output rules, while the former of course was faster in inference, allowing for faster testing of the framework utilizing the model.

LangChain offers countless wrappers and has many integrations;\
instead of `langchain_ollama.llm.OllamaLLM`, I could have used e.g `langchain_openai.llms.base.OpenAI` with similar effects.

Using cloud based LLMs requires setting up an API key in the env, storing secrets securely (not as plain text in a source file), and usually, inference takes a bit longer. For a live environment, I'd integrate [Trufflehog](https://trufflesecurity.com/trufflehog) for sniffing out accidentally exposed secrets such as API keys and login credentials.

**NOTE on inference:** if an error occurs parsing the output as a json object, it is saved as a raw text file.

### Choice of logger

I've been using `loguru` for over a year, and I prefer its simplicity and usability over other loggers.


# Resources

**Resources considered why solving the task.**

- Used OpenAI's `ChatGPT` to analyse requirements, generate some boilerplate code
    * TODO: feed the prompts + emails to GPT, to get something to act as Ground Truth

- [langchain-ai](https://github.com/langchain-ai/langgraph.git)

    * Generic tutorials for interfaces etc.

- [RAG With Llama 3.1 8B, Ollama, and Langchain: Tutorial](https://www.datacamp.com/tutorial/llama-3-1-rag)

- [Llama 3.1 Agent using LangGraph and Ollama](https://www.pinecone.io/learn/langgraph-ollama-llama/)



# Arguments (for main.py)

## Chunking Strategies

The project supports three modes of processing email data:

- `FULL_CONVERSATION` – feed the entire email thread as a single input.
- `AUTO_SPLIT` – automatically split using RecursiveCharacterTextSplitter.
- `MANUAL_SPLIT` – split along double-newline boundaries.


## Path

main accepts a path to a zip file as an argument.
