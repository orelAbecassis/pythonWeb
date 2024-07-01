# Utilisez l'image officielle de Python 3.12
FROM python:3.12-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le répertoire de travail
COPY requirements.txt .

# Installez les dépendances nécessaires
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le contenu de l'application dans le répertoire de travail
COPY . .

# Exposez le port 3000
EXPOSE 3000

# Commande pour lancer l'application Flask
CMD ["python", "app.py"]
