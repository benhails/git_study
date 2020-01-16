import peeweedbevolve
from orm_practise import db

if __name__ == '__main__':
   db.evolve(ignore_tables={'base_model'})