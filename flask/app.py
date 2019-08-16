from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

users = []

@app.route("/")
def hello():
    pages = ['/1','/2','/users']
    return render_template('index.html', pages = enumerate(pages))
    

@app.route('/1')
def page_1():
    return render_template('page_2.html')

@app.route('/2', methods=['GET', 'POST'])
def page_2():
    if request.method == 'POST':
        return render_template('hello.html', name = request.form['name'])        
    else:
        return render_template('hello.html')

@app.route('/users', methods=['GET','POST']) 
def list_users():
    global users
    user = ''
    return render_template('users.html', users = enumerate(users))

@app.route('/user/<int:user_id>')
def user_page(user_id):
    global users
    if user_id >= len(users):
        message = 'Такого пользователя не существует!'
        return render_template('error.html', message = message,url_back = url_for('user_page',user_id=user_id))
    user = users[user_id]
    return render_template('user.html', user = user)

@app.route('/user/', methods=['GET','POST'])
@app.route('/user', methods=['GET','POST'])
def new_user():
    global users
    if request.method == 'GET':
        return render_template('new_user.html')
    else:
        user = {}
        user['surname'] = request.form['surname']
        user['user_name'] = request.form['user_name']
        user['lastname'] = request.form['lastname']
        user['age'] = request.form['age']
        user['sex'] = request.form['sex']
        user['login'] = request.form['login']
        if user in users:
            message = 'Пользователь с логином {0} уже существует'.format(user['login'])
            return render_template('error.html', message = message)
        for elem in user:
            message = 'Заполните поле:' + ' ' + elem
            if (type(user[elem]) is str and user[elem] == '') or (type(user[elem]) is int and user[elem] == 0):
                return render_template('error.html', message = message)
        users += [user]
        #return render_template('user.html', user = users[len(users) - 1])
        user_id = len(users) - 1
        return redirect(url_for('user_page', user_id = user_id))


app.run(debug=True)
