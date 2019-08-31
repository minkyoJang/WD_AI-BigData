#!/usr/bin/env python
# coding: utf-8

# ORM을 사용하는 이유는 객체 지향 언어에서 관계형 데이터베이스를 객체형으로 사용하기 위함이다.
# ORM이 중간에서 객체형을 관계형으로 전환해주는 역할을 한다.

# engine은 데이터베이스 서버와의 연결을 제공해준다.

# In[1]:


from sqlalchemy import create_engine


# ### connecting
# - Lazy connecting이다.

# In[2]:


engine = create_engine("sqlite:///studyomr1.db")


# In[3]:


engine.echo = True


# In[4]:


print(engine)


# ### Create

# Table

# In[6]:


from sqlalchemy.schema import Table


# Column

# In[7]:


from sqlalchemy.schema import Column


# MetaData

# In[8]:


from sqlalchemy.schema import MetaData


# 예제

# In[10]:


from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey 


# MetaData 생성

# In[11]:


metadata = MetaData()


# Table 생성
# - Table('테이블명', 메타데이타, Columns)
# - metadata에 생성

# In[12]:


users = Table('users', metadata,
             Column('id', Integer, primary_key=True),
              Column('name', String),
              Column('fullname', String),
             )


# In[13]:


addresses = Table('addresses', metadata,
                 Column('id', Integer, primary_key = True),
                  Column('user_id', None, ForeignKey('users.id')),
                  Column('email_address', String, nullable=False)
                 )


# metadata에 생성한 것을 엔진을 통해 데이터베이스에 저장한다.

# In[14]:


metadata.create_all(engine)


# ### Insert

# insert
# - insert(values=None, inline=False, \*\*kwargs)

# compile
# - compile(bind=None, dialect=None, \*\*kw)
# - sql 표현식을 컴파일시킨다.
# - 리턴값은 컴파일된 객체이다.
# - params를 이용하여 컴파일된 객체의 파라미터 이름과 값을 받아올 수 있다.

# 예제

# users table의 insert객체

# In[24]:


insert = users.insert()


# In[25]:


type(insert)


# In[26]:


print(insert)


# In[27]:


insert = users.insert().values(name='kim', fullname='Anonymou, Kim ')
print(insert)


# In[28]:


insert.compile().params


# ### Executing

# Connection

# In[30]:


from sqlalchemy.engine import Connection


# execute
# - execute(object, \*multiparams, \*\*params)
# - SQL문을 생성하고 ResultProxy를 반환한다

# ResultProxy

# In[31]:


from sqlalchemy.engine import ResultProxy


# 예제

# In[32]:


conn = engine.connect()


# In[33]:


conn


# engine과 sql문을 바인딩하여야 데이터베이스로 전송할수 있다.

# In[35]:


insert.bind = engine


# In[36]:


str(insert)


# conn 연결 통로를 통하여 insert를 보내고 그 결과를 result에 담는다.

# In[39]:


result = conn.execute(insert)


# In[40]:


result.inserted_primary_key


# execute의 params를 사용하는 예

# In[41]:


insert = users.insert()


# In[42]:


result = conn.execute(insert, name="lee", fullname="Unknown, Lee")


# 결과의 primary_key값을 알려준다.

# In[43]:


result.inserted_primary_key


# executemany()처럼 사용하고싶다면 다음과 같이 사용하면 된다. multiparams에 list 속 dict형태로 전송하면 된다.

# addresses에 튜플 추가

# In[44]:


conn.execute(addresses.insert(),[
    {'user_id':1, 'email_address':'anonymous.kim@test.com'},
    {'user_id':2, 'email_address':'unknown.lee@test.com'}
])


# ### select

# select

# In[52]:


from sqlalchemy.sql import select


# 예제

# In[45]:


query = select([users])


# In[46]:


print(query)


# In[47]:


result = conn.execute(query)


# In[48]:


for row in result:
    print(row)


# In[49]:


result = conn.execute(select([users.c.name, users.c.fullname]))


# In[51]:


for row in result:
    print(row)


# ### ResultProxy

# - fetchone()
#     - Fetch one row(한 튜플을 받아온다.)
# - fetchall()
#     - Fetch all rows(모든 튜플을 받아온다.)

# 예제 - fetchone()

# In[53]:


result = conn.execute(query)


# In[54]:


row = result.fetchone()


# In[55]:


print(row)


# In[57]:


print("id - ", row['id'], ", name - ", row['name'], ", fullname -", row['fullname'])


# In[59]:


row = result.fetchone()


# In[60]:


print("id - ", row['id'], ", name - ", row['name'], ", fullname -", row['fullname'])


# fetchall()

# In[61]:


result = conn.execute(query)


# In[62]:


rows = result.fetchall()


# In[63]:


rows


# In[64]:


for row in rows:
    print("id - ", row['id'], ", name - ", row['name'], ", fullname -", row['fullname'])


# In[65]:


result.close()


# In[67]:


type(result)


# ### 활용 예제

# In[69]:


from sqlalchemy import and_, or_, not_


# 조건식으로 사용

# In[70]:


print(users.c.id == addresses.c.user_id)


# In[71]:


print(users.c.id == 1)


# In[72]:


print((users.c.id == 1).compile().params)


# In[73]:


print(or_(users.c.id == addresses.c.user_id, users.c.id==1))


# In[74]:


print(and_(users.c.id == addresses.c.user_id, users.c.id == 1))


# In[75]:


print(and_(
        or_(
            users.c.id == addresses.c.user_id,
            users.c.id == 1
        ),
    addresses.c.email_address.like("a%")
    )
)


# In[76]:


print((
    (users.c.id == addresses.c.user_id) |
    (users.c.id == 1)
) & (addresses.c.email_address.like("a%")))


# ### selecting

# 예제

# In[77]:


result = conn.execute(select([users]).where(users.c.id==1))


# In[78]:


for row in result:
    print(row)


# In[79]:


result = conn.execute(select([users, addresses]).where(users.c.id == addresses.c.user_id))


# In[80]:


for row in result:
    print(row)


# cross join

# In[81]:


result = conn.execute(select([users.c.id, users.c.fullname, addresses.c.email_address])
                     .where(users.c.id==addresses.c.user_id)
                     .where(addresses.c.email_address.like('un%')))


# In[82]:


for row in result:
    print(row)


# ### Join

# join(right, onclause=None, isouter=False, full=False)

# 예제

# In[83]:


from sqlalchemy import join


# join하면 자동으로 foreignkey를 확인해서 연결해준다

# In[84]:


print(users.join(addresses))


# In[85]:


print(users.join(addresses, users.c.id == addresses.c.user_id))


# In[87]:


query = select([users.c.id, users.c.fullname, addresses.c.email_address]).select_from(users.join(addresses))


# In[89]:


result = conn.execute(query).fetchall()


# In[90]:


for row in result:
    print(row)


# In[91]:


artist = Table("Artist", metadata,
              Column("id", Integer, primary_key=True),
              Column("name", String, nullable=False),
              extend_existing=True)


# In[92]:


album = Table("Album", metadata,
             Column("id", Integer, primary_key=True),
             Column("title", String, nullable =False),
             Column("artist_id", Integer, ForeignKey("Artist.id")),
             extend_existing=True)


# In[99]:


genre = Table("Genre", metadata,
             Column("id", Integer, primary_key = True),
             Column("name", String, nullable=False),
             extend_existing=True)


# In[93]:


track = Table("Track", metadata,
             Column("id", Integer, primary_key = True),
             Column("title", String, nullable=False),
             Column("length", Integer, nullable=False),
             Column("rating", Integer, nullable=False),
              Column("count", Integer, nullable=False),
              Column("album_id", Integer, ForeignKey("Album.id")),
              Column("genre_id", Integer, ForeignKey("Genre.id")),
              extend_existing=True)


# In[100]:


metadata.create_all(engine)


# In[101]:


tables = metadata.tables


# metadata에 있는 테이블들

# In[102]:


for table in tables:
    print(table)


# db에 있는 테이블들

# In[103]:


for table in engine.table_names():
    print(table)


# Insert

# In[104]:


conn.execute(artist.insert(), [
    {"name":"Led Zepplin"},
    {"name":"AC/DC"}
])


# In[105]:


conn.execute(album.insert(),[
    {"title":"IV", "artist_id":1},
    {"title":"Who Made Who", "artist_id":2}
])


# In[106]:


conn.execute(genre.insert(),[
    {"name":"Rock"},
    {"name":"Metal"}
])


# In[107]:


conn.execute(track.insert(),[
    {"title":"Black Dog", "rating":5, "length":297, "count":0, "album_id":1, "genre_id":1},
    {"title":"Stairway", "rating":5, "length":482, "count":0, "album_id":1, "genre_id":1},
    {"title":"About to rock", "rating":5, "length":313, "count":0, "album_id":2, "genre_id":1},
    {"title":"Who Made Who", "rating":5, "length":297, "count":0, "album_id":2, "genre_id":1},
])


# select

# In[108]:


artistResult = conn.execute(artist.select())
for row in artistResult:
    print(row)


# In[109]:


albumResult = conn.execute(album.select())
for row in albumResult:
    print(row)


# In[110]:


genreResult = conn.execute(genre.select())
for row in genreResult:
    print(row)


# In[112]:


trackResult = conn.execute(track.select())
for row in trackResult:
    print(row)


# Where

# In[113]:


trackResult = conn.execute(select([track])
                           .where(
                           and_(track.c.album_id==1, track.c.genre_id == 1)))


# In[114]:


for row in trackResult:
    print(row)


# Update

# In[115]:


from sqlalchemy import update


# In[116]:


conn.execute(track.update().values(genre_id = 2).where(track.c.id==2))


# In[117]:


conn.execute(track.update().values(genre_id = 1).where(track.c.id==3))


# Where

# In[118]:


trackResult = conn.execute(select([track])
                          .where(
                              and_(track.c.album_id == 1,
                                  or_(track.c.genre_id ==1,
                                     track.c.genre_id ==2))
                          ))


# In[119]:


for row in trackResult:
    print(row)


# Join

# In[120]:


print(track.join(album))


# In[124]:


result = conn.execute(track.select().select_from(track.join(album)))


# In[125]:


for row in result.fetchall():
    print(row)


# In[126]:


result = conn.execute(track
                     .select()
                     .select_from(track.join(album))
                     .where(album.c.id==1))


# In[127]:


for row in result.fetchall():
    print(row)


# Multiple Join

# In[128]:


print(track.join(album))


# In[129]:


print(track.join(album).join(genre))


# In[131]:


print(track.join(album).join(artist))


# In[132]:


print(track.join(album).join(genre).join(artist))


# In[133]:


result = conn.execute(select([track.c.title, album.c.title, genre.c.name, artist.c.name])
                     .select_from(track.join(album).join(genre).join(artist)))


# In[134]:


for row in result.fetchall():
    print(row)


# In[135]:


result = conn.execute(track
                     .select()
                     .select_from(track.join(album).join(genre).join(artist))
                     .where(
                         and_(genre.c.id==1,
                             artist.c.id==1,
                             )
                     ))


# In[136]:


for row in result.fetchall():
    print(row)


# 연결 종료와 메타데이터 클리어

# In[137]:


conn.close()
metadata.clear()


# ### Declare

# declarative_base

# In[138]:


from sqlalchemy.ext.declarative import declarative_base


# In[139]:


from sqlalchemy import create_engine


# In[140]:


engine = create_engine("sqlite:///sqlomr2.db", echo=True)


# 매핑하고 싶은 클래스에 상속시킨다.

# In[141]:


base = declarative_base()


# In[142]:


class User(base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname= Column(String)
    password = Column("passwd", String)
    
    def __repr__(self):
        return "<T'User(name='%s', fullname='%s', password='%s')>" % (self.name, self.fullname, self.password)


# In[143]:


User.__table__


# In[144]:


base.metadata.create_all(engine)


# In[145]:


kim = User(name = "kim", fullname = "anonymous, Kim", password="kimbap nara")


# In[146]:


print(kim)


# In[147]:


print(kim.id)


# ### Session

# Session
# - 세션은 데이터베이스와의 모든 대화를 설정하고 모든 개체를 나타냅니다.
# - ORM으로 매핑 된 객체에 대한 지속성 작업을 관리합니다.

# In[148]:


from sqlalchemy.orm.session import sessionmaker


# In[149]:


Session = sessionmaker(bind=engine)


# In[150]:


session = Session()


# Insert

# add

# Pending된다. commit까지 기다림

# In[151]:


session.add(kim)


# In[152]:


session.add_all([
    User(name="lee", fullname="unknown, Lee", password="hello"),
    User(name="park", fullname="nobody, Park", password = "pass Park")
])


# Update

# dirty
# - 삭제가 아닌 수정을 할 때 사용한다.

# In[158]:


kim.password = "all"

session.dirty


# In[159]:


session.is_modified(kim)


# In[160]:


session.commit()


# Select
# - query

# In[161]:


from sqlalchemy.orm import Query


# In[162]:


for row in session.query(User):
    print(type(row))
    print(row.id, row.name, row.fullname, row.password)


# In[164]:


str(session.query(User))


# filter
# - 필터링에 사용
# - 파이썬 연산자로 계산한다.
# 
# filter_by
# - keyword 표현식으로 사용

# In[165]:


for row in session.query(User.id, User.fullname).filter(User.name == "lee"):
    print(type(row))
    print(row.id, row.fullname)


# In[167]:


for row in session.query(User.id, User.fullname).filter_by(name = 'lee'):
    print(type(row))
    print(row.id, row.fullname)


# In[168]:


class Artist(base):
    __tablename__ = "Artist"
    
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)


# In[169]:


class Album(base):
    __tablename__ = "Album"
    
    id = Column(Integer, primary_key = True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey("Artist.id"))
    


# In[170]:


class Genre(base):
    __tablename__ = "Genre"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)


# In[171]:


class Track(base):
    __tablename__="Track"
    
    id = Column("id", Integer, primary_key = True)
    title = Column("title", String, nullable=False)
    length = Column("length", Integer, nullable=False)
    rating = Column("rating", Integer, nullable=False)
    count = Column("count", Integer, nullable=False)
    album_id = Column("album_id", Integer, ForeignKey("Album.id"))
    genre_id = Column("genre_id", Integer, ForeignKey("Genre.id"))


# In[179]:


base.metadata.create_all(engine)


# In[183]:


artist1 = Artist(name="Led Zepplin")
artist2 = Artist(name = "AC/DC")


# In[184]:


session.add_all([artist1, artist2])


# In[185]:


session.commit()


# In[186]:


album = [Album(title = "IV", artist_id = artist1.id),
        Album(title="Who Made Who", artist_id=artist2.id)]


# In[187]:


session.add_all(album)


# In[188]:


session.commit()


# In[189]:


session.add_all([
    Genre(name="Rock"), Genre(name="Metal")
])


# In[190]:


session.commit()


# In[191]:


album1 = session.query(Album).filter(Album.artist_id == artist1.id).one()


# In[192]:


album2 = session.query(Album).filter(Album.artist_id==artist2.id).one()


# In[193]:


genre1 = session.query(Genre).filter(Genre.name=="Rock").filter(Genre.id==1).one()


# In[196]:


genre2 = session.query(Genre).filter(Genre.id==2).one()


# In[197]:


track = [Track(title = "Black Dog", rating=5, length = 297, count = 0, album_id = album1.id, genre_id = genre1.id),
        Track(title = "Stairway", rating=5, length = 482, count = 0, album_id = album1.id, genre_id = genre2.id),
        Track(title = "About to rock", rating=5, length = 313, count = 0, album_id = album2.id, genre_id = genre1.id),
        Track(title = "Who Made Who", rating=5, length = 297, count = 0, album_id = album2.id, genre_id = genre2.id),
        ]


# In[198]:


session.add_all(track)


# In[199]:


session.commit()


# Join

# In[200]:


result = session.query(Track.title, Album.title, Genre.name, Artist.name).select_from(Track).join(Album).join(Genre).join(Artist).all()


# In[201]:


for row in result:
    print(row)


# In[204]:


songList = [dict(Track = row[0], Album=row[1], Genre=row[2], Artist=row[3]) for row in result]


# In[205]:


songList


# ### Relationship
# - 두 개의 매핑된 클래스 사이에 관계를 제공한다.
# - 부모-자식 또는 연관된 테이블 관계를 대응시켜준다.

# In[206]:


metadata = MetaData()


# In[209]:


engine = create_engine("sqlite:///sqlomr3.db", echo = True)


# In[210]:


Session = sessionmaker(engine)


# In[211]:


session = Session()


# In[214]:


class User(base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    fullname = Column(String)
    password=Column("passwd", String)


# In[218]:


class Address(base):
    __tablename__="addresses"
    
    id = Column(Integer, primary_key = True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


# In[220]:


base.metadata.create_all(engine)


# In[222]:


from sqlalchemy.orm import relationship


# In[223]:


class Artist(base):
    __tablename__ = "Artist"
    
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    
    albumList = relationship("Album", back_populates="artist")
    
class Album(base):
    __tablename__ = "Album"
    
    id = Column(Integer, primary_key = True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey("Artist.id"))
    
    artist = relationship("Artist", back_populates="albumList", uselist=False)
    trackList = relationship("Track", back_populates="album")
    
class Genre(base):
    __tablename__ = "Genre"
    
    id = Column(Integer, primary_key = True)
    name = Column(String)
    
    trackList = relationship("Track", back_populates="genre")
    
class Track(base):
    __tablename__="Track"
    
    id = Column("id", Integer, primary_key = True)
    title = Column("title", String, nullable=False)
    length = Column("length", Integer, nullable=False)
    rating = Column("rating", Integer, nullable=False)
    count = Column("count", Integer, nullable=False)
    album_id = Column("album_id", Integer, ForeignKey("Album.id"))
    genre_id = Column("genre_id", Integer, ForeignKey("Genre.id"))
    
    album = relationship("Album", back_populates = "trackList", uselist=False)
    genre = relationship("Genre", back_populates="trackList", uselist = False)


# In[224]:


base.metadata.create_all(engine)


# In[227]:


track1 = Track(title = "Black Dog", rating=5, length = 297, count = 0)
track2 = Track(title = "Stairway", rating=5, length = 482, count = 0)
track3 = Track(title = "About to rock", rating=5, length = 313, count = 0)
track4 = Track(title = "Who Made Who", rating=5, length = 297, count = 0)  


# In[228]:


track1.album = track2.album = Album(title = "IV")


# In[229]:


track3.album = track4.album = Album(title="Who Made Who")


# In[230]:


track1.genre = track3.genre = Genre(name="Rock")
track2.genre = track4.genre = Genre(name="Metal")


# In[231]:


track1.album.artist = track2.album.artist = Artist(name="Led Zepplin")
track3.album.artist = track4.album.artist = Artist(name ="AC/DC")


# In[232]:


session.add_all([track1, track2, track3, track4])


# In[233]:


session.commit()


# In[235]:


result = session.query(Artist)


# In[238]:


for row in result:
    print(row.name)


# In[ ]:




