
# coding: utf-8

# In[4]:


import re
import csv
import urllib2
import requests
import argparse
from bs4 import BeautifulSoup


ubicacion = 'barcelona'
max_pages = 50
precio = ''

parser = argparse.ArgumentParser()
parser.add_argument("--lugar", help="ciudad/provincia ej: 'madrid-provincia' o 'valencia' | defecto = barcelona")
parser.add_argument("--paginas", help="numero de paginas a realizar scraping | defecto = 50",type=int)
parser.add_argument("--precio", help="precio maximo del alquiler en euros/mes")
parser.add_argument("--acumular", help="se anadiran nuevos registros sin borrar los anteriores | defecto = 0")
args = parser.parse_args()

if args.lugar is not None:
    ubicacion  = args.lugar
    
if args.paginas is not None:
    max_pages  = args.paginas
    
if args.precio is not None:
    precio = "/f--" + args.precio + "-euros"
    
url_base = "https://www.yaencontre.com/alquiler/viviendas/"
url_base = url_base + ubicacion + precio

def grabar_vivienda(nueva_linea):
   
    f = open('dataset.csv','a')
    f.write(nueva_linea + "\n")
    f.close()

#borra el contenido del archivo, desactivando esta opción el fichero se vuelve acumulativo.
if args.acumular is None:
	open('dataset.csv', 'w').close() 
	grabar_vivienda("Tipo,Prov_Ciudad,Zona,Calle,Precio,Metros,Habitación,Baños")            

for j in range(1, max_pages):

    
    if j > 1:
        url = "%s/pag-%d" % (url_base, j)
    else:
        url = url_base

     
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, 'lxml')
    marco = soup.find_all('div', attrs={'class': 'results-listed col-md-12 col-sm-12 col-lg-12'})


    for i, vivienda in enumerate(marco):

        
        ubicacion = ubicacion[:1].upper() + ubicacion[1:]
        
        titulo = vivienda.find('span', attrs={'itemprop': 'name'})
        precio = vivienda.find('span', attrs={'class': 'price'})
        detalles = vivienda.find('p', attrs={'class': 'mb-sm'})
        detalles = detalles.next_element.next_element
        
        precio = precio.text.strip()
        titulo = titulo.text.strip()
        detalles = detalles.text.strip()
       
        detalles = [token for token in detalles.split() if token.isdigit()]
        
        precio = precio.encode('utf-8')
        precio = precio.replace('€','')
        precio = precio.replace('.','')
        precio = precio.strip()
        
        hab = 0
        aseos = 0
        
        if len(detalles) > 0:
            metros = detalles[0]

        if len(detalles) >= 2:
            hab = detalles[1]

        if len(detalles)==3:
            aseos = detalles[2]

        if not hab==aseos==0:    
            
            situacion = titulo.split("en alquiler en ",1)[1]
            calle = situacion.split(" en "+ubicacion,1)[0]
            tipo = titulo.split(" en alquiler en ",1)[0] 
            
            
            if calle.find(',')!=-1:
                barrio = calle.split(",",1)[1]
                barrio = barrio.strip()
                calle = calle.split(",",1)[0]
            else:
                barrio = 'NA'
                
            
            hab = str(hab)
            aseos = str(aseos)
            ubicacion = ubicacion.split("-",1)[0]
            barrio = barrio.replace(",","")
            calle = calle.replace(",","")
            
            grabar_vivienda(','.join([tipo,ubicacion,barrio,calle,precio,metros,hab,aseos]).encode('utf-8'))            

