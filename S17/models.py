from peewee import *
from playhouse.fields import ManyToManyField

db = SqliteDatabase('room_service.db')

class BaseModel(Model):
    class Meta:
        database = db

class RoomType(BaseModel):
    type_name = CharField(max_length=50, null=False, unique=True)
    is_active = BooleanField(null=False, default=True)

    class Meta:
        table_name = 'room_types'

    def to_dict(self):
        return {
            'id': self.id,
            'type_name': self.type_name,
            'is_active': self.is_active
        }

class Room(BaseModel):
    room_number = CharField(null=False)
    floor = IntegerField(constraints=[Check('floor >= 1')], null=False)
    building = CharField(max_length=50, null=False)
    capacity = IntegerField(constraints=[Check('capacity > 0')], null=False)
    is_active = BooleanField(null=False, default=True)
    room_types = ManyToManyField(RoomType, backref='rooms', through='RoomRoomType')

    class Meta:
        table_name = 'rooms'
        constraints = [SQL('UNIQUE(room_number, building)')]

    def to_dict(self):
        types_list = [rt.to_dict() for rt in self.room_types]
        return {
            'id': self.id,
            'room_number': self.room_number,
            'floor': self.floor,
            'building': self.building,
            'capacity': self.capacity,
            'is_active': self.is_active,
            'types': types_list
        }

class RoomRoomType(BaseModel):
    room_id = ForeignKeyField(Room, backref='room_types_link', field='id', on_delete='CASCADE')
    type_id = ForeignKeyField(RoomType, backref='rooms_link', field='id', on_delete='CASCADE')

    class Meta:
        table_name = 'room_room_type'
        primary_key = CompositeKey('room_id', 'type_id')
        indexes = (
            (('room_id', 'type_id'), True),
        )

def init_db():
    db.connect()
    db.create_tables([RoomType, Room, RoomRoomType])
    db.close()

if __name__ == "__main__":
    init_db()
