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
# API : http://localhost:5000 ou depuis frontend http://localhost:5173/api/search?q=machine
```

---

## 🧠 Comment fonctionne la recherche sémantique ?

### Le problème avec la recherche classique

Une recherche traditionnelle (comme CTRL+F) cherche des **correspondances exactes** :
- Requête : "voiture rapide"
- Trouve : documents contenant exactement "voiture" ET "rapide"
- Rate : "automobile sportive", "véhicule performant", "bolide"

### La solution : les embeddings vectoriels

Au lieu de comparer des mots, on compare des **vecteurs mathématiques** qui représentent le **sens** du texte.

```
"machine learning"     →  [0.2, 0.8, 0.1, ..., 0.5]  (384 dimensions)
"apprentissage automatique" →  [0.21, 0.79, 0.11, ..., 0.49]

Distance entre les vecteurs = faible → textes similaires !
```

---

## 📚 Cas d'usage

### 1. Documentation technique
Chercher dans une base de docs techniques : "comment gérer les erreurs" trouve aussi "exception handling" et "error management"

### 2. E-commerce
"chaussures de course" trouve aussi "baskets running", "sneakers sport"

### 3. Support client
"mon compte ne marche pas" trouve des articles sur "problèmes de connexion", "erreurs d'authentification"

### 4. Recherche académique
Trouver des papers similaires par le contenu plutôt que par mots-clés exacts

---

## 🔬 Architecture du moteur de recherche

### Étape 1 : Préparation des données (`dataset.py`)

```python
# Vos documents sources
documents = [
    "Machine learning is a subset of AI",
    "Deep learning uses neural networks",
    "Python is great for data science"
]

# Sauvegarde dans data/ et SQLite
```

Le script génère :
- **`data/`** : Fichiers sources bruts
- **`docs.db`** : Base SQLite avec les métadonnées (id, titre, texte)

### Étape 2 : Indexation (`indexer.py`)

**Le processus :**

```python
# 1. Charger le modèle de transformation texte → vecteur
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Pour chaque document
for doc in documents:
    # Transformer le texte en vecteur de 384 dimensions
    embedding = model.encode(doc)
    # → [0.12, -0.43, 0.89, ..., 0.15]

# 3. Créer l'index FAISS
index = faiss.IndexFlatL2(384)  # 384 = dimension des vecteurs

# 4. Ajouter tous les vecteurs à l'index
index.add(all_embeddings)

# 5. Sauvegarder l'index sur disque
faiss.write_index(index, "indexes.faiss")
```

**Résultat :**
- **`indexes.faiss`** : Index optimisé pour la recherche rapide

### Étape 3 : Recherche en temps réel (`app.py`)

Quand un utilisateur cherche quelque chose :

```python
# 1. L'utilisateur tape : "deep learning"
query = "deep learning"

# 2. Transformer la requête en vecteur avec le MÊME modèle
query_vector = model.encode(query)
# → [0.18, 0.72, -0.31, ..., 0.44]

# 3. Chercher les 5 vecteurs les plus proches dans l'index
distances, indices = index.search(query_vector, k=5)

# distances = [0.12, 0.45, 0.89, 1.23, 1.87]  # Plus petit = plus similaire
# indices = [42, 15, 103, 8, 67]  # IDs des documents

# 4. Récupérer les documents depuis SQLite
for doc_id in indices:
    doc = db.execute("SELECT * FROM docs WHERE id = ?", [doc_id])
    
# 5. Retourner les résultats avec leur score
results = [
    {"id": 42, "title": "...", "snippet": "...", "score": 0.12},
    {"id": 15, "title": "...", "snippet": "...", "score": 0.45},
    ...
]
```

---

## 🎯 Pourquoi c'est puissant ?

### 1. Comprend les synonymes

```
Requête : "automobile"
Trouve : documents sur "voiture", "véhicule", "car"
```

### 2. Comprend le contexte

```
Requête : "apple fruit"
Trouve : documents sur les pommes (fruit)
Ne trouve PAS : documents sur Apple (entreprise)
```

### 3. Fonctionne en multilingue

Le modèle `all-MiniLM-L6-v2` comprend plusieurs langues :
```
Requête en anglais : "machine learning"
Trouve aussi : documents français sur "apprentissage automatique"
```

### 4. Rapide et scalable

FAISS utilise des algorithmes optimisés :
- **10 000 documents** : recherche en ~5-10ms
- **1 million de documents** : recherche en ~50-100ms

---

## 🔍 FAISS : Le cœur du système

**FAISS** (Facebook AI Similarity Search) est une bibliothèque pour la recherche de similarité vectorielle ultra-rapide.

### Comment ça marche ?

Au lieu de comparer votre requête avec **tous** les documents un par un (lent), FAISS utilise des structures de données optimisées :

**Approche naïve (lente) :**
```python
# Comparer avec chaque document
for doc_vector in all_docs:
    distance = calculate_distance(query_vector, doc_vector)
# Complexité : O(n) → lent pour des millions de docs
```

**Approche FAISS (rapide) :**
```python
# Index organisé intelligemment (comme un arbre)
distances, indices = index.search(query_vector, k=5)
# Complexité : O(log n) ou mieux
```

### Types d'index FAISS

Notre projet utilise `IndexFlatL2` (recherche exacte) :
- Précis à 100%
- Rapide jusqu'à ~1 million de vecteurs
- Distance : L2 (euclidienne)

Pour des datasets énormes, FAISS propose :
- **IndexIVFFlat** : Approximation rapide
- **IndexHNSW** : Graphes hiérarchiques
- **IndexPQ** : Compression des vecteurs

---

## 📊 Sentence Transformers : Le cerveau

**Sentence Transformers** transforme du texte en vecteurs qui capturent le sens sémantique.

### Le modèle : all-MiniLM-L6-v2

**Caractéristiques :**
- **Dimension** : 384 (chaque texte → vecteur de 384 nombres)
- **Taille** : ~80 MB
- **Vitesse** : ~14 000 phrases/seconde sur CPU
- **Qualité** : Excellent équilibre performance/précision

**Comment il fonctionne :**
```python
model = SentenceTransformer("all-MiniLM-L6-v2")

# Un mot
model.encode("chat")  # → [0.12, -0.54, ...]

# Une phrase
model.encode("J'aime les chats")  # → [0.15, -0.52, ...]

# Un paragraphe entier
model.encode("Les chats sont des animaux...")  # → [0.14, -0.53, ...]
```

Le modèle a été entraîné sur des millions de paires de phrases pour apprendre :
- Quelles phrases sont similaires
- Quelles phrases sont différentes
- Comment capturer le contexte et les nuances

---

## 🎨 Flux complet d'une recherche

```
1. Utilisateur tape : "python data science"
   ↓
2. Frontend Vue envoie : GET /search?q=python data science
   ↓
3. Flask reçoit la requête
   ↓
4. Sentence Transformers encode la requête
   "python data science" → [0.23, 0.67, -0.12, ..., 0.89]
   ↓
5. FAISS cherche les 5 vecteurs les plus proches
   Résultat : [doc_42, doc_15, doc_103, doc_8, doc_67]
   ↓
6. SQLite récupère les métadonnées
   SELECT * FROM docs WHERE id IN (42, 15, 103, 8, 67)
   ↓
7. Flask construit la réponse JSON
   [{id: 42, title: "...", score: 0.12}, ...]
   ↓
8. Frontend affiche les résultats
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

**Étape 1 : Encodage**
```python
query_vector = model.encode("programmation python")
# → [0.45, 0.23, -0.67, ..., 0.12]
```

**Étape 2 : Calcul des distances**
```
Distance avec doc[1] : 0.15  ← Très proche !
Distance avec doc[2] : 0.89
Distance avec doc[3] : 0.32  ← Assez proche
Distance avec doc[4] : 1.45  ← Très différent
```

**Étape 3 : Résultats (triés par distance)**
```json
[
  {
    "id": 1,
    "title": "Python est un langage de programmation",
    "score": 0.15
  },
  {
    "id": 3,
    "title": "Le machine learning utilise Python",
    "score": 0.32
  }
]
```

**Remarque :** Le document [4] sur les pandas (animaux) n'est pas retourné car il est trop différent, même s'il contient le mot "pandas" qui existe aussi en Python !

---

## 🔧 API Endpoints

### `GET /`
Informations sur l'index

**Réponse :**
```json
{
  "message": "FAISS API ready",
  "index_size": 1000,
  "dimension": 384
}
```

### `GET /search?q=votre requête`
Recherche sémantique

**Paramètres :**
- `q` : Texte de la requête (requis)

**Réponse :**
```json
[
  {
    "id": 42,
    "title": "Introduction to Machine Learning",
    "snippet": "Machine learning is a subset...",
    "score": 0.12
  }
]
```

**Note :** Le score est une distance. **Plus il est bas, meilleur est le résultat.**

---

## 📖 Ressources

### Documentation
- [FAISS](https://faiss.ai/) - Bibliothèque de recherche vectorielle
- [Sentence Transformers](https://www.sbert.net/) - Modèles d'embeddings
- [Flask](https://flask.palletsprojects.com/) - Framework web Python

### Modèles alternatifs
Explorer sur [Hugging Face](https://huggingface.co/models?library=sentence-transformers) pour trouver des modèles adaptés à votre cas d'usage spécifique.

---

**Le principe fondamental :** Transformer du texte en nombres, puis utiliser les mathématiques pour trouver ce qui est similaire. Simple et puissant ! 🚀