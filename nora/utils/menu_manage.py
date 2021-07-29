import datetime
from nora.models import Menu, Ingredient


class MenuAction:
    """
    Class for save menu and ingredient
    """

    def __init__(self, list_menu=None):
        self.list_menu = list_menu

    @staticmethod
    def create_ingredient_menu(menu_data):
        """
        Function for create to specific menu, receive data with information about
        menu: date_menu, name_menu and ingredient , first create a new menu object
        after
        """
        menu_new = Menu.objects.create(name=menu_data.get('name'), date_menu=menu_data.get('date_menu'))
        for ingredient in menu_data.get('ingredient'):
            ingredient_new = Ingredient.objects.create(name=ingredient)
            menu_new.ingredient.add(ingredient_new)
        return menu_new

    def save_menu(self):
        """
        Function for send data of menu to function create_ingredient_menu
        returns a list of objects with all objects created of type menu
        """
        return [self.create_ingredient_menu(menu) for menu in self.list_menu]

    @staticmethod
    def filter_by_date(start_date=datetime.date.today(), end_date=datetime.date.today()):
        """
        Filter menu by date, initialize start date and end date with today
        return list object menus with this requirements
        """
        data = Menu.objects.filter(date_menu__range=[start_date, end_date])
        return data

    @staticmethod
    def filter_by_ingredient(ingredient_name=None):
        """
        method to filter by a specific ingredient in the object list of the menu model
        """
        list_ingredients = Ingredient.objects.filter(name__in=ingredient_name)
        recipe = Menu.objects.filter(ingredient__in=list_ingredients)
        return recipe
