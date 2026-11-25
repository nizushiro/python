import sqlite3

conn = sqlite3.connect("rezerwacje.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS Rezerwacje (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    wydarzenie TEXT,
    nr_miejsca INTEGER,
    imie TEXT
)
""")
conn.commit()

while True:
  print("\n--- SYSTEM REZERWACJI ---")
  print("1. Wyświetl wszystkie rezerwacje")
  print("2. Zarezerwuj miejsce")
  print("3. Anuluj rezerwację (po ID)")
  print("4. Zakończ")

  wybor = input("Wybierz opcję: ")

  if wybor == "1":
    rekordy = cursor.execute(
        "SELECT id, wydarzenie, nr_miejsca, imie FROM Rezerwacje"
    ).fetchall()

    if len(rekordy) == 0:
      print("Brak aktywnych rezerwacji.")
    else:
      print("\n--- LISTA REZERWACJI ---")
      for rekord in rekordy:
        print(
            f"ID: {rekord[0]} | Wydarzenie: '{rekord[1]}' | Miejsce nr:"
            f" {rekord[2]} | Osoba: {rekord[3]}"
        )

  elif wybor == "2":
    wydarzenie = input("Nazwa wydarzenia: ")
    try:
      nr_miejsca = int(input("Numer miejsca: "))
    except ValueError:
      print("Błąd: Numer miejsca musi być liczbą.")

    imie = input("Twoje imię i nazwisko: ")

    istnieje = cursor.execute(
        "SELECT id FROM Rezerwacje WHERE wydarzenie = ? AND nr_miejsca = ?",
        (wydarzenie, nr_miejsca),
    ).fetchone()

    if istnieje:
      print("To miejsce na tym wydarzeniu jest już zajęte!")
    else:
      cursor.execute(
          "INSERT INTO Rezerwacje (wydarzenie, nr_miejsca, imie) VALUES (?, ?,"
          " ?)",
          (wydarzenie, nr_miejsca, imie),
      )
      conn.commit()
      print("Zarezerwowano miejsce pomyślnie.")

  elif wybor == "3":
    try:
      id_rezerwacji = int(input("Podaj ID rezerwacji do anulowania: "))
    except ValueError:
      print("Błąd: ID musi być liczbą.")

    cursor.execute("DELETE FROM Rezerwacje WHERE id = ?", (id_rezerwacji,))
    conn.commit()
    print("Anulowano rezerwację.")

  elif wybor == "4":
    print("Zamykanie programu. Do zobaczenia!")
    break
  else:
    print("Nieznana opcja, wybierz liczbę od 1 do 4.")


cursor.close()
conn.close()