import tkinter as tk
import sqlite3
from PIL import Image, ImageTk
import os
import subprocess

# Pfad zur Musikdateien und Bildbibliothek
MUSIC_PATH = "path/to/your/music/folder"
IMAGE_LIBRARY_PATH = "path/to/your/image/library/folder"

# Funktion zum Hinzufügen von Musik zur Datenbank
def add_music_to_db(music_file):
    conn = sqlite3.connect("music_database.db")
    c = conn.cursor()
    c.execute("INSERT INTO music (file_path) VALUES (?)", (music_file,))
    conn.commit()
    conn.close()

# Funktion zum Hinzufügen von Bildern zur Bibliothek
def add_image_to_library(image_file):
    conn = sqlite3.connect("music_database.db")
    c = conn.cursor()
    c.execute("INSERT INTO images (file_path) VALUES (?)", (image_file,))
    conn.commit()
    conn.close()

# Funktion zum Erstellen der Ordner, falls sie nicht existieren
def create_folders_if_not_exist():
    # Erstelle den Musikordner, falls er nicht existiert
    if not os.path.exists(MUSIC_PATH):
        os.makedirs(MUSIC_PATH)
        print(f"Music folder created at {MUSIC_PATH}")

    # Erstelle den Bildordner, falls er nicht existiert
    if not os.path.exists(IMAGE_LIBRARY_PATH):
        os.makedirs(IMAGE_LIBRARY_PATH)
        print(f"Image folder created at {IMAGE_LIBRARY_PATH}")

# Funktion, die aufgerufen wird, wenn ein Knopf gedrückt wird
def play_music(music_file, image_file):
    try:
        import pygame
        pygame.mixer.init()
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()

        # Anzeigen des zugeordneten Bildes
        img = Image.open(image_file)
        img.show()

        # Optional: Schließe das Bild-Fenster nach 2 Sekunden automatisch
        root = tk.Tk()
        root.after(2000, root.destroy)
        root.mainloop()

        # Optional: Warte, bis die Musik zu Ende ist, bevor das Bild-Fenster geschlossen wird
        while pygame.mixer.music.get_busy():
            pass
        root.destroy()

    except ImportError:
        print("Die erforderlichen Bibliotheken pygame oder pillow sind nicht installiert.")
    except pygame.error as e:
        print("Fehler beim Abspielen der Musik:", str(e))

# Funktion zum Erstellen der GUI
def create_gui():
    root = tk.Tk()
    root.title("Soundbar")

    # Erstelle die Ordner, falls sie nicht existieren
    create_folders_if_not_exist()

    # Verbindung zur Datenbank herstellen oder erstellen
    conn = sqlite3.connect("music_database.db")
    c = conn.cursor()

    # Datenbanktabellen erstellen, falls sie noch nicht existieren
    c.execute('''CREATE TABLE IF NOT EXISTS music (id INTEGER PRIMARY KEY, file_path TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, file_path TEXT)''')

    # Musikdateien in der Datenbank hinzufügen (kann hier nach Bedarf angepasst werden)
    music_files = os.listdir(MUSIC_PATH)
    for music_file in music_files:
        add_music_to_db(os.path.join(MUSIC_PATH, music_file))

    # Bilder zur Bibliothek hinzufügen (kann hier nach Bedarf angepasst werden)
    image_files = os.listdir(IMAGE_LIBRARY_PATH)
    for image_file in image_files:
        add_image_to_library(os.path.join(IMAGE_LIBRARY_PATH, image_file))

    # Funktion zum Erstellen eines Knopfs mit zugewiesener Musik und Bild
    def create_button(music_file, image_file):
        button = tk.Button(root, text="Play", command=lambda: play_music(music_file, image_file))
        button.pack(side=tk.LEFT)

    # Alle Knöpfe erstellen (hier gehen wir davon aus, dass sowohl Musik als auch Bilder jeweils 30 Einträge haben)
    c.execute("SELECT file_path FROM music LIMIT 30")
    music_files = c.fetchall()
    c.execute("SELECT file_path FROM images LIMIT 30")
    image_files = c.fetchall()

    for music, image in zip(music_files, image_files):
        create_button(music[0], image[0])

    conn.close()

    root.mainloop()

if __name__ == "__main__":
    # Versuche, die erforderlichen Bibliotheken automatisch zu importieren
    try:
        import pygame
        from PIL import Image
    except ImportError:
        # Wenn eine Bibliothek fehlt, installiere sie automatisch
        subprocess.call(["pip", "install", "pygame", "pillow"])
        # Nach der Installation neu starten, um sicherzustellen, dass die Bibliotheken verfügbar sind
        import sys
        import os
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    else:
        # Wenn die erforderlichen Bibliotheken vorhanden sind, erstelle die GUI
        create_gui()
