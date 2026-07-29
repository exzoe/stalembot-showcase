# Security policy

This repository must never contain production credentials, user databases,
logs, backups, private API contracts, or deployment secrets.

Please report a suspected credential leak privately to the repository owner.
Do not open a public issue containing the secret itself.

Before every push, run:

```powershell
python scripts/check.py
```
