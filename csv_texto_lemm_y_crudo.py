# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 17:48:43 2023

@author: corir
"""
#%% librerias
import numpy as np
import pandas as pd
import re       # libreria de expresiones regulares
import string   # libreria de cadena de caracteres
import time
import nltk

import os

#para stanza
import stanza
#stanza.download('es') # descarga el modelo en español
nlp = stanza.Pipeline('es')

from tqdm import tqdm
#pip install python-docx 
from docx import Document

entrevista = 'Segunda' #aca podrías poner control

#%% FUNCIONES

def pre_analisis_texto(text): #le das el texto

    text = text.lower()  # pasa las mayusculas del texto a minusculas                                                             
    # reemplaza singnos de puntuacion por espacio en blanco. %s es \S+ que quiere decir cualquier caracter que no sea un espacio en blanco
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) 
    
    text = re.sub('\n', '', text)  #saca los enter
    
    text = re.sub('¿', '', text) #saca los ¿
    #re.sub sustituye una secuencia de caracteres por otra:
    #re.sub('lo que queres reemplazar', 'por lo que lo reemplazas', texto donde esta)

    stop_words = nltk.corpus.stopwords.words('spanish')          
    #dejo por si necesito agregar o sacar una stopword
    #stopwords.append('ejemplo')
    #stopwords.remove('ejemplo')

    stopwords_dict = {word: 1 for word in stop_words}

    text_sin_sw = " ".join([word for word in text.split() if word not in stopwords_dict])
    
    return(text_sin_sw)


def lemm_stanza(text):
    t0 = time.time()

    doc = nlp(text)
    list_lemmas_stanza = [word.lemma for sent in doc.sentences for word in sent.words]

    lemmas_stanza = ' '.join(list_lemmas_stanza)

    t1 = time.time()

    t_lemm_stanza = t1-t0
    
    return list_lemmas_stanza, lemmas_stanza, t_lemm_stanza

def leer_archivo_docx(nombre_archivo):
    doc = Document(nombre_archivo)
    texto = ""
    for paragraph in doc.paragraphs:
        texto += paragraph.text + "\n"
    return texto

def leer_archivo_txt(file_name):
    pre_text = open(file_name, 'r', encoding='utf-8') #esto es un <class '_io.TextIOWrapper'>
    text = pre_text.read() #esto es un string
    return text

#%% ACA SE HACE UN CSV SOLO DE LEMMATIZAR

'''
se hace uno por tema, asi que tenes que ir cambiando el tema, la nomenclatura es temas: "cfk", "campeones_del_mundo", "antesdevenir", "presencial", "arabia"
sorry nunca lo metí en una función y loop, no quiero hacerlo ahora porque no lo puedo probar y x si me mando un error
esta puesto como si los textos estan en formato docx, si estan en txt está comentado el principio del for como se bajan

'''
path = f'C:/Users/Usuario/Desktop/Cori/Tesis/{entrevista}_entrevista/Transcripciones_limpias/' #aca tenes que poner el path de donde tenes vos las trascripciones
path_guardado = f'C:/Users/Usuario/Desktop/Cori/Tesis/{entrevista}_entrevista/Texto_lemmatizado/Stanza/{tema}_usando_stanza.csv' #aca pone donde lo quieras guardar 

tema = "cfk"

 # Lista de los sujetos     
Sujetos = ['0']*65
for j in range(65):
    Sujetos[j] = f"Sujeto {j+1}"

data = {} # Creamos un diccionario vacio


for i, c in tqdm(enumerate(Sujetos)):
    # #cargamos el texto de un txt
    # filename = path + c  + f"/sujeto{i+1}_{tema}.txt"
    # if os.path.isfile(filename) is True: #si existe hacemos esto
    #     texto = leer_archivo_txt(filename)
    #     texto_limpio = pre_analisis_texto(texto)
    #     #lo lemmatizamos
    #     list_lemmas, lemmas, t_lemm = lemm_stanza(texto_limpio)
    #     data[i] = lemmas # asignamos los sujetos como key al diccionario y el valor es el texto
    # elif os.path.isfile(path + c  + f"/sujeto{i+1}_{tema}_2021.txt"):
    #     texto = leer_archivo_txt(path + c  + f"/sujeto{i+1}_{tema}_2021.txt")
    #     texto_limpio = pre_analisis_texto(texto)
    #     #lo lemmatizamos
    #     list_lemmas, lemmas, t_lemm = lemm_stanza(texto_limpio)
    #     data[i] = lemmas # asignamos los sujetos como key al diccionario y el valor es el texto
    # else:
    #     print(f"El archivo sujeto{i+1}_{tema}.txt")
    #     data[i] = np.nan
    #cargamos el texto de un docx
    filename = path + c  + f"/sujeto{i+1}_{tema}.docx"
    if os.path.isfile(filename) is True: #si existe hacemos esto
        texto = leer_archivo_docx(filename)
        texto_limpio = pre_analisis_texto(texto)
        #lo lemmatizamos
        list_lemmas, lemmas, t_lemm = lemm_stanza(texto_limpio)
        data[i] = lemmas # asignamos los sujetos como key al diccionario y el valor es el texto
    elif os.path.isfile(path + c  + f"/sujeto{i+1}_{tema}_2021.docx"):
        texto = leer_archivo_docx(path + c  + f"/sujeto{i+1}_{tema}_2021.docx")
        texto_limpio = pre_analisis_texto(texto)
        #lo lemmatizamos
        list_lemmas, lemmas, t_lemm = lemm_stanza(texto_limpio)
        data[i] = lemmas # asignamos los sujetos como key al diccionario y el valor es el texto
    elif os.path.isfile(path + c + f"/sujeto{i}_presencial_2do2022.docx"):
        texto = leer_archivo_docx(path + c + f"/sujeto{i}_presencial_2do2022.docx")
        texto_limpio = pre_analisis_texto(texto)
        #lo lemmatizamos
        list_lemmas, lemmas, t_lemm = lemm_stanza(texto_limpio)
        data[i] = lemmas # asignamos los sujetos como key al diccionario y el valor es el texto
    else:
        print(f"El archivo sujeto{i+1}_{tema}.docx")
        data[i] = np.nan
        

# la acomodamos en un dataframe 

data_combined = {key: [value] for (key, value) in data.items()}
data_df = pd.DataFrame.from_dict(data_combined).transpose()
data_df.columns = ['lematizado']    


data_df.to_csv(path_guardado, index = False)
           
            
#%% le agrego la columna del texto crudo, aca la función, la celda que viene el código a correr

'''
tenes que cambiar los path, el primero es donde guardaste el texto lemm (que es el path_guardado de la celda anterior),
el segundo es donde tenes los textos limpios en carpetas (el path de la celda anterior agregando que entras a la carpeta sujeto)
esta comentado con txt, puesto para docx
'''

def csv_con_texto_crudo(tema):

    path = f'C:/Users/Usuario/Desktop/Cori/Tesis/{entrevista}_entrevista/Texto_lemmatizado/Stanza/{tema}_usando_stanza.csv'
        
    df_textos = pd.read_csv(path)
    
    textos_crudos = []
    for i in range(1, len(Sujetos)+1):
        path = f'C:/Users/Usuario/Desktop/Cori/Tesis/{entrevista}_entrevista/Transcripciones_limpias/Sujeto {i}'
        # #cargamos el texto de un txt
        # filename = path + f"/sujeto{i}_{tema}.txt"
        # if os.path.isfile(filename) is True: #si existe hacemos esto
        #     texto = leer_archivo_txt(filename)
        #     textos_crudos.append(texto) 
        # elif os.path.isfile(path + f"/sujeto{i}_{tema}_2021.txt"):
        #     texto = leer_archivo_txt(path + f"/sujeto{i}_{tema}_2021.txt")
        #     textos_crudos.append(texto) 
        # else:
        #     print(f"El archivo sujeto{i}_{tema}.txt")
        #     textos_crudos.append(np.nan)
        #cargamos el texto de un docx
        filename = path + f"/sujeto{i}_{tema}.docx"
        if os.path.isfile(filename) is True: #si existe hacemos esto
            texto = leer_archivo_docx(filename)
            textos_crudos.append(texto) 
        elif os.path.isfile(path + f"/sujeto{i}_{tema}_2021.docx"):
            texto = leer_archivo_docx(path + f"/sujeto{i}_{tema}_2021.docx")
            textos_crudos.append(texto) 
        elif os.path.isfile(path + f"/sujeto{i}_presencial_2do2022.docx"):
            texto = leer_archivo_docx(path + f"/sujeto{i}_presencial_2do2022.docx")
            textos_crudos.append(texto)
        else:
            print(f"El archivo sujeto{i}_{tema}.docx")
            textos_crudos.append(np.nan)
            
    df_textos["texto_crudo"] = textos_crudos
    
    df_textos.insert(0, 'Sujetos', Sujeto)
    
    return df_textos

temas = ["cfk", "campeones_del_mundo", "antesdevenir", "presencial", "arabia"]

#%% aca guardas el csv con el texto crudo también

'''
tenes que acomodar la cantidad de sujetos y el path donde queres que se guarden
'''
 # Lista de los sujetos   
Sujetos = ['0']*65
for j in range(65):
    Sujetos[j] = f"Sujeto {j+1}"
    
Sujeto = np.linspace(1,65,65)
    

for tema in temas:
    
    df_textos = csv_con_texto_crudo(tema)
    
    df_textos.to_csv(f'C:/Users/Usuario/Desktop/Cori/Tesis/{entrevista}_entrevista/Texto/{tema}_crudo_y_lemm_usando_stanza_.csv', index=False)

