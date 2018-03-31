# coding:utf-8
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, Text, DateTime,\
    and_, or_, SmallInteger, Float, DECIMAL, desc, asc, Table, join, event
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session, aliased, mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm.collections import attribute_mapped_collection
import uuid
import datetime

# TODO move config variable to config.py
# TODO migrate
engine = create_engine("mysql+pymysql://root:root@0.0.0.0:3306/sharebicycle?charset=utf8", pool_recycle=7200)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def next_id():
    return uuid.uuid1().hex

class Extension(object):

    @classmethod
    def add(cls, resource):
        db_session.add(resource)
        try:
            db_session.commit()
            return resource
        except Exception as e:
            db_session.rollback()
            return str(e)
    
    @classmethod
    def delete(cls, resource):
        resource.is_del = 1
        # db_session.delete(resource)
        try:
            db_session.commit()
            return resource
        except Exception as e:
            db_session.rollback()
            return str(e)

    @classmethod
    def update(cls, resource, params={}):
        try:
            [setattr(resource, key, value) for key, value in params.items()]
            db_session.commit()
            return resource
        except Exception as e:
            db_session.rollback()
            return str(e)

            
    def _gen_tuple(self):
        "序列化输出"
        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""
    
        for col in self.__table__.columns:
            v = getattr(self, col.name)
            if not v:
                value = 0
            elif isinstance(col.type, DateTime):
                value = convert_datetime(v)
            elif isinstance(col.type, Integer):
                value = int(v)
            elif isinstance(col.type, Float):
                value = float(v)
            else:
                value = v
            yield (col.name, value)
    
    def to_dict(self):
        return dict(self._gen_tuple())
    
    def to_json(self):
        return json.dumps(self.to_dict())

class User(Base, Extension):
    __tablename__ = 'user'

    id = Column('id', String(255), primary_key=True, default=next_id)
    name = Column('name', String(255), index=True, nullable=False)
    head_pic = Column('head_pic', String(255), default='')
    sex = Column('sex', String(255), default='unknown')
    role = Column('role', Integer, default=0)
    mobile = Column('mobile', String(11), nullable=False)
    password = Column('password', String(16), nullable=False)
    email = Column('email', String(32), default=None)
    createTime = Column('createTime', DateTime, index=True, default=datetime.datetime.now)
    lastLoginTime = Column('lastLoginTime', DateTime, default=None)
    is_del = Column('is_del', Integer, default=0)
    credit = Column('credit', Integer, default=0)
    balance = Column('balance', Float, default=0)
    remark = Column('remark', String(500), default='')
    status = Column('status', Integer, default=0)


class Article(Base, Extension):
    __tablename__ = 'aritcle'
    id = Column('id', String(255), primary_key=True, default=next_id)
    title = Column('title', String(255), nullable=False)
    author = Column('author', String(255), nullable=False)
    source = Column('source', String(255), default=None)
    content = Column('content', Text, nullable=False)
    createTime = Column('createTime', DateTime, index=True, default=datetime.datetime.now)
    operator = Column('operator', String(255), nullable=False)
    like = Column('like', Integer, default=0)
    share = Column('share', Integer, default=0)
    ifopen = Column('ifopen', Integer, default=0)
    cover = Column('cover', String(255), default=None)
    categoryid = Column('categoryid', Integer, nullable=False)
    lastupdate = Column('lastupdate', DateTime, index=True, default=datetime.datetime.now)
    userid = Column('userid', Integer, nullable=False)
    is_del = Column('is_del', Integer, default=0)
    status = Column('status', Integer, default=1)


class Bike(Base, Extension):
    __tablename__ = 'bike'
    id = Column('id', String(255), primary_key=True, default=next_id)
    useTime = Column('useTime', DateTime, default=datetime.datetime.now)
    lastUseTime = Column('lastUseTime', DateTime, default=None)
    status = Column('status', Integer, default=0)
    btype = Column('btype', Integer, default=0)
    useCount = Column('useCount', Integer, default=0)
    repaireCount = Column('repaireCount', Integer, default=0)
    is_del = Column('is_del', Integer, default=0)


class Category(Base, Extension):
    __tablename__ = 'category'
    id = Column('id', String(255), primary_key=True, default=next_id)
    name = Column('name', String(255), nullable=False)
    is_del = Column('is_del', Integer, default=0)
    enable = Column('enable', Integer, default=0)


class Fee(Base, Extension):
    __tablename__ = 'fee'
    id = Column('id', String(255), primary_key=True, default=next_id)
    ftype = Column('ftype', Integer, nullable=False)
    title = Column('title', String(255), nullable=False)
    baseFee = Column('baseFee', Float, default=0)
    deposit = Column('deposit', Float, default=0)
    feePerHour = Column('feePerHour', Float, default=0)
    is_del = Column('is_del', Integer, default=0)


class Money(Base, Extension):
    __tablename__ = 'money'
    id = Column('id', String(255), primary_key=True, default=next_id)
    userId = Column('userId', Integer, nullable=False)
    mtype = Column('mtype', Integer, nullable=False)
    moneyTime = Column('moneyTime', DateTime, nullable=False)
    count = Column('count', Integer, default=0)
    result = Column('result', Integer, nullable=False)
    msg = Column('msg', String(255), default=None)
    resultTime = Column('resultTime', DateTime, nullable=False)
    is_del = Column('is_del', Integer, default=0)


class RepairHistory(Base, Extension):
    __tablename__ = 'repairhistory'
    id = Column('id', String(255), primary_key=True, default=next_id)
    repairTimeStart = Column('reaprTimeStart', DateTime, nullable=False)
    repairTimeStop = Column('reaprTimeStop', DateTime, nullable=False)
    remark = Column('remark', String(25), default=None)
    repairTime = Column('repairTime', DateTime, nullable=False)
    is_del = Column('is_del', Integer, default=0)
    bikeId = Column('bikeId', Integer, nullable=False)


class UseHistory(Base, Extension):
    __tablename__ = 'usehistory'
    id = Column('id', String(255), primary_key=True, default=next_id)
    userId = Column('userId', Integer, nullable=False)
    bikeId = Column('bikeId', Integer, nullable=False)
    useTimeStart = Column('useTimeStart', DateTime, nullable=False)
    useTimeStop = Column('useTimeStop', DateTime, nullable=False)
    fee = Column('fee', Float, default=0)
    is_del = Column('is_del', Integer, default=0)


if __name__ == '__main__':
    # CREATE DATABASE IF NOT EXISTS sharebicycle DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
    # SELECT CONCAT('drop table ',table_name,';') FROM information_schema.`TABLES` WHERE table_schema='sharebicycle';
    Base.metadata.create_all(engine)