from flask import Flask, render_template, redirect, url_for, request


app = Flask(__name__)


tareas = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', tareas=tareas)


@app.route('/agregar/', methods=['GET', 'POST'])
def agregar():
    if request.method == 'GET':
        return render_template('agregar.html')
    else:
        tarea = request.form.get('tarea')
        tareas.append(tarea)
        return redirect('/')




if __name__ == '__main__':
    app.run(debug=True)