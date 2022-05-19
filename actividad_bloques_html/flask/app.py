from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        'index.html',
    )

@app.route("/info")
def info():
    
    return render_template(
        'info.html',
        )

#AGREGAR UNA RUTA PARA ACERCA DE, QUE RETORNE UN TEMPLATE PARA ACERCA DE:

@app.route("/acerca_de")
def acerca_de():
    return render_template(
        'acerca_de.html',
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0")