import requests
import os
import argparse
from urllib.parse import urlparse


def main():
    parser = argparse.ArgumentParser(description="Wget Download Tool")
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("-o", "--output", help="Custom output filename")

    args = parser.parse_args()

    if args.output:
        filename = args.output
    else:
        parsed_url = urlparse(args.url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_file"

    with requests.get(args.url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    print(f"Download completed: {filename}")


if __name__ == "__main__":
    main()