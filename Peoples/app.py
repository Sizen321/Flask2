"""
С помощью библиотеки faker необходимо создать трои файла:
1. humans.txt - ФИО (hint -> .name(), разделитель запятая)
2. names.txt - Имя (hint -> .first_name())
3. users.txt - Профиль (hint -> .simple_profile(), разделитель запятая)

Создать по 10 строк в каждом файле.
"""
from flask import Flask, render_template
from faker import Faker

app = Flask(__name__)
fake = Faker("ru_RU")


def create_files() -> None:
    """Function to create 3 files."""
    pass


@app.route("/")
def hello():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)