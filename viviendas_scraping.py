
# coding: utf-8

# In[84]:


import re
import urllib2
from bs4 import BeautifulSoup


quote_page = 'https://www.yaencontre.com/alquiler/pisos/barcelona/pag-2'

page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'lxml')


marco = soup.find_all('div', attrs={'class': 'results-listed col-md-12 col-sm-12 col-lg-12'})


for i, vivienda in enumerate(marco):

    
    titulo = vivienda.find('span', attrs={'itemprop': 'name'})
    precio = vivienda.find('span', attrs={'class': 'price'})
    detalles = vivienda.find('div', attrs={'class': 'results-listed-resume'})
    
    titulo = titulo.text.strip()
    precio = precio.text.strip()
    detalles = detalles.text.strip()
    detalles = [token for token in detalles.split() if token.isdigit()]
    metros,hab,aseos = detalles

    situacion = titulo.split("en alquiler en ",1)[1] 
    situacion = situacion.split("en Barcelona",1)[0]
    tipo = titulo.split("en alquiler en ",1)[0] 

    print  "\033[1mVivienda num. %d\033[0m" % (i + 1)
    print "%s | %s | %s/mes | %s metros | %s habitaciones | %s aseos\n" % (tipo, situacion, precio, metros, hab, aseos)

