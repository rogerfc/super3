#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .model import Serie, Episodi, Base
from .scrapper import get_series, get_serie_episodes, get_episode_metadata
from .download import down_file, download_videos
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
import argparse
import sys


def main(filtre=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='filtre', action="store", default=None)
    args = parser.parse_args()
    if args.filtre:

        engine = create_engine('sqlite:///:memory:', encoding='utf-8', echo=False)
        session = sessionmaker()
        session.configure(bind=engine)
        Base.metadata.create_all(engine)

        s = session()

        for serie in scan(args.filtre):
            s.add(serie)
        s.commit()

        for episodi in get_episodis_per_descarregar(s, args.filtre):
            episodi.download_img()
            episodi.download_mp4()

def scan(filtre=None):
    for serie, url in get_series(filtre):
        print('Escannejant ...')
        sr = Serie(nom=serie, url=url)
        print('Sèrie: {}'.format(sr))
        for episodi, url in get_serie_episodes(sr.url):
            ep = Episodi(
                serie=sr,
                nom=episodi,
                url=url)
            meta = ep.get_metadata()
            ep.num = meta.get('capítol', None).get('num', None)
            ep.img = meta.get('miniatura', None)
            ep.mp4 = meta.get('video', None)
            print('  - Ep {}: {}'.format(ep.num, ep.nom))
        yield sr


def get_episodis_per_descarregar(session, filtre=None):
    print('Descarregant ... ')
    return session.query(Episodi).all()

    # for serie in s.query(Serie).all():
    #     print('Sèrie: {}'.format(serie))
    #     for episodi in serie.episodis:
    #         print('  - Ep {}: {}'.format(episodi.num, episodi.nom))
    #         download_mp4(episodi.mp4, episodi.fitxer)

    # download_data = [
    #     (episode.mp4, episode.fitxer)
    #     for serie in s.query(Serie).all()
    #     for episode in serie.episodis
    # ]
    # # print(download_data)
    # download_videos(download_data)

def download_from_url(url=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', dest='url', action="store", default=None)
    args = parser.parse_args()

    if args.url:
        meta = get_episode_metadata(url=args.url)
        filename = '{}.mp4'.format(meta['serie'].lower().replace(' ', '-'))
        print('Descarregant video des de {}'.format(meta['video']))
        down_file(meta['video'], filename)

if __name__ == '__main__':
    main()
