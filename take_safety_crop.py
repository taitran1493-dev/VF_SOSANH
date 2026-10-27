import subprocess
import os
from PIL import Image

artifact_dir = r"C:\Users\PC\.gemini\antigravity\brain\1e80d419-e01f-4ebc-8a77-b069525ba658"
output_full = os.path.join(artifact_dir, "preview_full_page.png")

if os.path.exists(output_full):
    im = Image.open(output_full)
    crop_safety = im.crop((0, 4800, 1440, min(6500, im.height)))
    crop_safety.save(os.path.join(artifact_dir, "crop_safety_economics_v4.png"))
    print("Saved crop_safety_economics_v4.png")
