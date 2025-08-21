# Blueprint.md – Automated QBR Analysis System

## Overview
This system ingests project emails and produces a Portfolio Health Report for the Director of Engineering. \
Its goal is to highlight key risks, unresolved items, and inconsistencies requiring immediate attention.

## Entry point and Control Flow
The entry point to the PoC is main.py.
It accepts a chunking strategy and a path arguments.

Path is the path to the .zip containing the emails; defaults to `'./data/content.zip'`.
Strategy determines if:
  1. ('none'): the entire conversation is passed per inference;
  2. ('manual'): the emails are fed one by one;
  3. ('auto'): the conversations are chunked using `LangChain`'s `RecursiveCharacterTextSplitter`.

Once these parameters are set, `main.py` calls `get_sanitized_data`, the only 'visible' function in data_transformers. \
This gets the path and returns the sanitized, preprocessed emails. \
Preprocessing involves 3 steps:
  1. removing email addresses, since they are redundant in the LLM context;
  2. adds the roles after each worker's name for additional context for the Model;
  3. cleans the dates: 1st mail is now "Start", every other mail gets a "Start + {ellapsed time}"-like tag. E.g "Start + 3h".

The emails are returned in a dict to also pass the file name and other meta data (possible to expand in the future with e.g IDs).

In the main loop of the program, I used a match-case construct (Pythono3.10+). \
I used an Enum to easily keep track of the chunking strategy.

- **Mode.FULL_CONVERSATION:**
  If the entire conversation is passed, we simply call `model.invoke` on our formatted input.

  The inference is traced by loguru, and appended to the global inference output pool. \
  Here we can add more metadata later.

- **Mode.AUTO_SPLIT:**
  If LangChain's splitter is selected, the code calls it to chunk the convo, then iterates with the inference on every chunk.
  All these outputs are summerized after all are processed, making this a 3-layered structure. \
  This may be inefficient compute-wise in the long run.

- **Mode.MANUAL_SPLIT:**
  This branch follows the same route except for chunking, it uses a simple `str.split()`. \
  It splits along '\n\n', so two newlines; effectively, the LLM iterates over every email in the conversation. \
  This is more of a naive experiment.

Once the model finishes with every email, a last inference is performed, using the previous, per-email outputs.

`save_json_safe(summary)` tries to write the summary as a parsed json object; if an Exception is thrown, it dumps the raw output instead, logging the error with loguru.



## 1. Data Ingestion & Preprocessing
- Emails are loaded from a zip file and sanitized:
  1. Dates normalized to relative format.
    First email is "Start", all other mails in the conversation give ellapsed time, e.g "Start + 2d 3h"
  2. Redundant email addresses removed
    This data is irrelevant to the LLM and only wastes valuable context length.
    PII's should be monitored when feeding inputs to LLMs (especially cloud based LLMs) and returning outputs (even with local LLMs)
  3. Roles appended to names.
    Transforming "Péter Kovács" to "Péter Kovács (Project Manager (PM))". This can be useful context for LLMs to determine responsibilities.

- **Scalability:** Supports chunking strategies (full conversation, auto-split, manual split) to handle large volumes of email data.
  - **Full conversation** passes the entire (preprocessed) conversation as input. This can be fine with smaller conversations but problematic down the line.
  - **Auto-split** utilizes LangChain's recursive text splitter. It feeds the conversation chunk by chunk to the LLM.\
    *TODO*: LLM should get previous inferences to make better calls as the convo goes forward!
  - **Manual Split** breaks the conversation along 2 newlines ('\n\n'), serving the llm one mail at a time. This is a naive experiment.


  - **Asyncronous invoke** function is implemented (langchain's `llm.ainvoke`, wrapped) but not yet integrated. It should boost performance.


  - **Hierarchical LLM calls** / extractions are semi-implemented, this can be levereged with e.g smaller models doing extractions per email, preserving context for larger, more costly LLM inferences. \
    *TODO*: this is quasy-ready, but not yet refined.


  - **Ollama / Local LLM** was used, which can be scalable by a flexible construct with a cloud-computing provider. E.g scale up during daytime in the EU. Local models are more secure (less of a chance of a data leak) than cloud providers.


## 2. Analytical Engine
- **Multi-Step AI Process:**
  1. **Chunk-level analysis:** Emails are split according to the chosen strategy. Each chunk is summarized via a **llama3.1:8b** model.
  2. **Email-level summarization:** Summaries of all chunks are combined and re-summarized. Alternatively, the entire e-mail is ingested at once by the LLM.
  3. **Portfolio-level summarization:** Combined summaries across all emails produce a final top-level report.
- **Attention Flags:** Defined in prompts.py; currently, e-mails are monitored for these two flags:
  - Unresolved high-priority tasks
  - Emerging risks or blockers
- **Prompt Templates:** Prompt engineering was done in a trial-and-error experiment. Outermost inference (portfolio level) is forced into structured output. \
  *TODO*: force structured output for all levels, log them all properly.

## 3. Cost & Robustness
- **Cost Management:** Uses an 8B param Llama3.1 through Ollama for lightweight, cost-efficient inference.
- **Robustness:** Multi-step summarization reduces the risk of missing key points; overlapping chunks help maintain context. \
  Chunking, especially manually, runs the threat of missing information. Chunks don't get previous inference output as of yet; *TODO*!
- **Quantization of LLM**: Quantization is a Neural Network optimization technique that gains speed in exchange for less accurate numerical representation of the individual neurons' weights. \
In "[A Comprehensive Evaluation of Quantized Instruction-Tuned Large Language Models: An Experimental Analysis up to 405B](https://arxiv.org/pdf/2409.11055v1)", researchrs demonstrated that larger but more quantized LLMs can outperform smaller but more refined LLMs in many benchmarks. This should be checked as a higher quality but *computationally competitive* alternative.

## 4. Monitoring & Trust
- Logging via `loguru` tracks processing per email and chunk. Logs to standard output and a log file.
- Suggested metrics for production:
  - Tokens processed per email
  - Chunk completion rates
  - Consistency of summaries across chunks
- Future enhancements: QA checks on top-level summaries to detect inconsistencies + text similarity check with **Ground Truth** (missing as of yet)

## 5. Architectural Risk & Mitigation
- **Risk:** Multi-step summarization may introduce hallucinations or omit critical information.
- **Mitigation:**
  - Enforce structured output with explicit formatting.
  - Iteratively design prompts and review model outputs for greatest effect.
  - *TODO*: Include cross-chunk consistency checks.
  - *TODO*: Chunks context fix: they should get the previous N chunk's summaries.
  - *TODO*: More rigid prompts specifying output rules.

## 6. Deliverables
- GitHub repo with modular Python code (`main.py`, helpers, prompts, JSON outputs)
- Blueprint.md (this document)
- README.md documenting AI models used (LLaMA 3B) and design rationale
