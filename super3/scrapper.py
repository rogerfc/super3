# -*- coding: utf-8 -*-

import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse
import os.path

site = 'http://www.ccma.cat'
main_url = '/tv3/super3/series-i-programes'

def get_series(filtre=None):
    result = requests.get(urljoin(site, main_url))
    content = result.content
    soup = BeautifulSoup(content, 'lxml')

    for serie in [
            s.find('a').attrs
            for s in soup.find_all("div", "F-itemContenidorIntern")]:
        title = serie['title']
        if not filtre or filtre.lower() in title.lower():
            yield title, urljoin(site, serie['href'])


def get_serie_episodes(url, filtre=None):
    result = requests.get(urljoin(urljoin(site, url), 'videos'))
    content = result.content
    soup = BeautifulSoup(content, 'lxml')

    for video in [s for s in soup.find_all('article', 'T-video')]:
        title = video.find('a', 'media-object').find('h2').string.strip()
        if not filtre or filtre.lower() in title.lower():
            yield title, urljoin(site, video.a.attrs['href'])


def get_episode_metadata(url):
    video_id = os.path.basename(os.path.normpath(url))
    download_url = (
        'http://www.tv3.cat/pvideo/'
        'FLV_bbd_dadesItem_MP4.jsp?idint={}'.format(video_id))

    result = requests.get(urljoin(site, download_url))
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
