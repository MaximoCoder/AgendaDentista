#CONTROLES QUE HACEN CONSULTAS A LA DB
import flet as ft
#CONEXION A DB
from .conexionDB import *
class Controls:
    def obtenerNombresColumnas(self, nombre_tabla):
            connect = conexion.conexionDB() 
            if connect.is_connected():
                cursor = connect.cursor()
                cursor.execute(f"SELECT * FROM {nombre_tabla}")
                nombres_columnas = [columna[0].upper() for columna in cursor.description]
                return nombres_columnas
            else:
                return None
    
    #Envio de datos
    def submit_data(self, e:ft.TapEvent, row_values):
        try:
            connect = conexion.conexionDB() 
            if connect.is_connected():
                cursor = connect.cursor()
                # Verificar si el registro ya existe
                sql_check = "SELECT * FROM clientes WHERE nombre_cliente = %s AND tel_cliente = %s AND email_cliente = %s"
                cursor.execute(sql_check, row_values)
                if cursor.fetchone() is not None:
                    #print("El registro ya existe.")
                    return False  # Devolver False si el registro ya existe
                else:
                    # Preparar la consulta SQL para insertar el registro
                    sql_insert = "INSERT INTO clientes (nombre_cliente, email_cliente, tel_cliente, fecha_registro) VALUES (%s, %s, %s, now())"
                    cursor.execute(sql_insert, row_values)
                    if cursor.rowcount > 0:
                        connect.commit()  # Confirmar la transacción
                        #print(cursor.rowcount, "record inserted.")
                        return True  # Devolver True si los datos se insertaron correctamente
        except mysql.connector.Error as e:
            print("No se pudo conectar", e)
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
                #print("MySQL connection is closed")
        return False  # Devolver False si los datos no se insertaron
    
    #TRAER LOS DATOS DE LA DB
    def get_data(self, nombre_tabla):
        try:
            connect = conexion.conexionDB()
            if connect.is_connected():
                with connect.cursor() as cursor: 
                    cursor.execute(f"SELECT * FROM {nombre_tabla}")
                    result = cursor.fetchall()
                
                    #Convertir los datos en un diccionario
                    columns = [column[0] for column in cursor.description]
                    rows = [dict(zip(columns, row)) for row in result]
                    #print(rows)
                    return rows
            else:
                return None
        except mysql.connector.Error as e:
            print("No se pudo conectar", e)
        finally:
            if connect.is_connected():
                connect.close()
                #print("MySQL connection is closed")
    #Eliminar registros de la DB
    def delete_data(self, nombre_tabla, condition):
        try:
            connect = conexion.conexionDB()
            if connect.is_connected():
                with connect.cursor() as cursor: 
                    # Ejecuta la sentencia SQL DELETE
                    cursor.execute(f"DELETE FROM {nombre_tabla} WHERE {condition}")
                    # Confirma los cambios
                    connect.commit()
                    #print(cursor.rowcount, "registro(s) eliminado(s)")
            else:
                print("No se pudo conectar a la base de datos")
        except mysql.connector.Error as e:
            print("Ocurrió un error al eliminar el registro:", e)
        finally:
            if connect.is_connected():
                connect.close()
                #print("Conexión a MySQL cerrada")
    #Funcion para editar registros
    def update_data(self, nombre_tabla, row_values, condition):
        try:
            connect = conexion.conexionDB()
            if connect.is_connected():
                with connect.cursor() as cursor:
                    cursor.execute(f"UPDATE {nombre_tabla} SET nombre_cliente = %s, email_cliente = %s, tel_cliente = %s WHERE {condition}", row_values)
                    connect.commit()
                    #print(cursor.rowcount, "record(s) affected")
                    return True  # Retorna True si la actualización fue exitosa
            else:
                print("No se pudo conectar a la base de datos")
        except mysql.connector.Error as e:
            print("Ocurrio un error al actualizar el registro:", e)
        finally:
            if connect.is_connected():
                connect.close()
                #print("Conexión a MySQL cerrada")
    def check_disponibilidad(self, check_values, id_cita=None):
        try: 
            connect = conexion.conexionDB()
            if connect.is_connected():
                cursor = connect.cursor(buffered=True)
                with connect.cursor() as cursor:
                    if id_cita:
                        # Si se proporciona un id_cita, excluye esa cita de la verificación
                        cursor.execute(f"SELECT * FROM citas WHERE fecha = %s AND hora = %s AND id_cita != %s", (*check_values, id_cita))
                    else:
                        cursor.execute(f"SELECT * FROM citas WHERE fecha = %s AND hora = %s", check_values)
                    
                    result = cursor.fetchall()  # Fetch all rows
                    if result:
                        return False  # Retorna False si la cita ya existe
                    else:
                        return True  # Retorna True si la cita no existe
        except mysql.connector.Error as e:
            print("No se pudo conectar", e)
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
                print("MySQL connection is closed")
    def agendar_cita(self , row_values):
        try: 
            #Insertamos los datos luego de verificar que la fecha y hora no esten ocupadas
            connect = conexion.conexionDB()
            if connect.is_connected():
                cursor = connect.cursor(buffered=True)
                #EL HORARIO ESTA DISPONIBLE ENTONCES SE INSERTAN LOS DATOS
                sql_insert = "INSERT INTO citas (nombre_cliente, email_cliente, tipo_cita ,costo_cita ,fecha, hora) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_insert, row_values)
                if cursor.rowcount > 0:
                    connect.commit()  # Confirmar la transacción
                    #print(cursor.rowcount, "record(s) affected, cita agendada.")
                    return True  # Retorna True si se guardaron los datos
        except mysql.connector.Error as e:
            print("Ocurrio un error al agendar una cita:", e)
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
                #print("Conexión a MySQL cerrada")

    def get_citas(self):
        try: 
            connect = conexion.conexionDB()
            if connect.is_connected():
                cursor = connect.cursor(buffered=True)
                with connect.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM citas WHERE estado_cita IS NULL AND fecha >= CURDATE() ORDER BY fecha ASC") #SE trae todo de la tabla de citas
                    result = cursor.fetchall()  # Fetch all rows
                    #Convertir los datos en un formato manejable
                    columns = [column[0] for column in cursor.description]
                    rows = [dict(zip(columns, row)) for row in result]
                    #print(rows)
                    return rows
        except mysql.connector.Error as e:
            print("No se pudo conectar", e)
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
                #print("MySQL connection is closed")

    def cancelar_cita(self, nombre_tabla, condition):
        try:
            connect = conexion.conexionDB()
            if connect.is_connected():
                with connect.cursor() as cursor:
                    cursor.execute(f"DELETE FROM {nombre_tabla} WHERE {condition}")
                    connect.commit()
                    #print(cursor.rowcount, "record(s) affected")
                    return True  # Retorna True si la actualización fue exitosa
            else:
                print("No se pudo conectar a la base de datos")
        except mysql.connector.Error as e:
            print("Ocurrio un error al cancelar la cita:", e)
    def reagendar_cita(self, condition, row_values):
        try: 
            connect = conexion.conexionDB()
            if connect.is_connected():
                cursor = connect.cursor(buffered=True)
                with connect.cursor() as cursor:
                    cursor.execute(f"UPDATE citas SET tipo_cita = %s, costo_cita = %s, fecha = %s, hora = %s WHERE {condition}", row_values)
                    connect.commit()
                    #print(cursor.rowcount, "record(s) affected")
                    return True  # Retorna True si la actualización fue exitosa
        except mysql.connector.Error as e:
            print("Ocurrio un error al reagendar la cita:", e)
        finally:
            if connect.is_connected():
                cursor.close()
                connect.close()
                #print("Conexión a MySQL cerrada")

    