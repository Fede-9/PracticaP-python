from flask import Flask, render_template, request

app = Flask(__name__)

# SI EL METODO O VERBO HTTP NO ESTA ESTABLECIDO, ES UN GET
@app.route('/')
def index():
    return 'Index'

@app.route('/info')
def info():
    """ 
    La libreria request sirve para obtener peticiones
    y en este caso, hacemos una peticion de los argumentos
    que vienen por la ruta, se envian despues del signo (?) 
    con el formato clave=valor
    por ejemplo localhost:5000/info?pag=1&can=10
    argumento pag valor 1
    argumento pag valor 10
    """
    # Accedo a todos los argumentos
    argumentos = request.args
    # Accedo al argumento a traves del metodo get('nombre')
    lista = argumentos.get('lista')
    
    if argumentos != {}:
        return argumentos
    return "No tiene argumentos"

# DEVOLVEMOS UN HTML
# IMPORTAR EL METODO render_template de la libreria Flask, y creamos un template
# (home.html) en
# la carpeta /templates que tiene que estar al mismo nivel que app.py
@app.route('/home')
def home():
    return render_template('home.html')

#Enviar parametros al html
@app.route('/parametros')
def parametros():
    lista_nombres = ["Juan","Pedro", "Jose"]
    return render_template(
        'parametros.html',
        nombres=lista_nombres 
     )

# SEGUNDA PARTE ---> DEFINIR UN LAYOUT
# EL LAYOUT SERA EL TEMPALTE BASE, DONDE EL RESTO DE LOS TEMPLATES
# SE FUSIONARAN A ESTE
@app.route('/modifica') #ruta
def modifica(): #funcion
    return render_template(
        'modificador.html',
        titulo="Modicado"
    ) #retorno

@app.route('/acerca_de') #ruta
def acerca_de(): #funcion
    return render_template(
        'acerca_de.html',
        titulo="Acerca de"
    ) #retorno



if __name__ == '__main__':
    app.run(host="0.0.0.0")