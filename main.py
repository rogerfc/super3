#!/usr/bin/env python
# -*- coding: utf-8 -*-

from super3.model import Serie, Episodi, Base
from super3.scrapper import get_series
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def main():
    engine = create_engine('sqlite:///:memory:', encoding='utf-8', echo=False)

    session = sessionmaker()
    session.configure(bind=engine)
    Base.metadata.create_all(engine)

    s = session()
    for serie, url in get_series('Kratt'):
        sr = Serie(name=serie, url=url)
        s.add(sr)
    s.commit()

    for serie in s.query(Serie).all():
        print(serie)


if __name__ == '__main__':
    main()
