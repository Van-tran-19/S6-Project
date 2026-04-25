import sqlite3
import random
import os

class DatabaseManager:
    def __init__(self, db_name="blindtest.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Concatène le chemin du dossier avec le nom du fichier .db
        self.db_name = os.path.join(base_dir, db_name)
        self.setup_database()

    def get_connection(self):
        # Permet d'avoir des résultats sous forme de dictionnaire (plus facile à manipuler)
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def setup_database(self):
        """Crée les tables si elles n'existent pas déjà."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Table des chansons
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS songs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    title TEXT NOT NULL,
                    phonetic_answers TEXT,
                    difficulty INTEGER DEFAULT 1
                )
            ''')
            
            # Table des sessions joueurs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    total_score INTEGER DEFAULT 0
                )
            ''')
            
            # Table des logs de réaction (L'aspect "Serious Game")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reaction_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    song_id INTEGER,
                    reaction_time_ms REAL,
                    was_correct BOOLEAN,
                    FOREIGN KEY(session_id) REFERENCES sessions(id),
                    FOREIGN KEY(song_id) REFERENCES songs(id)
                )
            ''')
            conn.commit()

    # --- MÉTHODES POUR LES CHANSONS ---

    def add_song(self, filename, artist, title, phonetic_answers, difficulty=1):
        """Ajoute une chanson à la base."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO songs (filename, artist, title, phonetic_answers, difficulty)
                VALUES (?, ?, ?, ?, ?)
            ''', (filename, artist, title, phonetic_answers, difficulty))
            conn.commit()

    def get_random_song(self):
        """Récupère une chanson au hasard pour le jeu."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # L'astuce magique de SQLite : ORDER BY RANDOM()
            cursor.execute('SELECT * FROM songs ORDER BY RANDOM() LIMIT 1')
            return dict(cursor.fetchone())

    # --- MÉTHODES POUR LE SERIOUS GAME (STATS) ---

    def create_session(self, player_name):
        """Crée une nouvelle partie et retourne son ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO sessions (player_name) VALUES (?)', (player_name,))
            conn.commit()
            return cursor.lastrowid

    def log_reaction(self, session_id, song_id, reaction_time_ms, was_correct):
        """Enregistre la performance du joueur sur une chanson."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reaction_logs (session_id, song_id, reaction_time_ms, was_correct)
                VALUES (?, ?, ?, ?)
            ''', (session_id, song_id, reaction_time_ms, was_correct))
            conn.commit()
