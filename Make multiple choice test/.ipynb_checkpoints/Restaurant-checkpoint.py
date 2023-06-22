# -*- coding: utf-8 -*-
"""
Created on Sun Sep 12 00:59:23 2021

@author: TeoHangXanh
"""
import random
from termcolor import colored

food_dict = {'Appetizer': ['Adamame',
                           'Fishcake',
                           'Crab Cheese Rangoon',
                           'Fried tofu',
                           'Rolls',
                           'Shrimp Blanket',
                           'Chicken wings',
                           'Pork riblets',
                           'Lao Heavenly Beef',
                           'Lao Spicy Sausage',
                           'Thai Lettuce Wrap',
                           'Pot stickers',
                           'Thai Herbal Chicken',
                           'Salt and Pepper Squid',
                           'Nam Khao',
                           'Fried Meat Balls',
                           ],
             'Grill': ['Pork Skewer',
                       'Chicken Satay',
                       'Marinated Beef Steak',
                       ],
             'Salad': ['Larb',
                       'Yum Woon Sen', ],
             'Soup': ['Pho',
                      'Kao',
                      'Tom Yum',
                      ],
             'Entree': ['Sesame Chicken',
                        'Orange Chicken',
                        'Sweet and Sour stir fry',
                        'Mongolian Beef',
                        'Mixed Vegies',
                        'Cashew stir fry',
                        'Pepper Steak',
                        'Thai Spicy Basil',
                        'Broccoli Beef',
                        ]
             }

lookup = {
    'A': 'Appetizer',
    'B': 'Grill',
    'C': 'Salad',
    'D': 'Soup',
    'E': 'Entree',
}
category, name = [], []
for cat, n in food_dict.items():
    category.append(cat)
    name.extend(n)
random.shuffle(name)

scores = maximum_scores = 0
for food in name:
    answer = input(f'What is the category of {food}?\nA. Appetizer\nB. Grill\nC. Salad\nD. Soup\nE. Entree\n')
    if food in food_dict[lookup[answer.strip().title()]]:
        print('Correct!')
        scores += 1
    else:
        print(colored('Wrong!', 'red'))
    maximum_scores += 1
print(f'You got {scores / maximum_scores * 100}%')
