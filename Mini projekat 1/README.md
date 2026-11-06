# Mini projekat 1

Skripta za obradu hotelskih rezervacija iz CSV fajla, refaktorisana primjenom principa S (Single Responsibility) i D (Dependency Inversion). Ispod su svi upiti koje sam koristio da bih došao do krajnjeg rezultata, redom kojim su poslani.

## Upiti

### Upit 1
*(upit s priloženim zadatkom)*

> imam ovaj zadatak. Napravi plan kako da ga odradim. Najvise me buni ova monolitna skripta, ne znam šta je to. Prikacen attachment zadatka.

### Upit 2

> nemam monolitnu skriptu, napravi je

### Upit 3
*(zalijepljena poruka greške pri pokretanju skripte)*

```
OSError: [Errno 22] Invalid argument: 'Mini Projekat 1\rezervacije.csv'
```

### Upit 4
*(zalijepljena poruka greške pri ispisu)*

```
UnicodeEncodeError: 'charmap' codec can't encode character 'ć' in position 31: character maps to <undefined>
```

### Upit 5

> ja bih uklonio taj encoding, i sve čćšžđ karaktere iz csv i py fajla

### Upit 6

> Kontekst: Python 3.13, mala skripta (rezervacije.py) za obradu hotelskih rezervacija iz CSV fajla rezervacije.csv. Trenutno je monolit: čitanje podataka, validacija, poslovna logika (broj noći, popust 10% za 7 i više noći) i ispis su pomiješani u jednoj petlji. Ovo je školski zadatak, pa mi je važno da kod bude jasan i da razumijem svaku odluku.
>
> Zadatak: refaktoriši skriptu primjenom principa S (Single Responsibility) i D (Dependency Inversion), a zatim napiši pytest testove.
>
> Zahtjevi za refaktorisanje:
> 1. Napravi dataclass Reservation (gost, soba, dolazak, odlazak, cijena_noci, status).
> 2. Uvedi dva Protocola (typing.Protocol):
>    - ReservationSource sa metodom get_reservations()
>    - ReportWriter sa metodom write(report)
> 3. Napravi konkretne implementacije: CsvReservationSource i ConsoleReportWriter.
> 4. Napravi klasu ReservationProcessor koja u konstruktor prima source i writer (ne smije direktno koristiti open, csv ni print). Logika cijene (noći, popust) neka bude odvojena funkcija ili klasa.
> 5. Ponašanje mora ostati isto: neispravne rezervacije se preskaču i broje kao greške, otkazane se ignorišu, ispis i ukupan iznos isti kao prije.
> 6. Samo standardna biblioteka, type hints, kratki docstringovi.
>
> Zahtjevi za testove (pytest, fajl test_reservations.py):
> - Napiši najmanje tri testa koja koriste zamjenski izvor podataka (FakeSource sa fiksnom listom rezervacija, bez CSV fajla) i zamjenski writer (FakeWriter koji samo pamti šta je dobio, bez printa).
> - Testovi neka provjere: (a) popust od 10% za boravak od 7 i više noći, (b) otkazane i neispravne rezervacije se ne računaju, (c) ukupan prihod i broj obrađenih rezervacija su tačni.
> - Svaki test ima opisno ime i jedan kratak komentar šta provjerava.
>
> Format odgovora:
> - prijedlog strukture fajlova
> - kod za svaki fajl (uključujući testove)
> - kratko objašnjenje (3 do 5 rečenica) gdje je primijenjen S, a gdje D, i zašto FakeSource radi bez nasljeđivanja
>
> Ne dodaj funkcionalnosti koje nisam tražio.

### Upit 7

> zašto smo razdvojili u posebne fajlove sve?

### Upit 8

> ajde spoj čisto zbog predaje, a mogu dodati pojašnjenje vezano za broj fajlova

### Upit 9

> reservations.py bih preimenovao u rezervacije_refaktorisano.py

## Pojašnjenje broja fajlova

Rješenje se sastoji od četiri koda i jednog CSV fajla:

| Fajl | Uloga |
|---|---|
| `rezervacije_refaktorisano.py` | Logika: `Reservation` i `Report`, Protocoli (`ReservationSource`, `ReportWriter`), obračun cijene i `ReservationProcessor`. Ne koristi `open`, `csv` ni `print`. |
| `adapters.py` | Konkretne implementacije: `CsvReservationSource` (čita CSV) i `ConsoleReportWriter` (ispisuje izvještaj). |
| `rezervacije.py` | monolitna skripta. |
| `test_reservations.py` | Pytest testovi sa `FakeSource` i `FakeWriter`, bez CSV fajla i bez ispisa. |
| `rezervacije.csv` | Ulazni podaci. |

Prvobitno je kod bio razdvojen u više manjih modula (modeli, protocoli, cijena, procesor, adapteri). Zbog predaje sam modele, protocole, logiku cijene i procesor spojio u jedan fajl (`rezervacije_refaktorisano.py`), tako da je broj fajlova manji. Principi S i D se odnose na klase i zavisnosti, a ne na broj fajlova, pa su ostali primijenjeni i nakon spajanja: svaka klasa ima jednu odgovornost, a `ReservationProcessor` zavisi od Protocola, a ne od CSV-a ili `print`-a.

Adaptere sam namjerno ostavio u zasebnom fajlu (`adapters.py`). Tako se u fajlu sa logikom vidi da nema `import csv` ni `print`, a to je upravo ono što D principom želimo pokazati.



