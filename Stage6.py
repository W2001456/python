import requests
import argparse
import os
from tqdm import tqdm


def download(url, output=None, retry=3, timeout=10):
    filename = output or os.path.basename(url) or "file"
    attempt = 0

    while attempt < retry:
        try:
            attempt += 1
            print(f"Attempt {attempt} downloading...")
            with requests.get(url, stream=True, allow_redirects=True, timeout=timeout) as r:
                if r.status_code >= 400:
                    print(f"Server error {r.status_code}")
                    continue

                total = int(r.headers.get("content-length", 0))
                with tqdm(total=total, unit='B', unit_scale=True) as bar:
                    with open(filename, 'wb') as f:
                        for chunk in r.iter_content(32768):  # 32KB chunk
                            f.write(chunk)
                            bar.update(len(chunk))
            print(f"\nDone: {filename}")
            return

        except Exception as e:
            print(f"Attempt {attempt} failed: {str(e)[:50]}")

    print(f"\nDownload failed after {retry} retries")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Downloader with retry and progress bar")
    parser.add_argument("url", help="URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("--retry", type=int, default=3, help="Number of retries")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds")
    args = parser.parse_args()
    download(args.url, args.output, args.retry, args.timeout)