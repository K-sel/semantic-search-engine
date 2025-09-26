import os
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import sqlite3

# Files
path = "./data"
docs = os.listdir(path)

# Database
con = sqlite3.connect("docs.db")
db = con.cursor()
db.execute("CREATE TABLE IF NOT EXISTS docs(title, snippet)")

# Embeedings
model = SentenceTransformer("all-MiniLM-L6-v2")
all_embeddings = []
doc_ids = []


def vectorise_text(model, text, doc_id):

    embedding = model.encode(text)
    print(f"Embedding shape: {embedding.shape}")

    all_embeddings.append(embedding)
    doc_ids.append(doc_id)


for i, file in enumerate(docs):
    with open(f"{path}/{file}", "rt") as f:

        content = f.read()

        vectorise_text(model, content, i)

        snippet = content[:200] + "..."

        words = content.split()
        title = " ".join(words[:1]) if len(words) >= 3 else " ".join(words)

        print(f"Titre: {title}")
        print(f"Snippet: {snippet}")
        print("-" * 40)

        db.execute("INSERT INTO docs (title, snippet) VALUES (?,?)", [title, snippet])
        con.commit()

con.close()


if all_embeddings:
    
    # FlatIP pour effectuer des recherches par similarité cosinus entre les vecteurs

    embeddings_matrice = np.array(all_embeddings).astype("float32")  # on regarde le nombre de dimensions sur les embeddings pour pouvoir crée la base de données

    dimensions = embeddings_matrice.shape[1]
    print(embeddings_matrice)

    
    faiss.normalize_L2(embeddings_matrice)
    index = faiss.IndexFlatIP(dimensions)
    index.add(embeddings_matrice)
        
    faiss.write_index(index, "indexes.faiss")