import hashlib # Importer la librairie hashlib pour générer un hash
import time # Importer la librairie time pour générer un timestamp
import requests # Importer la librairie requests pour faire des requêtes HTTP
from flask import Flask, jsonify # Importer la librairie Flask pour créer une API et jsonify pour retourner du JSON

app = Flask(__name__) # Créer une instance de l'application Flask
app.config.from_pyfile('config.py') # Charger la configuration depuis le fichier config.py

PUBLIC_KEY = app.config['MARVEL_PUBLIC_KEY'] # Récupérer la clé publique depuis la configuration
PRIVATE_KEY = app.config['MARVEL_PRIVATE_KEY'] # Récupérer la clé privée depuis la configuration
BASE_URL = app.config['BASE_URL'] # Récupérer l'URL de base depuis la configuration

def generate_hash(ts, private_key, public_key):
    m = hashlib.md5()
    m.update(f"{ts}{private_key}{public_key}".encode('utf-8'))
    return m.hexdigest()

@app.route('/characters')
def get_characters():
    ts = str(time.time())
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY)
    params = {
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash,
        'limit': 100
    }
    response = requests.get(f"{BASE_URL}characters", params=params)
    return jsonify(response.json())

app.run(debug=True)