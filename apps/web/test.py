from tornado.web import RequestHandler


class TestHandler(RequestHandler):
    def get(self, *args, **kwargs):
        name = self.get_query_argument('name')
        age = self.get_query_argument('age')
        self.render('test2.html', name=name, age=age)


class DemoHandler(RequestHandler):
    def post(self, *args, **kwargs):
        name = self.get_body_argument('name')
        password = self.get_body_argument('password')
        self.render('demo.html', name=name, password=password)


class UpdateFiledHandler(RequestHandler):
    def get(self):
        self.render('file.html')

    def post(self, *args, **kwargs):
        files = self.request.files.get('filename')
        print(files)
        self.write('file')
