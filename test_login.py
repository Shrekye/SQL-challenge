"""
test_login.py

Script de tests simples pour vérifier :
- qu'en mode vulnérable on peut récupérer le flag via une injection,
- qu'en mode sécurisé la même injection ne le permet pas.

Usage :
- Démarrer l'application (Docker ou local).
- Lancer : python test_login.py

Le script interroge /mode pour savoir si l'application est en mode 'vulnerable' ou 'safe'.
"""
import requests
from urllib.parse import urljoin

BASE = "http://127.0.0.1:5000"  # changer si nécessaire

def get_mode():
    r = requests.get(urljoin(BASE, "/mode"), timeout=5)
    if r.status_code == 200:
        return r.text.strip()
    return None

def attempt_injection_get_flag():
    s = requests.Session()
    payload = "' OR '1'='1' -- "
    login_url = urljoin(BASE, "/login")
    resp = s.post(login_url, data={"username": payload, "password": ""}, timeout=5)
    # Même si la réponse de login est 200/401, on vérifie /flag car c'est la preuve finale
    flag_resp = s.get(urljoin(BASE, "/flag"), timeout=5)
    return flag_resp

def main():
    mode = get_mode()
    if not mode:
        print("Erreur : impossible de joindre /mode. Le serveur est-il lancé sur http://127.0.0.1:5000 ?")
        return

    print(f"Mode détecté sur le serveur : {mode}")

    flag_resp = attempt_injection_get_flag()

    if mode == "vulnerable":
        if flag_resp.status_code == 200 and "FLAG{" in flag_resp.text:
            print("[OK] En mode vulnérable : injection réussie, flag récupéré.")
            print(flag_resp.text)
        else:
            print("[ERREUR] En mode vulnérable : l'injection n'a pas permis de récupérer le flag.")
            print("Status:", flag_resp.status_code)
            print(flag_resp.text)
    else:
        # mode safe : l'injection ne doit pas permettre d'accéder au flag
        if flag_resp.status_code == 200 and "FLAG{" in flag_resp.text:
            print("[ERREUR] En mode sécurisé : le flag a été récupéré (cela ne devrait pas arriver).")
            print(flag_resp.text)
        else:
            print("[OK] En mode sécurisé : l'injection n'a pas permis d'accéder au flag (comportement attendu).")
            print("Status /flag:", flag_resp.status_code)
            print(flag_resp.text)

if __name__ == "__main__":
    main()
