from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

CONFIRMED = "potvrdjena"
DATE_FORMAT = "%Y-%m-%d"
DISCOUNT_MIN_NIGHTS = 7
DISCOUNT_FACTOR = 0.9  # popust 10%


# --- Modeli ---


@dataclass(frozen=True)
class Reservation:
    """Jedna rezervacija onako kako stize iz izvora (vrijednosti su jos tekst)."""

    id: str
    gost: str
    soba: str
    dolazak: str  # ocekivani format: YYYY-MM-DD
    odlazak: str  # ocekivani format: YYYY-MM-DD
    cijena_noci: str
    status: str


@dataclass
class Report:
    """Rezultat obrade: linije za ispis i zbirni podaci."""

    lines: list[str] = field(default_factory=list)
    processed: int = 0
    errors: int = 0
    total: float = 0.0


# --- Protocoli (apstrakcije od kojih zavisi procesor) ---


class ReservationSource(Protocol):
    """Sve sto zna dati rezervacije (CSV, baza, test podaci...)."""

    def get_reservations(self) -> Iterable[Reservation]: ...


class ReportWriter(Protocol):
    """Sve sto zna ispisati izvjestaj (konzola, fajl, test...)."""

    def write(self, report: Report) -> None: ...


# --- Logika cijene ---


def count_nights(arrival: datetime, departure: datetime) -> int:
    """Vraca broj noci izmedju dolaska i odlaska."""
    return (departure - arrival).days


def calculate_price(nights: int, price_per_night: float) -> float:
    """Vraca ukupnu cijenu, sa popustom za boravak od 7 i vise noci."""
    price = nights * price_per_night
    if nights >= DISCOUNT_MIN_NIGHTS:
        price *= DISCOUNT_FACTOR
    return price


# --- Procesor ---


class ReservationProcessor:
    """Obradjuje rezervacije iz izvora i salje izvjestaj writeru."""

    def __init__(self, source: ReservationSource, writer: ReportWriter) -> None:
        self._source = source
        self._writer = writer

    def run(self) -> None:
        """Validira potvrdjene rezervacije, racuna cijene i ispisuje izvjestaj."""
        report = Report()
        for r in self._source.get_reservations():
            if r.status != CONFIRMED:
                continue
            try:
                arrival = datetime.strptime(r.dolazak, DATE_FORMAT)
                departure = datetime.strptime(r.odlazak, DATE_FORMAT)
                price_per_night = float(r.cijena_noci)
            except ValueError:
                self._add_error(report, f"Rezervacija {r.id}: neispravni podaci, preskacem")
                continue

            nights = count_nights(arrival, departure)
            if nights <= 0:
                self._add_error(report, f"Rezervacija {r.id}: odlazak prije dolaska, preskacem")
                continue

            price = calculate_price(nights, price_per_night)
            report.lines.append(f"{r.gost} (soba {r.soba}): {nights} noci, {price:.2f} EUR")
            report.total += price
            report.processed += 1

        self._writer.write(report)

    @staticmethod
    def _add_error(report: Report, message: str) -> None:
        report.lines.append(message)
        report.errors += 1
