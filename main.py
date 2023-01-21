from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)
# app.config.from_object(__name__)

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

    if (request.method == 'POST' and
        "cl_name" in request.form and
        "cl_surname" in request.form and
        "cl_patronymic" in request.form and
        "cl_ph_number" in request.form and
        "clients_type" in request.form and
        "cl_address" in request.form
    ):

        cur = mysql.connection.cursor()

        cl_name = request.form["cl_name"]
        cl_surname = request.form["cl_surname"]
        cl_patronymic = request.form["cl_patronymic"]
        cl_ph_number = request.form["cl_ph_number"]
        clients_type = request.form["clients_type"]
        cl_address = request.form["cl_address"]

        cur.callproc('add_client_phys', [cl_surname, cl_name, cl_patronymic, clients_type, cl_ph_number, cl_address])

        cur.close()

        mysql.connection.commit()

        return redirect(url_for('add_client'))

    elif request.method == 'GET':
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
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():

    if (request.method == 'POST' and
        "emp_name" in request.form and
        "emp_surname" in request.form and
        "emp_patronymic" in request.form
    ):
        cur = mysql.connection.cursor()

        emp_name = request.form["emp_name"]
        emp_surname = request.form["emp_surname"]
        emp_patronymic = request.form["emp_patronymic"]

        cur.callproc('add_employee', [emp_name, emp_surname, emp_patronymic])

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('add_employee'))

    else:
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
