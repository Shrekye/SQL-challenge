FROM python:3.10-slim

# Mettre en place un répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialiser la base de données lors du build (créera challenge.db)
RUN python init_db.py

# Port exposé
EXPOSE 5001

# Variable d'environnement par défaut : vulnérable
ENV VULNERABLE=1
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

# Commande de démarrage
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]