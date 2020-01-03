
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(16), index=True)
    phone = sa.Column(sa.String(11))
    password = sa.Column(sa.String(64))
    email = sa.Column(sa.String(64))
    token = sa.Column(sa.String(64))
    status = sa.Column(sa.String(10))
    create_time = sa.Column(sa.DateTime)
    remark = sa.Column(sa.String(250))


class Ranking(Base):
    __tablename__ = 'ranking_manage'
    id = sa.Column(sa.Integer, primary_key=True)
    title = sa.Column(sa.String(100), index=True)
    url = sa.Column(sa.String(500))
    remark = sa.Column(sa.String(200))
    click_num = sa.Column(sa.Integer(), index=True)
    create_time = sa.Column(sa.DateTime)


if __name__ == "__main__":

    engine = sa.create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
