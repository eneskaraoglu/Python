from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

# Load model
model = SentenceTransformer("models/paraphrase-multilingual-MiniLM-L12-v2")

# Load dataset
with open("llama_training_data_35b.jsonl", "r", encoding="utf-8") as f:
    dataset = [json.loads(line.strip()) for line in f]

# Extract questions and answers
questions = [item["instruction"].strip() for item in dataset]
answers = [item["output"].strip() for item in dataset]

# Create embeddings for questions
question_embeddings = model.encode(questions)

# Build FAISS index
dim = question_embeddings[0].shape[0]
index = faiss.IndexFlatL2(dim)
index.add(np.array(question_embeddings))

# Ask user for a question
print("🔍 Type a question to test (or press Enter to exit):")
while True:
    test_question = input("\nYour question: ").strip()
    if not test_question:
        print("Exiting...")
        break

    # Embed the user question
    q_embed = model.encode([test_question])

    # Search top 10 similar questions
    top_k = 10
    D, I = index.search(np.array(q_embed), top_k)

    print("\n📊 Top 10 Most Similar Questions:\n")
    found_exact = False

    for rank, (dist, idx) in enumerate(zip(D[0], I[0]), start=1):
        matched_q = questions[idx]
        matched_a = answers[idx]
        score = 1 - (dist / 10)
        #score = max(0.0, score)  # clamp

        print(f"{rank}. Similarity: {score:.4f} | Raw distance: {dist:.4f}")
        print(f"   Q: {matched_q}")
        print(f"   A: {matched_a}")
        if matched_q == test_question:
            print("   ✅ Exact match found here!")
            found_exact = True
        print()


    if not found_exact:
        print("❌ Exact match NOT found in top 10.\n")
