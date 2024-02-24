import time
import pylast
from getpass import getpass
from config import APP_CONFIG
from pylast_ext import PyLastExt


def main():
    # load configs
    lastfm_config = APP_CONFIG['lastfm']  # lastfm
    config = lastfm_config['config']['api']  # config > api

    config_keys = list(config.keys())
    keys: list = ['key', 'secret', 'username', 'password']

    if 'key' not in config_keys:
        config_keys.append(keys[0])
        config[keys[0]] = None
    if 'secret' not in config_keys:
        config_keys.append(keys[1])
        config[keys[1]] = None
    if 'username' not in config_keys:
        config_keys.append(keys[2])
        config[keys[2]] = None
    if 'password' not in config_keys:
        config_keys.append(keys[3])
        config[keys[3]] = None

    for k in config.keys():
        # Environment variables overwrite values
        formatted_key = f'{k}'

        if not config[k]:
            # request all the missing keys
            if k == 'secret' or k == 'password':
                config[k] = getpass(f'Enter {config["username"]} last.fm {formatted_key}: ')
            else:
                config[k] = input(f'Enter {formatted_key}: ')

    if type(config['artists_search_limit']) != int:
        print('artists_search_limit value must be a valid number')
        exit(1)

    if config['artists_search_limit'] < 1 or config['artists_search_limit'] > 1000:
        print('artists_search_limit value must be a valid number between 1 and 1000')
        exit(1)

    if type(config['play_count']) != int:
        print('play_count value must be a valid number')
        exit(1)

    network = pylast.LastFMNetwork(
        api_key=config['key'],
        api_secret=config['secret'],
        username=config['username'],
        password_hash=pylast.md5(config['password']),
    )

    print('searching for items:\n')

    library: pylast.Library = pylast.Library(user=config['username'], network=network)  # <class 'pylast.Library'>
    library_items: list[pylast.LibraryItem] = library.get_artists(limit=config['artists_search_limit'])  # <class 'list'>

    start = time.time()
    idx: int = 0

    for library_item in library_items:
        artist: pylast.Artist = library_item.item
        if library_item.playcount == config['play_count']:
            idx += 1
            print(artist.name, library_item.playcount)

            ext: PyLastExt = PyLastExt(user=config['username'], network=network, artist=artist)
            ext.remove_artist()
            print(f'\n{idx} artists cleaned up from your last.fm user library.')

    if idx == 0:
        print(f"no artists found with play_count = {config['play_count']}.")

    total_time = time.time() - start
    message = f'Execution end time: {time.strftime("%m/%d/%Y %H:%M:%S")}. ' \
              f'Execution took: {total_time / 60:0.2f} min to complete.'
    print(message)


if __name__ == '__main__':
    main()
