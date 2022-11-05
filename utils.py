import random
from Crypto.Util.number import *
from Crypto import Random
import Crypto
import miller_rabin as mr
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def mcd(a,b):
    """
    Algoritmo de Euclides para devolver el mcd(a,b), lo usaremos para hallar la funcion de Carmichael y comprobar coprimalidad
    """
    if (b==0):
        return a
    else:
        return mcd(b,a%b)

def generar_p_q(bits = 80,e = 65537): 
    """
    Fijado el e al mayor primo de Fermat conocido, hallamos primos y nos aseguramos que sean coprimos con la función de Euler
    (Existen cracks de RSA utilizados cuando e comparte factores con la función de Euler)
    """
    while (True):
        p = mr.generate_probable_prime(bits)
        if mcd(e,p-1)== 1:
            break
    while (True): 
        q = mr.generate_probable_prime(bits)
        if mcd(e,q-1)== 1:
            break

    return p,q

def generate_keys_rsa(bits = 80):
    """
    En esta función crearemos las claves pública y privada para un usuario en el criptosistema RSA.
    """
    e = 65537
    while (True): #Fijado e, generamos los primos y nos aseguramos que e sea coprimo con la función de Carmichael.
        p,q = generar_p_q(bits)
        carmichael = abs((p-1)*(q-1))//mcd((p-1),(q-1))
        if mcd(e,carmichael)==1:
            break
    n = p*q

    d = pow(e,-1,carmichael)
    
    #Una vez calculamos lo necesario, devolvemos las claves.
    publicKey = (e,n)
    privateKey = (d,n)

    return publicKey,privateKey

def generate_keys_ou(bits=80):
    """
    En esta función crearemos las claves pública y privada para un usuario en el criptosistema Okamoto Uchiyama
    """
    #Generamos p y q primos
    p = mr.generate_probable_prime(bits)
    q = mr.generate_probable_prime(bits)

    n=p**2 * q
    while True:
        g = random.randrange(2,n-1) #Escogemos un  g perteneciente al grupo multiplicativo tal que g^{p-1} != 1 mod p^2
        if mcd(g,n)==1 and pow(g,p-1,p**2)!=1:
            break
    h = pow(g,n,n) #h=g^n (mod n)
    #Devolvemos la clave pública y privada
    publicKey=(n,g,h)
    privateKey=(p,q)
    return publicKey,privateKey 


def M_to_m(M,tam_bloque = 2):
    """
    En esta función vamos a transformar el mensaje M a una representación adecuada al algoritmo RSA que llamaremos m.
    """
    bloques = []

    try:
        asc_val = ord(M[0]) # calcula el valor ascii del caracter M[0]
        for i in range(1, len(M)):
            if (i%tam_bloque == 0):
                bloques.append(asc_val)
                asc_val=0
            asc_val = 1000 * asc_val + ord(M[i]) #Los valores de ASCII tienen como máximo 3 cifras 
        bloques.append(asc_val) #pega el último.
        return bloques
    except:
        print("El mensaje no puede estar vacío") 

def m_to_M(int_blocks,tam_bloque=2):
    """
    En esta función vamos a transformar el mensaje m a la representación en letras M
    """
    try:
        message = ""
        for i in range(len(int_blocks)):
            tmp = ""
            for _ in range(tam_bloque): #sacamos por bloque los números de derecha a izquierda 
                tmp = chr(int_blocks[i] % 1000) + tmp #chr es la inversa de ord
                int_blocks[i] //= 1000 #Quitamos la parte que hemos traducido
            message += tmp
        return message
    except:
        print("El mensaje no puede estar vacío") 

def cifrar_rsa(M,clave,tam_bloque = 2):
    e ,n = clave
    m = M_to_m(M)
    cifrado = []
    for bloque in m:
        cifrado.append(str(pow(bloque, e, n))) #cifra bloque^e mod n
    return " ".join(cifrado) #Devuelve una string con los bloques separados.

def descifrar_rsa(c,clave,tam_bloque = 2):
    d ,n = clave
    list_blocks = c.split(' ') #Separamos el string en bloques
    int_blocks = [] #Aqui lo iremos traduciendo

    for s in list_blocks:
            int_blocks.append(int(s))

    for i in range(len(int_blocks)): 
            int_blocks[i] = pow(int_blocks[i], d, n) #desciframos bloque^d mod n
    return m_to_M(int_blocks)

def cifrar_ou(M,clave,tam_bloque = 2):
    n,g,h = clave
    m = M_to_m(M)
    cifrado = []
    r = random.randrange(1,n-1)
    for bloque in m:
        cifrado.append(str(pow(g, bloque, n)*pow(h,r,n))) #cifro por bloque 
    return " ".join(cifrado)

def descifrar_ou(c,clavePrivada,clavePublica,tam_bloque=2):
    p,q = clavePrivada
    n,g,h = clavePublica
    def L(x):
        return (x-1)//p
    list_blocks = c.split(' ')
    int_blocks = []
    for s in list_blocks:
            int_blocks.append(int(s)) #Como antes aqui tenemos los bloques en enteros
    for i in range(len(int_blocks)):
        x = pow(int_blocks[i],p-1,p**2) #c^p-1 mod p^2
        a = L(x) 
        y = pow(g,p-1,p**2) #g^p-1 mod p^2
        b = L(y)
        b_prime = pow(b,-1,p) 
        int_blocks[i]= (a*b_prime)%p #meto en int_blocks el mensaje descifrado
    return m_to_M(int_blocks)
