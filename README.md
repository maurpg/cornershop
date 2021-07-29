# Cornershop Nora
| key | value | 
| --------     | --------  |
| URL branch  |  https://gitlab.com/maurpg/cornershop/-/tree/master-28-jul |
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

3==> for create 


