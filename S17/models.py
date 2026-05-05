from peewee import *

db = SqliteDatabase('room_service.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomType(BaseModel):
    type_name = CharField(unique=True)

class Room(BaseModel):
    room_number = CharField()
    floor = IntegerField()
    building = CharField()
    capacity = IntegerField()

class RoomRoomType(BaseModel):
    room = ForeignKeyField(Room, backref='types')
    room_type = ForeignKeyField(RoomType, backref='rooms')

def init_db():
    db.connect()
    db.create_tables([RoomType, Room, RoomRoomType], safe=True)

if __name__ == '__main__':
    init_db()
