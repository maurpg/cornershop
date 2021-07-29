from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from nora.tasks import send_reminder_menu
from nora.utils.menu_manage import MenuAction


class UploadMenuView(APIView):
    """
    Class for get json file witn information about transactions
    """
    parser_classes = (MultiPartParser, )

    def post(self, request):
        """
        Method for get json file and process data , here create instance of Class
        Execute Workflow ,we need user_id and pin for create instance and execute all function
        """
        try:
            bytes_file = request.data.get('filename').read()
            data = json.loads(bytes_file.decode("UTF-8"))
            menu_information = list(data.values())[0]
            menu_actions = MenuAction(menu_information)
            #menu_actions.save_menu()
            #print(menu_actions.filter_by_date('2021-07-10', '2021-07-11'))
            print(menu_actions.filter_by_ingredient(['start']))
            send_reminder_menu.delay()
        except UnicodeDecodeError:
            print("Could not open file:")
        return Response({'Processing data': []})
