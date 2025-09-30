from flask import Flask, request, jsonify
import faiss
from sentence_transformers import SentenceTransformer
import sqlite3

index = faiss.read_index("./indexes.faiss")
k = 5 
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
        q = request.args.get("q")

        if not q:
            return jsonify({"error": "Paramètre 'q' requis"}), 400

        embedding = model.encode(q)
        embedding = embedding.astype("float32")  
        embedding_2d = embedding.reshape(1, -1) 
        faiss.normalize_L2(embedding_2d) 

        distances, indices = index.search(embedding_2d, k) 

        results = []

        con = sqlite3.connect("docs.db")
        db = con.cursor()

        for i, doc_id in enumerate(indices[0]):
            id = int(doc_id)
            doc = db.execute(
                "SELECT id, title, content FROM docs WHERE id = ?", [id]
            ).fetchone()

            if doc:
                results.append(
                    {
                        "id": doc[0],
                        "title": doc[1],
                        "content": doc[2],
                        "score": float(distances[0][i]),
                    }
                )
        con.close()
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
