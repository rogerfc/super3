from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Serie(Base):
    __tablename__ = 'serie'

    id = Column(Integer, primary_key=True)
    nom = Column(Unicode, unique=True)
    url = Column(Unicode)
    episodis = relationship('Episodi', backref='serie')

    def __str__(self):
        return self.nom

    def __repr__(self):
        return u'<Serie(id={}, name={})>'.format(self.id, self.nom)


class Episodi(Base):
    __tablename__ = 'episodi'

    id = Column(Integer, primary_key=True)
    serie_id = Column(Integer, ForeignKey('serie.id'))
    nom = Column(Unicode, unique=True)
    url = Column(Unicode)
    mp4 = Column(Unicode)

    def __str__(self):
        return self.nom

    def __repr__(self):
        return u'<Episodi(id={}, nom={})>'.format(self.id, self.nom)
