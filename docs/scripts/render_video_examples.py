"""Render real-video documentation examples; never modify source videos.

Requires opencv-python-headless and Pillow. Run with --help for input paths.
Frames use zero-based indices. All sources must have the same frame rate;
matching timestamps alone do not establish experimental alignment.
"""
import argparse
import hashlib
import json
from pathlib import Path

import cv2
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("full", "background", "centered", "rotated"):
        parser.add_argument(f"--{key}", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font", type=Path, required=True)
    parser.add_argument("--frame", type=int, default=5700)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    names = ("full", "background", "centered", "rotated")
    titles = ("A  Full-frame video", "B  Background-subtracted full frame",
              "C  Centered crop (not rotated)", "D  Centered + rotated + background-subtracted")
    subtitles = ("Arena context retained", "Arena coordinates retained; background suppressed",
                 "Local intermediate: animal follows the crop", "Shared export: rotated_bg_sub_fc_video.mp4")
    caps = []
    sources = {}
    try:
        for name in names:
            path = getattr(args, name)
            cap = cv2.VideoCapture(str(path))
            caps.append(cap)
            if not cap.isOpened():
                raise RuntimeError(f"Cannot open {path}")
            with path.open("rb") as f:
                sha = hashlib.file_digest(f, "sha256").hexdigest()
            sources[name] = {
                "filename": path.name, "sha256": sha,
                "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                "fps": cap.get(cv2.CAP_PROP_FPS),
                "frames": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            }
        fps = sources["full"]["fps"]
        if fps <= 0 or any(abs(s["fps"] - fps) > 1e-6 for s in sources.values()):
            raise ValueError("Expected matching positive frame rates")
        indices = list(range(args.frame, args.frame + 60, 2))
        if args.frame < 0 or any(indices[-1] >= s["frames"] for s in sources.values()):
            raise ValueError("Requested frames outside source bounds")
        font = lambda size: ImageFont.truetype(str(args.font), size)

        def compose(index):
            canvas = Image.new("RGB", (1680, 1320), "#101820")
            draw = ImageDraw.Draw(canvas)
            draw.text((40, 24), "ONE TRIAL, FOUR VIDEO REPRESENTATIONS", font=font(32), fill="#eef5f7")
            draw.text((40, 72), f"khorne / Food_eaten / 0   |   frame {index}   |   {index / fps:.1f} s into exported clip", font=font(23), fill="#aebfc9")
            for i, (name, cap) in enumerate(zip(names, caps)):
                cap.set(cv2.CAP_PROP_POS_FRAMES, index)
                ok, frame = cap.read()
                if not ok:
                    raise RuntimeError(f"Failed decoding {name} frame {index}")
                image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                image.thumbnail((780, 488), Image.Resampling.LANCZOS)
                x, y = 30 + (i % 2) * 825, 125 + (i // 2) * 580
                draw.rounded_rectangle((x, y, x + 795, y + 563), radius=10, fill="#1b2832")
                draw.text((x + 15, y + 13), titles[i], font=font(23), fill="#72dfc5" if i == 3 else "#eef5f7")
                draw.rectangle((x + 8, y + 53, x + 787, y + 541), fill="black")
                canvas.paste(image, (x + 8 + (780 - image.width) // 2, y + 53 + (488 - image.height) // 2))
                draw.text((x + 15, y + 542), subtitles[i], font=font(16), fill="#b7c7d1")
            draw.text((40, 1292), "Real decoded frames; no contrast enhancement. Panels resized independently; pixel scales differ.", font=font(18), fill="#aebfc9")
            return canvas

        still = compose(args.frame)
        still.save(args.output / "representations.png")
        frames = []
        for index in indices:
            image = compose(index)
            image = image.resize((1008, 792), Image.Resampling.LANCZOS)
            frames.append(image)
        frames[0].save(args.output / "representations.gif", save_all=True,
                       append_images=frames[1:], duration=200, loop=0, optimize=True)
        provenance = {
            "trial": "khorne/Food_eaten/0", "sources": sources,
            "still_frame": args.frame, "animation_frame_indices": indices,
            "animation_frame_duration_ms": 200,
            "display": "Aspect-preserving resize; no intensity adjustment; no generated animal imagery",
            "note": "Full frame and centered crop from local archive; background and rotated exports from shared Dropbox. Centered crop is a local intermediate, not promised in the share.",
        }
        (args.output / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
        for path in sorted(args.output.iterdir()):
            print(path.name, path.stat().st_size, "bytes")
    finally:
        for cap in caps:
            cap.release()


if __name__ == "__main__":
    main()
