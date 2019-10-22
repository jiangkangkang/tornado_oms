
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


if __name__ == "__main__":

    engine = sa.create_engine("sqlite:///test.db")
    Base.metadata.create_all(engine)
