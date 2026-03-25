# Python Wget Clone
A step-by-step implementation of the Linux `wget` tool in Python, across 9 stages.

---

## Stage 1: Basic Download
**Function**: Simplest file download (no extra features)
![Stage1](screenshots/Stage1.png)

---

## Stage 2: Custom Output Filename `-o` / `--output`
**Function**: Allow users to specify the output filename via command line arguments
![Stage2](screenshots/Stage2.png)

---

## Stage 3: Progress Bar
**Function**: Show real-time progress of downloaded bytes
![Stage3](screenshots/Stage3.png)

---

## Stage 4: Download Speed + ETA (Estimated Time of Arrival)
**Function**: Display download speed (KB/s / MB/s) and estimated remaining time
![Stage4](screenshots/Stage4.png)

---

## Stage 5: Redirects + Error Code Handling (404/500/403)
**Function**: Automatically follow HTTP redirects and handle common error codes (404 Not Found, 500 Server Error, 403 Forbidden)
![Stage5](screenshots/Stage5.png)

---

## Stage 6: Retry Mechanism `--retry` + Timeout
**Function**: Add configurable retry attempts (`--retry N`) and request timeout
![Stage6](screenshots/Stage6.png)

---

## Stage 7: HTTP Auth + Custom Headers `--user` `--password` `--header`
**Function**: Support HTTP Basic Authentication and custom request headers
![Stage7](screenshots/Stage7.png)

---

## Stage 8: Package to EXE Binary File
**Function**: Compile the Python script into a standalone Windows executable (using PyInstaller / cx_Freeze / py2exe)
![Stage8.1](screenshots/Stage8.1.png)
![Stage8.2](screenshots/Stage8.2.png)

---

## Stage 9: Async Download + 128KB Buffer Optimization
**Function**: Implement asynchronous download (aiohttp) with 128KB buffer size for optimal performance, separating progress bar from file I/O
![Stage9](screenshots/Stage9.png)
