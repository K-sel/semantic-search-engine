FROM continuumio/miniconda3:latest

WORKDIR /app

# Copier le fichier d'environnement Conda
COPY environment.yml .

# Créer l'environnement Conda
RUN conda env create -f environment.yml

SHELL ["conda", "run", "-n", "semantic-search", "/bin/bash", "-c"]

# Copier le code
COPY . .

EXPOSE 5000

# Script de démarrage avec vérifications conditionnelles en cascade
CMD ["conda", "run", "--no-capture-output", "-n", "semantic-search", "bash", "-c", "\
    if [ ! -d data ] || [ ! \"$(ls -A data 2>/dev/null)\" ]; then \
        echo 'Dossier data manquant ou vide. Lancement de dataset.py...'; \
        python dataset.py; \
    else \
        echo 'Dossier data trouvé et non vide.'; \
    fi && \
    if [ ! -f indexes.faiss ] || [ ! -f docs.db ]; then \
        echo 'Fichiers indexes.faiss ou docs.db manquants. Lancement de indexer.py...'; \
        python indexer.py; \
    else \
        echo 'Fichiers indexes.faiss et docs.db trouvés.'; \
    fi && \
    python app.py"]