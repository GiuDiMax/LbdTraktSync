from syncWatchlist import setWatchlist
from syncAllRatings import syncAll
from syncLibrary import getDiff


if __name__ == '__main__':
    print("SET LIBRARY")
    getDiff()
    print("SET WATCHLIST")
    setWatchlist()
    print("SET RATINGS")
    syncAll()
