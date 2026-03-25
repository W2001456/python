import requests
import argparse
import os
from tqdm import tqdm


def download(url, output=None):
    try:

        with requests.get(url, stream=True, allow_redirects=True, timeout=10) as r:

            if r.status_code >= 400:
                print(f" Error: Server returned {r.status_code}")
                return

            total = int(r.headers.get("content-length", 0))
            filename = output or os.path.basename(r.url) or "file"

            with tqdm(total=total, unit='B', unit_scale=True) as bar:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(16384):
                        f.write(chunk)
                        bar.update(len(chunk))
        print(f"\nDone: {filename}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.ConnectionError:
        print("Network connection failed")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except Exception as e:
        print(f"Unknown error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File downloader with progress bar")
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("-o", "--output", help="Custom output filename")
    args = parser.parse_args()
    download(args.url, args.output)