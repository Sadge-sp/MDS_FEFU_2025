
from db_init import engine
from modules_for_app.models.user import Base

Base.metadata.create_all(bind=engine)
