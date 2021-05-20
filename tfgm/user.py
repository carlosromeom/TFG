from flask_login import UserMixin

from . import database

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic, rol_):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.rol =  rol_ #inicialmente todos los usuarios tendran el rol de Estudiante

    @staticmethod
    def get(user_id):
        db_object = database.get_db()
        user = db_object.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], rol_=user[4]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, rol):
        db_object = database.get_db()
        db_object.execute(
            "INSERT INTO user (id, name, email, profile_pic, rol) "
            "VALUES (?, ?, ?, ?, ?)",
            (id_, name, email, profile_pic, "Estudiante"),  ) #inicialmente todos los usuarios tendran el rol de Estudiante
        db_object.commit()