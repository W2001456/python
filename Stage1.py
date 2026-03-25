import requests
import os
from urllib.parse import urlparse


def download_file(url):

    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Download completed: {filename}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python Stage1.py <download_url>")
        sys.exit(1)
    download_file(sys.argv[1])