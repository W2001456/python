import aiohttp
import asyncio
import argparse
import os
from tqdm import tqdm


def parse_headers(headers_list):

    headers = {}
    if headers_list:
        for h in headers_list:
            k, v = h.split(":", 1)
            headers[k.strip()] = v.strip()
    return headers


async def download_async(url, output=None, retry=3, timeout=10, user=None, pwd=None, headers=None):
    # Determine output filename
    filename = output or os.path.basename(url) or "file"

    # HTTP Basic Auth support
    auth = aiohttp.BasicAuth(user, pwd) if user and pwd else None

    for attempt in range(retry):
        try:
            timeout_cfg = aiohttp.ClientTimeout(total=timeout)


            # Async download core (aiohttp)
            # Non-blocking HTTP request
            async with aiohttp.ClientSession(timeout=timeout_cfg) as session:
                async with session.get(url, headers=headers or {}, auth=auth) as r:
                    if r.status >= 400:
                        print(f"❌ Status error: {r.status}")
                        await asyncio.sleep(1)
                        continue

                    # Get total file size for progress bar
                    total = int(r.headers.get("Content-Length", 0))


                    # Progress bar and file I/O separated from async network
                    # Progress bar runs in sync, but network is async → no blocking

                    with tqdm(total=total, unit="B", unit_scale=True, desc="Downloading") as bar:
                        with open(filename, "wb") as f:


                            # Buffer optimization: 131072 bytes = 128KB
                            # Best balance for speed, low memory, no lag

                            while True:
                                # Async read from network (non-blocking)
                                chunk = await r.content.read(131072)
                                if not chunk:
                                    break


                                f.write(chunk)
                                bar.update(len(chunk))


            print(f"\nAsync download completed: {filename}")
            return

        except Exception as e:
            print(f" Attempt {attempt + 1} failed: {str(e)[:70]}")
            await asyncio.sleep(1)

    print("\n All retries failed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async high-performance downloader (aiohttp)")
    parser.add_argument("url", help="Target URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("--retry", type=int, default=3, help="Retry count")
    parser.add_argument("--timeout", type=int, default=15, help="Total timeout in seconds")
    parser.add_argument("--user", help="Basic auth username")
    parser.add_argument("--password", help="Basic auth password")
    parser.add_argument("--header", action="append", help="Custom header e.g. --header 'Key: Value'")
    args = parser.parse_args()

    headers = parse_headers(args.header)

    # Run async download main function
    asyncio.run(download_async(
        args.url, args.output, args.retry, args.timeout,
        args.user, args.password, headers
    ))