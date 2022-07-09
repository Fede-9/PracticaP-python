from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, true



app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://BD2021:BD2021itec@143.198.156.171/sql_cometto'

db = SQLAlchemy(app)

class Provincia(db.Model):
    __tablename__ = 'provincia'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

    def __str__(self):
        return self.nombre


class Localidad(db.Model):
    __tablename__ = 'localidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    provincia_id = db.Column(db.Integer, ForeignKey('provincia.id'))
    provincia = db.relationship('Provincia')


@app.route('/provincias')
def provincias():
    provincias = db.session.query(Provincia).all()
    return render_template(
        'provincias.html', 
        provs=provincias
        )

@app.route('/provincias/<id>')
def localidades_provincias(id):
    localidades = db.session.query(Localidad).filter_by(provincia_id = id).all()
    nombre_provincia = localidades[0].provincia
    return render_template(
        'localidades_de_provincias.html',
        localidades = localidades,
        provincia = nombre_provincia
    )

@app.route('/localidades')
def localidades():
    localidades = db.session.query(Localidad).all()
    return render_template(
        'localidades.html', 
        localidades=localidades
        )


if __name__ == '__main__':
    app.run(host="0.0.0.0")