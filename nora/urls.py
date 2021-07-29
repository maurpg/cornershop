from django.urls import path

from nora.views import UploadMenuView
from nora.viewset import MenuList, UpdateMenu, CreateMenuSelectedUser, CreateIngredient, CreateMenu, DestroyMenu, \
    CreateUserView, MenuUserList

urlpatterns = [path('', UploadMenuView.as_view(), name='index'),
               path('api/menu_list', MenuList.as_view({'get': 'list'}), name='menu_list'),
               path('api/menu_list/<int:pk>', MenuList.as_view({'get': 'retrieve'}), name='menu_detail'),
               path('api/menu_list_user_selected', MenuUserList.as_view({'get': 'list'}), name='menu_select_user'),
               path('api/update_menu/<int:pk>', UpdateMenu.as_view(), name='menu_update'),
               path('api/destroy_menu/<int:pk>', DestroyMenu.as_view(), name='remove_menu'),
               path('api/select_menu', CreateMenuSelectedUser.as_view(), name='select_menu'),
               path('api/create_ingredient', CreateIngredient.as_view(), name='create_ingredient'),
               path('api/create_menu', CreateMenu.as_view(), name='create_menu'),
               path('api/create_user', CreateUserView.as_view(), name='create_user'),
               ]
