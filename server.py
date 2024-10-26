from flask import Flask, request, render_template_string
import re
import os

app = Flask(__name__)

# HTML-шаблон для отображения формы и результатов
html_template = '''
    <form method="POST">
        <label for="text">Введите текст с EAN кодами и количеством:</label><br>
        <textarea id="text" name="text" rows="4" cols="50">{{ request.form.get('text', '') }}</textarea><br><br>
        <input type="submit" value="Отправить">
    </form>
    <style>
        body {
            .table-container { 
            display: flex; 
            justify-content: left; 
            margin: 2px; 
        } 
        }
    </style>
    {% if results %}
        <h2>Результаты:</h2>
        <div class="table-container"> 
            <table border="1">
                <tr><th>EAN Code</th>
                {% for ean in results %}
                    <tr><td>{{ ean }}</td></tr>
                {% endfor %}
            </table> 
            <table border="1">
                <tr><th>Quantity</th></tr>
                {% for qty in results %}
                    <tr><td>{{ qty }}</td></tr>
                {% endfor %}
            </table>
        </div>
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)