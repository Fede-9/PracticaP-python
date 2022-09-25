from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


# esto se necesita para los mensajes flash es necesario tenerla
app.config['SECRET_KEY'] = 'clave_secretaa'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/flask_contacts'

db = SQLAlchemy(app)


# modelado de la base
class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)

    # para no pasar el id inicializamos las otras columnas
    def __init__(self, fullname, phone, email):
        self.fullname = fullname
        self.phone = phone
        self.email = email

    # def __str__(self):
    #     return self.fullname, self.phone, self.email
        

# rutas
@app.route('/')
def index():
    tabla = db.session.query(Contacts).all()
    data = [contacto for contacto in tabla]

    # print(data)
    return render_template('index.html', contactos = data)



@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        #Comienzo la creacion del objecto Contact
        contact = Contacts(fullname, phone, email)
        db.session.add(contact)
        db.session.commit()
        flash('Contacto agregado correctamente', 'success')

        return redirect(url_for('index'))



@app.route('/edit/<id>')
def get_contact(id):
    contacto = db.session.query(Contacts).filter_by(id=id).first()
    # print(contacto.fullname)
    return render_template('editar.html', contacto = contacto )


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombreCompleto = request.form['fullname']
        celular = request.form['phone']
        correo = request.form['email']
       
        contacto = db.session.query(Contacts).filter_by(id=id).first()
        contacto.fullname = nombreCompleto
        contacto.phone = celular
        contacto.email = correo
        db.session.commit()

        flash('Contacto actualizado correctamente', 'success')
        return redirect(url_for('index'))



@app.route('/delete/<id>')
def delete_contact(id):
    contacto = db.session.query(Contacts).filter_by(id=id).first()
    db.session.delete(contacto)
    db.session.commit()
    flash('Contacto eliminado', 'warning')
    return redirect(url_for('index'))
   




if __name__ == '__main__':
    app.run(debug=True)
