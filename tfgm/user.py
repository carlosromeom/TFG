from flask_login import UserMixin

from . import database

class User(UserMixin):
    def __init__(self, id_, name, email, rol_):
        self.id = id_
        self.name = name
        self.email = email
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
            id_=user[0], name=user[1], email=user[2], rol_=user[3]
        )
        return user

    @staticmethod
    def create(obj):
        db_object = database.get_db()
        db_object.execute(
            "INSERT INTO user (id, name, email, rol) "
            "VALUES (?, ?, ?, ?)",
            (obj.id_, obj.name, obj.email, "Estudiante"),  ) #inicialmente todos los usuarios tendran el rol de Estudiante
        db_object.commit()
