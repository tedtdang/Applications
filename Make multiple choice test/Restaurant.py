"""
Created on Sun Sep 12 00:59:23 2021

@author: TeoHangXanh
"""
import random
import time
import math
from termcolor import colored
from itertools import groupby, chain

food_dict = {
    "Appetizer": [
        'Combination plate',
        "Chicken Satay",
        'Beef skewers',
        "Calamari",
        'Crab Angels',
        "Thai Dumplings",
        "Triangle Tofu",
        'Chicken curry puff',
        'Fish cake',
        'Shrimp blanket',
        'Fried / fresh spring rolls',
        'Chicken wings'
    ],
    "Soup": [
        "Tom Yum",
        "Tom Kha",
        "Wonton soup",
    ],
    "Salad": [
        'Wonder salad',
        "Papaya / Som Tum",
        "Lettuce Wrap",
        "Tiger's tear salad",
        'Yum Talay / Seafood salad',
        "Yum Woon Sen",
    ],
    "Fried Rice": [
        "Spicy Basil Fried Rice",
        "Pineaple Fried Rice",
        'Anothai Fried Rice',
        'Java Fried Rice',
        'Fried Rice'
        "Crab Fried Rice",
    ],
    "Stir-fried": [
        'Teriyaki',
        "Peanut sauce chicken",
        "Orange chicken",
        'Sweet & sour chicken',
        'Shrimp mango',
        'Veggie delight',
        'Ginger lover',
        'Cashew nut',
        'Bell pepper',
        'Pad Ka-tiem',
        'Pad Kra Pow',
        "Pad Prik Khing",
        'Eggplant basil',
    ],
    "Curry": ["Red curry",
              "Green curry",
              "Yellow curry",
              "Beef Musamun curry",
              "Panang curry",
              "Pineapple curry",
              'Roasted Duck red curry',
              'Wild curry'
              ],
    "Noodle": [
        "Pad Thai",
        'Thai style Spaghetti basil',
        "Pad See Eew",
        "Pad Kee Mow",
        "Pad Woon Sen",
        "Poorman noodle",
    ],
    "Signature dish": [
        "Spicy Cat Fish",
        'Volcano Shrimp',
        'Shrimp paradise',
        'Seafood paradise',
        'Seafood dot com',
        'Tilapia deep fried',
        'Red snapper deep fried',
    ],
    "Kid": [
        "Kid's orange chicken",
        "Kid's Teriyaki chicken / beef",
    ],
}


class Restaurant:
    def __init__(self, menu):
        self.menu = dict(sorted(menu.items(), key=lambda kv: kv[1]))
        self.cat_and_name = []
        self.final_dict = dict()

    def to_tuples(self):
        for category, names in food_dict.items():
            for name in names:
                self.cat_and_name.append((category, name))

    def get_abb(self):
        '''Create a dict of which keys are abbreviations of items in a_list'''
        categories = sorted(self.menu.keys())
        for item in categories:
            count = 1
            while item[:count] in self.final_dict:
                count += 1
            self.final_dict[item[:count].title()] = item

    def play(self):
        scores = maximum_scores = 0
        random.shuffle(self.cat_and_name)
        for food in self.cat_and_name:
            answer = input(f"{food[1]}?\n{self.final_dict}").strip().title()
            while answer not in self.final_dict.keys():
                print("Please answer again")
                answer = input(f"{food[1]}?\n{self.final_dict}").strip().title()
            if food[1] in self.menu[self.final_dict[answer]]:
                print(colored("Correct", "green"))
                scores += 1
            else:
                print(
                    colored("Wrong!", "red")
                    + " The category of "
                    + colored(food[1], "yellow")
                    + " is "
                    + colored(food[0], "magenta")
                )
            maximum_scores += 1
        print(f"You got {scores / maximum_scores * 100}%")


restaurant = Restaurant(food_dict)
restaurant.to_tuples()
restaurant.get_abb()
restaurant.play()
