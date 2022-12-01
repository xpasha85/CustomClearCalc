import streamlit as st
from constants import *

from customs_funcs import util_fizik, poshlina, tamozh_sbor, to_currency
import tabulate
from datetime import date


tabulate.PRESERVE_WHITESPACE = True





year = None
price = None
capacity = None
currency = None
st.set_page_config(page_title='Калькулятор растаможки авто', page_icon='🚗')
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.header('Калькулятор растаможки авто')

# ------- Данные автомобиля --------
expander_parameters = st.expander('Введите параметры расчета:', True)
with expander_parameters:
    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox('Год выпуска: ', YEARS)
        price = st.number_input('Введите стоимость автомобиля:', min_value=1, step=100, format='%d')
    with col2:
        currency = st.selectbox('Валюта стоимости:', CURRENCYS, 1)
        capacity = st.number_input('Введите объем двигателя (см³):',
                                   min_value=100, max_value=6000, step=100, value=2200)


is_ok_paranetrs = False
if st.button('Рассчитать'):
    if not any([year, price, capacity, currency]):
        is_ok_paranetrs = False
        st.error('Ошибка в исходных данных')
        st.stop()
    else:
        is_ok_paranetrs = True

# ------ Рассчет таможни ---------
if not is_ok_paranetrs:
    st.stop()
expander_result = st.expander('Расчет таможенных платжей', expanded=is_ok_paranetrs)
with expander_result:
    st.text(f'Для расчета были использованы следующие курсы валют: \n'
            f'USD - {round(USD,2)} руб. (1$)\n'
            f'EUR - {round(EUR,2)} руб. (1€) \n'
            f'KRW - {round(KRW * 1000,2)} руб. (1000₩)')
    captions = ['Вид', 'Сумма руб', 'Сумма $']
    price_rub = float(price * rates[currency].rate)
    price_euro = float((price * float(rates[currency].rate)) / EUR)
    poshlina_eur = round(poshlina(price_euro, capacity, year), 2)
    poshlina_rub = round(poshlina(price_euro, capacity, year) * float(EUR), 2)
    poshlina_usd = round(poshlina_rub / USD, 2)
    poshlina_rub_str = to_currency(poshlina_rub)
    poshlina_usd_str = to_currency(poshlina_usd)
    poshlina_row = ['Пошлина', poshlina_rub_str, poshlina_usd_str]

    sbor_rub = tamozh_sbor(price_rub)
    sbor_usd = round(sbor_rub / USD, 2)
    sbor_rub_str = to_currency(sbor_rub)
    sbor_usd_str = to_currency(sbor_usd)
    sbor_row = ['Таможенные сборы', sbor_rub_str, sbor_usd_str]

    util_rub = util_fizik(year)
    util_usd = round(util_rub / USD, 2)
    util_rub_str = to_currency(util_rub)
    util_usd_str = to_currency(util_usd)
    util_row = ['Утилизационный сбор', util_rub_str, util_usd_str]

    itogo_poshlina_rub = poshlina_rub + sbor_rub + util_rub
    itogo_poshlina_usd = round(poshlina_rub / USD, 2)
    itogo_poshlina_rub_str = to_currency(itogo_poshlina_rub)
    itogo_poshlina_usd_str = to_currency(itogo_poshlina_usd)
    itogo_row = ['             Итого:', itogo_poshlina_rub_str, itogo_poshlina_usd_str]

    data = [
        poshlina_row,
        sbor_row,
        util_row,
        itogo_row
    ]
    table = tabulate.tabulate(data, headers=captions, colalign=("left", "right", "right"))

    st.text(table)

# ------- Блок расчета стоимости авто в России ----------
if currency != 'KRW':
    is_price_won = False
else:
    is_price_won = True


expander_russia = st.expander('Рассчет стоимости в РФ', expanded=False)
with expander_russia:
    if not is_price_won:
        st.error('Для рассчетов необходимо использовать валюту KRW')
        st.stop()
    new_price_rub = ((price + KOMISSIYA_WON_PRIMORYE) * KRW_PRIM) + FIZIK_V_BANK
    new_price_rub_str = to_currency(new_price_rub)
    komision_bank = round(itogo_poshlina_rub * 0.015, 2)
    komision_bank_str = to_currency(komision_bank)
    s = f'Стоимость автомобиля: {new_price_rub_str} руб.'
    s += f'\nПошлина: {itogo_poshlina_rub_str} руб.'
    s += f'\nКомиссия за оплату пошлины (1,5%): {komision_bank_str} руб.'
    st.text(s)
    if date.today().year - year <= 2:
        dop_uslugi = 460_000
    else:
        dop_uslugi = 440_000
    dop_uslugi_str = to_currency(dop_uslugi)
    st.text(f'Доп услуги: {dop_uslugi_str} руб.')
    itogo_in_russia = new_price_rub + itogo_poshlina_rub + komision_bank + dop_uslugi
    itogo_in_russia_str = to_currency(itogo_in_russia)
    col1, col2 = st.columns(2)
    with col1:
        st.text(f'\nИтого цена авто (около): ')
    with col2:
        st.subheader(f'{itogo_in_russia_str} руб.')

    st.write('Дополнительно оплачивается:')
    s = f'Комиссия компании: {to_currency(KOMISSIYA_OF_COMPAMY)} руб.\n' \
        f'Физик (физическое лицо для растаможки авто): {to_currency(FIZIK_TAMOZHNYA)} руб. \n' \
        f'СВХ (склад временного хранения): {SVH} \n' \
        f'Мойка, перегон, и дргуая подготовка (если необходимо).'
    st.text(s)