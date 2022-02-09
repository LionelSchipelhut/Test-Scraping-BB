"""
- Obtener todas las películas y series
- Obtener la metadata de cada contenido: título, año, sinopsis, link, duración (solo para movies)
- Guardar la información obtenida en una base de datos, en archivo .json o .csv automáticamente

- PLUS: Episodios de cada serie
- PLUS: Metadata de los episodios
- PLUS: Si es posible obtener mas información/metadata por cada contenido
- PLUS: Identificar modelo de negocio

Fecha límite para entrega: viernes 11 de febrero a las 11:00hs.
https://www.starz.com/ar

- Tenes la libertad de utilizar la librería que quieras para realizarlo.
- Subir a GitHub el script trabajado junto con un archivo de los resultados 
que se obtienen al correr el script creado (JSON, xlsx, csv, etc)

"""

from requests import get
import pandas as pd
import json


def get_movies(QUERY_URL, BASE_MOVIE_LINK):
    """Extrae la metadata de las películas, la procesa y agrega
    el link correspondiente a cada una.

    :param QUERY_URL: URL con los parámetros correspondientes para la
    petición
    :type: str

    :param BASE_MOVIE_LINK: URL base para generar el enlace a la película
    mediante su contentId
    :type: str

    :rtype: list
    :return: una lista conteniendo todas las películas con su metadata

    """
    all_movies = get(QUERY_URL).json()
    all_movies = [movie for movie in all_movies['playContentArray']['playContents']]

    for movie in all_movies:
        movie['link'] = '{}/movies/{}'.format(BASE_MOVIE_LINK, movie['contentId'])             

    return all_movies


def get_series(QUERY_URL, BASE_SERIE_LINK):
    """Extrae la metadata de las series, la procesa y agrega
    el link correspondiente a cada una.

    :param QUERY_URL: URL con los parámetros correspondientes para la
    petición
    :type: str

    :param BASE_MOVIE_LINK: URL base para generar el enlace a la película
    mediante su contentId
    :type: str

    :rtype: list
    :return: una lista conteniendo todas las series con su metadata

    """
    all_series = get(QUERY_URL).json()
    all_series = [serie for serie in all_series['playContentArray']['playContents']]
    
    for serie in all_series:
        serie['link'] = '{}/series/{}'.format(BASE_SERIE_LINK, serie['contentId'])
        
        serie['seasons'] = serie['childContent']
        del serie['childContent']

        for season in serie['seasons']:
            season['episodes'] = season['childContent']
            del season['childContent']

    return all_series


def create_json(file_name, content):
    """Crea un archivo .json con el nombre y contenido indicado.
    
    :param file_name: nombre del archivo JSON que se quiere crear
    :type: str

    :param content: contenido del JSON
    :type: str
    """
    with open(file_name, 'w', encoding='utf-8') as file_stream:
        file_stream.write(
            json.dumps(
                content, indent=4, 
                sort_keys=True, 
                ensure_ascii=False
            )
        )


def create_csv(json_path, csv_path):
    """Crea un archivo .csv simple en la ubicación y con el JSON dados

    :param json_path: dirección del json sobre el cual se debe hacer
    el .csv
    :type: str

    :param csv_path: dirección donde se debe crear el .csv más el nombre
    :type: str
    """
    dataframe = pd.read_json(json_path)
    dataframe.to_csv(csv_path)


if __name__ == '__main__':
    QUERY_URL = 'https://playdata.starz.com/metadata-service/play/partner/Web_AR/v8/content'
    BASE_MEDIA_LINK = 'https://www.starz.com/ar/es'
    
    MOVIES_QUERY = '&contentType=Movie'
    SERIES_QUERY = '&contentType=Series'
    
    ITEM_QUERY = (
        '?lang=es-419'
        '&includes=title,logLine,runtime,ratingCode,'
        'free,contentId,releaseYear,newContent,'
        'comingSoon,genres,contentType,'
        'childContent'
    )

    
    movies_data = get_movies(f'{QUERY_URL}{ITEM_QUERY}{MOVIES_QUERY}', BASE_MEDIA_LINK)
    series_data = get_series(f'{QUERY_URL}{ITEM_QUERY}{SERIES_QUERY}', BASE_MEDIA_LINK)

    #create_json('starz_movies.json', movies_data)
    #create_json('starz_series.json', series_data)
    create_json('starz_media.json', dict(movies=movies_data, series=series_data))
    #create_csv('./starz_movies.json', './starz_movies.csv')
    #create_csv('./starz_series.json', './starz_series.csv')
