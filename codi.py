import pygame
import time
from drawMagatzem import draw



def obtenirMagatzem(filePath):
    # Abrimos el archivo del almacén y leemos todas las líneas
    with open(filePath, 'r') as file:
        lines = file.readlines()

    # Procesamos la posición inicial del robot (primera línea del archivo)
    robot_posicio = lines[0].strip().split(';')
    error = False
    if len(robot_posicio) < 2:
        error = True
        print("Formato inesperado en la primera línea: " + lines[0].strip())

    if error == False:
        fila_robot = ord(robot_posicio[0].strip().upper()) - 65  # Convertimos letra a índice de fila
        columna_robot = int(robot_posicio[1].strip()) - 1  # Convertimos columna a índice

        # Procesamos las filas del almacén (resto del archivo)
        magatzem = []
        for line in lines[1:]:
            fila = []
            elementos = line.strip().split(';')
            for elemento in elementos:
                if elemento == '-' or elemento.strip() == '':
                    fila.append(' ')  # Casilla vacía
                else:
                    tipus, codi = elemento.split(',')  # Dividimos en tipo y código
                    fila.append((tipus.strip(), codi.strip()))
            magatzem.append(fila)

        num_filas_originales = len(magatzem)
        num_columnas_originales = len(magatzem[0]) 

        num_filas_finales = num_filas_originales * 2 + 1  # Se multiplica por 2 y se suma 1 para incluir todos los pasillos horizontales
        num_columnas_finales = num_columnas_originales + 2

        print(f"Filas originales: {num_filas_originales}, Columnas originales: {num_columnas_originales}")
        print(f"Filas finales: {num_filas_finales}, Columnas finales: {num_columnas_finales}")

        if (10 <= num_filas_finales <= 20) and (num_filas_finales % 2 == 1) and (15 <= num_columnas_finales <= 25):
            # Añadimos pasillos entre las filas del almacén
            pasillo = [] 
            for i in range(num_columnas_finales):  
                pasillo.append(' ')  # Agregar un espacio en cada iteración
            magatzem_con_pasillos = []
            for fila in magatzem:
                magatzem_con_pasillos.append([' '] + fila + [' '])  # Añadimos espacio a los lados
                magatzem_con_pasillos.append(pasillo)  # Añadimos un pasillo
            
            magatzem = magatzem_con_pasillos
        else:
            print(f"Dimensions incorrectes: {num_filas_finales} filas, {num_columnas_finales} columnas.")

    return magatzem, fila_robot, columna_robot






def introduirProductes(filePath_productes, magatzem, fila_robot, columna_robot, log):
    # Llegim la llista de productes del fitxer
    with open(filePath_productes, 'r') as file:
        lines = file.readlines()

    for line in lines:
        codi, tipus, estanteria = line.strip().split(";")
        fila_estanteria = ord(estanteria.upper()) - 65  # Convertim lletra a índex de fila
        pasillo_robot = fila_estanteria + 1

        # Busquem una posició buida a la fila d'estanteries
        posicion_columna = None
        estanterias_visitadas = []
        estanteria_actual = fila_estanteria

        while posicion_columna is None and 0 <= estanteria_actual < len(magatzem):
            # Comprova si ja hem visitat aquesta estanteria
            visitada = False
            for visitada_estanteria in estanterias_visitadas:
                if visitada_estanteria == estanteria_actual:
                    visitada = True

            if not visitada:
                estanterias_visitadas.append(estanteria_actual)

                columna = 0
                while columna < len(magatzem[0]) and posicion_columna is None:
                    casella = magatzem[estanteria_actual][columna]

                    # Validem manualment si la casella és vàlida
                    if len(casella) >= 2:
                        tipus_correcte = casella[0] == tipus
                        esta_buida = casella[1] == '-'
                        if tipus_correcte and esta_buida:
                            posicion_columna = columna
                    columna += 1

            if posicion_columna is None:
                if estanteria_actual < fila_estanteria:
                    estanteria_actual -= 1
                else:
                    estanteria_actual += 1

        # Si no hi ha posició disponible, registrem l'error i continuem
        if posicion_columna is None:
            log.append(f"No s'ha trobat posició per al producte {codi} a l'estanteria {estanteria}.")
 

        # Movem el robot fins a la posició desitjada
        while columna_robot != 0 and columna_robot != len(magatzem[0]) - 1:
            if columna_robot < len(magatzem[0]) - 1:
                columna_robot += 1
            else:
                columna_robot -= 1
            draw(magatzem, fila_robot, columna_robot)
            time.sleep(0.25)

        while fila_robot != pasillo_robot:
            if fila_robot < pasillo_robot:
                fila_robot += 1
            else:
                fila_robot -= 1
            draw(magatzem, fila_robot, columna_robot)
            time.sleep(0.25)

        while columna_robot != posicion_columna:
            if columna_robot < posicion_columna:
                columna_robot += 1
            else:
                columna_robot -= 1
            draw(magatzem, fila_robot, columna_robot)
            time.sleep(0.25)

        # Col·loquem el producte a l'estanteria
        magatzem[estanteria_actual][posicion_columna] = (tipus, codi)

        # Movem el robot de tornada
        if fila_robot == pasillo_robot and columna_robot != len(magatzem[0]) - 1:
            while columna_robot != len(magatzem[0]) - 1:
                columna_robot += 1
                draw(magatzem, fila_robot, columna_robot)
                time.sleep(0.25)

        # Registrem l'èxit al log
        mensaje = f"El producte {codi} s'ha col·locat a l'estanteria {chr(estanteria_actual + 65)} casella {posicion_columna + 1}."
        log.append(mensaje)

    return magatzem, fila_robot, columna_robot




def guardarMagatzem(filePath, magatzem, fila_robot, columna_robot):
    error = False 

    with open('/Users/neus/Desktop/UVic/Progra1r/practica_neus_alex/'+filePath, 'w') as file:

        fila_robot_letra = chr(fila_robot + 65)
        columna_robot_humana = columna_robot + 1

        file.write(fila_robot_letra + ";" + str(columna_robot_humana) + "\n")

        for fila in magatzem:

            fila_relevante = fila[1:-1]#no mira ni la primera ni la ultima columna

            hi_ha_element = False

            for casella in fila_relevante:
                if casella != ' ' and casella != '' and casella is not None:
                    hi_ha_element = True


            # Si hi ha algun element rellevant, el processem
            if hi_ha_element:
                fila_line = []
                # Construïm la línia per guardar al fitxer
                for casella in fila_relevante:
                    if casella == ' ':  # Casella buida
                        fila_line.append('-')  # Guardem com "-"
                    elif len(casella) >= 2:  # Comprovem si té l'estructura esperada
                        tipus = casella[0]
                        codi = casella[1]
                        fila_line.append(str(tipus) + "," + str(codi))  # Guardem com "tipus,codi"
                    else:  # Si l'estructura no és correcta, guardem "-"
                        fila_line.append('-')
                # Escrivim la fila al fitxer, separant les caselles amb ";"
                file.write(';'.join(fila_line) + '\n')

    if not error:
        print("L'estat del magatzem s'ha guardat correctament al fitxer: " + filePath)
    else:
        print("Error al guardar l'estat del magatzem.")





def introduir1Producte(magatzem, fila_robot, columna_robot, log):
    continuar = input("Vols continuar (S/N)? ").strip().upper()

    while continuar not in ["S", "N"]:
        continuar = input("Vols continuar (S/N)? ").strip().upper()

    while continuar == "S":
        codi = input("Codi del producte (mida 3): ").strip().upper()
        while len(codi) != 3:
            print("El codi ha de tenir exactament 3 caràcters.")
            codi = input("Codi del producte (mida 3): ").strip().upper()

        tipus = input("Entra el tipus (BLUE, ORANGE, GREEN, YELLOW, PURPLE): ").strip().upper()
        while tipus not in ("BLUE", "ORANGE", "GREEN", "YELLOW", "PURPLE"):
            print("Tipus no vàlid. Prova amb (BLUE, ORANGE, GREEN, YELLOW, PURPLE).")
            tipus = input("Entra el tipus (BLUE, ORANGE, GREEN, YELLOW, PURPLE): ").strip().upper()

        estanteria = input("Entra estanteria (A, C, E, G, I, K): ").strip().upper()
        while estanteria not in ("A", "C", "E", "G", "I", "K"):
            print("Estanteria no vàlida. Prova amb (A, C, E, G, I, K).")
            estanteria = input("Entra estanteria (A, C, E, G, I, K): ").strip().upper()

        fila_estanteria = ord(estanteria) - 65
        pasillo_robot = fila_estanteria + 1

        posicion_columna = None
        estanterias_visitadas = []
        estanteria_actual = fila_estanteria

        intentos = 0
        max_intentos = len(magatzem)

        while posicion_columna is None and 0 <= estanteria_actual < len(magatzem) and intentos < max_intentos:
            intentos += 1
            if estanteria_actual not in estanterias_visitadas:
                estanterias_visitadas.append(estanteria_actual)
            else:
                estanteria_actual += 1

            columna = 0
            while columna < len(magatzem[0]) and posicion_columna is None:
                casella = magatzem[estanteria_actual][columna]
                if len(casella) >= 2:  # Comprobación de que tiene al menos dos elementos
                    tipus_correcte = casella[0] == tipus
                    esta_buida = casella[1] == '-'
                    if tipus_correcte and esta_buida:
                        posicion_columna = columna
                columna += 1

            if posicion_columna is None:
                if estanteria_actual < fila_estanteria:
                    estanteria_actual -= 1
                else:
                    estanteria_actual += 1

        if posicion_columna is not None:
            while fila_robot != pasillo_robot:
                fila_robot += 1 if fila_robot < pasillo_robot else -1
                draw(magatzem, fila_robot, columna_robot)
                time.sleep(0.25)

            while columna_robot != posicion_columna:
                columna_robot += 1 if posicion_columna is not None and columna_robot < posicion_columna else -1
                draw(magatzem, fila_robot, columna_robot)
                time.sleep(0.25)

            magatzem[estanteria_actual][posicion_columna] = (tipus, codi)

            while columna_robot != len(magatzem[0]) - 1:
                columna_robot += 1
                draw(magatzem, fila_robot, columna_robot)
                time.sleep(0.25)

            print(f"El producte {codi} s'ha col·locat a l'estanteria {chr(estanteria_actual + 65)} casella {posicion_columna + 1}.")
            log.append(f"El producte {codi} s'ha col·locat a l'estanteria {chr(estanteria_actual + 65)} casella {posicion_columna + 1}.")
        else:
            print("No s'ha trobat una columna adequada per col·locar el producte.")

        continuar = input("Vols continuar (S/N)? ").strip().upper()
        while continuar not in ["S", "N"]:
            continuar = input("Vols continuar (S/N)? ").strip().upper()

    if continuar == 'N':
        print("Finalitzant la introducció de productes.")

        guardar = input("Vols guardar l'estat actual del magatzem (S/N)? ").strip().upper()
        if guardar == 'S':
            nom_fitxer = input("Nom del fitxer on guardar el magatzem: ").strip()
            if nom_fitxer[-4:] != '.csv': 
                nom_fitxer += '.csv'
            guardarMagatzem(nom_fitxer, magatzem, fila_robot, columna_robot)

        with open('/Users/neus/Desktop/UVic/Progra1r/practica_neus_alex/log_productes.txt', 'w') as log_file:
            log_file.write('\n'.join(log))

    

# Definimos las rutas de los archivos para el almacén y productos
filepath_magatzem = '/Users/neus/Desktop/UVic/Progra1r/practica_neus_alex/magatzem.csv'
filepath_productes = '/Users/neus/Desktop/UVic/Progra1r/practica_neus_alex/prods1.csv'

# Cargamos el estado inicial del almacén desde el archivo especificado
magatzem, fila_robot, columna_robot = obtenirMagatzem(filepath_magatzem)

# Verificamos si el almacén se cargó correctamente
if magatzem is not None:
    log = []  # lista para registrar las operaciones realizadas

    # Introducimos los productos desde el archivo de productos en el almacén
    magatzem, fila_robot, columna_robot = introduirProductes(
        filepath_productes,  # Archivo con la lista de productos
        magatzem,  # Estado actual del almacén
        fila_robot,  # Posición inicial del robot (fila)
        columna_robot,  # Posición inicial del robot (columna)
        log  # Lista de registro para guardar mensajes
    )

    # Permite al usuario añadir manualmente un producto al almacén
    introduir1Producte(magatzem, fila_robot, columna_robot, log)

    # Guardamos el registro de todas las operaciones realizadas en un archivo de texto
    with open('log_productes.txt', 'w') as log_file:
        log_file.write('\n'.join(log))  # Escribimos cada mensaje del log en una nueva línea

    # Dibujamos el estado final del almacén para mostrar los cambios 
        
    draw(magatzem, fila_robot, columna_robot)
    



    # Pausamos 5 segundos para permitir que el usuario vea el resultado final en pantalla
    time.sleep(5)

    # Cerramos la ventana de Pygame para finalizar el programa
    pygame.quit()
