#Traer la clase de base de datos
import hashlib
from .conexionDB import *
class Login:
    @staticmethod
    def authenticate(username, password):
        try:
            connect = conexion.conexionDB() 
            if connect.is_connected():
                cursor = connect.cursor()
                # Aplica SHA1 a la contraseña ingresada
                hashed_password = hashlib.sha1(password.encode()).hexdigest()
                sql = "SELECT * FROM usuarios WHERE nombreUsuario=%s AND password=%s"
                values = (username, hashed_password)
                cursor.execute(sql, values)
                #TRAE EL RESULTADO DE LA CONSULTA
                account = cursor.fetchone()
                if account:
                    return True
                else:
                    return False
        except mysql.connector.Error as e:
            print("No se pudo conectar", e)
    def logOut(self, page):
        page.go("/")