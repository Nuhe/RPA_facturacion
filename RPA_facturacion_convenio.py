import PyPDF2
import re
import os
import shutil

class pdf_organizer:
    def __init__(self):
        self.ORIGIN_FOLDER_PATH = r'.\\'
        self.DESTINY_FOLDER_PATH = r'.\destino\\'
        
        self.almacenar_paginas = []
        self.nro_internacion = []
        self.nro_afiliado = []
        self.nombre_completo = []

    def leer_datos_facturacion(self):
        with open('resumenfacturacion.pdf', 'rb') as archivo:
            lector_pdf = PyPDF2.PdfReader(archivo)

            cantidad_paginas = len(lector_pdf.pages)

            for i in range(cantidad_paginas):
                # Seleccionar la página actual
                pagina = lector_pdf.pages[i]
                
                # Extraer el texto de la página
                texto = pagina.extract_text()

                # Patrón regex para encontrar el formato específico
                patron = re.compile(r'(\d{11})\s([A-ZÑñ, ]+)')
                patron_nro_internacion = re.compile(r'\b(\d{10})\b')

                # Busca todas las coincidencias en el texto
                coincidencias = patron.findall(texto)
                coincidencia_nro_internacion = patron_nro_internacion.findall(texto)

                # Imprime las coincidencias
                for c in coincidencias:
                    self.nro_afiliado.append(c[0])
                    self.nombre_completo.append(c[1])

                for i in coincidencia_nro_internacion:
                    nro = str(i)[3:]
                    self.nro_internacion.append(nro)

        return self.nro_afiliado, self.nro_internacion, self.nombre_completo

    def leer_archivos_nombres(self, path):
        nombre_archivos = os.listdir(path)
        return nombre_archivos
    
    def renombrar_archivos(self, file, nro):
        dict_rename = dict(zip(self.nro_internacion, self.nro_afiliado))
        for d in dict_rename:
            if d in file:
                try:
                    os.rename(file, self.DESTINY_FOLDER_PATH + nro + '_' + dict_rename[d] + '.pdf')
                except FileExistsError:
                    # Verificar si el nuevo nombre ya existe
                    counter = 1
                    if os.path.exists(self.DESTINY_FOLDER_PATH + nro + '_' + dict_rename[d] + '.pdf'):
                        os.rename(self.DESTINY_FOLDER_PATH + nro + '_' + dict_rename[d] + '.pdf', self.DESTINY_FOLDER_PATH + nro + '_' + dict_rename[d] + f'_{counter}.pdf')
                        
                        # Agregar sufijo numérico al nuevo archivo
                        counter += 1
                        new_file = self.DESTINY_FOLDER_PATH + nro + '_' + dict_rename[d] + f'_{counter}.pdf'

                    os.rename(file, new_file)    
    def archivos_faltantes(self):
        nro_afiliado_1 = self.nro_afiliado

#Identificar y copiar los archivos a la carpeta destino
organizer = pdf_organizer()
data_facturacion_pdf = organizer.leer_datos_facturacion() 
nro_internacion = data_facturacion_pdf[1]
ruta_origen = organizer.ORIGIN_FOLDER_PATH
ruta_destino = organizer.DESTINY_FOLDER_PATH
data_origen = organizer.leer_archivos_nombres(ruta_origen)
data_destino = organizer.leer_archivos_nombres(ruta_destino)

renombrar_si_no = input('¿Desea renombrar los archivos? si | no        ')

lista_numeros = []

if renombrar_si_no == 'si':
    nro_facturacion = input('Ingrese el numero de factura:   ')
    for nro in nro_internacion:
        for data in data_origen:
            if nro in data:
                shutil.copy2(ruta_origen + data, ruta_destino + data)
                #RENOMBRAR FUNCION      
                organizer.renombrar_archivos(ruta_destino + data, nro_facturacion)
                lista_numeros.append(nro)
            else:
                pass
else:
    for nro in nro_internacion:
        for data in data_origen:
            if nro in data:
                shutil.copy2(ruta_origen + data, ruta_destino + data)
                lista_numeros.append(nro)
            else:
                pass

for l in lista_numeros:
    if l in nro_internacion:
        nro_internacion.remove(l)

contenido_str = ', '.join(nro_internacion)
with open("pacientes_faltantes.txt", 'w') as archivo:
    archivo.write(contenido_str)