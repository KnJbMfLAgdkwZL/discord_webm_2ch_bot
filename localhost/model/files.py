from sqlalchemy import Column, String
from _core.model import Base, model


class files(Base, model):
    __tablename__ = 'files'
    md5 = Column(String(120), primary_key=True)
    thumbnail = Column(String(120))
    path = Column(String(120))
    fullname = Column(String(120))
    name = Column(String(120))

    def __init__(self, md5=None, thumbnail=None, path=None, fullname=None, name=None):
        self.md5 = md5
        self.thumbnail = thumbnail
        self.path = path
        self.fullname = fullname
        self.name = name

    def __repr__(self):
        return f'<files: {self.md5}, {self.thumbnail}, {self.path}, {self.fullname}, {self.name}>'
