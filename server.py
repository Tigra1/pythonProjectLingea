from flask import Flask, request, render_template_string
import re
import os

app = Flask(__name__)

# HTML-шаблон для отображения формы и результатов
html_template = '''
<style>
        .motto {
            display: flex;
            height: 12px;
            flex-direction: column;
            justify-content: center;
            flex-shrink: 0;
            margin-top: 9px;
            color: #fff;
            font-family: "arial", "serif";
            font-size: 10.5px;
            font-style: normal;
            font-weight: 300;
            line-height: 24px;
            letter-spacing: 1px;
            text-transform: uppercase;
            width: max-content;
            text-decoration: none;
        }
        .table-container { 
            display: flex; 
            justify-content: left; 
            gap: 10px; 
            background-color: rgb(231, 227, 227);
            margin-left: 5%;
            padding: 3%;
            max-width: 24%;
        }
        .top-menu-logo {
            margin-left: 5%;
        }
        .top-menu-sale {
            background: #457a0f;
            display: flex;
            height: 60px;
            color: aliceblue;
            padding: 1%;
            position: relative;
        }
        .form {
            margin-left: 5%;
            color: #10185a;
            background-color: rgb(231, 227, 227);
            padding: 1%;
            max-width: fit-content;
        }
        .text {
            margin-left: 5%;
            font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
        }
        .button {
            background-color: #457a0f;
            color: #ffffff;
            width: 30%;
        }
        footer {
            text-align: center;
            margin-top: 2%;
        }
        table {
            background-color: #fff;
            padding: 1%;
        }
</style>

<div class="top-menu-sale"> 
    <div class="top-menu-logo">
        <a href="https://www.lingea.cz" title="lingea" class="top-logo">
            <img src="https://www.lingea.cz/img/lingea/logo-white.svg?v=1" title="lingea" alt="lingea">
        </a>
        <span class="motto">Radost z poznávání</span>
    </div>
</div>
<span class="motto">Radost z poznávání</span>

<label for="text"><h2 class="text">Enter text with EAN codes and quantity:</h2></label>
<form method="POST" class="form">
    <textarea id="text" name="text" rows="4" cols="50">{{ request.form.get('text', '') }}</textarea><br><br>
    <input type="submit" value="Submit" class="button">
</form>

{% if results %}
    <h2 class="text">Result:</h2>
    <div class="table-container"> 
        <table border="1">
            <tr><th>EAN Code</th></tr>
            {% for ean, qty in results %}
                <tr><td>{{ ean }}</td></tr>
            {% endfor %}
        </table> 
        <table border="1">
            <tr><th>Quantity</th></tr>
            {% for ean, qty in results %}
                <tr><td>{{ qty }}</td></tr>
            {% endfor %}
        </table>
    </div>
    <footer>&copy Igor</footer>
{% endif %}
'''


def find_ean_and_quantity(text):
    # Шаблон для поиска EAN (13-значный штрих-код)
    ean_pattern = r'\b\d{13}\b'
    # Шаблон для поиска целого количества (исключаем числа с точкой)
    quantity_pattern = r'(?<!\d\.)\b\d{1,2}\b(?!\.\d)'

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
