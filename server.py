from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# HTML-шаблон для отображения формы и результатов
html_template = '''
    <form method="POST">
        <label for="text">Введите текст с EAN кодами и количеством:</label><br>
        <textarea id="text" name="text" rows="4" cols="50">{{ request.form.get('text', '') }}</textarea><br><br>
        <input type="submit" value="Отправить">
    </form>

    {% if results %}
        <h2>Результаты:</h2>
        <table border="1">
            <tr><th>EAN Code</th><th>Quantity</th></tr>
            {% for ean, qty in results %}
                <tr><td>{{ ean }}</td><td>{{ qty }}</td></tr>
            {% endfor %}
        </table>
    {% endif %}
'''


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
        return None

    return list(zip(ean_codes, quantities))


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    if request.method == 'POST':
        text = request.form['text']
        results = find_ean_and_quantity(text)
    return render_template_string(html_template, results=results)


if __name__ == '__main__':
    app.run(debug=True)
