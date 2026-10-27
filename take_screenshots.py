import subprocess
import time
import os

artifact_dir = r"C:\Users\PC\.gemini\antigravity\brain\1e80d419-e01f-4ebc-8a77-b069525ba658"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

tasks = [
    {
        "url": "http://localhost:8088/index.html?theme=dark",
        "output": os.path.join(artifact_dir, "preview_dark_v4.png"),
        "size": "1440,2400"
    },
    {
        "url": "http://localhost:8088/index.html?theme=light",
        "output": os.path.join(artifact_dir, "preview_light_v4.png"),
        "size": "1440,2400"
    },
    {
        "url": "http://localhost:8088/index.html?theme=dark",
        "output": os.path.join(artifact_dir, "preview_mobile_v4.png"),
        "size": "390,1600"
    }
]

for t in tasks:
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        f"--screenshot={t['output']}",
        f"--window-size={t['size']}",
        "--virtual-time-budget=3000",
        t['url']
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Captured {os.path.basename(t['output'])}: code={res.returncode}, exists={os.path.exists(t['output'])}, size={os.path.getsize(t['output']) if os.path.exists(t['output']) else 0}")
