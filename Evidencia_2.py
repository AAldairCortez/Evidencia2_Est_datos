import openpyxl
import datetime
import sys
import csv

evento = {1000: (1, 102, 'Evento Uno ', 3, datetime.date(2022, 10, 20)), 1001: (2, 100,'Evento Dos', 1, datetime.date(2022, 10, 25)), 1002: (3, 101, 'Evento tres', 2, datetime.date(2022, 10, 29)), 1003: (2, 100, 'Evento cuatro', 1, datetime.date(2022, 10, 20))}
cliente = {1: 'Jesus', 2: 'Pedro', 3: 'Aldair'}
sala = {100: ('Grande', 500), 101: ('Mediana', 250), 102: ('Pequena', 100)}
turno_dict = {1:"Matutino", 2:"Vespertino", 3:"Nocturno"}
encontradas = []
disponibles = []

libro = openpyxl.Workbook()
hoja = libro["Sheet"]
hoja.title = "PRIMERA"

with open("Evidendia2_datos_sala.csv", "w", newline = "") as archivo_salaE:
    guardado_sala = csv.writer(archivo_salaE)
    guardado_sala.writerow(("ID sala", "Nombre sala", "Cupo"))
    guardado_sala.writerows([(sclave, sdato[0], sdato[1]) for sclave, sdato in sala.items()])

with open("Evidendia2_datos_cliente.csv", "w", newline = "") as archivo_clienteE:
    guardado_cliente = csv.writer(archivo_clienteE)
    guardado_cliente.writerow(("Clave cliente", "Nombre cliente"))
    guardado_cliente.writerows([(cclave, cdato) for cclave, cdato in cliente.items()])

with open("Evidendia2_datos_evento.csv", "w", newline = "") as archivo_eventoE:
    guardado_evento = csv.writer(archivo_eventoE)
    guardado_evento.writerow(("Folio evento", "Clave cliente","ID sala", "Nombre evento", "Turno", "Fecha"))
    guardado_evento.writerows([(eclave, edato[0], edato[1], edato[2], edato[3], edato[4]) for eclave, edato in evento.items()])

def agregar_evento():
    global evento
    print("\nDespliegue de usuarios registrados: ") 
    print(cliente)
    print("\nSalas registradas:")
    print(sala)
    print("\nRegistro de un evento")
    print("*" *36) 
    print("Revisaremos que seas un usuario registrado")
    #boton_encendido = True
    try:
        r_Cliente = int(input("ingresa tu clave: "))
        if r_Cliente in cliente.keys():
            r_Sala = int(input("Ingresa el ID de la sala que quieres usar: "))
            if r_Sala in sala.keys():
                folio = max(evento.keys(), default=999) + 1
                nombreEvento=input("Ingresa el nombre del evento: ").title()
                turno=int(input("Ingresa un turno (1:Matutino, 2:Vespertino, 3:Nocturno): "))
                if turno in turno_dict.keys():
                    fechaEvento=input("Ingresa la fecha del evento en formato dd/mm/aaaa: ")
                    fechaEvento = datetime.datetime.strptime(fechaEvento,"%d/%m/%Y").date()
                    fecha_actual =datetime.date.today()
                    diasAntes = fechaEvento.day - fecha_actual.day
                    for persona, salon, nevento, nturno, nfecha in evento.values():
                        if (r_Sala == salon) and (fechaEvento == nfecha) and (turno == nturno):
                            print("\n**La fecha y turno no estan disponibles para ese dia, por favor selecciona otra**\n")
                        else:
                            if diasAntes < 2:
                                print("\n**Para reservar una fecha debe hacerlo con al menos 2 dias de anticipación\n**")
                            elif diasAntes >= 2:
                                print("\n**Su reservación ha sido éxitosa**")
                                evento[folio] = r_Cliente, r_Sala, nombreEvento, turno, fechaEvento
                                print(evento)
                                break
                else:
                    print("\n*Turno fuera de los disponibles, por favor ingrese un turno valido*\n") 
            else:
                print("\n**No existe esa sala**\n")
        else:
            print("\n**No estas aun registrado como cliente**\n")
    except ValueError:
        print(f"\n**El valor proporcionado no es compatible con la operación solicitada**\n")
    except Exception:
        print("\nSe ha presentado una excepcion: ")
        print(Exception)

def editarReservacion():
    global evento
    print("\nEdita el nombre de un evento")
    print("*" *36)
    boton = True
    try:
        while boton:
            busqueda_evento=int(input("Ingrese el folio de su evento: "))
            resultado_evento = evento.get(busqueda_evento)
            for persona, salon, nevento, nturno, nfecha in evento.values():
                if busqueda_evento == None:
                    print("\n**El folio no puede quedar vacio, por favor proporcione uno**\n")
                    continue
                if not busqueda_evento in evento.keys():
                    print("\n**Folio no encontrado en eventos, revisa tu respuesta**\n")
                    break
                else:
                    print("Reserva a cambiar:", {resultado_evento[0]},{resultado_evento[1]},{resultado_evento[2]},{resultado_evento[3]},{resultado_evento[4]})
                    nuevo_nevento=input("Nuevo nombre del evento reservado : ")
                    evento.update({busqueda_evento:[persona, salon, nuevo_nevento, nturno, nfecha]})
                    print("**Cambio realizado** ")
                    print(evento[busqueda_evento])
                    boton = False
                    break
    except ValueError:
        print(f"\n**El valor proporcionado no es compatible con la operación solicitada**\n")

def consultar():
    print("\nConsulta de reservaciones")
    print("*" *54)
    encendido_1 = True
    while encendido_1:
        try:
            fecha_consulta=input("Ingresa la fecha del evento en formato dd/mm/aaaa: ")
            fecha_consulta = datetime.datetime.strptime(fecha_consulta,"%d/%m/%Y").date()
            print("\n")
            print("**"*34)
            print("**" + " "*8 + f" REPORTE DE RESERVACIONES PARA EL DÍA {fecha_consulta}" + " " *8 + "**")
            print("**"*34)
            print("{:<15} {:<15} {:<15} {:<15}".format('SALA','NOMBRE','EVENTO', 'TURNO' ))
            print("**"*34)
            for llave,[persona, salon, nevento, nturno, nfecha] in evento.items():
                    if fecha_consulta == nfecha:
                        print("{:<15} {:<15} {:<15} {:<15}".format (salon, persona , nevento, nturno ))
                        encendido_1 = False
            print("*"*25 + " FIN DEL REPORTE  " + "*"*25)
                        
        except ValueError:
            print(f"\n**El valor proporcionado no es compatible con la operación solicitada**\n")
            continue

def agregar_cliente():
    global cliente
    print("\nRegistro de un cliente")
    print("*" *36)
    while True:
        nombreCliente=input("Introduce el nombre: ").title()
        if nombreCliente.strip() == "":
            print("*El nombre no puede quedar vacio, por favor proporcione uno*")
            continue
        else:
            claveCliente = max(cliente.keys(), default=0) + 1
            print("Clave generada unica: ", claveCliente)
            print("**Registro echo**")
            cliente[claveCliente] = nombreCliente
            print(cliente)
            break

def registroSala():
    global sala
    print("\nRegistro de una sala")
    print("*" *36)
    reg_sala = True
    while reg_sala: 
        nombreSala=input("Introduce el nombre de la sala: ").title()
        if nombreSala.strip() == "":
            print("\n*El nombre no puede quedar vacio, por favor proporcione uno*")
            continue
        while reg_sala:   
            try: 
                cupoSala=int(input("Introduce el cupo de la sala: "))
                if cupoSala == 0:
                    print("\n**El cupo de la sala no puede ser 0**")
                    continue
                else:
                    claveSala = max(sala.keys(), default=99) + 1
                    print("Clave generada unica: ", claveSala)
                    print("\n**Registro echo**")
                    sala[claveSala] = nombreSala, cupoSala
                    print(sala)
                    reg_sala = False
            except ValueError:
                print("**La respuesta no es valida**")

#PENDIENTE  -------------------------------------------------------------------------------------------------------------------
def rep_fechas():
    print("\nReporte de reservaciones")
    print("*" *36)
    fecha_consulta = input("Ingresa la fecha del evento en formato dd/mm/aaaa: ")
    fecha_consulta = datetime.datetime.strptime(fecha_consulta,"%d/%m/%Y").date()
    for clave, valor in list(evento.items()):
        nfecha, nturno, salon = (valor[4], valor[3], valor[1])
        if nfecha == fecha_consulta:
            encontradas.append((salon, nturno))
            reservas_ocupadas = set(encontradas)
        for salon in sala.keys():
            for nturno in turno_dict.keys():
                disponibles.append((salon, nturno))
                combinaciones_reservaciones_disponibles = set(disponibles)

                salas_turnos_disponibles = sorted(list(combinaciones_reservaciones_disponibles - reservas_ocupadas))

            print("\n las opciones disponibles para rentar en esa fecha son : ")
            print(f"**Salas disponibles para rentar el {fecha_consulta} **\n")
            print("Salas\t\tTurnos")
            for salon, nturno in salas_turnos_disponibles:
                print(f"{salon}\t\t{nturno[nturno]}")

#PENDIENTE  -------------------------------------------------------------------------------------------------------------------
def exp_reporte():
    print("\nReporte de reservaciones")
    print("*" *36)
    fecha_solicitada = input("Ingrese la fecha del evento (dd/mm/aaaa): ")
    hoja["B1"].value = f"REPORTE DE RESERVACIONES PARA EL DÍA {fecha_solicitada}"
    hoja["A2"].value = "SALA"
    hoja["B2"].value = "CLIENTE"
    hoja["C2"].value = "EVENTO"
    hoja["D2"].value = "TURNO"
    elementos_sala=[(expersona,exsalon,exevento,exturno,exfecha)]
    for  exclave,[expersona,exsalon,exevento,exturno,exfecha] in evento.items():
        if fecha_solicitada == exfecha:
            elementos_sala=[((expersona,exsalon,exevento,exturno,exfecha))]
            for elemento in elementos_sala:
                hoja.append(elemento)
            libro.save("ExcelEvidencia2.xlsx")
            print("Libro creado exitosamente")
        else:
          print("No se guardo su Libro")

def sub_menu_reserva():
    while True:
        print("\n**MENU RESERVACION DE UN EVENTO**")
        print("*" *36 )
        print("1 - Registrar nueva reservacion.")
        print("2 - Modificar descripcion de una reservacion.")
        print("3 - Consultar disponibilidad de salas para una fecha.")
        print("4 - Salir")
        respuesta_reserva = input("\nIndique la opcion deseada: ")
        try:
            respuesta_int2 = int(respuesta_reserva)
        except ValueError:
            print("\n**La respuesta no es valida**\n")
        except Exception:
            print("\nSe ha presentado una excepcion: ")
            print(Exception)

        if respuesta_int2 == 1:
            agregar_evento()

        elif respuesta_int2 == 2:
            editarReservacion()

        elif respuesta_int2 == 3:
            rep_fechas()

        elif respuesta_int2 == 4:
            break

        else: 
            print("\n*Su respuesta no corresponde con ninguna de las opciones*.")

def reportes():
    while True:
        print("\n**MENU REPORTES**")
        print("*" *36)
        print("1 - Reporte en pantalla de reservaciones para una fecha.")
        print("2 - Exportar reporte tabular en Excel.")
        print("3 - Salir.")
        respuesta_reportes = input("\n Indique la opcion deseada: ")
        
        try:
            respuesta_int3 = int(respuesta_reportes)
        except ValueError:
            print("\n**La respuesta no es valida**\n")
        except Exception:
            print("\nSe ha presentado una excepcion: ")
            print(Exception)

        if respuesta_int3 == 1:
            consultar()

        elif respuesta_int3 == 2:
            exp_reporte()

        elif respuesta_int3 == 3:
            break

def menu():
    while True:
        print("\n**MENU DE OPERACIONES**")
        print("*" *36 )
        print("1 - Reservaciones")
        print("2 - Reportes.")
        print("3 - Registrar un cliente")
        print("4 - Registrar una sala ")
        print("5 - Salir")
        respuesta = input("\nIndique la opcion deseada: ")

        try:
            respuesta_int = int(respuesta)
        except ValueError:
            print("\n**La respuesta no es valida**\n")
        except Exception:
            print("\nSe ha presentado una excepcion: ")
            print(Exception)

        if respuesta_int == 1:
            sub_menu_reserva()

        elif respuesta_int == 2:
            reportes()

        elif respuesta_int == 3:
            agregar_cliente()

        elif respuesta_int == 4: 
            registroSala()

        elif respuesta_int == 5:
            print("\n**TERMINO EL MENU DE OPERACIONES**")
            print("*" *36)
            break
        else: 
            print("\n*Su respuesta no corresponde con ninguna de las opciones*.")

menu()



