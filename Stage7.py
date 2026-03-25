import requests
import argparse
import os
from tqdm import tqdm


def parse_headers(headers_list):
    headers = {}
    for h in headers_list:
        key, val = h.split(":", 1)
        headers[key.strip()] = val.strip()
    return headers


def download(url, output=None, retry=3, timeout=10, user=None, pwd=None, headers=None):
    filename = output or os.path.basename(url) or "file"
    auth = (user, pwd) if user and pwd else None

    for i in range(retry):
        try:
            r = requests.get(
                url, stream=True, auth=auth, headers=headers or {},
                timeout=timeout, allow_redirects=True
            )
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))

            with tqdm(total=total, unit='B', unit_scale=True) as bar:
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(65536):  # 64KB chunk
                        f.write(chunk)
                        bar.update(len(chunk))
            print(f"\nDone: {filename}")
            return
        except Exception as e:
            print(f"Attempt {i + 1} failed: {e}")
    print("Download failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advanced downloader with auth, headers, retries")
    parser.add_argument("url", help="URL to download")
    parser.add_argument("-o", "--output", help="Output file name")
    parser.add_argument("--retry", type=int, default=3, help="Number of retries")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds")
    parser.add_argument("--user", help="Username for authentication")
    parser.add_argument("--password", help="Password for authentication")
    parser.add_argument("--header", action="append", help="Custom header e.g. --header 'Auth: 123'")
    args = parser.parse_args()

    headers = parse_headers(args.header or [])
    download(args.url, args.output, args.retry, args.timeout, args.user, args.password, headers)