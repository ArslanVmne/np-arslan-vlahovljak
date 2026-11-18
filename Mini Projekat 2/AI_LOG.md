# AI_LOG: dnevnik rada s AI alatom

Alat: Claude Code. Za svaki korak: moj prompt, šta je AI predložio ili uradio.

## Tok rada

**1. Prompt** (u cjelosti):

```text
Radim fakultetski zadatak iz softverskih šablona (design patterns) u Pythonu. Ovo je početak mog naprednog programiranja, zato mi treba JEDNOSTAVAN, ŠKOLSKI kod koji mogu u potpunosti da razumijem i odbranim na usmenom. Ne usložnjavaj.

ZADATAK:
1. Factory za ML modele (linearni, stablo odlučivanja, kNN iz scikit-learn)
2. Strategy za metrike i Observer za praćenje treninga
3. Template Method za tok eksperimenta i Decorator za mjerenje vremena
4. Demonstracija na skupu iris, najmanje pet pytest testova
5. README sa Mermaid dijagramom klasa i opisom upotrebe AI alata

OCJENJIVANJE: primjena šablona (2), kvalitet koda i testovi (2), dijagram i README (1), dokumentovan rad sa AI (1).

PRAVILA JEDNOSTAVNOSTI:
- Python i scikit-learn, pytest. Bez dodatnih biblioteka.
- Što manje fajlova i klasa. Svaki šablon u svom malom fajlu, najviše 30 do 50 linija po fajlu.
- Bez naprednih stvari (bez metaklasa, generika, async, složenog nasljeđivanja). Samo obične klase, funkcije i apstraktne klase (abc).
- Jasna imena na engleskom, kratki komentari na srpskom/bosanskom koji objašnjavaju ŠTA radi svaki šablon.
- Svaki šablon mora biti lako prepoznatljiv:
  * Factory: jedna funkcija ili klasa koja na osnovu imena ("linear", "tree", "knn") vraća model.
  * Strategy: nekoliko metrika (npr. accuracy, f1) sa istim interfejsom, bira se pri pozivu.
  * Observer: trening obavještava jednog ili dva posmatrača (npr. ispis u konzolu i čuvanje u listu).
  * Template Method: osnovna klasa sa fiksnim redoslijedom koraka (učitaj podatke, treniraj, evaluiraj, ispiši), podklasa mijenja samo jedan korak.
  * Decorator: dekorator @timed koji mjeri vrijeme funkcije.
- Najmanje 5 pytest testova, svaki kratak i jasan, jedan test za jednu stvar.
- demo.py na iris skupu koji pokazuje sve šablone zajedno.
- README.md: kratak opis, kako pokrenuti, Mermaid dijagram klasa (jednostavan), i odjeljak o korišćenju AI alata.
- AI_LOG.md: bilježi svaki moj prompt, šta je AI predložio i šta sam ja promijenio ili provjerio.

NAČIN RADA:
1. Prvo mi u 5 do 10 rečenica predloži plan i strukturu fajlova. Čekaj potvrdu.
2. Radi jedan šablon po jedan. Nakon svakog napiši 3 do 4 rečenice objašnjenja običnim jezikom: šta je problem, kako šablon to rješava, gdje je u kodu.
3. Nakon svakog koraka pokreni pytest.
4. Na kraju mi postavi 5 pitanja kakva bi profesor mogao postaviti na usmenom, da provjerim da li razumijem.
```

**AI:** Plan sa strukturom fajlova i redoslijedom rada.

**2. Prompt:** Folder je "Mini Projekat 2", a AI_LOG je u redu.

**AI:** Napravio folder i `factory.py` s prvim testovima.

**3. Prompt:** Da li je Factory isto što i abstract method?

**AI:** Objasnio da nije: Factory pravi objekte, a abstract method propisuje šta podklasa mora imati.

**4. Prompt:** dalje.

**AI:** `strategy.py` (`Metric`, `Accuracy`, `F1`, `evaluate`) i 4 testa.

**5. Prompt:** Ne kapiram šta radi `evaluate` i kako bi pozvala F1.

**AI:** Objasnio tok poziva korak po korak.

**6. Prompt:** dalje.

**AI:** `observer.py` (`Observer`, `ConsoleObserver`, `ListObserver`, `Trainer`) i 3 testa.

**7. Prompt:** Gdje je iris skup?

**AI:** Objasnio da se iris učitava tek u koraku `load_data` u Template Methodu.

**8. Prompt:** dalje.

**AI:** `@timed` dekorator i 3 testa.

**9. Prompt:** Možemo li ga nazvati `decorator_timing.py`?

**AI:** Preimenovao fajl i ažurirao import u testovima.

**10. Prompt:** dalje.

**AI:** `template.py` (`Experiment`, `ScaledExperiment`) i 4 testa.

**11. Prompt:** dalje.

**AI:** `demo.py`. Skripta je pala zbog slova "č" u ispisu (Windows konzola), pa je ispis ispravljen.

**12. Prompt:** Ispisi u konzoli nisu jasni.

**AI:** Jasniji naslovi, formatiran rezultat i oznake `[Decorator @timed]` i `[Observer console]`.

**13. Prompt:** Provjera mog razumijevanja: Strategy čuva vrijeme, Observer prati početak i kraj, Decorator mjeri trajanje?

**AI:** Ispravio: vrijeme mjeri Decorator, ne Strategy.

**14. Prompt:** Šta je ispis `[Decorator @timed] train() took ...`?

**AI:** Objasnio da je to trajanje metode `train()` koje ispisuje dekorator.

**15. Prompt:** dalje.

**AI:** `README.md` i prva verzija `AI_LOG.md`, pa 5 pitanja za usmeni.

## Pitanja za usmeni, moji odgovori i ocjena AI-ja

**1. Zašto je `create_model` Factory?**
Moj odgovor: Kod se širi i mijenjao bih ga na više mjesta. Ovako samo na jednom mjestu.
Ocjena: Tačno. Nova vrsta modela dodaje se samo u `create_model`.

**2. Razlika između Strategy i Observer?**
Moj odgovor: Strategy mjeri metrike, a Observer osluškuje događaje, odnosno početak i kraj treninga.
Ocjena: Uglavnom tačno. Strategy ne mjeri samo metrike, nego su metrike zamjenjive klase s istim interfejsom i bira se pri pozivu. Strategy bira *kako* se nešto računa, Observer javlja *da se nešto desilo*.

**3. Šta je fiksno u `Experiment.run()`, a šta mijenja podklasa?**
Moj odgovor: Fiksni su `self.model_name`, `self.metric`, `self.trainer` i observers. `ScaledExperiment` mijenja `load_data`, odnosno dodatno skalira podatke.
Ocjena: Netačno u prvom dijelu. To je konstruktor. Fiksan je redoslijed koraka u `run()` (`load_data`, `train`, `evaluate`, `report`). Drugi dio je tačan.
Šta učim: šablon drži redoslijed koraka u `run()`, a ne konstruktor.

**4. Šta znači `@timed` i čemu služi `@wraps(func)`?**
Moj odgovor: Zaboravio sam ekvivalent, ali `@wraps(func)` čuva originalno ime funkcije. `timed` je wrap funkcija.
Ocjena: Djelimično tačno. Ekvivalent bez znaka `@` je `train = timed(train)`.

**5. Zašto je `Metric` apstraktna klasa?**
Moj odgovor: Svaka metrika mora imati `compute()`, pa je to zajednički interfejs.
Ocjena: Tačno, ali nepotpuno. Dodati: `Metric()` i podklasa bez `compute` bacaju `TypeError`, pa se greška vidi odmah pri pravljenju objekta.

## Šta sam provjerio sam

- Pokrenuo sam sav kod (`python demo.py` i `python -m pytest -q`).
- Pročitao sam kod svakog fajla.
- Tražio sam preimenovanje fajla u `decorator_timing.py` i jasniji ispis u konzoli.
- Odgovorio sam svojim riječima na pitanja za usmeni. Najslabije sam znao Template Method (pitanje 3), pa sam to ponovio.
