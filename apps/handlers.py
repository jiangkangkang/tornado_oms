from web import LoginHandler
from web import HomeHandler
from web import CreateUserHandler
from web import LogOutHandler
from web.top_play import LoadTopRankingHandler

handlers = [
    (r"/", HomeHandler),
    (r"/login", LoginHandler),
    (r"/logout", LogOutHandler),
    (r"/create_user", CreateUserHandler),
    (r"/api/top_ranking", LoadTopRankingHandler),
]
