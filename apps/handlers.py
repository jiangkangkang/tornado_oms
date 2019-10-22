from web import LoginHandler
from web import HomeHandler
from web import CreateUserHandler
from web import LogOutHandler

handlers = [
    (r"/", HomeHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogOutHandler),
    (r"/create_user", CreateUserHandler),
]
