'''
Proyecto 1 - chat usando protocolo existente
Redes 
Miguel Novella - Seccion 10 
Mirka Monzon 18139
'''
from os import system, name
import getpass

def clear_screen():
    #clear screen
    #para windows
    if name == 'nt':
        _ = system('cls')
    #para mac y linux
    else:
        _ = system('clear')

def enter_para_continuar():
    #continuar
    input("\nPresionar ENTER para continuar.")

def obtener_clave():
    #obtener clave
    try:
        p = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    else:
        return p
    
    return None


def menu():
    #menu principal    
    return '''
    
    Proyecto #1

1. Registrarse
2. Iniciar Sesion
3. Salir
    '''

def menu_inicio():
    #menu al login 

    return '''
    
    Inicia Sesion

    '''

def menu_chat():
    #menu del chat

    return '''
    
    Redes XMPP Chat

1. Listado de contactos
2. Agregar un usuario a tus contactos
3. Mostrar detalles de un usuario
4. Chats Personales
5. Chats Grupales
6. Definir Mensaje de Presencia
7. Enviar un archivo
8. Cerrar Sesion
9. Eliminar cuenta

    '''
