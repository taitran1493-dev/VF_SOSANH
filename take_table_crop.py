import subprocess
import time
import os
from PIL import Image

artifact_dir = r"C:\Users\PC\.gemini\antigravity\brain\1e80d419-e01f-4ebc-8a77-b069525ba658"
chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

output_full = os.path.join(artifact_dir, "preview_full_page.png")

cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    f"--screenshot={output_full}",
    "--window-size=1440,6500",
    "--virtual-time-budget=4000",
    "http://localhost:8088/index.html?theme=dark"
]
subprocess.run(cmd, capture_output=True, text=True)

if os.path.exists(output_full):
    im = Image.open(output_full)
    print("Full page captured:", im.size)
    # Crop Safety & ADAS section and Equipment section
    # Let's crop from y=2500 to y=4500
    crop_specs = im.crop((0, 2400, 1440, min(5000, im.height)))
    crop_specs.save(os.path.join(artifact_dir, "crop_specs_table_v4.png"))
    print("Saved crop_specs_table_v4.png")
