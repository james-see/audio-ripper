# audio-ripper

## what  
get mp3s local with Piezo and Spotify and Python in Mac OS

## why  
I needed to get mp3s to my Light Phone https://www.thelightphone.com


## steps to perform to get run

1. `git clone https://github.com/jamesacampbell/audio-ripper.git`
2. `cd audio-ripper`
3. `cp example_config.py config.py`
4. open Spotify desktop app and the Piezo app
4. select a playlist you want to rip, copy the URL of the playlist by using the right click "Copy link to playlist"
5. truncate just the playlist id from the url, for instance my best of 2022 playlist url: https://open.spotify.com/playlist/4bAnOAgblJnWhMYSQWbZHL?si=dfec2f38667744fb, the id is just `4bAnOAgblJnWhMYSQWbZHL`
6. put the playlist id from step 5 in thr config.py file replacing the example variable
7. Go https://developer.spotify.com/console/get-playlist-tracks/ and generate a bearer token. (You may have to do it twice, errors first time from Brave) Copy the token from the right column and paste it into the config.py replacing the example token
8. By default the files are stored at {your home directory}/Ripped/
9. Run `pip3 install -f requirements.txt`
10. Run `python3 recordtracks.py` and wait for it to finish. You will see it running.

## questions / issues?

Use the issues tab above and submit problems / suggestions.

Otherwise Enjoy. 

Note: Piezo cost $25 USD. It is available here: https://rogueamoeba.com/piezo/


