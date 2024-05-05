# NLP-IFIByNE
Códigos para análisis de textos que buscan variables de Autopercepción Contenido, Sentimiento, Estructurales y Memoria.

Primero tenes que armar un csv con las transcripciones:

Una vez que ya tengas las transcripciones limpias se ponen en una carpeta, llamada por ejemplo "Transcripciones_limpias" adentro de esa carpeta tiene que haber una carpeta para cada sujeto llamada "Sujeto {num}", y adentro de la carpeta de cada sujeto estan sus textos de transcripciones en formato o txt o docx.
El código para hacer el csv después es csv_texto_lemm_y_crudo.py, adentro se explica las variables que tenes que cambiar por las de tu data (paths y número de sujetos)
Se guarda el csv en donde vos le indiques.
La primer columna es el número de sujeto (contando desde 1) (no tiene nombre), la segunda es el texto lematizado ‘lematizado’ y la tercera el texto crudo ‘texto_crudo’.


Aca explico como hacer el csv con todas las variables. Primero se busca cada variable por separado. Cada una se va a ir guardando al final en una carpeta que diga {Primera/Segunda/Control}_entrevista/ aca alguna carpeta referencia al tipo de variables/ csv, uno por tema. 

Variables autopercepción:
   Primero tenes el csv que te devuelve el formulario de una, si tenias mas de un formulario (para diferentes sujetos) tenes que juntarlos. El csv se arma a mano, vas a armarte uno para cada tema con 4 columas. Las mismas son: "Sujetos", donde va el número de sujetos. "Recordaste" "Cuanto_recordaste", "Tipo_emocion", "Intensidad". Estas hacen referencia a las preguntas hechas en el forms. Dejo un ejemplo de Arabia en la primer entrevista. Estos csv (recuerdo, uno por tema), se menten en una carpeta  que llamas como quieras y cada csv se puede llamar algo asi como 'Post_entrevista_{tema}_{primera/segunda/contol}.csv'. Después vas a usar el código variables_autop.py que va a pasarte las respuestas a números, y guardas las variables en una carpeta de la pinta 'C:/blabla/{Primera/Segunda/Control}_entrevista/Variables autopercepcion/variables_autopercepcion_{tema}.csv'. A este código le vas a tener que cambiar paths y cosas en las variables de "el santo trial"

   
Variables de contenido:
  Se calculan todas en variables_contenido.py, se guarda en f'C:/blabla/{Primera/Segunda/Control}_entrevista/Variables contenido/variables_contenido_{tema}.csv'
     Las variables son: número de palabras únicas normalizadas (con zscore con media y desviación por participante). Número de sust, verb, etc totales (NO UNICAS) normalizadas al número de palabras totales del relato. Número de palabras en primera y tercera persona normalizado al núm total de palabras del texto. En santo trial vas a tener que acomodar a tus datos las variables, al principio del código vas a tener que modificar el path donde guardaste los textos crudos y lemmatizados, al final el código donde queres que se guarden.
    
Variable sentimiento: 
     Se hace en el colab https://colab.research.google.com/drive/1YvTq6fZMl1AfxEhjIjcuMI9ZIvdto3Wb#scrollTo=7hvVQONDgI6k (en la compu tenia problema con librerias y dependencias), busca el sentimiento con pysentimiento sobre el texto crudo (estaría mal hacerlo lematizado por cómo funciona pysentimiento). Al principio el código tiene instrucciones claras de cómo usarlo. Yo lo uso desde Tesis Corina.

Variables estructurales:
     El modelo nulo de coherencia tarda 5/6 horas en guardarse el código para ver el grafico de coherencia en distancia está en graf_cohe_todos.py (no lo abrí, seguro tiene para adaptar cosas, pero creo q este gráfico no es importante). Lo de redes ya esta apto también.
      Las variables son: coherencia a d =1 2 y 3 normalizadas por …. De redes son 'num_nodes_norm', 'Comunidades_LSC', 'diámetro', 'k_mean', 'transitivity', 'ASP', 'average_CC', 'selfloops', 'L2', 'L3', 'density'.
El código de las variables está es variables_estructurales.py. Todo lo que necesites cambiar (creo, es un poco largo este) esta marcado con #adaptar y dsp dice a qué cosa. El modelo nulo se hace y guarda aca. Hay celas que dice recomiendo no usar que guardan por separado las vars de coherencia de las de redes. Se pueden borrar.
	IMPORTANTE: cambié el modelo nulo, ahora toma dos oraciones de cada relao del sujeto. Si un sujeto no tiene un relato no agarra mas oraciones de los demas, siempre son dos de los relatos que tiene. Esto aumentó la cantidad de sujetos que superan el modelo nulo.

Variables memoria: Lo primero que hay que hacer es traducir los textos con la API de chatGPT, el código es csv_para_codigo_ruben.py. En la celda “el santo trial” hay que poner qué entrevista queres traducir (Primera, Segunda o control) y después ademas tenes que poner el tema en la celda de traducción, dado que el código tarda como 30 minutos en los textos cortos y como una hora en los largos SOLO con 30 participantes (imaginate cuando haga los 60 de una) y chatGPT cuando le pedis muchas cosas seguidas te empieza a hacer 7 mins entre requests. Se traba todo el tiempo, por eso esta separando en dos celdas, si se traba tener que cambiar desde donde arranca a traducir y seguir. Un dolor de huevos inevitable esta parte de momento. Los códigos en inglés se guardan en f'C:/Users/Usuario/Desktop/Cori/Tesis/{entrevista}_entrevista/Clasificacion_episodico_semantico/clean_text_{tema}.csv', se suben a drive a automated_autobiographical_interview_scoring/Inglés/Textos limpios en inglés, **hay que corregir los csv sacar que chatGPT a veces al principio agrega algo antes de empezar a traducir**. 
**este código esta muy feo que lo iba cambiando segun lo que necesitaba porque se traba mucho la api, dice #adaptar en los lugares que tenes que cambiar cosas**
      Para poder usar el algorítmo de Ruben (https://colab.research.google.com/drive/1Pn0UNBhCLSNulR5ID52onhkdoxJj3OMW#scrollTo=jONHybF0biWZ), en el README (https://github.com/rubenvangenugten/autobiographical_interview_scoring/blob/main/README.md) indica que hay que hacer un csv con tres columnas y subirlo a drive. Uso el drive de Corina Tesis para hacer la carpeta que pide y ahi subo el csv. Lo edite¿é un poco al colab para que yo al principio ponga el tema y el número de entrevista (primera/segunda) y me devuelve la data lista para ELcsv. La data es num de palabras internas/externas normalizado al num de palabras que tiene el relato. La data se guarda en drive tesis corina. Me la bajo en mi compu en C:\Users\Usuario\Desktop\Cori\Tesis\Primera_entrevista\Variables memoria (#adaptar). OJO QUE NO DEJA LOS SUJETOS SIN UN RELATO LOS TIRA DEL TEMA. Igual en ELcsv hace el merge para que agregue nans ahí. Esto se hace desde Tesis Corina. Tenes que adaptar las primeras dos celdas y si queres las últimas 3 (estas es sobre como guarda). Al principio el colab tiene instrucciones.

      
Finalmente para obtener ELcsv correr: ELcsv.py. Podes elegir si guarda con o sin autopercepcion, si es primera o segunda entrevista. Guarda en C:/blabla/{entrevista}_entrevista/ELcsv/ un csv por tema. #adaptar para lo que tiene que cambiar
