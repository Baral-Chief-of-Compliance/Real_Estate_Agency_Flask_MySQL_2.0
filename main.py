from flask import Flask, request, render_template, redirect, url_for,  session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from config import Config


app = Flask(__name__)
app.config.from_object(Config)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'real_estate_agency_3'

mysql = MySQL(app)


@app.route('/', methods=['GET'])
def home():
    if 'loggedin' in session:
        if request.method == 'GET':

            cur = mysql.connection.cursor()

            cur
            return render_template('home.html', title='Главная')

    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():

    msg = ""

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM operator WHERE op_login = %s AND op_password = %s', (username, password,))

        account = cursor.fetchone()

        if account:

            session['loggedin'] = True
            session['id'] = account['op_number']
            session['username'] = account['op_login']

            return redirect(url_for('home'))

        else:
            msg = 'Неправильный логин/пароль'

    return render_template('login.html', msg=msg)


''' CLIENTS '''


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if 'loggedin' in session:
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

        return redirect(url_for('login'))


@app.route('/search_client', methods=['GET', 'POST'])
def search_client():
    if 'loggedin' in session:

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

    return redirect(url_for('login'))


@app.route('/search_results_phone', methods=['GET'])
def search_results_phone():
    if 'loggedin' in session:
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

        return redirect(url_for('login'))


@app.route('/search_results_surname_name', methods=['GET'])
def search_results_surname_name():
    if 'loggedin' in session:

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

        return redirect(url_for('login'))


@app.route('/all_clients', methods=['GET', 'POST'])
def all_clients():
    if 'loggedin' in session:
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

    return redirect(url_for('login'))


@app.route('/phys_client', methods=['GET', 'POST'])
def phys_client():
    if 'loggedin' in session:

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

    return redirect(url_for('login'))


@app.route('/entity_client', methods=['GET', 'POST'])
def entity_client():
    if 'loggedin' in session:

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

    return redirect(url_for('login'))


''' REO '''


@app.route('/add_reo', methods=['GET', 'POST'])
def add_reo():
    if 'loggedin' in session:

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

    return redirect(url_for('login'))


@app.route('/search_reo', methods=['GET', 'POST'])
def search_reo():
    if 'loggedin' in session:

        if request.method == 'POST':
            reo_address = request.form['reo_address']

            return redirect(url_for('search_result_reo', reo_address=reo_address))

        elif request.method == 'GET':

            return render_template('search_reo.html', title='Найти объект недвижимости')

    return redirect(url_for('login'))


@app.route('/search_result_reo', methods=['GET'])
def search_result_reo():
    if 'loggedin' in session:

        if request.method == 'GET':

            reo_address = request.args['reo_address']

            print(reo_address)

            cur = mysql.connection.cursor()

            cur.callproc('search_real_estate_objects', [reo_address])

            search_result = cur.fetchall()

            print(search_result)

            cur.close()

            return render_template('search_result_reo.html', search_result=search_result)

    return redirect(url_for('login'))


@app.route('/all_reos', methods=['GET', 'POST'])
def all_reos():
    if 'loggedin' in session:

        if request.method == 'GET':

            cur = mysql.connection.cursor()

            cur.callproc('show_real_estate_objects')

            real_estate_objects = cur.fetchall()

            cur.close()

            return render_template('all_reos.html', title='Список объектов недвижимости', real_estate_objects=real_estate_objects)

    return redirect(url_for('login'))


@app.route('/reo_inf', methods=['GET', 'POST'])
def reo_inf():
    if 'loggedin' in session:

        if request.method == 'POST':
            reo_number = request.args['reo_number']

            cur = mysql.connection.cursor()

            cur.callproc('delete_real_estate_objects', [reo_number])

            cur.close()

            mysql.connection.commit()

            return redirect(url_for('all_reos'))

        elif request.method == 'GET':

            reo_number = request.args['reo_number']
            emp_number = request.args['emp_number']

            cur = mysql.connection.cursor()

            cur.callproc('real_estate_objects_inf', [reo_number])

            inf_reo = cur.fetchone()

            cur.close()

            cur = mysql.connection.cursor()

            cur.callproc('employee_inf', [emp_number])

            inf_emp = cur.fetchone()

            cur.close()

            cur = mysql.connection.cursor()

            cur.callproc('show_viewing_history_reo', [reo_number])

            viewing_history = cur.fetchall()

            cur.close()

            return render_template('reo.html', title='Информация об объекте недвижимости', inf_reo=inf_reo, inf_emp=inf_emp, viewing_history=viewing_history)

    return redirect(url_for('login'))


''' EMPLOYEE '''


@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if 'loggedin' in session:

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

    return redirect(url_for('login'))


@app.route('/all_employees', methods=['GET', 'POST'])
def all_employees():
    if 'loggedin' in session:

        if request.method == 'GET':

            cur = mysql.connection.cursor()

            cur.callproc('show_employee')

            employees = cur.fetchall()

            cur.close()

            return render_template('all_employees.html', title='Список сотрудников', employees=employees)

    return redirect(url_for('login'))


@app.route('/employee_inf', methods=['GET', 'POST'])
def employee_inf():
    if 'loggedin' in session:

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

    return redirect(url_for('login'))


'''viewing_history'''


@app.route('/add_viewing_history', methods=['GET', 'POST'])
def add_viewing_history():
    if 'loggedin' in session:

        if request.method == 'POST':
            reo_number = request.args['reo_number']
            emp_number = request.args['emp_number']
            date_view = request.form['date_view']

            print(date_view)

            client_inf = request.form['client-data']
            client_inf = client_inf.split()
            client_phone_number = client_inf[3]

            cur = mysql.connection.cursor()

            cur.callproc('search_client_with_phone', [client_phone_number])

            client_number = cur.fetchone()

            cur.close()

            cur = mysql.connection.cursor()

            cur.callproc('add_viewing_history', [client_number, reo_number, date_view])

            cur.close()

            mysql.connection.commit()

            return redirect(url_for('reo_inf', reo_number=reo_number, emp_number=emp_number))

        if request.method == 'GET':

            reo_number = request.args['reo_number']
            reo_address = request.args['reo_address']

            cur = mysql.connection.cursor()

            cur.callproc('show_all_clients')

            clients = cur.fetchall()

            cur.close()

            return render_template('add_viewing_history.html', reo_number=reo_number, reo_address=reo_address, clients=clients)

    return redirect(url_for('login'))


'''APPLICATION'''


@app.route('/add_application', methods=['GET', 'POST'])
def add_application():
    if 'loggedin' in session:

        if request.method == 'GET':
            return render_template('add_application.html', title='Добавить заявку')

    return redirect(url_for('login'))


@app.route('/remove_application', methods=['GET', 'POST'])
def remove_application():
    if 'loggedin' in session:
        if request.method == 'GET':
            return render_template('remove_application.html', title='Удалить заявку')

    return redirect(url_for('login'))


@app.route('/all_applications', methods=['GET', 'POST'])
def all_applications():
    if 'loggedin' in session:
        if request.method == 'GET':
            return render_template('all_applications.html', title='Список заявок')

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
