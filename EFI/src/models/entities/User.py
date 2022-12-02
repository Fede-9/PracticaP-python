from werkzeug.security import check_password_hash

class Usuario():
   
    # para no pasar el id inicializamos las otras columnas
    def __init__(self, nombre, apellido, username, email, password, estado, fecha_creacion):
        self.nombre = nombre
        self.apellido = apellido
        self.username = username
        self.email = email
        self.password = password
        self.estado = estado
        self.fecha_creacion = fecha_creacion 

        # decorador para no instanciar la clase
    @classmethod
    def check_password(self, hashed_pasword, password):
        return check_password_hash(hashed_pasword, password)

