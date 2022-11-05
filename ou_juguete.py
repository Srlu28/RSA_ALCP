from utils import *
from colorama import Fore,Style

menu_options = {
    1: 'Mostrar los usarios con sus claves públicas.',
    2: 'Enviar a un mensaje cifrado a un usuario.',
    3: 'Salir.'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def generate_users():
    x,y = generate_keys_ou()
    main_user = {"usuario": "usuario_principal",
                 "clave_privada": y,
                 "clave_publica": x}
    users=[]
    for i in range(5):
        x,y = generate_keys_ou()
        users.append( {"usuario": "USUARIO "+ str(i+1),"clave_privada": y,"clave_publica": x})
    return main_user,users

def mostrarUsuarios(main_user,users):
    print('Mostrando información del usuario principal.')
    print(f"{bcolors.OKBLUE}CLAVE PUBLICA: {bcolors.ENDC}")
    print( str(main_user['clave_publica']) )
    print(f"{bcolors.OKBLUE}CLAVE PRIVADA: {bcolors.ENDC}")
    print( str(main_user['clave_privada']))
    print('Mostrando información del resto de usuarios.')
    for user in users:
        print(f"{bcolors.OKBLUE}CLAVE PUBLICA {user['usuario']}: {bcolors.ENDC}")
        print(str(user['clave_publica']))

def enviarMensaje(users):
    try:
        option = -1
        while(option >5 or option <1):
            option = int(input('Seleccione un usario al que mandarle un mensaje: '))
            if (option >5 or option <1):
                print('Usuario inexistente. Introduzca un numero entre 1 y 5.')
        publicKey = users[option-1]['clave_publica']
        mssg = input('Seleccione el mensaje a cifrar: ')
        c = cifrar_ou(mssg,publicKey)
        print('MENSAJE CIFRADO : ')
        print(f"{bcolors.OKBLUE}{c}{bcolors.ENDC}")
        print('Todos los usuarios van a intentar cifrar el mensaje con su clave privada: ')
        for user in users:
            privateKey = user['clave_privada']
            m = descifrar_ou(c,privateKey,publicKey)
            print('DESCIFRADO DE  '+ user['usuario'])
            print(f"{bcolors.OKCYAN}{m}{bcolors.ENDC}")
            
        
    except:
        print('Entrada errónea, por favor introduzca un entero ...')

def main():
    main_user , users = generate_users()
    while(True):
        print("Bienvenido a este programa de juguete de Okamoto-Uchiyanama, seleccione una de las siguientes opciones: ")
        print_menu()
        option = ''
        try:
            option = int(input('Opción: '))
        except:
            print('Entrada erronea, por favor introduzca un entero ...')
        if option == 1:
            mostrarUsuarios(main_user,users)
        elif option == 2:
            enviarMensaje(users)
        elif option == 3:
            print('Finalizando el programa.')
            break
        else:
            print('Opción inválida. Introduzca un numero entre 1 y 4.')

main()