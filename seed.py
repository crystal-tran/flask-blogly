from models import User, db
from app import app


db.drop_all()
db.create_all()


eric = User(first_name="Eric", last_name="Huie")
crystal = User(first_name="Crystal", last_name="Tran",
               image_url="https://static.vecteezy.com/system/resources/thumbnails/002/098/203/small/silver-tabby-cat-sitting-on-green-background-free-photo.jpg")

db.session.add(eric)
db.session.add(crystal)

db.session.commit()
