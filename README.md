# SQL-challenge

## But pédagogique
Fournir une application minimale et autonome illustrant une vulnérabilité **SQL Injection** dans un formulaire de connexion, puis montrer la version corrigée. **Usage local uniquement**.

## Contenu
- `app.py` : application Flask (mode vulnérable ou corrigé) avec interface HTML.
- `init_db.py` : script d'initialisation de la base SQLite (`challenge.db`) contenant des comptes et la table `flags`.
- `requirements.txt` : dépendances Python.
- `Dockerfile` et `docker-compose.yml` : pour builder et lancer le conteneur.
- `hints/` : 3 indices progressifs.
- `SOLUTION.md` : solution complète (uniquement pour l'enseignant).
- `test_login.py` : tests automatisés (attendent que le serveur tourne localement).
- `templates/` et `static/` : interface web (HTML + CSS).

## Objectifs pédagogiques
- Montrer l'impact d'une concaténation de chaîne dans une requête SQL.
- Montrer la correction par requêtes paramétrées (prepared statements).
- Fournir un exercice simple et sûr pour débutants.

## Pré-requis
- Docker (ou Python 3.9+ pour exécuter sans Docker).
- (Optionnel) docker-compose si vous utilisez `docker-compose.yml`.

## Commandes pour builder / lancer (Docker)

### Builder l'image Docker
```bash
docker build -t sql-chal .
Lancer en mode vulnérable (montrer la faille)
bash
Copier le code
docker run --rm -p 5000:5000 -e VULNERABLE=1 --name sql-chal-vuln sql-chal
Application accessible : http://0.0.0.0:5000/

Lancer en mode corrigé (sécurisé)
bash
Copier le code
docker run --rm -p 5000:5000 -e VULNERABLE=0 --name sql-chal-safe sql-chal
Remarque : la variable d'environnement VULNERABLE contrôle le comportement. Valeurs acceptées : 1, true, True → vulnérable. Autres valeurs → version sécurisée.

Commandes Docker Compose (optionnel)
bash
Copier le code
docker-compose up --build
(par défaut le compose lance le conteneur en mode vulnérable ; voir docker-compose.yml)

Exécution sans Docker (local)
Créer un environnement virtuel Python 3.9+.

pip install -r requirements.txt

Initialiser la DB : python init_db.py

Lancer le serveur (mode vulnérable) :

bash
Copier le code
VULNERABLE=1 FLASK_APP=app.py flask run --host=0.0.0.0
ou en mode corrigé :

bash
Copier le code
VULNERABLE=0 FLASK_APP=app.py flask run --host=0.0.0.0
Tests
Lancer l'application (vulnérable).

Exécuter : python test_login.py

Le script détecte si le serveur est en mode vulnérable ou sécurisé (via /mode) et vérifie le comportement attendu.

Sécurité & règles
Usage local uniquement. Ne déployez jamais cette application vulnérable sur un réseau public.

Les fichiers et exemples d’exploitation fournis (dans SOLUTION.md) sont uniquement pour l'enseignant / usage pédagogique.

Pour corriger la vulnérabilité : utiliser des requêtes paramétrées (ex. cursor.execute("SELECT ... WHERE a=? AND b=?", (a,b))) — explication courte incluse plus bas.

Correction : pourquoi ça marche ?
Problème : concaténer directement des entrées utilisateur dans une requête SQL permet à l'attaquant d'injecter du SQL arbitraire.

Solution : utiliser des requêtes paramétrées (placeholders), ce qui dissocie le code SQL des données. La DB traite les entrées comme données même si elles contiennent des caractères spéciaux, empêchant l'interprétation comme code SQL.

Exemple rapide (curl)
Lancement en mode vulnérable :

bash
Copier le code
docker run --rm -p 5000:5000 -e VULNERABLE=1 sql-chal
Exemple d'attaque (voir SOLUTION.md pour détails) :

bash
Copier le code
curl -v -X POST -F "username=' OR '1'='1' -- " -F "password=" http://0.0.0.0:5000/login
Remarques pédagogiques
Les sources sont commentées pour indiquer où se trouve la faille et comment la corriger.

Le drapeau (flag) est FLAG{injection_reussie} et est stocké dans la table flags — il n'est accessible qu'en cas de contournement de l'authentification (vulnérable) ou d'accès légitime (admin).

Bon apprentissage ! 🎓