"""
С помощью библиотеки faker необходимо создать трои файла:
1. humans.txt - ФИО (hint -> .name(), разделитель запятая)
2. names.txt - Имя (hint -> .first_name())
3. users.txt - Профиль (hint -> .simple_profile(), разделитель точка с запятой)

Создать по 10 строк в каждом файле.
"""
import sys
from flask import Flask, abort, render_template
from faker import Faker

app = Flask(__name__)
fake = Faker("ru_RU")


def create_files() -> None:
    """Function to create 3 files."""
    with open("./files/humans.txt", "w", encoding="utf-8") as humans_f:
        for _ in range(10):
            print(*fake.name().split(), sep=',', file=humans_f)

    with open("./files/names.txt", "w", encoding="utf-8") as names_f:
        for _ in range(10):
            print(*fake.first_name().split(), sep=',', file=names_f)

    with open("./files/users.txt", "w", encoding="utf-8") as users_f:
        for _ in range(10):
            print(*fake.simple_profile().values(), sep=';', file=users_f)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/names")
def get_names():
    names = list()
    with open("./files/names.txt", encoding="utf-8") as f:
        for raw_line in f:
            names.append(raw_line.strip())
        # return "<br>".join(names)
    return render_template("names.html", people_names=names) # {"people_names": name}


@app.route("/table")
def get_table():
    entities = list()
    with open("files/humans.txt", encoding="utf-8") as f: 
        for raw_line in f:
            data = raw_line.strip().split(',')
            entities.append({'last_name': data[0], 
            'name': data[1], 'surname': data[2]})
    return render_template('table.html', entities=entities)


@app.route("/users") 
def users_list():
    entities = list()
    with open('files/users.txt', encoding="utf-8") as f: 
        for raw_line in f:
            data = raw_line.strip().split(';')
            names = data[1].split()
            entities.append({'login': data[0], 'last_name': names[0], 
                            'name': names[1], 'surname': names[2], 
                            'birth_date' : data[5], 'email': data[4]})
    return render_template('users_list.html', entities=entities)


@app.route("/users/<login>") 
def user_info(login):
    item = None
    with open('files/users.txt', encoding="utf-8") as f: 
        for raw_line in f:
            data = raw_line.strip().split(';') 
            names = data[1].split()
            if data[0] == login:
                item = {'login': data[0], 'last_name': names[0], 'name': names[1], 
                    'surname': names[2], 'birth_date' : data[5], 'email': data[4]} 
                break
    if item is None: 
        abort(404)
    return render_template('user_item.html', item=item)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--files":
        create_files()
    app.run(debug=True)