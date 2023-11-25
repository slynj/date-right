from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def testing():
    userLocationInput = request.form['user']
    partnerLocationInput = request.form['partner']

    midpoint = (int(userLocationInput) + int(partnerLocationInput)) / 2

    return str(midpoint)




if __name__ == '__main__':
    app.run(debug=True)
