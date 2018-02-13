#!/usr/bin/env python
# -*- coding: utf-8 -*-

from super3.model import Serie, Episodi, Base
from super3.scrapper import get_series, get_serie_videos, get_video_download_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib


def main():
    engine = create_engine('sqlite:///:memory:', encoding='utf-8', echo=False)

    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()
    for serie, url in get_series('Kratt'):
        sr = Serie(nom=serie, url=url)
        for episodi, url in get_serie_videos(sr.url):
            mp4 = get_video_download_url(url)
            ep = Episodi(serie=sr, nom=episodi, url=url, mp4=mp4)
        s.add(sr)
    s.commit()

    for serie in s.query(Serie).all():
        print('Sèrie: {}'.format(serie))
        for episodi in serie.episodis:
            print('  - Ep: {}'.format(episodi))
            print('    {}'.format(episodi.url))
            print('    {}'.format(episodi.mp4))
            filename = '{}-{}.mp4'.format(
                serie.nom.lower().replace(' ', '-'),
                episodi.nom.lower().replace(' ', '-'))
            urllib.request.urlretrieve(episodi.mp4, filename)
            print('    Descarregat')

if __name__ == '__main__':
    main()
