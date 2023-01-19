from flask import Flask, request, render_template
from flask_mysqldb import MySQL



app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'real_estate_agency_3'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():

    if request.method == 'GET':
        return render_template('home.html', title='Главная')


''' CLIENTS '''
@app.route('/add_client', methods=['GET', 'POST'])
def add_client():

    if request.method == 'GET':
        return render_template('add_client.html', title='Добавить клиента')


@app.route('/remove_client', methods=['GET', 'POST'])
def remove_client():

    if request.method == 'GET':
        return render_template('remove_client.html', title='Удалить клиента')


@app.route('/all_clients', methods=['GET', 'POST'])
def all_clients():
    if request.method == 'GET':
        return render_template('all_clients.html', title='Список клиентов')


''' REO '''
@app.route('/add_reo', methods=['GET', 'POST'])
def add_reo():
    if request.method == 'GET':
        return render_template('add_reo.html', title='Добавить объект недвижимости')


@app.route('/remove_reo', methods=['GET', 'POST'])
def remove_reo():
    if request.method == 'GET':
        return render_template('remove_reo.html', title='Удалить объект недвижимости')


@app.route('/all_reos', methods=['GET', 'POST'])
def all_reos():
    if request.method == 'GET':
        return render_template('all_reos.html', title='Список объектов недвижимости')


''' EMPLOYEE '''
@app.route('/add_EMPLOYEE', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'GET':
        return render_template('add_employee.html', title='Добавить сотрудника')


@app.route('/remove_employee', methods=['GET', 'POST'])
def remove_employee():
    if request.method == 'GET':
        return render_template('remove_employee.html', title='Удалить сотрдуника')


@app.route('/all_employees', methods=['GET', 'POST'])
def all_employees():
    if request.method == 'GET':
        return render_template('all_employees.html', title='Список сотрудников')


'''APPLICATION'''
@app.route('/add_application', methods=['GET', 'POST'])
def add_application():
    if request.method == 'GET':
        return render_template('add_application.html', title='Добавить заявку')


@app.route('/remove_application', methods=['GET', 'POST'])
def remove_application():
    if request.method == 'GET':
        return render_template('remove_application.html', title='Удалить заявку')


@app.route('/all_applications', methods=['GET', 'POST'])
def all_applications():
    if request.method == 'GET':
        return render_template('all_applications.html', title='Список заявок')


if __name__ == '__main__':
    app.run(debug=True)
