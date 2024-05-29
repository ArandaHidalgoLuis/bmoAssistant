import urllib

url = 'https://datosabiertos.malaga.eu/api/3/action/datastore_search?resource_id=9bc05288-1c11-4eec-8792-d74b679c8fcf&limit=5&q=title:jones'  
fileobj = urllib.urlopen(url)
print(fileobj.read())