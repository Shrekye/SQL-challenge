# SOLUTION (uniquement pour l'enseignant) — Exploitation de la vulnérabilité

> **AVERTISSEMENT** : Ces étapes sont fournies **uniquement pour un usage pédagogique et local**. N'utilisez pas ces techniques contre des systèmes réels sans autorisation explicite.

## Contexte
L'application possède un formulaire `/login` qui, en mode vulnérable (`VULNERABLE=1`), construit la requête SQL par concaténation :
```sql
SELECT * FROM users WHERE username = '<USERNAME>' AND password = '<PASSWORD>'
