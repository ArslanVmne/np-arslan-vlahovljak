import csv
from pathlib import Path

from rezervacije_refaktorisano import Report, Reservation


class CsvReservationSource:
    """Cita rezervacije iz CSV fajla."""

    def __init__(self, path: Path) -> None:
        self._path = path

    def get_reservations(self) -> list[Reservation]:
        with open(self._path, encoding="utf-8") as f:
            return [
                Reservation(
                    id=row["id"],
                    gost=row["gost"],
                    soba=row["soba"],
                    dolazak=row["dolazak"],
                    odlazak=row["odlazak"],
                    cijena_noci=row["cijena_noci"],
                    status=row["status"],
                )
                for row in csv.DictReader(f)
            ]


class ConsoleReportWriter:
    """Ispisuje izvjestaj u konzolu."""

    def write(self, report: Report) -> None:
        print("=== IZVJESTAJ O REZERVACIJAMA ===")
        for line in report.lines:
            print(line)
        print("---------------------------------")
        print(f"Obradjeno rezervacija: {report.processed}")
        print(f"Gresaka: {report.errors}")
        print(f"Ukupan prihod: {report.total:.2f} EUR")


if __name__ == "__main__":
    from rezervacije_refaktorisano import ReservationProcessor

    source = CsvReservationSource(Path(__file__).with_name("rezervacije.csv"))
    ReservationProcessor(source, ConsoleReportWriter()).run()