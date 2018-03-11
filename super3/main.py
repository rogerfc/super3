#!/usr/bin/env python
# -*- coding: utf-8 -*-

from super3.model import Serie, Episodi, Base
from super3.scrapper import get_series, get_serie_episodes, get_episode_mp4
from super3.download import download_mp4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import argparse


def main(filtre='Kratt'):
    engine = create_engine('sqlite:///:memory:', encoding='utf-8', echo=False)

    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()
    for serie, url in get_series(filtre):
        sr = Serie(nom=serie, url=url)
        for episodi, url in get_serie_episodes(sr.url):
            mp4 = get_episode_mp4(url)
            ep = Episodi(serie=sr, nom=episodi, url=url, mp4=mp4)
        s.add(sr)
    s.commit()

    for serie in s.query(Serie).all():
        print('Sèrie: {}'.format(serie))
        for episodi in serie.episodis:
            print('  - Ep: {}'.format(episodi))
            filename = '{}-{}.mp4'.format(
                serie.nom.lower().replace(' ', '-'),
                episodi.nom.lower().replace(' ', '-'))
            download_mp4(episodi.mp4, filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='filtre', action="store", default=None)
    args = parser.parse_args()
    main(args.filtre)
