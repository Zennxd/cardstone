import requests

class Fetcher:
    api_link: str = "https://api.hearthstonejson.com/v1/91040/enUS/cards.json"

    @staticmethod
    def fetch(api_link: str = None):
        if api_link is None:
            api_link = Fetcher.api_link

        # curl
        json = requests.get(api_link).json()

        for card in json:  # type: dict
            if card.get("battlegroundsPremiumDbfId") is not None:
                text: str = card.get("text")
                if text is not None:
                    text = text.replace("\n", " ")

                print(f'{card.get("name")} - {text}')


if __name__ == "__main__":
    Fetcher.fetch()
