import pymysql

# def obtener_conexion():
#     return pymysql.connect(host='ProyectoWeb2024A.mysql.pythonanywhere-services.com',
#                                 user='ProyectoWeb2024A',
#                                 password='grupo3-2024',
#                                 db='ProyectoWeb2024A$bd_proyecto')

def obtener_conexion():
    return pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 db='venta')