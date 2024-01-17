from plexapi.server import PlexServer
from config import *
import requests


def get_plex_movie(MOVIE_LIBRARY_NAME):
    plex = PlexServer(PLEX_URL, PLEX_TOKEN)
    print("Retrieving a list of movies from the '{library}' library in Plex...".format(library=MOVIE_LIBRARY_NAME))
    movie_library = plex.library.section(MOVIE_LIBRARY_NAME)
    #return movie_library.get('Dream Scenario')
    return movie_library.all()


if __name__ == '__main__':
    url = f'{PLEX_URL}/library/sections/6/all?X-Plex-Token={PLEX_TOKEN}'
    a = requests.get(url)
    print(a.text)
    #films = get_plex_movie('FILM')
    #print(films[0])
