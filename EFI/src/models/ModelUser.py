from .entities.User import Usuario


class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, nombre, apellido, username, password, estado, fecha_creacion FROM usuario WHERE username = '{}' """.format(user.username) 
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=Usuario(row[0],row[1],row[2],row[3],Usuario.check_password(row[4], user.password), row[5], row[6])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)