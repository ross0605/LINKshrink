import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///database.db', echo=True)

# create a session
Session = sessionmaker(bind=engine)
session = Session()

user = User("Ross Ross", "admin","password")
session.add(user)

user = User("Langan Langan", "python","python")
session.add(user)

user = User("Name Name", "username","password")
session.add(user)


url = URLTab("https://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/basic_use.html", "https://set09103.napier.ac.uk:9147/999")
session.add(url)







session.commit()

session.commit()
