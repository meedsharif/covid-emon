from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def hadnle_form():
  form = {
    "email": request.form['email'],
    "username": request.form['username'],
    "coronasym": request.form.getlist('coronasym'),
    "msg": request.form['msg']
  }

  return "Submitted by " + form.get('username')

if __name__ == '__main__':
    app.run(debug=True)