'''
Proyecto 1 - chat usando protocolo existente
Redes 
Miguel Novella - Seccion 10 
Mirka Monzon 18139
'''

#imports 
from sheet import clear_screen, enter_para_continuar, obtener_clave, menu, menu_inicio, menu_chat
from cliente import DeleteAccount, ListClients, MUC, SendFile, SendMsg, SubscribeClient
from registro import Registro

#main 
if __name__ == '__main__':
    start = True
    while start:

        #pantalla en blanco
        clear_screen()

        #print menu
        print(menu())

        menu_opciones = input("Escoga una opcion: ")
        if menu_opciones == '1':
            #registro
            clear_screen()
            print("\n\t\tRegistrar")
            usuario = input("\nIngresar el nombre de usuario: ")
            clave = None
            while clave == None:
                clave = obtener_clave()

            #configuracion de RegisterBot y plugins de registro
            xmpp = Registro(usuario, clave)

            #soporte para el registro 
            xmpp['xep_0077'].force_registration = True

            #conexion y procesamiento al servidor XMPP
            xmpp.connect()
            xmpp.process(forever=False)
            xmpp.disconnect()
            enter_para_continuar()

        elif menu_opciones == '2':
            #inicio de sesion
            clear_screen()
            print(menu_inicio())

            usuario = input("Ingresa tu nombre de usuario: ")
            clave = None
            while clave == None:
                clave = obtener_clave()

            start_2 = True
            while start_2:
                clear_screen()
                print(menu_chat())

                menu_opciones_2 = input("Ingresa una opcion: ")

                if menu_opciones_2 == '1':
                    #lista de contactos
                    clear_screen()
                    print("\n\t\tLista de contactos\n")

                    xmpp = ListClients(usuario, clave)
                    xmpp.connect()
                    xmpp.process(forever=False)
                    enter_para_continuar()

                elif menu_opciones_2 == '2':
                    #agregar contacto
                    clear_screen()
                    print("\n\t\tAgregar un usuario\n")

                    nuevo_contacto = input("Ingresa nuevo contacto: ")

                    xmpp = SubscribeClient(usuario, password, nuevo_contacto)
                    xmpp.connect()
                    xmpp.process(forever=False)
                    enter_para_continuar()
                
                elif menu_opciones_2 == '3':
                    #iformacion del usuario
                    clear_screen()
                    print("\n\t\tMostrar informacion de un usuario\n")

                    info_contact = input("Ingresa nombre de contacto: ")

                    xmpp = ListClients(usuario, password, info_contact)
                    xmpp.connect()
                    xmpp.process(forever=False)
                    enter_para_continuar()
                
                elif menu_opciones_2 == '4':
                    #chats personales
                    clear_screen()
                    print("\n\t\tChats Personales\n")

                    chat_contacto = input("Ingresar nombre de contacto: ")
                    msg = input(">>")

                    xmpp = SendMsg(usuario, password, chat_contacto, msg)
                    xmpp.connect()
                    xmpp.process(forever=False)

                elif menu_opciones_2 == '5':
                    #chats grupales
                    clear_screen()
                    print("\n\t\tChats Grupales\n")

                    rusuario = input("Ingresa Room de usuario: ")

                    alias = input("Ingresa tu alias: ")

                    xmpp = MUC(usuario, password, rusuario, alias)

                    xmpp.connect()
                    xmpp.process(forever=False)
                
                elif menu_opciones_2 == '6':
                    #mensaje de presencia
                    clear_screen()
                    print("\n\t\tDefinir Mensaje de Presencia\n")

                    msg_precencia = input("Mensaje de presencia: ")

                    xmpp = ListClients(usuario, password, presence_msg=msg_precencia)
                    xmpp.connect()
                    xmpp.process(forever=False)
                
                elif menu_opciones_2 == '7':
                    #enviar archivo
                    clear_screen()
                    print("\n\t\tEnviar un archivo\n")

                    chat_contacto = input("Ingresa nombre de contacto: ")
                    path = input("Ingresa path del archivo: ")

                    xmpp = SendFile(usuario, password, chat_contacto, path)
                    xmpp.connect()
                    xmpp.process(forever=False)
                    enter_para_continuar()
                
                elif menu_opciones_2 == '8':
                    #cerrar sesion
                    wantsToContinue_2 = False
                    usuario = None
                    password = None

                elif menu_opciones_2 == '9':
                    #borrar cuenta

                    xmpp = DeleteAccount(usuario, password)

                    wantsToContinue_2 = False
                    usuario = None
                    password = None
                
                else:
                    print("\nERROR: la opcion ingresada no es valida")
                    enter_para_continuar()
        
        elif menu_opciones == '3':
            #salir
            wantsToContinue = False

        else:
            print("\nERROR: la opcion ingresada no es valida")
            enter_para_continuar()

