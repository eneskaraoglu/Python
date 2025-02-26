import spacy

# Türkçe Transformer modelini yükle
nlp = spacy.load("tr_core_news_trf")

# Örnek bir cümleyi işleyelim
text = "OpenAI, yapay zeka alanında lider bir araştırma şirketidir. 2024 yılında birçok yenilik getirdi."

# NLP işleminden geçir
doc = nlp(text)

# Kelimeleri ve kök halleri
for token in doc:
    print(f"Kelime: {token.text}, Kök: {token.lemma_}, POS: {token.pos_}")


for ent in doc.ents:
    print(f"Varlık: {ent.text}, Türü: {ent.label_}")