class Ksiazka:

    def __init__(self, tytul, autor, rok_wydania):
        self.tytul = tytul
        self.autor = autor
        self.rok_wydania = rok_wydania

    def __str__(self):
        return "'" + self.tytul + "', '" + self.autor + "'"

    def __eq__(self, other):
        return self.tytul == other.tytul

    def __hash__(self):
        return hash(len(self.tytul) * len(self.autor))


def get_input():
    return int(input())


class Biblioteka:
    def __init__(self, egzemplarze: dict, limit_wypozyczen: int):
        self.limit_wypozyczen = limit_wypozyczen
        self.egzemplarze = egzemplarze
        self.wypozyczenia = {}

    def dodaj_egzemplarz_ksiazki(self, tytul: str, autor: str, rok_wydania: int) -> bool:

        if not Ksiazka(tytul, autor, rok_wydania) in self.egzemplarze.keys():
            self.egzemplarze[Ksiazka(tytul, autor, rok_wydania)] = 1
            return True
        else:
            self.egzemplarze[Ksiazka(tytul, autor, rok_wydania)] += 1
            return True

    def wypozycz(self, nazwisko, tytul) -> bool:
        tytuly = map(lambda x: x.tytul, self.egzemplarze.keys())
        if tytul not in tytuly:
            return False
        elif self.obecna_liczba_egzemplarzy_dla(tytul) <= 0:
            return False
        elif len(list(tytuly)) > self.limit_wypozyczen:
            return False
        elif nazwisko not in self.wypozyczenia.keys():
            self.wypozyczenia[nazwisko] = [tytul]
            self.zmniejsz_liczbe_dostepnych_egzemplarzy(tytul)
            return True
        else:
            if self.czy_juz_posiada(tytul, nazwisko):
                return False
            self.wypozyczenia[nazwisko].append(tytul)
            self.zmniejsz_liczbe_dostepnych_egzemplarzy(tytul)
            return True

    def zmniejsz_liczbe_dostepnych_egzemplarzy(self, tytul: str):
        for ksiazka in self.egzemplarze.keys():
            if ksiazka.tytul == tytul:
                obecna_liczba_egzemplarzy = self.egzemplarze[ksiazka]
                obecna_liczba_egzemplarzy -= 1
                self.egzemplarze[ksiazka] = obecna_liczba_egzemplarzy

    def zwieksz_liczbe_dostepnych_egzemplarzy(self, tytul: str):
        for ksiazka in self.egzemplarze.keys():
            if ksiazka.tytul == tytul:
                obecna_liczba_egzemplarzy = self.egzemplarze[ksiazka]
                obecna_liczba_egzemplarzy += 1
                self.egzemplarze[ksiazka] = obecna_liczba_egzemplarzy

    def oddaj(self, nazwisko, tytul):
        tytuly = map(lambda x: x.tytul, self.egzemplarze.keys())
        if tytul not in tytuly:
            return False
        elif nazwisko not in self.wypozyczenia.keys():
            return False
        else:
            if tytul in self.wypozyczenia[nazwisko]:
                self.wypozyczenia[nazwisko].remove(tytul)
                self.zwieksz_liczbe_dostepnych_egzemplarzy(tytul)
                return True
            else:
                return False

    def obecna_liczba_egzemplarzy_dla(self, tytul: str):
        for ksiazka in self.egzemplarze.keys():
            if ksiazka.tytul == tytul:
                return self.egzemplarze[ksiazka]

    def czy_juz_posiada(self, tytul:str, nazwisko:str):
        return tytul in self.wypozyczenia[nazwisko]

print('liczba akcji: ')
liczba_akcji = get_input()

biblioteka = Biblioteka({}, 3)

for i in range(0, liczba_akcji):
    data = eval(input())
    if (data[0] == ' dodaj '):
        print(biblioteka.dodaj_egzemplarz_ksiazki(data[1], data[2], data[3]))
    elif (data[0] == ' wypozycz '):
        print(biblioteka.wypozycz(data[1], data[2]))
    elif (data[0] == ' oddaj '):
        print(biblioteka.oddaj(data[1], data[2]))

