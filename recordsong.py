"""record spotify songs to mp3s from a playlist id"""

# Example usage:
# cp example_config.py config.py
# python3 recordsong.py
# https://developer.spotify.com/console/get-playlist-tracks/

import subprocess, sys, os, time, shutil, eyed3
from threading import BrokenBarrierError
from urllib.request import urlopen

# must copy over example_config.py to config.py and populate
from config import bearertoken, playlistid

import requests
from requests.structures import CaseInsensitiveDict

# Setup variables
piezoStorageLocation = '/Users/jamescampbell/Music/Piezo/'
ripStorageLocation   = '/Users/jamescampbell/Music/Ripped/'
playlisturl = f"https://api.spotify.com/v1/playlists/{playlistid}/tracks"

# Clear all previous recordings if they exist
for f in os.listdir(piezoStorageLocation):
    os.remove(os.path.join(piezoStorageLocation,f))


def getTrackIds(bearertoken, playlisturl) -> set():
    """Get trackids list from playlist id"""
    trackids = []
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    headers["Authorization"] = f"Bearer {bearertoken}"
    resp = requests.get(playlisturl, headers=headers)
    rawdict = resp.json()
    # print(rawdict)
    for k in rawdict["items"]:
        trackids.append(k["track"]["uri"])
    return set(trackids)



def main():
    trackids = getTrackIds(bearertoken, playlisturl)
    for trackid in trackids:
        # Tell Spotify to pause, tell Piezo to record, tell Spotify to play a specified song
        subprocess.Popen('osascript -e "tell application \\"Spotify\\" to pause"', shell=True, stdout=subprocess.PIPE).stdout.read()
        time.sleep(.300)
        subprocess.Popen('osascript -e "activate application \\"Piezo\\"" -e "tell application \\"System Events\\"" -e "keystroke \\"r\\" using {command down}" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()
        subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "play track \\"'+trackid+'\\"" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()

        time.sleep(1)
        print(f"recording {trackid}")
        # Get the artist name, track name, album name and album artwork URL from Spotify
        artist  = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s artist" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
        track   = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s name" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
        album   = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s album" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')
        artwork = subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "current track\'s artwork url" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8').rstrip('\r\n')

        # Download album artwork
        artworkData = urlopen(artwork).read()

        # Check every 500 milliseconds if Spotify has stopped playing
        while subprocess.Popen('osascript -e "tell application \\"Spotify\\"" -e "player state" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read() == b"playing\n":
            time.sleep(.500)

        # Spotify has stopped playing, stop the recording in Piezo
        subprocess.Popen('osascript -e "activate application \\"Piezo\\"" -e "tell application \\"System Events\\"" -e "keystroke \\"r\\" using {command down}" -e "end tell"', shell=True, stdout=subprocess.PIPE).stdout.read()

        time.sleep(.500)

        # Create directory for the artist
        if not os.path.exists(ripStorageLocation+artist):
            os.makedirs(ripStorageLocation+artist)

        # Create directory for the album
        if not os.path.exists(ripStorageLocation+artist+"/"+album):
            os.makedirs(ripStorageLocation+artist+"/"+album)

        # Move MP3 file from Piezo folder to the folder containing rips.
        for f in os.listdir(piezoStorageLocation):
                if f.endswith(".mp3"):
                    shutil.move(piezoStorageLocation+f, ripStorageLocation+artist+"/"+album+"/"+track+".mp3")

        # Set and/or update ID3 information
        musicFile = eyed3.load(ripStorageLocation+artist+"/"+album+"/"+track+".mp3")
        musicFile.tag.images.set(3, artworkData, "image/jpeg", trackid)
        musicFile.tag.artist = artist
        musicFile.tag.album  = album
        musicFile.tag.title  = track

        musicFile.tag.save()
        continue


if __name__ == "__main__":
    main()