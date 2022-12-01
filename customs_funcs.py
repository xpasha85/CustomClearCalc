from datetime import datetime
import tabulate


tabulate.PRESERVE_WHITESPACE = True


RATE_UTIL = 20_000
USD = EUR = RUB = float


def util_fizik(year: int):
    year_now = datetime.now().year
    if 3 <= year_now - year:
        percent = 0.26
    else:
        percent = 0.17
    return int(percent * RATE_UTIL)


def poshlina(price_eur: EUR, capacity: int, year: int) -> EUR:
    year_now = datetime.now().year
    if year_now - year < 3:
        p1 = price_eur * 0.48
        if price_eur <= 8500:
            p1 = price_eur * 0.54
            p2 = 2.5 * capacity
        elif price_eur <= 16700:
            p2 = 3.5 * capacity
        elif price_eur <= 42300:
            p2 = 5.5 * capacity
        elif price_eur <= 84500:
            p2 = 7.5 * capacity
        elif price_eur <= 169000:
            p2 = 15 * capacity
        else:
            p2 = 20 * capacity
        return p2 if p2 > p1 else p1
    elif 3 <= year_now - year < 5:
        if capacity <= 1000:
            p = 1.5 * capacity
        elif capacity <= 1500:
            p = 1.7 * capacity
        elif capacity <= 1800:
            p = 2.5 * capacity
        elif capacity <= 2300:
            p = 2.7 * capacity
        elif capacity <= 3000:
            p = 3 * capacity
        else:
            p = 3.6 * capacity
        return p
    else:
        if capacity <= 1000:
            p = 3.0 * capacity
        elif capacity <= 1500:
            p = 3.2 * capacity
        elif capacity <= 1800:
            p = 3.5 * capacity
        elif capacity <= 2300:
            p = 4.8 * capacity
        elif capacity <= 3000:
            p = 5 * capacity
        else:
            p = 5.7 * capacity
        return p


def tamozh_sbor(price_rub: RUB) -> RUB:
    if price_rub <= 200_000:
        return 775
    elif price_rub <= 450_000:
        return 1550
    elif price_rub <= 1_200_000:
        return 3100
    elif price_rub <= 2_700_000:
        return 8530
    elif price_rub <= 4_200_000:
        return 12000
    elif price_rub <= 7_000_000:
        return 20000
    elif price_rub <= 8_000_000:
        return 23000
    elif price_rub <= 9_000_000:
        return 25000
    elif price_rub <= 10_000_000:
        return 27000
    else:
        return 30000


def to_currency(value: float) -> str:
    number_str = round(value, 2)
    str_format = "{:,.2f}".format(number_str)
    str_format = str_format.replace('.', ' ')
    str_format = str_format.replace(',', '.')
    str_format = str_format.replace(' ', ',')
    return str_format


def main():
    # year = 2020
    # print(util_fizik(year))
    # ps = poshlina(180000, 3000, 2021)
    # print(ps)
    caption = ['Вид', 'Сумма руб', 'Сумма $']
    data = [
        ['Пошлина', '244.700,00', '14.600'],
        ['Таможенные сборы', '5.400', '72.40'],
        ['Утилизационный сбор', '5.200', '45.30'],

        ['             Итого:', '264.900,00', '15.100,00' ]
    ]

    t = tabulate.tabulate(data, headers=caption, colalign=("left", "right", "right"))

    print(t)




if __name__ == "__main__":
    main()
