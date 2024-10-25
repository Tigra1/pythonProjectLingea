import re
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def home():
    return "HW"

if __name__ == "__main__":
    app.run(debug=True)
def find_ean_and_quantity(text):
    # Шаблон для поиска EAN (13-значный штрих-код)
    ean_pattern = r'\b\d{13}\b'
    # Шаблон для поиска однозначного количества (одно число)
    quantity_pattern = r'\b\d\b'

    # Поиск всех EAN кодов и количеств
    ean_codes = re.findall(ean_pattern, text)
    quantities = re.findall(quantity_pattern, text)

    # Проверяем, что количество найденных элементов совпадает
    if len(ean_codes) != len(quantities):
        print("Несоответствие количества EAN и чисел. Проверьте ввод.")
        return

    # Выводим в два столбца
    print(f"{'EAN Code':<20}{'Quantity'}")
    print("-" * 30)
    for ean, qty in zip(ean_codes, quantities):
        print(f"{ean:<20}{qty}")


# Пример текста
text = """
Товар: 5901234123457 количество 5
Товар: 4006381333931 количество 2
Товар: 4006381333931 количество 2
"""

find_ean_and_quantity(text)
