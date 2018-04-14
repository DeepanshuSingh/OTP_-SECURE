import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine =  create_engine(os.getenv("db2"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    userdata = db.execute("SELECT source,destination,duration FROM flights").
    for flight in flights:
        print(f"{flight.source} to {flight.destination}, distance is {flight.duration} km")

if __name__ = "__main__":
    main()