import sqlite3


conn = sqlite3.connect("biblioteka.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Ksiazki (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tytul TEXT,
    autor TEXT,
    rok INTEGER
)
""")
conn.commit()

while True:
  print("\n--- SYSTEM BIBLIOTEKI ---")
  print("1. Dodaj książkę")
  print("2. Wyświetl książki")
  print("3. Zaktualizuj rok wydania")
  print("4. Usuń książkę")
  print("5. Zakończ")

  wybor = input("Wybierz opcję: ")

  if wybor == "1":
    tytul = input("Tytuł: ")
    autor = input("Autor: ")
    try:
      rok = int(input("Rok wydania: "))
    except ValueError:
      print("Błąd: Wiek/rok musi być liczbą całkowitą.")

    cursor.execute(
        "INSERT INTO Ksiazki (tytul, autor, rok) VALUES (?, ?, ?)",
        (tytul, autor, rok),
    )
    conn.commit()
    print("Dodano książkę pomyślnie.")

  elif wybor == "2":
    rekordy = cursor.execute(
        "SELECT id, tytul, autor, rok FROM Ksiazki"
    ).fetchall()

    if len(rekordy) == 0:
      print("Brak książek w bazie.")
    else:
      print("\n--- LISTA KSIĄŻEK ---")
      for rekord in rekordy:
        print(f"ID: {rekord[0]} | '{rekord[1]}' – {rekord[2]} ({rekord[3]})")

  elif wybor == "3":
    try:
      id_ksiazki = int(input("ID książki do aktualizacji: "))
      nowy_rok = int(input("Nowy rok wydania: "))
    except ValueError:
      print("Błąd: Wprowadź poprawne wartości liczbowe.")

    cursor.execute(
        "UPDATE Ksiazki SET rok = ? WHERE id = ?", (nowy_rok, id_ksiazki)
    )
    conn.commit()
    print("Zaktualizowano rok wydania.")

  elif wybor == "4":
    try:
      id_ksiazki = int(input("ID książki do usunięcia: "))
    except ValueError:
      print("Błąd: ID musi być liczbą.")
    

    cursor.execute("DELETE FROM Ksiazki WHERE id = ?", (id_ksiazki,))
    conn.commit()
    print("Usunięto książkę.")

  elif wybor == "5":
    print("Zamykanie programu. Do zobaczenia!")
    break
  else:
    print("Nieznana opcja, wybierz liczbę od 1 do 5.")

cursor.close()
conn.close()