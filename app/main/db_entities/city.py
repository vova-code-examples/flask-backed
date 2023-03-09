from app.main import DB


class City(DB.Model):
    __tablename__ = "cities"

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name_en = DB.Column(DB.String(255), unique=True, nullable=False)
    name_ua = DB.Column(DB.String(255), unique=True, nullable=False)

    def __repr__(self):
        return str({c.name: getattr(self, c.name) for c in self.__table__.columns})
