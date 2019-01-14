from bs4 import BeautifulSoup
import os.path
import requests
from requests.compat import urljoin
from sqlalchemy import Column, Integer, Unicode, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from urllib.request import urlretrieve

from super3.download import down_file

site = 'http://www.ccma.cat'

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
    num = Column(Integer, unique=True)
    url = Column(Unicode)
    img = Column(Unicode)
    mp4 = Column(Unicode)

    def __str__(self):
        return self.nom

    def __repr__(self):
        return u'<Episodi(num={}, nom={})>'.format(self.num, self.nom)

    @property
    def video_id(self):
        return os.path.basename(os.path.normpath(self.url))

    @property
    def fitxer_mp4(self):
        # TODO: Use file extension from metadata
        return '{}-{}-{}.mp4'.format(
            self.serie.nom.lower().replace(' ', '-'),
            self.num,
            self.nom.lower().replace(' ', '-'))

    @property
    def fitxer_img(self):
        # TODO: Use file extension from metadata
        return '{}-{}-{}.jpg'.format(
            self.serie.nom.lower().replace(' ', '-'),
            self.num,
            self.nom.lower().replace(' ', '-'))

    @property
    def download_url(self):
        return (
            'http://www.tv3.cat/pvideo/'
            'FLV_bbd_dadesItem_MP4.jsp?idint={}'.format(self.video_id))

    def get_metadata(self):
        result = requests.get(urljoin(site, self.download_url))
        content = result.content
        soup = BeautifulSoup(content, 'xml')

        return {
            'serie': soup.item.promo.string,
            'capítol': {
                'num': soup.item.capitol.string,
                'titol': soup.item.title.string},
            'miniatura': soup.item.imgsrc.string,
            'video': soup.item.videos.find('file').string
        }

    def download_mp4(self):
        down_file(self.mp4, self.fitxer_mp4)

    def download_img(self):
        down_file(self.img, self.fitxer_img)
