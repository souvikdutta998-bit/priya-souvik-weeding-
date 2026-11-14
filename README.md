# Priya & Souvik — Wedding Invitation

A mobile-first, continuous-scroll wedding invitation with a scratch-to-reveal date, illustrated couple outfits, reduced-motion support, and a persistent SQLite blessing book.

## Run locally
1. Install Python 3.10+.
2. In this folder run: `python -m venv .venv`
3. Activate the environment and run: `pip install -r requirements.txt`
4. Set a private password before starting:
   - macOS/Linux: `export COUPLE_PASSWORD='choose-a-long-private-password'`
   - Windows PowerShell: `$env:COUPLE_PASSWORD='choose-a-long-private-password'`
5. Start: `python app.py`
6. Open `http://localhost:8000`. Couple-only messages page: `http://localhost:8000/private` (browser sign-in; username defaults to `couple`).

The SQLite database `blessings.sqlite3` is created automatically and stores guest wishes on the server.

## Deployment
Deploy the folder to a Python host that supports Flask and persistent disk storage. Set `COUPLE_PASSWORD` (or `COUPLE_PASSWORD_HASH`) and `COUPLE_USERNAME` as environment variables. Keep the SQLite file on a persistent volume and use HTTPS. Do not deploy with the development server; use a production WSGI server such as Gunicorn (`gunicorn app:app`).

## Important
- Guest wish submissions are saved in SQLite by the Flask backend. A static-only host cannot save messages; the backend must be deployed with the site.
- The private page is protected with HTTP Basic authentication. Use a strong password and HTTPS.
- Update the location text if a more specific venue name/address is available.
- The opening monogram uses the requested A & A; change it to P & S if you prefer the couple's initials.
