from werkzeug.security import generate_password_hash
from mongo_manager import MongoManager
md = MongoManager(uri='mongodb://mongo:mongoadmin@localhost:27017/')
md.create_user('admin@example.com', generate_password_hash('admin123'))