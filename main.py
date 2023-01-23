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

    if (
            request.method == 'POST' and
            request.form.get("physical_person") != None
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

    elif (
            request.method == 'POST' and
            request.form.get("entity") != None
    ):
        cur = mysql.connection.cursor()

        cl_name = request.form["cl_name"]
        cl_surname = request.form["cl_surname"]
        cl_patronymic = request.form["cl_patronymic"]
        cl_ph_number = request.form["cl_ph_number"]
        clients_type = request.form["clients_type"]
        company_name = request.form["company_name"]
        inn = request.form["inn"]

        cur.callproc('add_client_entity', [cl_surname, cl_name, cl_patronymic, clients_type, cl_ph_number, company_name, inn])

        cur.close()

        mysql.connection.commit()

        return redirect(url_for('add_client'))

    elif request.method == 'GET':
        return render_template('add_client.html', title='Добавить клиента')


@app.route('/search_client', methods=['GET', 'POST'])
def search_client():

    if (request.method == 'POST' and request.form.get("entity") != None):

        cl_phone = request.form['cl_phone']

        return redirect(url_for('search_results_phone', cl_phone=cl_phone))

    elif request.method == 'GET':
        return render_template('search_client.html', title='Поиск клиента')


@app.route('/search_results_phone', methods=['GET'])
def search_results_phone():

    if request.method == 'GET':

        cl_phone = request.args['cl_phone']

        cur = mysql.connection.cursor()

        # cur.callproc('search_phys_client_phone_number', [cl_phone])

        cur.execute('select cl_number from client where client.cl_phone = %s', (cl_phone,))

        client_number = cur.fetchone()

        cur.execute('select client.cl_surname, client.cl_name, client.cl_patronymic, client.cl_type , client.cl_phone, physical_person.cl_address from client, physical_person where (physical_person.cl_number = %s  and client.cl_number = %s);',(client_number[0], client_number[0],))

        results_phys = cur.fetchall()

        cur.execute('select client.cl_surname, client.cl_name, client.cl_patronymic, client.cl_type , client.cl_phone, entity.company_name, entity.inn from client, entity where (entity.cl_number = %s  and client.cl_number = %s);', (client_number[0], client_number[0],))

        results_entity = cur.fetchall()

        cur.close()

        return render_template('search_results_phone.html', title='Поиск по номеру телефона', cl_phone=cl_phone, results_phys=results_phys, results_entity=results_entity )


@app.route('/all_clients', methods=['GET', 'POST'])
def all_clients():
    if request.method == 'GET':

        cur = mysql.connection.cursor()

        cur.callproc('show_client_phys')

        clients_phys = cur.fetchall()

        cur.close()

        cur = mysql.connection.cursor()

        cur.callproc('show_client_entity')

        clients_entity = cur.fetchall()

        cur.close()

        return render_template('all_clients.html', title='Список клиентов', clients_phys=clients_phys, clients_entity=clients_entity)


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
