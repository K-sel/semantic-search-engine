# Image de base Node.js
FROM node:24-alpine

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le code du frontend
COPY . .

# Exposer le port du serveur de dev (Vite utilise 5173 par défaut)
EXPOSE 5173

# Lancer le serveur de développement
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]