from utils import *
from colorama import Fore,Style

menu_options = {
    1: 'Mostrar los usarios con sus claves públicas.',
    2: 'Enviar a un mensaje cifrado a un usuario.',
    3: 'Firmar un mensaje.',
    4: 'Salir.'
}

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def generate_users():
    x,y = generate_keys_rsa()
    main_user = {"usuario": "usuario_principal",
                 "clave_privada": y,
                 "clave_publica": x}
    users=[]
    for i in range(5):
        x,y = generate_keys_rsa()
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
        c = cifrar_rsa(mssg,publicKey)
        print('MENSAJE CIFRADO : ')
        print(f"{bcolors.OKBLUE}{c}{bcolors.ENDC}")
        print('Todos los usuarios van a intentar cifrar el mensaje con su clave privada: ')
        for user in users:
            privateKey = user['clave_privada']
            m = descifrar_rsa(c,privateKey)
            print('DESCIFRADO DE  '+ user['usuario'])
            print(f"{bcolors.OKCYAN}{m}{bcolors.ENDC}")
        
    except:
        print('Entrada errónea, por favor introduzca un entero ...')

def firmarMensaje(main_user):
    mssg = input('Seleccione el mensaje a firmar: ')
    privateKey = main_user['clave_privada']
    publicKey = main_user['clave_publica']
    c = cifrar_rsa(mssg,privateKey)
    print('Para firmar este texto se usara mi clave privada: ')
    print(f"{bcolors.OKBLUE}{str(privateKey)}{bcolors.ENDC}")
    print('El texto cifrado ahora es: ')
    print(f"{bcolors.OKGREEN}{c}{bcolors.ENDC}")
    print('Cualquier usuario puede usar mi clave pública: ')
    print(f"{bcolors.OKBLUE}{str(publicKey)}{bcolors.ENDC}")
    print('El uso de mi clave pública permite verificar que el emisor del mensaje soy yo')
    print('El texto descifrado es : ')
    print(f"{bcolors.OKGREEN}{descifrar_rsa(c,publicKey)}{bcolors.ENDC}")



def main():
    main_user , users = generate_users()
    while(True):
        print("Bienvenido a este programa de juguete de RSA, seleccione una de las siguientes opciones: ")
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
            firmarMensaje(main_user)
        elif option == 4:
            print('Finalizando el programa.')
            break
        else:
            print('Opción inválida. Introduzca un numero entre 1 y 4.')

main()