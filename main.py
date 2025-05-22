import json
import typing
from color import *

class item :
    def __init__(self, name : str, price : int, quantity : int):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.probability = 0

        


def JsonToItem(jsondata : dict) -> list[item]:

    items : list[item] = []
    for item_data in jsondata["items"]:
        items.append(item(
            name=item_data["name"],
            price=item_data["price"],
            quantity=item_data["quantity"]
        ))
    return items


def calculate_proba(items :  list[item]):

    expected_value = 0
    total_quantity = sum(item.quantity for item in items if item.quantity > 0)

    for item in items:
        if item.quantity > 0:
            probability = item.quantity / total_quantity
            item.probability = round(probability * 100, 2)
            expected_value += round(item.price * probability, 2)

    return expected_value

def display_items(items : list[item], type : str):

    expected_value = calculate_proba(items)
    if type == "base":
        for item in items:
            print(f"{item.name:|^12} - {item.price:|^12} - {item.quantity:|^12} - {item.probability:|^12}")
    elif type == "available":
        i = 0
        for item in items:
            name_len = len(item.name)
            i_len = len(str(i))
            price_len = len(str(item.price))
            quantity_len = len(str(item.quantity))
            probability_len = len(str(item.probability))
            if item.quantity > 0:
                print(f"{i:|^{i_len + 2}} - {BOLD}{item.name:|^{name_len + 2}}{RESET} - {item.price:|^{price_len + 2}} - {item.quantity:|^{quantity_len + 2}} - {BOLD}{item.probability:|^{probability_len + 2}}{RESET}")
                i += 1
            else:
                items.remove(item)
    
    print(f"Valeur attendu a la participation : {expected_value}")

    

def main():
    items : list[item] = []

    json_data = json.load(open("item.json"))
    items = JsonToItem(json_data)
    print("BONJOURRR")
    print(f"Nombre d'item : {len(items)}")
    print(f"Nombre d'objet total : {sum(item.quantity for item in items if item.quantity > 0)}")
    calculate_proba(items)
    #display_items(items, "base")

    while True:
        try:
            display_items(items, "available")
            UserInput = int(input("Quels objets vient de sortir ? Enter number\n$"))
            if UserInput < 0 or UserInput > (len(items) - 1):
                raise ValueError
            print(f"voici l'entre utilisateur --> {items[UserInput].name}")
            items[UserInput].quantity -= 1
        except ValueError:
            print("Veuillez entrer un nombre VALIDE")


if __name__ == "__main__":
    main()