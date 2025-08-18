ollama_url = "http://localhost:11434/"

model_name = "llama3.2:1b"

template = "Question: {question} \nAnswer: Let's think step by step."

system_prompt = "You are am assistant knowledgable in space. \
                Only answer questions related to space. \
                If the question is not related to space \
                then reply with 'I don't know'."
