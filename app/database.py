from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
class Participant(db.Model):
    seqid: Mapped[int] = mapped_column(primary_key=True)
    subid: Mapped[str] = mapped_column(unique=True)
    workerid: Mapped[str] = mapped_column(unique=True)