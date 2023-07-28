### Code by Jeremy Fleming! ### 
import requests
from bs4 import BeautifulSoup
import random

# URL of all Jumpstart 2022 Pack Decklists to webscrape from
URL = "https://magic.wizards.com/en/news/feature/jumpstart-2022-booster-themes-and-card-lists/"

# Get the html of the website
response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Scrape for all decklists, storing lists for the deck titles and cardlists (while also stripping away excess characters)
deck_names = soup.find_all(name="deck-list")
deck_list = [deck.getText().strip("\n") for deck in deck_names]
deck_list_titles = ["".join(c for c in deck['deck-title'] if c.isalpha() or c == ' ').strip(' ') for deck in deck_names]

# Main function to generate a random decklist according to user preference
def main():
    indices = range(len(deck_list))
    option = ""
    while option != "1" and option != "2" and option!= "3":
        option = input("Would you like... \nA completely random decklist? [1]\nA two color decklist? [2]\nOr an MTG Arena style decklist? [3]\n> ")
        deck_indices = []
        match option:
            case "1":
                # Completely random decklist by sampling 2 unique deck halves 
                deck_indices = random.sample(indices, 2)
            case "2":
                # There are 24 packs for each color and 1 colorless. 1/121 trials we'll get the colorless pack.
                # Otherwise, we sample 2 uniquely colored deck halves
                if random.randint(0, 120) == 0:
                    deck_indices = random.sample(indices[0:120], 1)
                    deck_indices.append(120)
                else:
                    colors = random.sample(range(5), 2)
                    deck_indices.append(random.sample(indices[colors[0] * 24:(colors[0] + 1) * 24], 1)[0])
                    deck_indices.append(random.sample(indices[colors[1] * 24:(colors[1] + 1) * 24], 1)[0])
            case "3":
                # "MTG Arena Style" - Gives users 3 choices for each deck half and they input which halves they want
                deck_options = random.sample(indices, 6)
                for i in range(2):
                    choice = ""
                    while choice != "1" and choice != "2" and choice != "3":
                        choice = input("Would you like... \n" + deck_list_titles[deck_options[i * 3]] + \
                            " [1]\n" + deck_list_titles[deck_options[i * 3 + 1]] + \
                                " [2]\nOr " + deck_list_titles[deck_options[i * 3 + 2]] + " [3]\n> ")
                        if choice == "1" or choice == "2" or choice == "3":
                            deck_indices.append(indices[deck_options[i * 3 + (int) (choice) - 1]])
                        else:
                            print("\nType '1', '2', or '3'\n")
            case _:
                print("\nType '1', '2', or '3'\n")
                continue
        # Prints out deck titles and decklist!
        print('"' + deck_list_titles[deck_indices[0]] + " & " + deck_list_titles[deck_indices[1]] + '"')
        print(deck_list[deck_indices[0]] + "\n" + deck_list[deck_indices[1]])

main()