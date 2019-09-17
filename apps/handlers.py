from apps.web import TestHandler, DemoHandler, UpdateFiledHandler

handlers = [
    (r'/', TestHandler),
    (r'/demo', DemoHandler),
    (r'/file', UpdateFiledHandler),
]
