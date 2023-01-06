from flask import Flask, request, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'real_estate_agency_3'

mysql = MySQL(app)


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():

    if request.method == 'GET':
        return render_template('add_client.html', title='Добавить клиента')


if __name__ == '__main__':
    app.run(debug=True)
