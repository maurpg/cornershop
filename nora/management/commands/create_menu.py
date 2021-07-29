from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command for save menu informations'

    def add_arguments(self, parser):
        """
        Commands receive id parameter for search pokemon in Api
        """
        parser.add_argument('list_ingredients', nargs='+', type=list, help='list ingredient menus')

    def handle(self, *args, **kwargs):
        list_ingredients = kwargs['list_ingredients']
        if list_ingredients is not None:
            print(list_ingredients)
