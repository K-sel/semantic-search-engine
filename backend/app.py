from flask import Flask, request, jsonify
import faiss
from sentence_transformers import SentenceTransformer
import sqlite3

index = faiss.read_index("./indexes.faiss")
k = 5 # On garde les 5 meilleurs resultats 
model = SentenceTransformer("all-MiniLM-L6-v2")


app = Flask(__name__)


@app.route("/")
def home():
    return jsonify(
        {"message": "FAISS API ready", "index_size": index.ntotal, "dimension": index.d}
    )

@app.route("/search", methods=["GET", "POST"])
def search_indexes():
    try:
        # Récupérer les données de la requête
        q = request.args.get("q")

        if not q:
            return jsonify({"error": "Paramètre 'q' requis"}), 400

        # Encoder et préparer l'embedding
        embedding = model.encode(q)
        embedding = embedding.astype("float32")  # ← Assigner le résultat
        embedding_2d = embedding.reshape(1, -1)  # ← Créer une variable pour la forme 2D
        faiss.normalize_L2(embedding_2d)  # ← Normaliser la version 2D

        # Rechercher avec la version 2D
        distances, indices = index.search(embedding_2d, k)  # ← Décomposer le tuple

        results = []

        con = sqlite3.connect("docs.db")
        db = con.cursor()

        for i, doc_id in enumerate(indices[0]):
            id = int(doc_id)
            doc = db.execute(
                "SELECT id, title, snippet FROM docs WHERE id = ?", [id]
            ).fetchone()
            print(doc)
            
            if doc:
                results.append(
                    {
                        "id": doc[0],
                        "title": doc[1],
                        "snippet": doc[2],
                        "score": float(distances[0][i]),
                    }
                )
        con.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
