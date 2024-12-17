from api import db
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from sqlalchemy import String
# from api.models.quote import QuoteModel


class AuthorModel(db.Model):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index= True, unique=True)
    surname: Mapped[str] = mapped_column(String(32), index=True, unique=True, default='surname is unknown', nullable=True)
    quotes: Mapped[WriteOnlyMapped] = relationship(back_populates='author')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            }