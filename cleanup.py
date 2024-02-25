import logging
import time
import pylast
from typing import Optional
from getpass import getpass
from config import APP_CONFIG, CustomLoggingFormatter
from pylast_ext import PyLastExt

# logging configuration
logger = logging.getLogger("app")
logger.setLevel(level=logging.INFO)

simple_logger = logging.getLogger("app_simple")
simple_logger.setLevel(level=logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(CustomLoggingFormatter(pattern="%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"))

simple_ch = logging.StreamHandler()
simple_ch.setLevel(logging.INFO)
simple_ch.setFormatter(CustomLoggingFormatter(pattern="%(message)s"))

logger.addHandler(ch)
simple_logger.addHandler(simple_ch)


def validate(k: str, v: int, higher: int, lower: int = 1):
    if type(v) != int:
        logger.error(f'{k} value must be a valid number')
        exit(1)

    if v < lower or v > higher:
        logger.error(f'{k} value must be a valid number between {lower} and {higher}')
        exit(1)


def main():
    # load configs
    lastfm_config = APP_CONFIG['lastfm']
    config = lastfm_config['config']['api']

    config_keys = list(config.keys())
    keys: list = ['key', 'secret', 'username', 'password']

    # initialize config keys
    idx: int = 0
    for k in keys:
        if k not in config_keys:
            config_keys.append(keys[idx])
            config[keys[idx]] = None
        idx += 1

    for k in config.keys():
        if not config[k]:
            # request all the missing keys
            input_msg: str = f'Enter {config["username"]} last.fm {k}: '
            if k == 'secret' or k == 'password':
                config[k] = getpass(input_msg)
            else:
                config[k] = input(input_msg)

    # validate key values
    validate(k='artists_search_limit', v=config['artists_search_limit'], higher=1000)
    validate(k='play_count', v=config['play_count'], higher=100)

    network: Optional[pylast.LastFMNetwork] = None

    try:
        network = pylast.LastFMNetwork(
            api_key=config['key'],
            api_secret=config['secret'],
            username=config['username'],
            password_hash=pylast.md5(config['password']),
        )
    except pylast.WSError:
        logger.error('username/password incorrect. Check your config file and try again.')

    logger.warning('play count:%s', config['play_count'])
    logger.info('searching for items:')

    try:
        library: pylast.Library = pylast.Library(user=config['username'], network=network)
        library_items: list[pylast.LibraryItem] = library.get_artists(limit=config['artists_search_limit'])

        start = time.time()
        idx: int = 0
        print(' ')

        ext: PyLastExt = PyLastExt(user=config['username'], network=network)

        for library_item in library_items:
            artist: pylast.Artist = library_item.item
            if library_item.playcount == config['play_count']:
                idx += 1
                simple_logger.warning('%s %s', artist.name, library_item.playcount)

                ext.remove_artist(artist=artist)

        if idx == 0:
            message = f"no artists found with play_count = {config['play_count']}."
        else:
            message = f'{idx} artists found from your last.fm user library.'
        logger.info(message)

        total_time = time.time() - start
        message = f'Execution end time: {time.strftime("%m/%d/%Y %H:%M:%S")}. ' \
                  f'Execution took: {total_time / 60:0.2f} min to complete.'
        logger.info(message)
    except pylast.PyLastError:
        logger.info('Something wrong happened. Check your config file and try again.')


if __name__ == '__main__':
    main()
