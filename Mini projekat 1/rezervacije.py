from pathlib import Path

from adapters import ConsoleReportWriter, CsvReservationSource
from rezervacije_refaktorisano import ReservationProcessor


def main() -> None:
    """Sastavlja konkretne dijelove i pokrece obradu."""
    source = CsvReservationSource(Path(__file__).with_name("rezervacije.csv"))
    ReservationProcessor(source, ConsoleReportWriter()).run()


if __name__ == "__main__":
    main()
