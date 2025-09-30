# Semantic Search Engine - Mon premier projet IA avec Python

## 📋 Vue d'ensemble

Application de **recherche sémantique** qui comprend le sens des requêtes plutôt que de faire une simple correspondance de mots-clés. Par exemple, chercher "voiture rapide" trouvera aussi des documents contenant "automobile sportive" ou "véhicule performant".

Ce projet a été développé pour apprendre et comprendre comment fonctionne un moteur de recherche moderne et a par la même occasion servi de projet final soumis à Harvard pour valider mon cours CS50.

### Technologies principales
- **Backend** : Flask + FAISS + Sentence Transformers
- **Frontend** : Vue.js 3 + Vite
- **Orchestration** : Docker Compose

---

## 🚀 Démarrage

```bash
# Cloner et lancer
git clone <repo>
cd semantic-search
docker-compose up --build

# Puis ouvrir dans votre navigateur
# Frontend : http://localhost:5173
# API : http://localhost:5000
```

---

## 🧠 Comment fonctionne la recherche sémantique ?

### Le problème avec la recherche classique

Une recherche traditionnelle cherche des **correspondances exactes** :
- Requête : "voiture rapide"
- Trouve : documents contenant exactement "voiture" ET "rapide"
- Rate : "automobile sportive", "véhicule performant", "bolide"

### La solution : les embeddings vectoriels

Au lieu de comparer des mots, on compare des **vecteurs mathématiques** qui représentent le **sens** du texte.

```
"machine learning"          →  [0.2, 0.8, 0.1, ..., 0.5]  (384 dimensions)
"apprentissage automatique" →  [0.21, 0.79, 0.11, ..., 0.49]

Similarité cosinus élevée → textes similaires !
```

---

## 🔬 Architecture du moteur de recherche

### Étape 1 : Préparation des données (`dataset.py`)

```python
documents = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "Python is great for data science"
]
```

Génère :
- **`data/`** : Fichiers sources bruts
- **`docs.db`** : Base SQLite avec métadonnées (id, titre, texte)

### Étape 2 : Indexation (`indexer.py`)

```python
# 1. Charger le modèle
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Encoder tous les documents
embeddings = model.encode(documents)
# → Matrice de vecteurs normalisés pour la similarité cosinus

# 3. Créer l'index FAISS avec similarité cosinus
index = faiss.IndexFlatIP(384)  # IP = Inner Product (cosinus sur vecteurs normalisés)

# 4. Ajouter les vecteurs
index.add(embeddings)

# 5. Sauvegarder
faiss.write_index(index, "indexes.faiss")
```

**Résultat :** `indexes.faiss` - Index optimisé pour la recherche rapide

### Étape 3 : Recherche en temps réel (`app.py`)

```python
# 1. Utilisateur cherche : "deep learning"
query_vector = model.encode(query)

# 2. Chercher les 5 vecteurs les plus similaires
similarities, indices = index.search(query_vector, k=5)

# similarities = [0.95, 0.87, 0.72, 0.65, 0.58]  # Plus élevé = plus similaire
# indices = [42, 15, 103, 8, 67]

# 3. Récupérer les documents depuis SQLite
results = [
    {"id": 42, "title": "...", "score": 0.95},
    {"id": 15, "title": "...", "score": 0.87},
    ...
]
```

---

## 🎯 Pourquoi c'est puissant ?

### 1. Comprend les synonymes
```
Requête : "automobile"
Trouve : "voiture", "véhicule", "car"
```

### 2. Comprend le contexte
```
Requête : "apple fruit"
Trouve : documents sur les pommes (fruit)
Pas : documents sur Apple (entreprise)
```

### 3. Fonctionne en multilingue
```
Requête : "machine learning"
Trouve aussi : "apprentissage automatique"
```

### 4. Rapide et scalable
- **10 000 documents** : ~5-10ms
- **1 million de documents** : ~50-100ms

---

## 🔍 FAISS : Le cœur du système

**FAISS** (Facebook AI Similarity Search) permet la recherche vectorielle ultra-rapide.

### IndexFlatIP vs IndexFlatL2

Notre projet utilise `IndexFlatIP` qui calcule le **produit scalaire** :

```python
index = faiss.IndexFlatIP(384)
```

**Quand utiliser IndexFlatIP :**
- **Vecteurs normalisés** (comme Sentence Transformers) : équivalent à la similarité cosinus
- **Score intuitif** : valeurs 0-1, plus élevé = meilleur
- **Recherche sémantique** : on compare l'orientation (le sens), pas la magnitude
- **Recommandations** : "cet article est similaire à celui-ci"

**Quand utiliser IndexFlatL2 :**
- **Vecteurs non normalisés** où la magnitude compte
- **Embeddings d'images** avec des modèles qui ne normalisent pas
- **Distance physique** : coordonnées GPS, données spatiales
- **Données numériques brutes** : température, prix, mesures

**Note importante :** Avec Sentence Transformers, les vecteurs sont automatiquement normalisés. Dans ce cas, **IndexFlatIP et IndexFlatL2 donnent des classements identiques** (seule l'échelle des scores diffère). On préfère IP pour l'interprétabilité du score.

### Comparaison des index FAISS

| Index | Vitesse | Précision | RAM | Meilleur pour |
|-------|---------|-----------|-----|---------------|
| **FlatIP/L2** | Lent (O(n)) | 100% | Élevée | < 100k vecteurs, précision critique |
| **IVFFlat** | Rapide (O(log n)) | 90-95% | Moyenne | 100k-10M vecteurs, bon équilibre |
| **IVFPQ** | Très rapide | 85-90% | Faible | 10M+ vecteurs, RAM limitée |
| **HNSW** | Très rapide | 95-99% | Élevée | Meilleure qualité approximative |

**Notre choix :** IndexFlatIP car précision maximale pour un dataset de taille modérée (~1k-100k documents).

---

## 📊 Sentence Transformers : Le cerveau

### Le modèle : all-MiniLM-L6-v2

**Caractéristiques :**
- **Dimension** : 384
- **Taille** : ~80 MB
- **Vitesse** : ~14 000 phrases/seconde (CPU)
- **Qualité** : Excellent équilibre performance/précision

```python
model = SentenceTransformer("all-MiniLM-L6-v2")

model.encode("chat")  # → [0.12, -0.54, ...]
model.encode("J'aime les chats")  # → [0.15, -0.52, ...]
```

Le modèle a été entraîné sur des millions de paires de phrases pour capturer le sens sémantique.

---

## 🎨 Flux complet d'une recherche

```
1. Utilisateur : "python data science"
   ↓
2. Frontend → GET /search?q=python data science
   ↓
3. Flask encode la requête
   → [0.23, 0.67, -0.12, ..., 0.89]
   ↓
4. FAISS calcule les similarités cosinus
   → [doc_42: 0.89, doc_15: 0.82, doc_103: 0.75]
   ↓
5. SQLite récupère les métadonnées
   ↓
6. JSON → Frontend
   [{id: 42, title: "...", score: 0.89}, ...]
```

---

## 🧪 Exemple concret

### Documents indexés :
```
[1] "Python est un langage de programmation"
[2] "JavaScript est utilisé pour le web"
[3] "Le machine learning utilise Python"
[4] "Les pandas mangent du bambou"
```

### Requête : "programmation python"

**Similarités cosinus calculées :**
```
doc[1] : 0.92  ← Très similaire !
doc[2] : 0.35
doc[3] : 0.78  ← Assez similaire
doc[4] : 0.12  ← Peu similaire
```

**Résultats (triés par score décroissant) :**
```json
[
  {
    "id": 1,
    "title": "Python est un langage de programmation",
    "score": 0.92
  },
  {
    "id": 3,
    "title": "Le machine learning utilise Python",
    "score": 0.78
  }
]
```

---

## 🔧 API Endpoints

### `GET /`
Informations sur l'index

```json
{
  "message": "FAISS API ready",
  "index_size": 1000,
  "dimension": 384
}
```

### `GET /search?q=votre requête`
Recherche sémantique

**Réponse :**
```json
[
  {
    "id": 42,
    "title": "Introduction to Machine Learning",
    "snippet": "Machine learning is a subset...",
    "score": 0.89
  }
]
```

**Note :** Avec `IndexFlatIP`, **plus le score est élevé, meilleur est le résultat** (contrairement à L2 où un score bas est meilleur).

---

## 📖 Ressources

- [FAISS](https://faiss.ai/) - Bibliothèque de recherche vectorielle
- [Sentence Transformers](https://www.sbert.net/) - Modèles d'embeddings
- [Flask](https://flask.palletsprojects.com/) - Framework web Python
- [Hugging Face Models](https://huggingface.co/models?library=sentence-transformers) - Modèles alternatifs

---

**Le principe :** Transformer du texte en vecteurs, calculer leur similarité cosinus pour trouver ce qui est sémantiquement proche. Simple et puissant ! 🚀