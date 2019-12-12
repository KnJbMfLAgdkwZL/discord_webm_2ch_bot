from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///main.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


# Для создания базы данных можно воспользоваться функцией init_db
def init_db():
    # Здесь нужно импортировать все модули, где могут быть определены модели,
    # которые необходимым образом могут зарегистрироваться в метаданных.
    # В противном случае их нужно будет импортировать до вызова init_db()
    # import model.user
    # Base.metadata.create_all(bind=engine)
    pass


class model:
    def __init__(self):
        # print(f'Constructor {self.getName()}')
        pass

    def __del__(self):
        # print(f'Destructor {self.getName()}')
        pass

    def getName(self):
        return self.__class__.__name__
