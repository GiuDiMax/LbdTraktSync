from syncWatchlist import setWatchlist
from syncAllRatings import syncAll
from syncLibrary import getDiff
import time

if __name__ == '__main__':
    print("\nSET LIBRARY")
    getDiff()
    time.sleep(1)
    print("\nSET WATCHLIST")
    setWatchlist()
    time.sleep(1)
    print("\nSET RATINGS")
    syncAll()
