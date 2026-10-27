import os
from PIL import Image

artifact_dir = r"C:\Users\PC\.gemini\antigravity\brain\1e80d419-e01f-4ebc-8a77-b069525ba658"
output_full = os.path.join(artifact_dir, "preview_full_page.png")

if os.path.exists(output_full):
    im = Image.open(output_full)
    crop_eco = im.crop((0, 5600, 1440, im.height))
    crop_eco.save(os.path.join(artifact_dir, "crop_economics_footer_v4.png"))
    print("Saved crop_economics_footer_v4.png")
