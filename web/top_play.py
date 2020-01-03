from tornado.gen import coroutine
from tornado.web import authenticated

from execute_sqls.ranking_manage_sql import get_top_ranking
from web import BaseHandler


class LoadTopRankingHandler(BaseHandler):

    @authenticated
    @coroutine
    def get(self):
        top_ranking_list = yield get_top_ranking()
        self.build_json_response(top_ranking_list)
