
# coding: utf-8

# In[19]:


import re
import urllib2
from bs4 import BeautifulSoup


quote_page = 'https://www.yaencontre.com/alquiler/pisos/barcelona/pag-2'

page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'lxml')


titulo = soup.find('span', attrs={'itemprop': 'name'})
precio = soup.find('span', attrs={'class': 'price'})
detalles = soup.find('div', attrs={'class': 'results-listed-resume'})

titulo = titulo.text.strip()
precio = precio.text.strip()
detalles = detalles.text.strip()
detalles = [token for token in detalles.split() if token.isdigit()]
metros,hab,aseos = detalles

situacion = titulo.split("en alquiler en ",1)[1] 
situacion = situacion.split("en Barcelona",1)[0]
tipo = titulo.split("en alquiler en ",1)[0] 

print tipo
print situacion
print precio
print metros + ' metros'
print hab + ' habitaciones'
print aseos + ' aseos\n'

