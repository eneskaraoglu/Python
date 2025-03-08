from transformers import pipeline

summarizer = pipeline("summarization")
text = "Hugging Face, doğal dil işleme ve yapay zeka modelleri konusunda uzmanlaşmış bir platformdur."
print(summarizer(text))
