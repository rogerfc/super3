#!/usr/bin/env python
# -*- coding: utf-8 -*-

from super3.model import Serie, Episodi, Base
from super3.scrapper import get_series, get_serie_videos
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def main():
    engine = create_engine('sqlite:///:memory:', encoding='utf-8', echo=False)

    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()
    for serie, url in get_series('Kratt'):
        sr = Serie(nom=serie, url=url)
        for episodi, url in get_serie_videos(sr.url):
            ep = Episodi(serie=sr, nom=episodi, url=url)
        s.add(sr)
    s.commit()

    for serie in s.query(Serie).all():
        print(serie)
        for episode in serie.episodis:
            print(episode)

if __name__ == '__main__':
    main()
