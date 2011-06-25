#!/usr/bin/python
# Nick Travers 2011

import sys
import os
import time
from appscript import *
from pyechonest import config
from pyechonest import artist

# colors class
class bcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
    

def getSong():
    """
    Get the currently playing iTunes song and return
    relevant information in a dictionary
    """    
    # connection to iTunes
    itunes = app('itunes')
    
    # the currenyly playing
    track = itunes.current_track()
    
    # the dictionary to return
    song = {}
    
    # get the relevant pieces of information
    song['item'] = track
    song['name'] = track.name()
    song['artist'] = track.artist()
    song['album'] = track.album()
    # song['length'] = track.time()
    song['rating'] = track.rating()
    song['ID'] = track.database_ID()
    
    return song

def printInfo(song):
    """
    Get the library reference to the song
    """
    print bcolours.FAIL + 'Current song:' + bcolours.ENDC
    print '\t%s' % song['name']
    print '\tArtist: %s' % song['artist']
    print '\tAlbum: %s' % song['album']
    print '\tRating [0-100]: %d' % song['rating']    


def updateRating(song, rating):
    """
    Update the rating for the current;y playing song
    """
    # make sure the input is an integer
    try:
        rating = int(rating)
    except:
        'Could not convert rating to an int'
        return
    if rating < 0 and rating > 100:
        print 'Rating is not in range [0-100]'
        return
        
    # update the song rating    
    song['item'].rating.set(rating)
    
    # print a message and exit
    print '\nUpdated rating!'
    time.sleep(1)
    
    return

def printAlbumStats(song):
    """
    Print off some stats for the sonf
    """
    print bcolours.FAIL + '\nAlbum Information:\n' + bcolours.FAIL
    print bcolours.OKGREEN + '%5s%25s%16s%s' % ('#', ' -- Title -- ', '', 'Rating') + bcolours.ENDC
    # get the main library as a playlist
    itunes = app('itunes')
    lib = itunes.playlists()[0]
    
    # run a search for the album
    results = itunes.search(lib, for_=song['album'], only=k.albums)
    
    tracks = []
    for item in results:
        track = {}
        track['track number'] = item.track_number()
        track['name'] = item.name()
        track['rating'] = item.rating()
        track['ID'] = item.database_ID()
            
        tracks.append(track)
            
    tracks = sorted(tracks, key = lambda item: item['track number'])
    
    for track in tracks:
        if track['ID']== song['ID']:          
            print '%5d %-40s %3d' % (track['track number'], track['name'], track['rating']) + bcolours.FAIL +' <<-- PLAYING'+ bcolours.ENDC
        else:
            print '%5d %-40s %3d' % (track['track number'], track['name'], track['rating'])
    
    return

def getSimilarArtists(artist_name):
    "Get similar artists to display"
    similar_artists = []
    
    bk_results = artist.search(artist_name)
    bk = bk_results[0]
    similar_artists = bk.similar
    
    return similar_artists
    
    toPrint = ''
    for similar_artist in similar_artists[:3]:
        toPrint = toPrint + str(similar_artist) + ', '
        
    print '\t' + toPrint[:-2]

def printSimilarArtists(artists, n=3):
    """Print n similar artists"""
    print '\n' + bcolours.FAIL + 'Similar Artists:' + bcolours.ENDC
    for artist in artists[:n]:
        print '\t', artist

def main():
    config.ECHO_NEST_API_KEY = 'CIF1V52LAHFAM0NBO'
    previous_artist = ''
    
    # continue until 'q' is input
    while True:
        # get the song and print information
        os.system('clear')
        song = getSong()
        printInfo(song)
        
        # print song information here ---
        printAlbumStats(song)
        
        # print similar artists if artist has changed
        current_artist = song['artist']
        if current_artist != previous_artist:
            similar_artists = getSimilarArtists(song['artist'])
            
        printSimilarArtists(similar_artists, 3)    
        previous_artist = current_artist
            
        # get the user input
        print "\n-- Press 'r' to rate, 'q' to quit --"
        key = raw_input()
        
        # press 'r' to rate the song
        if key == 'r':
            print "Enter a rating for the song [0 - 100], 'c' to cancel"
            # update the rating for the song
            rating = raw_input()
            if int(rating) >= 0 and int(rating) <= 100:
                updateRating(song, rating)
            else:
                print 'Cancelled!'
        elif key == 'q':
            exit()


if __name__ == '__main__':
	main()