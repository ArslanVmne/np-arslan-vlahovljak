from rezervacije_refaktorisano import Report, Reservation, ReservationProcessor


class FakeSource:
    """Zamjenski izvor: vraca fiksnu listu, bez CSV fajla."""

    def __init__(self, reservations: list[Reservation]) -> None:
        self._reservations = reservations

    def get_reservations(self) -> list[Reservation]:
        return self._reservations


class FakeWriter:
    """Zamjenski writer: samo pamti izvjestaj, bez printa."""

    def __init__(self) -> None:
        self.report: Report | None = None

    def write(self, report: Report) -> None:
        self.report = report


def make_reservation(**overrides: str) -> Reservation:
    """Ispravna potvrdjena rezervacija od 3 noci; polja se mogu prepisati."""
    data = {
        "id": "1",
        "gost": "Test Gost",
        "soba": "101",
        "dolazak": "2026-11-10",
        "odlazak": "2026-11-13",
        "cijena_noci": "50.00",
        "status": "potvrdjena",
    }
    data.update(overrides)
    return Reservation(**data)


def run(reservations: list[Reservation]) -> Report:
    writer = FakeWriter()
    ReservationProcessor(FakeSource(reservations), writer).run()
    assert writer.report is not None
    return writer.report


def test_discount_applied_for_seven_or_more_nights():
    # 7 noci po 70.00 = 490.00, uz popust 10% = 441.00
    report = run([make_reservation(odlazak="2026-11-17", cijena_noci="70.00")])
    assert report.total == 441.00


def test_no_discount_below_seven_nights():
    # 6 noci po 70.00 = 420.00, bez popusta
    report = run([make_reservation(odlazak="2026-11-16", cijena_noci="70.00")])
    assert report.total == 420.00


def test_cancelled_and_invalid_reservations_are_not_counted():
    # otkazana se ignorise, a losa cijena i odlazak prije dolaska idu u greske
    report = run(
        [
            make_reservation(id="1"),
            make_reservation(id="2", status="otkazana"),
            make_reservation(id="3", cijena_noci="abc"),
            make_reservation(id="4", odlazak="2026-11-09"),
        ]
    )
    assert report.processed == 1
    assert report.errors == 2
    assert report.total == 150.00


def test_total_revenue_and_processed_count_are_correct():
    # 3 noci x 50 = 150, 1 noc x 60 = 60, 7 noci x 70 x 0.9 = 441 -> 651
    report = run(
        [
            make_reservation(id="1"),
            make_reservation(id="2", odlazak="2026-11-11", cijena_noci="60.00"),
            make_reservation(id="3", odlazak="2026-11-17", cijena_noci="70.00"),
        ]
    )
    assert report.processed == 3
    assert report.errors == 0
    assert report.total == 651.00
