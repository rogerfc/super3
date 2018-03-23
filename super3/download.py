import progressbar
import urllib.request
from multiprocessing.dummy import Pool # use threads for I/O bound tasks
from urllib.request import urlretrieve

pbar = None

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def down_file(url, filename):
    urllib.request.urlretrieve(url, filename, show_progress)


def download_videos(urldata):

    def fetch_url(urldata):
        url, filename = urldata
        urllib.request.urlretrieve(url, filename, show_progress)

    result = Pool(4).map(fetch_url, urldata)
