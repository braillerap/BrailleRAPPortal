from datetime import datetime
from flask_login import UserMixin,LoginManager
from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()

USER_ROLE = "user"
ADMIN_ROLE = "admin"

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=USER_ROLE)  # "user" ou "admin"
    is_active_account = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, raw_password: str) -> None:
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    @property
    def is_admin(self) -> bool:
        return self.role == ADMIN_ROLE

    # Flask-Login utilise cette propriété pour savoir si le compte est actif
    @property
    def is_active(self) -> bool:
        return self.is_active_account

    def __repr__(self) -> str:
        return f"<User {self.username}>"
