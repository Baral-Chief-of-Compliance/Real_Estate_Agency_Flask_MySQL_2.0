from flask import Flask


app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/index', methods = ['GET'])
def index():
    return 'здарова бандиты'

if __name__ == '__main__':
    app.run(debug=True)
