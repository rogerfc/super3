# -*- coding: utf-8 -*-

import requests
from requests.compat import urljoin
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse
import os.path

site = 'http://www.ccma.cat'
main_url = '/tv3/super3/videos'

def get_series(filter=None):
    result = requests.get(urljoin(site, main_url))
    content = result.content
    soup = BeautifulSoup(content, 'lxml')

    for serie in [
            s.find('p', 'titol').find('a')
            for s in soup.find_all("div", "F-llistaItem")]:
        title = serie.string.strip()
        if not filter or filter.lower() in title.lower():
            yield title, urljoin(site, serie.attrs['href'])


def get_serie_episodes(url, filter=None):
    result = requests.get(urljoin(site, url))
    content = result.content
    soup = BeautifulSoup(content, 'lxml')

    for video in [s for s in soup.find_all('article', 'T-video')]:
        title = video.find('a', 'media-object').find('h2').string.strip()
        if not filter or filter.lower() in title.lower():
            yield title, urljoin(site, video.a.attrs['href'])


def get_episode_mp4(url):
    video_id = os.path.basename(os.path.normpath(url))
    download_url = (
        'http://www.tv3.cat/pvideo/'
        'FLV_bbd_dadesItem_MP4.jsp?idint={}'.format(video_id))

    result = requests.get(urljoin(site, download_url))
    content = result.content
    soup = BeautifulSoup(content, 'lxml')

    return soup.find('videos').find('file').string
