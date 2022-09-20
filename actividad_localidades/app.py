from flask import Flask, flash, render_template, redirect, url_for,request
from enum import unique

# para la conexion a sql
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

# creamos la aplicacion
app = Flask(__name__)

# esto se necesita para los mensajes flash es necesario tenerla
app.config['SECRET_KEY'] = 'clave_secretaa'

#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://usuario:contrasenia@host/nombreDB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BD2021:BD2021itec@143.198.156.171/sqlpalma'


db = SQLAlchemy(app)


# MODELAR LA BASE DE DATOS

class Provincia(db.Model):
    __tablename__ = 'provincia'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    
# para no pasar el id solo inicializamos el nombre
    def __init__(self, nombre):
        self.nombre = nombre

    def __str__(self):
        return self.nombre



class Localidad(db.Model):
    __tablename__ = 'localidad'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    provinciaID = db.Column(db.Integer, ForeignKey("provincia.id"))
    provincia = db.relationship("Provincia")

    def __init__(self, nombre, idProvincia):
        self.nombre = nombre
        self.idProvincia = idProvincia

    def __str__(self):
        return self.nombre


# DEFINIMOS LA PRIMER RUTA PARA EL INDEX
# En el primer parametro recibe la ruta y en el segundo el metodo

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



# RUTAS DE PROVINCIAS

@app.route('/provincias/')
def provincias():
    provincias = db.session.query(Provincia).order_by('nombre').all()
    return render_template(
        'provincias.html',
        # asi le pasamos parametros al front
        provs = provincias
        )


@app.route('/agregar_provincia', methods=['POST'])
def agregar_provincia():
    if request.method == 'POST':
        #Recibo el parametro por el formulario
        nombre = request.form['nombreProvincia']

        # validar nombre provincia
        validar_nombre = db.session.query(Provincia).filter_by(nombre=nombre).first()
        if validar_nombre:
            flash(f'Ya existe la provincia con el nombre {nombre}','warning')
            return redirect(url_for('provincias'))

        #Comienzo la creacion del objecto Provincia
        provincia = Provincia(nombre)
        db.session.add(provincia)
        db.session.commit()
        # mensaje para mostrar al usuario
        flash('Provincia creada correctamente', 'success')
        # esto me redireciona a la funcion provincias
        return redirect(url_for('provincias'))


@app.route('/provincias/editar/<id>', methods=['GET'])
def editar_provincias(id):
    provincia = db.session.query(Provincia).filter_by(id=id).first()
    return render_template(
        'edit_provincia.html',
        provincia = provincia
    )

@app.route('/provincias/borrar/<id>', methods=['GET'])
def borrar_provincias(id):
    provincia = db.session.query(Provincia).filter_by(id=id).first()

    try:
        db.session.delete(provincia)
        db.session.commit()
        flash('Provincia eliminada correctamente', 'success')
    except:
        flash('No es posible eliminar esta provincia ya que esta asociada a localidades', 'danger')
    return redirect(url_for('provincias'))




@app.route('/guardar_edicion_provincia', methods=['POST'])
def guardar_edicion_provincia():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nuevo_nombre']
        validar_nombre = db.session.query(Provincia).filter_by(nombre=nombre).first()
        if validar_nombre:
            flash(f'Ya existe un provincia con el nombre {nombre}','danger')
            return redirect(url_for('provincias'))
        # busco la provincia por el id
        provincia = db.session.query(Provincia).filter_by(id=id).first()
        # modifico el campo deseado
        provincia.nombre = nombre
        # guardo
        db.session.commit()

        flash(f'La provincia cambio su nombre a {provincia}', 'success')
        return redirect(url_for('provincias'))




#  RUTAS  LOCALIDADES


@app.route('/localidades/')
def localidades():
    localidades = db.session.query(Localidad).order_by('nombre').all()
    provincias = db.session.query(Provincia).order_by('nombre').all()
    return render_template(
        'localidades.html',
        locs = localidades,
        provs = provincias
    )


@app.route('/agregar_localidad', methods=['POST'])
def agregar_localidad():
    if request.method == 'POST':
        #Recibo el parametro por el formulario
        nombre = request.form['nombreLocalidad']
        idProvincia = request.form['idProvincia']
        # validar nombre de localidad
        validar_nombre = db.session.query(Localidad).filter_by(nombre=nombre).first()
        if validar_nombre:
            flash(f'Ya existe la localidad con el nombre {nombre}','danger')
            return redirect(url_for('localidades'))

        #Comienzo la creacion del objecto Localidad
        localidad = Localidad(nombre, idProvincia)
        db.session.add(localidad)
        db.session.commit()
        # mensaje para mostrar al usuario
        flash('Localidad creada correctamente', 'success')
        # esto me redireciona a la funcion localidades
        return redirect(url_for('localidades'))



@app.route('/localidades/editar/<id>', methods=['GET'])
def editar_localidades(id):
    localidad = db.session.query(Localidad).filter_by(id=id).first()
    return render_template(
        'edit_localidad.html',
        localidad = localidad
    )


@app.route('/localidades/borrar/<id>', methods=['GET'])
def borrar_localidades(id):
    localidad = db.session.query(Localidad).filter_by(id=id).first()
    try:
        db.session.delete(localidad)
        db.session.commit()
        flash('Localidad eliminada correctamente', 'success')
    except:
        flash('No es posible eliminar esta localidad ya que esta asociada a una provincia', 'danger')
    return redirect(url_for('localidades'))




@app.route('/guardar_edicion_localidad', methods=['POST'])
def guardar_edicion_localidad():
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nuevo_nombre']
        validar_nombre = db.session.query(Localidad).filter_by(nombre=nombre).first()
        if validar_nombre:
            flash(f'Ya existe una localidad con el nombre {nombre}','danger')
            return redirect(url_for('localidades'))
        localidad = db.session.query(Localidad).filter_by(id=id).first()
        localidad.nombre = nombre
        db.session.commit()

        flash(f'La localidad cambio su nombre a {localidad}', 'success')
        return redirect(url_for('localidades'))










if __name__ == '__main__':
    app.run(debug=True)