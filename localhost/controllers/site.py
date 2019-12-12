from _core.controller import controller
from flask import render_template, session
from flask import request


class site(controller):
    def index(self):
        from model.files import files
        page = 1
        size = 100
        # files.query.offset(page * size).limit(size).all()
        f = files.query.all()
        return render_template('site/index.html', files=f)

    def page404(self):
        return render_template('site/page404.html')
