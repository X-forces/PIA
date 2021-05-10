import sys
import sqlite3
import datetime
from sqlite3 import Error
def registrar1(articulos,opcion):
    while True:
        try:
            fecha_registro=input("Dime una fecha (dd/mm/aaaa): ")
            fecha_converter = datetime.datetime.strptime(fecha_registro, "%d/%m/%Y").date()
            fecha_actual = datetime.datetime.combine(fecha_converter, datetime.datetime.min.time())
            break
        except:
            print(f"Captura de fecha erronea : {sys.exc_info()[0]}")
    try:
        
        with sqlite3.connect("PIA.db") as conn:
            monto_total=0
            print("\n\t\tRegistrar\n") 
            contador= max(articulos,default=0)+1
            while opcion!='0':
                mi_cursor = conn.cursor()
                while True:
                    try:
                        descripcion = input(f"Escribe la descripcion de la venta {contador}: ")
                        cantidad = int(input("Escribe la cantidad a comprar del articulo: "))
                        precio= float(input("Escribe el precio del articulo: "))
                        space_white=descripcion.isspace()
                        cantidad_descripcion=len(descripcion)
                        total_no_negativo=cantidad*precio
                        if space_white==False and cantidad_descripcion>0 and total_no_negativo>0:
                            valores = {"folio": contador, "descripcion":descripcion.strip(), "cantidad":cantidad,"precio":precio,"fecha_Registro": fecha_actual}
                            compra = (contador,descripcion.upper(),cantidad,precio,cantidad*precio,fecha_registro)
                            monto_total=monto_total+cantidad*precio
                            break
                        else:
                            print("\t<<__Error\tCapturaste no puedes dejar el campo descripcion vacio o tu monto no puede ser negativo__>>")
                    except:
                        print("\n\tVuelve a escribir|..")
                if contador in articulos:
                    articulos[contador].append(compra)
                    mi_cursor.execute("INSERT INTO ARTICULOS VALUES(:folio, :descripcion, :cantidad,:precio)", valores)
                        
                else:
                    articulos[contador]=[]
                    articulos[contador].append(compra)
                    mi_cursor.execute("INSERT INTO VENTAS VALUES(:folio, :fecha_Registro)", valores)
                    mi_cursor.execute("INSERT INTO ARTICULOS VALUES(:folio, :descripcion, :cantidad,:precio)", valores)
                opcion=input("Escribe si deseas continuar (1-Continuar registrando/0-Dejar de registar: ")
            print(f"N° {contador}")
            for i in articulos[contador]:
                print(f"Descripcion: {i[1]} {i[2]}X ${i[3]}\tMonto Total: {i[4]}\n")
            print("\nMonto total a pagar: ",monto_total)
            input("<<Press ENTER to continue>>")
            print("Registro agregado exitosamente")
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            

    return articulos,opcion

    
def LeerFecha_SQL():
    separador='*'
    print("\nConsulta de reportes\n")
    while True:
        try:
            fecha_consultar = input("Dime la fecha a buscar (dd/mm/aaaa): ")
            fecha_consultar = datetime.datetime.strptime(fecha_consultar, "%d/%m/%Y").date()
            break        
        except:
            print("Error al capturar la fecha, Vuelva a capturar....")
    try:
        with sqlite3.connect("PIA.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            criterios = {"fecha":fecha_consultar}
            mi_cursor.execute("SELECT v.ID_VENTAS,a.NOMBRE,a.CANTIDAD,a.PRECIO,a.PRECIO*a.CANTIDAD AS TOTA,v.fecha FROM ARTICULOS as a,VENTAS as v WHERE a.ID_VENTAS=v.ID_VENTAS AND DATE(v.FECHA)=:fecha;", criterios)
            registros = mi_cursor.fetchall()
            total=0
            if registros:
                print("\t\tConsultas de pago")
                print(f"\t\t\t\tFecha {registros[0][5].strftime('%d/%m/%Y')}\n")
                print("Folio\tDescripcion\tCantidad\tPrecio\tTotal")
                for i in registros:
                    total+=i[4] 
                    print(f"   {i[0]}\t{i[1]}\t\t{i[2]}\t${i[3]}\t{i[4]}")
                print("Monto total pagado:",total)
            else:
                print("\nNo hay registros realizados en la fecha indicada\n")
    except sqlite3.Error as e:
        print (e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        if (conn):
            conn.close()
            input("<<Press ENTER to continue>>")

def Leer_SQL(articulos):
    try:
        with sqlite3.connect("PIA.db",detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("SELECT v.ID_VENTAS,a.NOMBRE,a.CANTIDAD,a.PRECIO,a.PRECIO*a.CANTIDAD AS TOTAL,v.Fecha FROM ARTICULOS as a,VENTAS as v where a.ID_VENTAS=v.ID_VENTAS order by v.ID_ventas")
            registros = mi_cursor.fetchall()
            for registro in registros:
                if registro[0] in articulos:
                    articulos[registro[0]].append(registro)
                else:
                    articulos[registro[0]]=[registro]
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    return articulos

articulos={}
Leer_SQL(articulos)
while True:
    print("\n\tMenu prinicpal de Cosmeticos")
    print("1-Registrar una venta")
    print("2-Consultar de ventas de un dia especifico")
    print("X-Salir ")
    opcion = input("Elige una opcion: ")
    if opcion =='1':
        registrar1(articulos,opcion)
    elif opcion =='2':
        LeerFecha_SQL()
    elif opcion =='X':
        print("\nSaliendo...\n")
        break
    else:
        print("\n\nError vuelve a intentarlo\n\n")
        input("<<Press ENTER to continue>>")
