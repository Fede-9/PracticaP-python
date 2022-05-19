from flask import Flask, request

app = Flask(__name__)




# si el metodo o verbo HTTP no esta establecido, es un get 
@app.route('/')
def index():
    return 'index'



@app.route('/info')
def info():
    argumentos = request.args # obtiene los argumentos de la url
    lista = argumentos.get('lista') # obtiene el argumento lista
    print(type(lista))

    for x in [lista]:
        print(x)
    if argumentos != {}: 
        return argumentos
    return 'No tiene argumentos'
    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)