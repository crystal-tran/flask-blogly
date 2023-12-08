from models import User, db, Post
from app import app


db.drop_all()
db.create_all()


eric = User(first_name="Eric", last_name="Huie")
crystal = User(first_name="Crystal", last_name="Tran",
               image_url="https://static.vecteezy.com/system/resources/thumbnails/002/098/203/small/silver-tabby-cat-sitting-on-green-background-free-photo.jpg")


test_post = Post(title="Test", content="This is a test", user_id=1)

db.session.add(eric)
db.session.add(crystal)
db.session.add(test_post)

db.session.commit()
