import math

prices = [49.99, 15.50, 120.00]


def calculate_average_price(prices):
    """Vraća prosječnu cijenu zaokruženu na 2 decimale.

    Baca ValueError ako je lista prazna, ako je neka cijena negativna,
    NaN ili beskonačna. Baca TypeError ako cijena nije broj (uključujući bool).
    """
    if not prices:
        raise ValueError("Lista cijena ne smije biti prazna.")

    for price in prices:
        if isinstance(price, bool) or not isinstance(price, (int, float)):
            raise TypeError(f"Cijena mora biti broj, dobijeno: {price!r}")
        if not math.isfinite(price):
            raise ValueError(f"Cijena mora biti konačan broj, dobijeno: {price!r}")
        if price < 0:
            raise ValueError(f"Cijena ne smije biti negativna, dobijeno: {price!r}")

    return round(sum(prices) / len(prices), 2)


if __name__ == "__main__":
    print(f"Prosjecna cijena: {calculate_average_price(prices)}")
