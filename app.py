import hashlib # Importer la librairie hashlib pour générer un hash
import time # Importer la librairie time pour générer un timestamp
import requests # Importer la librairie requests pour faire des requêtes HTTP
from flask import Flask, jsonify # Importer la librairie Flask pour créer une API et jsonify pour retourner du JSON

app = Flask(__name__) # Créer une instance de l'application Flask
app.config.from_pyfile('config.py') # Charger la configuration depuis le fichier config.py

PUBLIC_KEY = app.config['MARVEL_PUBLIC_KEY'] # Récupérer la clé publique depuis la configuration
PRIVATE_KEY = app.config['MARVEL_PRIVATE_KEY'] # Récupérer la clé privée depuis la configuration
BASE_URL = app.config['BASE_URL'] # Récupérer l'URL de base depuis la configuration

def generate_hash(ts, private_key, public_key): # Définir une fonction pour générer un hash
    m = hashlib.md5() # Créer une instance de l'algorithme MD5
    m.update(f"{ts}{private_key}{public_key}".encode('utf-8')) # Mettre à jour le hash avec le timestamp, la clé privée et la clé publique
    return m.hexdigest() # Retourner le hash en hexadécimal

@app.route('/characters') # création d'une route pour récupérer les personnages
def get_characters(): # Définir une fonction pour récupérer les personnages
    ts = str(time.time()) # Générer un timestamp
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY) # Générer un hash avec le timestamp, la clé privée et la clé publique
    params = { # Définir les paramètres de la requête
        'apikey': PUBLIC_KEY,
        'ts': ts,
        'hash': hash,
        'limit': 100
    }
    response = requests.get(f"{BASE_URL}characters", params=params) # Faire une requête HTTP GET sur l'URL de base + characters
    return jsonify(response.json()) # Retourner le JSON de la réponse

@app.route('/characters/<int:character_id>', methods=['GET']) # Créer une route pour récupérer un personnage
def get_character(character_id): # Définir une fonction pour récupérer un personnage
    ts_hash = generer_ts_hash() # Générer un timestamp et un hash
    params = { # Définir les paramètres de la requête
        'apikey': PUBLIC_KEY,
        'ts': ts_hash['ts'],
        'hash': ts_hash['hash']
    }
    response = requests.get(f"{BASE_URL}characters/{character_id}", params=params) # Faire une requête HTTP GET sur l'URL de base + characters + l'identifiant du personnage
    return jsonify(response.json()) # Retourner le JSON de la réponse

def generer_ts_hash():
    ts = str(time.time()) # Générer un timestamp
    hash = generate_hash(ts, PRIVATE_KEY, PUBLIC_KEY) # Générer un hash avec le timestamp, la clé privée et la clé publique
    return {'ts': ts, 'hash' : hash}

app.run(debug=True) # Lancer l'application en mode debug