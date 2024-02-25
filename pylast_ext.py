from urllib.parse import quote_plus
import pylast as pylast


class PyLastExt(pylast.Library):
    def __init__(self, user: str, network: pylast.LastFMNetwork, artist: pylast.Artist):
        super().__init__(user=user, network=network)
        self.artist = artist
        self.network = network

    def remove_artist(self) -> None:
        """Remove an artist from user's library."""
        """This api doesn't exists on ws.audioscrobbler.com, so this method could be improved in the future """

        # print('-----')
        # params = self._get_params()
        # req: pylast._Request = pylast._Request(self.network, self.ws_prefix + ".removeTag", params)
        # print(self.ws_prefix)
        # print(params)
        # print(self.ws_prefix + ".removeTag")
        # print(req)
        # print(req.__str__())
        # print('-----')

        url_safe: str = 'library/music/' + quote_plus(quote_plus(str(self.artist.name))).lower()

        url1: str = f"https://www.last.fm/user/{self.user}/{url_safe}"
        url2: str = f"https://www.last.fm/user/{self.user}/{url_safe}/+delete"

        print(url1)
        print(url2)
        print('---')
