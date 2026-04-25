from database import DatabaseManager

def init_test_data():
    db = DatabaseManager()
    
    print("Ajout des musiques de test...")
    
    # Exemples (Assurez-vous que les fichiers existent dans votre dossier "audio/")
    db.add_song(
        filename="audio/queen_we_will_rock_you.mp3",
        artist="Queen",
        title="We Will Rock You",
        phonetic_answers="Kouine, Queen, Wi wil rock you",
        kind="rock",
        difficulty=1
    )
    
    db.add_song(
        filename="audio/mj_billie_jean.mp3",
        artist="Michael Jackson",
        title="Billie Jean",
        phonetic_answers="Mickael Jackson, Billy Jean",
        kind="variety",
        difficulty=2
    )

    db.add_song(
        filename="audio/daftpunk_getlucky.mp3",
        artist="Daft Punk",
        title="Get Lucky",
        phonetic_answers="Daf Punk, Get Luki",
        kind="electro",
        difficulty=1
    )
    
    print("Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_test_data()
