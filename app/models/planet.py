from app import db

# class Planet:
#     def __init__(self, id, description, name, distance_from_sun):
#         self.id = id
#         self.description = description
#         self.name = name
#         self.distance_from_sun = distance_from_sun

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    name = db.Column(db.String)
    distance_from_sun = db.Column(db.Integer)

