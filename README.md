# Cornershop Nora
| key | value | 
| --------     | --------  |
| URL branch  | https://github.com/maurpg/cornershop/tree/master_cornershop |
| Requirements path   | cornershop/requirements.txt |
| Settings path       | cornershop/settings.py |
| Default Email From Error 500   | n/a |
| Django version      | 3.2.5  |
| DB Extension        | n/a |
| Point of Contact    | mauricio_pacheco_grijalbi@hotmail.com |

Functionality
the solution proposed to this exercise is an api, based on django rest framework, 
all the necessary services were created to satisfy all the requirements, the authentication was worked with jwt

1==> For the creation of the menu a service was created, which receives a json file with the information 
of the menus such as the name of the menu, entries and date url ===>http://{host}/

2==> to list all the menus a service was created with the following url 
http://{host}/api/menu_list and http://{host}/api/menu_list/{id} for retrieve

3==> to select the desired menu from the options sent to the mail http://{host}/api/confirm_menu/

4==> for update menu http://{host}/api/update_menu/{id}

5==> for destroy menu http://{host}/api/destroy_menu/{id}

6==> to get all the menus selected by the users http://{host}/api/menu_list_user_selected

7==>Additionally, token authentication was implemented, in case it is required to protect any service
   
get_token ===>api/get_token/
refresh_token ===>api/get_token_refresh/


