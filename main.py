# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import re

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    data = [
        "Kauravaahtoa (A ,G ,L ,M ,Veg)",
        "Uuniomenoita (G ,L ,M ,Veg)"
    ]
    food_re = re.compile(r"(?P<Food>.*?) ?\((?P<Allergens>.+(?=\)))")
    food = []
    all = []
    for m in [food_re.findall(x) for x in data]:
        f, a = m[0]
        food.append(f)
        all += a.split(',')
    print(",".join(food))
    print(all)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
