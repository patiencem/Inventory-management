from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("login.html")
database={'admin':'admin'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
        return render_template('login.html', info='invalid User')
    else:
            if database[name1]!=pwd:
                return render_template('login.html',info='invalid Password')
            else:
                    return render_template('login.html', name=name1)

                    
if (__name__=="__main__"):
      app.run()
