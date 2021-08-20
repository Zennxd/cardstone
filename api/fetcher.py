import requests
from typing import Dict, List
from json import dumps

TIER: str = "techLevel"

class Fetcher:
    api_link: str = "https://api.hearthstonejson.com/v1/91040/enUS/cards.json"

    @staticmethod
    def fetch(api_link: str = None):
        if api_link is None:
            api_link = Fetcher.api_link

        # curl
        json = requests.get(api_link).json()  # type: list
        filtered_json = []
        categorized_by_tier: Dict[int, List[str]] = {}
        for ii in range(1, 7):
            categorized_by_tier[ii] = []

        for card in json:  # type: dict
            if card.get(TIER) is not None:
                filtered_json.append(card)

        filtered_json.sort(key=lambda c: c[TIER])
        for card in filtered_json:
            text: str = card.get("text")
            if text is not None:
                text = text.replace("\n", " ")
            print(f'{card.get(TIER)} - {card.get("name")} - {text}')
            categorized_by_tier[card[TIER]].append(card["name"])

        with open("fetch.json", "w") as fetch:
            fetch.write(dumps(filtered_json, indent=2))

        for key, val in categorized_by_tier.items():
            print(f"\nTier {str(key)}:")
            print("\n".join(val))


if __name__ == "__main__":
    Fetcher.fetch()
