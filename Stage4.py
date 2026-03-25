import requests
import argparse
import os
from urllib.parse import urlparse
from tqdm import tqdm

def download(url, output=None):
    filename = output or os.path.basename(urlparse(url).path) or "file"
    with requests.get(url, stream=True) as r:
        total = int(r.headers.get("content-length", 0))

        with tqdm(total=total, unit='B', unit_scale=True, unit_divisor=1024) as bar:
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=16384):
                    f.write(chunk)
                    bar.update(len(chunk))
    print(f"\nDone: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File downloader with progress bar")
    parser.add_argument("url", help="URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    args = parser.parse_args()
    download(args.url, args.output)