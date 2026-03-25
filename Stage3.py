import requests
import argparse
import os
from urllib.parse import urlparse
from tqdm import tqdm

def download_with_progress(url, output=None):
    parsed_url = urlparse(url)
    filename = output or os.path.basename(parsed_url.path) or "downloaded_file"

    with requests.get(url, stream=True) as r:
        total_size = int(r.headers.get("content-length", 0))

        with tqdm(total=total_size, unit="B", unit_scale=True, desc=filename) as pbar:
            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    pbar.update(len(chunk))
    print(f"\nDownload completed: {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("-o", "--output", help="Custom output file name")
    args = parser.parse_args()
    download_with_progress(args.url, args.output)