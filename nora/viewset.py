from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from nora.choices import nora
from nora.models import Menu, MenuUser, Ingredient
from nora.permissions import EmployeePermission, NoraPermission
from nora.serializers import MenuSerializer, SerializerSelectUserMenu, IngredientSerializer, CreateUserSerializer
import json

from nora.tasks import send_reminder_menu
from nora.utils.menu_manage import MenuAction
from nora.utils.utils import assign_menu


class MenuList(viewsets.ModelViewSet):
    """
    ViewSet for listing or retrieving all menu objects , list all menu objects
    with list function and detail specific menu with retrieve function, serializer
    class is instance
    """
    #permission_classes = (IsAuthenticated, EmployeePermission, NoraPermission)
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def list(self, request, *args, **kwargs):
        serializer = MenuSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        request_object = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        serializer = MenuSerializer(request_object)
        return Response(serializer.data)


class MenuUserList(viewsets.ModelViewSet):
    """
    ViewSet for listing or retrieving all menu objects , list all menu objects
    with list function and detail specific menu with retrieve function, serializer
    class is instance
    """
    #permission_classes = (IsAuthenticated, EmployeePermission, NoraPermission)
    queryset = MenuUser.objects.all()
    serializer_class = SerializerSelectUserMenu

    def get_queryset(self):
        """
        function to obtain the list of menus selected by users, if the role of the user is nora
        all records are returned, if it is an employee only the menus of the employee
        in session are returned
        """
        data = MenuUser.objects.all() if self.request.user.profile is not None and self.request.user.profile.role == nora \
            else MenuUser.objects.filter(user=self.request.user)
        return data

    def list(self, request, *args, **kwargs):
        serializer = SerializerSelectUserMenu(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        request_object = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        serializer = SerializerSelectUserMenu(request_object)
        return Response(serializer.data)


class CreateMenu(CreateAPIView):
    """
    class for the creation of menu, through the api,
    all the parameters such as name, ingredients and
    date are expected
    """
    #permission_classes = (IsAuthenticated, NoraPermission)
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


class UpdateMenu(UpdateAPIView):
    """
    class to update a specific menu, it is validated
    that on the indicated date there is no other menu with
    the same nam
    """
    #permission_classes = (IsAuthenticated, NoraPermission)
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


class DestroyMenu(DestroyAPIView):
    """
    Class for destroy or remove specific menu , receive one
    <pk:id> of menu selected for destroy
    """
    #permission_classes = (IsAuthenticated, NoraPermission)
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


class CreateMenuSelectedUser(CreateAPIView):
    """
    class to create a relationship between the user and a menu
    on a certain date for example the user mauricio chose the
    tray for July 27, 2021
    """
    #permission_classes = (IsAuthenticated, NoraPermission, EmployeePermission)
    serializer_class = SerializerSelectUserMenu
    queryset = MenuUser


class CreateIngredient(CreateAPIView):
    """
    Class for create instance of Ingredient Model
    """
    #permission_classes = (IsAuthenticated, NoraPermission)
    serializer_class = IngredientSerializer
    model = Ingredient


class CreateUserView(CreateAPIView):
    """
    class for create user in the system and create the profile of user, the profile user
    is create once the user is created, this is done by means of a signal,
    the relationship between user and profile is one to one
    """
    #permission_classes = (IsAuthenticated, NoraPermission)
    model = User
    serializer_class = CreateUserSerializer


class UploadMenuView(APIView):
    """
    Class for get json file with information about Menu
    """
    parser_classes = (MultiPartParser, )
    #permission_classes = (IsAuthenticated, NoraPermission)

    def post(self, request):
        """
        Method for get json file and process data , here create instance of Class
        Execute Workflow ,we need user_id and pin for create instance and execute all function
        """
        try:
            url = request.get_full_path()
            bytes_file = request.data.get('filename').read()
            data = json.loads(bytes_file.decode("UTF-8"))
            menu_information = list(data.values())[0]
            menu_actions = MenuAction(menu_information)
            menu_actions.save_menu()
            send_reminder_menu.delay(request.get_host())
        except UnicodeDecodeError:
            print("Could not open file:")
        return Response({'Processing data': []})


class ConfirmMenu(APIView):
    """
    Class for confirm menu via email , receive a token and filter in model
    UserToken if token in model , save menu user select information of instance
    model and destroy token
    """
    def get(self, request):
        token = request.GET['token']
        create = assign_menu(token)
        if create.get('response'):
            menu = create.get('menu')
            return Response({'Information': f'Menu {menu.menu.name} for {menu.date} was assigned'}, status=200)
        return Response({'error': 'some errors'}, status=400)
