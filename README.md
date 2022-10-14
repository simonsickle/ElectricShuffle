### Electric Shuffle

This is a (terrible) app to shuffle your Tidal playlists since there are not (currently) any native ways to due so on a Tesla. Hopefully it will be depreciated in the near future and we can go back to just shuffling in the car :)

## WARNING, DRAGONS

I'm not responsible for bricked devices, dead SD cards, thermonuclear war, or you getting fired because your entire playlist got deleted and you are now too sad to work. This _shouldn't happen_ but the app is very lightly tested.

### Setting up Environment

1. Clone this repo to your computer
1. Create a venv to install packages by running `python3 -m venv .venv`
1. Start using the virtual env by running `source .venv/bin/activate`
1. Install required packages by running `pip3 install -r requirements.txt`

### Running ElectricShuffle
1. Run the program `./ElectricShuffle.py`
1. Log in by clicking the link (or copying it to your browser). Once logged in return to the terminal. (Once per environment)
1. Pick a playlist to shuffle
1. Confirm that is the playlist you want
1. Go enjoy some tunes! Notice your new playlist which is a copy of your current one but with an " - Electrified" suffix. This is the shuffled one.

### Running ElectricShuffleAll
This script requires no human intervention beyond the initial login. Run it one time manually to login, then automate to your heart's content.

**Note:** On linux VMs there is an issue where the tidalapi package sends requests too fast for the tidal servers. Adding time.sleep(1) to the tidalapi playlist.py \__init__ resolves the issue.

1. Run the program `./ElectricShuffleAll.py`
1. Log in by clicking the link (or copying it to your browser). Once logged in return to the terminal. (Once per environment)
1. Shuffles all playlists

### Contributing

Contributions are welcome, this is just a little hobby script I wrote to make my life easier. Feel free to change it and send a pull request.

### Disclaimer

While I work at Block as of writing this, I do not work on the Tidal team. This is ENTIRELY unofficial and unsupported and is my own work.