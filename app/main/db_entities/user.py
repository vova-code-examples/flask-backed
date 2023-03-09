from app.main import DB, FLASK_BCRYPT


class User(DB.Model):
    __tablename__ = "users"

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    username = DB.Column(DB.String(50), unique=True)
    password_hash = DB.Column(DB.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = FLASK_BCRYPT.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return FLASK_BCRYPT.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<user '{}'>".format(self.username)

    def __str__(self):
        return f"id: {self.id}, nickname: {self.username}>"
