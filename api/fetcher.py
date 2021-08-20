import requests
from typing import Dict, List
from json import dumps

TIER: str = "techLevel"

class Fetcher:
    api_link: str = "https://api.hearthstonejson.com/v1/91040/enUS/cards.json"
    cached_json: list = None

    @staticmethod
    def fetch(api_link: str = None, debug: bool = False, invalidate_cache: bool = False) -> List[dict]:
        if api_link is None:
            api_link = Fetcher.api_link

        # buffers
        if invalidate_cache:
            Fetcher.cached_json = None

        if Fetcher.cached_json is None:
            print("No api cache, requesting")
            json = requests.get(api_link).json()  # type: list
            Fetcher.cached_json = json
        else:
            json = Fetcher.cached_json
        filtered_json = []
        categorized_by_tier: Dict[int, List[str]] = {}
        for ii in range(1, 7):
            categorized_by_tier[ii] = []

        # if no battlegrounds tier is set, dont care about it
        for card in json:  # type: dict
            if card.get(TIER) is not None:
                filtered_json.append(card)

        # sort filtered cards by tier
        filtered_json.sort(key=lambda c: c[TIER])
        for card in filtered_json:
            text: str = card.get("text")
            if text is not None:
                text = text.replace("\n", " ")
            if debug:
                print(f'{card.get(TIER)} - {card.get("name")} - {text}')
            categorized_by_tier[card[TIER]].append(card["name"])

        with open("fetch.json", "w") as fetch:
            fetch.write(dumps(filtered_json, indent=2))

        for key, val in categorized_by_tier.items():
            if debug:
                print(f"\nTier {str(key)}:")
                print("\n".join(val))

        return filtered_json


if __name__ == "__main__":
    Fetcher.fetch()
