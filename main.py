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

    if (request.method == 'POST' and request.form.get("physical_person") != None):

        cl_surname = request.form['cl_surname']
        cl_name = request.form['cl_name']
        cl_patronymic = request.form['cl_patronymic']

        return redirect(url_for('search_results_surname_name', cl_surname=cl_surname, cl_name=cl_name, cl_patronymic=cl_patronymic))


    elif (request.method == 'POST' and request.form.get("entity") != None):

        cl_phone = request.form['cl_phone']

        return redirect(url_for('search_results_phone', cl_phone=cl_phone))

    elif request.method == 'GET':
        return render_template('search_client.html', title='Поиск клиента')


@app.route('/search_results_phone', methods=['GET'])
def search_results_phone():

    if request.method == 'GET':

        cl_phone = request.args['cl_phone']

        results_phys = []
        results_entity = []

        cur = mysql.connection.cursor()

        cur.execute('select cl_number from client where client.cl_phone = %s', (cl_phone,))

        client_number = cur.fetchone()

        if client_number != None:

            cur.callproc('phys_client_inf', [client_number])

            results_phys = cur.fetchall()

            cur.close()

            cur = mysql.connection.cursor()

            cur.callproc('entity_client_inf', [client_number])

            results_entity = cur.fetchall()

            cur.close()

        else:
            cur.close()

        return render_template('search_results_phone.html', title='Поиск по номеру телефона', cl_phone=cl_phone, results_phys=results_phys, results_entity=results_entity)


@app.route('/search_results_surname_name', methods=['GET'])
def search_results_surname_name():

    if request.method == 'GET':

        cl_surname = request.args['cl_surname']
        cl_name = request.args['cl_name']
        cl_patronymic = request.args['cl_patronymic']

        results_phys = []
        results_entity = []

        cur = mysql.connection.cursor()

        cur.execute('select cl_number from client where (client.cl_surname=%s and client.cl_name=%s and client.cl_patronymic = %s )', (cl_surname,cl_name, cl_patronymic))

        client_number = cur.fetchone()

        if client_number != None:

            cur.callproc('phys_client_inf', [client_number])

            results_phys = cur.fetchall()

            cur.close()

            cur = mysql.connection.cursor()

            cur.callproc('entity_client_inf', [client_number])

            results_entity = cur.fetchall()

            cur.close()

        else:

            cur.close()

        return render_template('search_results_surname_name.html', title='Поиск по Фамилии, Имени', results_phys=results_phys, results_entity=results_entity, cl_surname=cl_surname, cl_name=cl_name, cl_patronymic=cl_patronymic)

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


@app.route('/phys_client', methods=['GET', 'POST'])
def phys_client():

    if request.method == 'GET':

        client_number = request.args['cl_number']

        cur = mysql.connection.cursor()

        cur.callproc('phys_client_inf', [client_number])

        results_phys = cur.fetchone()

        cur.close()

        return render_template('phys_client.html', title=f'{results_phys[1]} {results_phys[2]} {results_phys[3]}', results_phys=results_phys)

    elif request.method == 'POST':

        client_number = request.args['cl_number']

        cur = mysql.connection.cursor()

        cur.callproc('delete_phys_client', [client_number])

        cur.close()

        mysql.connection.commit()

        return redirect(url_for('all_clients'))


@app.route('/entity_client', methods=['GET', 'POST'])
def entity_client():

    if request.method == 'GET':

        client_number = request.args['cl_number']

        cur = mysql.connection.cursor()

        cur.callproc('entity_client_inf', [client_number])

        results_entity = cur.fetchone()

        cur.close()

        return render_template('entity_client.html', title=f'{results_entity[1]} {results_entity[2]} {results_entity[3]}', results_entity=results_entity)

    elif request.method == 'POST':

        client_number = request.args['cl_number']

        cur = mysql.connection.cursor()

        cur.callproc('delete_entity_client', [client_number])

        cur.close()

        mysql.connection.commit()

        return redirect(url_for('all_clients'))



''' REO '''
@app.route('/add_reo', methods=['GET', 'POST'])
def add_reo():

    if request.method == 'POST':

        reo_room_type = request.form['reo_room_type']
        reo_type_of_operation = request.form['reo_type_of_operation']
        reo_district = request.form['reo_district']
        reo_address = request.form['reo_address']
        reo_employee_number = request.form['reo_employee_number']
        reo_floor = request.form['reo_floor']
        reo_number_of_rooms = request.form['reo_number_of_rooms']
        reo_availability_of_the_Internet = request.form['reo_availability_of_the_Internet']
        reo_availability_of_furniture = request.form['reo_availability_of_furniture']
        reo_price = request.form['reo_price']


        reo_employee_number = reo_employee_number.split()

        cur = mysql.connection.cursor()

        cur.callproc('show_employee')

        employees = cur.fetchall()

        cur.close()

        emp_number = 0

        for emp in employees:
            if (emp[1] == reo_employee_number[0] and emp[2] == reo_employee_number[1] and emp[3] == reo_employee_number[2]):
                emp_number = emp[0]

        cur = mysql.connection.cursor()

        cur.callproc('add_real_estate_object', [reo_room_type,
                                                reo_type_of_operation,
                                                reo_district,
                                                reo_address,
                                                emp_number,
                                                reo_floor,
                                                reo_number_of_rooms,
                                                reo_availability_of_the_Internet,
                                                reo_availability_of_furniture,
                                                reo_price
                                                ]
        )

        cur.close()

        mysql.connection.commit()

        return redirect(url_for('all_reos'))

    elif request.method == 'GET':
        cur = mysql.connection.cursor()

        cur.callproc('show_employee')

        employees = cur.fetchall()

        cur.close()

        return render_template('add_reo.html', title='Добавить объект недвижимости', employees=employees)


@app.route('/remove_reo', methods=['GET', 'POST'])
def remove_reo():
    if request.method == 'GET':

        return render_template('remove_reo.html', title='Удалить объект недвижимости')


@app.route('/all_reos', methods=['GET', 'POST'])
def all_reos():
    if request.method == 'GET':

        cur = mysql.connection.cursor()

        cur.callproc('show_real_estate_objects')

        real_estate_objects = cur.fetchall()

        for res in real_estate_objects:
            print(res[10])

        cur.close()

        return render_template('all_reos.html', title='Список объектов недвижимости', real_estate_objects=real_estate_objects)


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

        cur.callproc('add_employee', [emp_surname, emp_name, emp_patronymic])

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

        cur = mysql.connection.cursor()

        cur.callproc('show_employee')

        employees = cur.fetchall()

        cur.close()

        return render_template('all_employees.html', title='Список сотрудников', employees=employees)


@app.route('/employee_inf', methods=['GET', 'POST'])
def employee_inf():

    if request.method == 'GET':

        employee_number = request.args['employee_number']

        cur = mysql.connection.cursor()

        cur.callproc('employee_inf', [employee_number])

        employee_inf = cur.fetchone()

        return render_template('employee.html', title=f'{employee_inf[1]} {employee_inf[2]} {employee_inf[3]}', employee_inf=employee_inf)

    elif request.method == 'POST':

        employee_number = request.args['employee_number']

        cur = mysql.connection.cursor()

        cur.callproc('delete_employee', [employee_number])

        cur.close()

        mysql.connection.commit()

        return redirect(url_for('all_employees'))


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
