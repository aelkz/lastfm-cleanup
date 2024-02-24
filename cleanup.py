import logging
import time
import pylast
from typing import Optional
from getpass import getpass
from config import APP_CONFIG
from pylast_ext import PyLastExt


def main():
    logging.basicConfig(level=logging.INFO)

    # load configs
    lastfm_config = APP_CONFIG['lastfm']  # lastfm
    config = lastfm_config['config']['api']  # config > api

    config_keys = list(config.keys())
    keys: list = ['key', 'secret', 'username', 'password']

    idx: int = 0
    for k in keys:
        if k not in config_keys:
            config_keys.append(keys[idx])
            config[keys[idx]] = None
        idx += 1

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
        logging.error('artists_search_limit value must be a valid number')
        exit(1)

    if config['artists_search_limit'] < 1 or config['artists_search_limit'] > 1000:
        logging.error('artists_search_limit value must be a valid number between 1 and 1000')
        exit(1)

    if type(config['play_count']) != int:
        print('play_count value must be a valid number')
        exit(1)

    network: Optional[pylast.LastFMNetwork] = None
    try:
        network = pylast.LastFMNetwork(
            api_key=config['key'],
            api_secret=config['secret'],
            username=config['username'],
            password_hash=pylast.md5(config['password']),
        )
    except pylast.WSError:
        logging.error('username/password incorrect. Check your config file and try again.')

    logging.info('play count:%s', config['play_count'])
    logging.info('searching for items:')

    try:
        library: pylast.Library = pylast.Library(user=config['username'], network=network)  # <class 'pylast.Library'>
        library_items: list[pylast.LibraryItem] = library.get_artists(limit=config['artists_search_limit'])  # <class 'list'>

        start = time.time()
        idx: int = 0
        print(' ')

        for library_item in library_items:
            artist: pylast.Artist = library_item.item
            if library_item.playcount == config['play_count']:
                idx += 1
                logging.info('%s %s', artist.name, library_item.playcount)

                ext: PyLastExt = PyLastExt(user=config['username'], network=network, artist=artist)
                ext.remove_artist()

        if idx == 0:
            message = f"no artists found with play_count = {config['play_count']}."
            logging.info(message)
        else:
            message = f'{idx} artists found from your last.fm user library.'
            logging.info(message)

        total_time = time.time() - start
        message = f'Execution end time: {time.strftime("%m/%d/%Y %H:%M:%S")}. ' \
                  f'Execution took: {total_time / 60:0.2f} min to complete.'
        logging.info(message)
    except pylast.PyLastError:
        logging.info('Something wrong happened. Check your config file and try again.')


if __name__ == '__main__':
    main()
