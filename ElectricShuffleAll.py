#!/bin/env python3

import datetime
import json
import os
from os import path
import random
from select import select
import tidalapi


def token_refresh(session, refresh_token):
    """
    Retrieves a new access token using the specified parameters, updating the current access token

    :param refresh_token: The refresh token retrieved when using the OAuth login.
    :return: True if we believe the token was successfully refreshed, otherwise False
    """
    url = 'https://auth.tidal.com/v1/oauth2/token'
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': session.config.client_id,
        'client_secret': session.config.client_secret
    }

    request = session.request_session.post(url, params)
    json = request.json()
    if not request.ok:
        log.warning("The refresh token has expired, a new login is required.")
        return json
    session.access_token = json['access_token']
    session.expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=json['expires_in'])
    session.token_type = json['token_type']
    return json

dir = path.dirname(path.realpath(__file__))
credential_file = path.join(dir, '.credentials.json')

need_oauth = True
print("Creating Session")
session = tidalapi.Session()

# Check if the credentials are still valid
if os.path.exists(credential_file):
    with open(credential_file, "r") as open_file:
        token_json = json.load(open_file)

    token_refresh(session, token_json["refresh_token"])

    # Check tokens with tidal
    session.load_oauth_session(
        token_json["token_type"],
        token_json["access_token"],
        token_json["refresh_token"],
        datetime.datetime.fromisoformat(token_json["expiry_time"])
    )

    new_token_json = token_refresh(session, token_json["refresh_token"])
    session_dict = {
        "token_type": session.token_type,
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "expiry_time": session.expiry_time.isoformat()
    }
    with open(credential_file, "w") as out_file:
        out_file.write(json.dumps(session_dict))

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
print("Getting Playlists")
playlists = session.user.playlists()

for playlist in playlists:
    ### Signify that this is a copy for the user
    shuffled_name = f"{playlist.name} - Electrified"
    
    if "- Electrified" in playlist.name:
        playlist.delete()
    else:
        print("Shuffling playlist " + playlist.name)

        ### Do the thing
        tracklist = playlist.tracks()
        track_ids = []

        for track in tracklist:
            track_ids.append(track.id)

        ## Create (or re create) the electric playlist
        new_playlist = session.user.create_playlist(shuffled_name, playlist.description)

        ## Add the beautiful music after a quick shuffle
        random.shuffle(track_ids)
        new_playlist.add(track_ids)
