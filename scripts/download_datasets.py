import os
import urllib.request
from tqdm import tqdm
from zipfile import ZipFile
from zipfile import BadZipFile
from clear import clear
from time import sleep

EYEBLINK8_URL = "https://www.blinkingmatters.com/files/upload/research/eyeblink8.zip"
EYEBLINK8_PATH = os.path.join("datasets", "eyeblink8")

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path):
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def load_eyeblink8_data(eyeblink8_url=EYEBLINK8_URL, eyeblink8_path=EYEBLINK8_PATH):
    if not os.path.isdir(eyeblink8_path):
        os.makedirs(eyeblink8_path)
    zip_path = os.path.join(eyeblink8_path, "eyeblink8.zip")
    if not os.path.isfile(zip_path):
        download_url(eyeblink8_url, zip_path)
    try:
        with ZipFile(zip_path) as eyeblink8_zip:
            print("Extracting all files", end='')
            count = 0
            while count < 3:
                sleep(1)
                print('.', end='')
                count += 1
            eyeblink8_zip.extractall(path=eyeblink8_path)
            print("\nDone!")
    except BadZipFile as bzf:
        print("Error: {}".format(bzf))
        sleep(1)
        os.remove(zip_path)
        print("Restarting the script", end='')
        count = 0
        while count < 3:
            sleep(1)  
            print('.', end='')
            count += 1
        sleep(1)
        clear()
        load_eyeblink8_data()

load_eyeblink8_data()
