#!/bin/env python3

import datetime
import json
import os
from os import path
import random
from select import select
import tidalapi

dir = path.dirname(path.realpath(__file__))
credential_file = path.join(dir, '.credentials.json')

need_oauth = True
session = tidalapi.Session()

# Check if the credentials are still valid
if os.path.exists(credential_file):
    with open(credential_file, "r") as open_file:
        token_json = json.load(open_file)

    # Check tokens with tidal
    session.load_oauth_session(
        token_json["token_type"],
        token_json["access_token"],
        token_json["refresh_token"],
        datetime.datetime.fromisoformat(token_json["expiry_time"])
    )
    
if not session.check_login():
    # Have user go log in and when this completes, we will auto continue
    session.login_oauth_simple()

    session_dict = {
        "token_type": session.token_type,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "expiry_time": session.expiry_time.isoformat()
    }
    with open(credential_file, "w") as out_file:
        out_file.write(json.dumps(session_dict))

### Now that session is handled, get playlists
playlists = session.user.playlists()
print(playlists)
print("Please select the playlist you wish to shuffle by intering it's number below")
for idx, playlist in enumerate(playlists):
    if("- Electrified" not in playlist.name):
       print(f"  [{idx+1}] {playlist.name}")
# Get playlists on user account
playlist_num = int(input("Playlist Number: ")) - 1

selected_playlist = playlists[playlist_num]
print(f"Electric shuffle {selected_playlist.name}?")
should_continue = bool(input("Continue (Yes/No): "))

### Allow bailing
if not should_continue:
    exit(1)

### Do the thing
tracklist = selected_playlist.tracks()
track_ids = []

for track in tracklist:
    track_ids.append(track.id)

### Signify that this is a copy for the user
shuffled_name = f"{selected_playlist.name} - Electrified"
for playlist in playlists:
    ### Delete an existing version of this playlist if we are re-rolling
    if playlist.name == shuffled_name:
        playlist.delete()

## Create (or re create) the electric playlist
new_playlist = session.user.create_playlist(shuffled_name, selected_playlist.description)

## Add the beautiful music after a quick shuffle
random.shuffle(track_ids)
new_playlist.add(track_ids)
