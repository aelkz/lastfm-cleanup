# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm

APP_CONFIG = {
    'lastfm': {
        'config': {
            'api': {
                'app_name': 'lastfm',
                'key': '<YOUR_KEY>',
                'secret': '<YOUR_SECRET>',
                'username': '<YOUR_USERNAME>',
                'artists_search_limit': 1000,
                'play_count': 1
            }
        },
    }
}
