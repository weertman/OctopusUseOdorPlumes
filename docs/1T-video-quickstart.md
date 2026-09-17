# Working with the 1T octopus-centered, rotated videos

This guide is for collaborators who want to work with **videos from the single-target (1T) experiment**, especially in an octopus-centered reference frame. Start with the **existing processed MP4s**; you do not need to train or run DeepLabCut, download all the full-frame recordings, or rerun the paper's notebooks just to use them.

## 1. Download the right files

Open the [shared trajectories folder on Dropbox](https://www.dropbox.com/scl/fo/m2efo9lybu48gpjqfbo8e/APp2MDWyOpfX3CW15w5maho?rlkey=msy8iuzk9qmtxxomfy89c93gw&st=m1l56jy7&dl=0).

Navigate through **animal → condition → trial folder** and download:

**`rotated_bg_sub_fc_video.mp4`**

This is the background-subtracted, octopus-centered, rotated video. Start with one trial, confirm it opens locally, and only then download more. Use Dropbox's **Download** action rather than saving the preview web page. A folder download may arrive as a ZIP; extract it before opening the videos. If a large folder download fails, download smaller condition/trial folders or individual files. The shared folder was browsable without signing in during the check below; if access changes, contact the repository owner.

The shared trajectories folder contains the animals `khorne`, `korra`, `kratos`, `larsson`, and `ninja`. Condition folders use these exact spellings:

- `Food_eaten`
- `Food_not_eaten`
- `No_food_Control` — preserve the capital `C`, particularly on Linux.

### A concrete first trial

Open [khorne / Food_eaten / 0](https://www.dropbox.com/scl/fo/m2efo9lybu48gpjqfbo8e/ABCXbBv7f4h2KQ0IHINahTM/khorne/Food_eaten/0?rlkey=msy8iuzk9qmtxxomfy89c93gw&dl=0) and download `rotated_bg_sub_fc_video.mp4` (approximately 13 MB).

On Linux/macOS, this equivalent command downloads that specific file. Run it in your chosen data directory; it does not download the whole dataset:

```bash
mkdir -p trajectories/khorne/Food_eaten/0
curl --fail --location --retry 3 \
  'https://www.dropbox.com/scl/fo/m2efo9lybu48gpjqfbo8e/AOtBDnIyfelG06CdyDGmyhE/khorne/Food_eaten/0/rotated_bg_sub_fc_video.mp4?rlkey=msy8iuzk9qmtxxomfy89c93gw&dl=1' \
  --output trajectories/khorne/Food_eaten/0/rotated_bg_sub_fc_video.mp4
```

The quotes around the URL matter: it contains `&`. This command overwrites that destination if it already exists, so do not use it on a modified working copy. On Windows, the browser download is the simplest option.

### Keep trial identities intact

Every trial's rotated video has the **same filename**. Do not put all downloads into one flat directory: they will collide or acquire ambiguous suffixes. Preserve the hierarchy, for example:

```text
my-octopus-data/
└── trajectories/
    ├── khorne/
    │   └── Food_eaten/
    │       └── 0/
    │           └── rotated_bg_sub_fc_video.mp4
    └── ...
```

Treat `(animal, condition, trial folder)` as the identifier, not the MP4 basename or trial number alone. Keep downloaded originals unchanged and put derived clips, annotations, and transcodes somewhere separate. Keep the full-frame filename and small metadata files if downloading whole trial folders.

### Which other files do I need?

| File | Purpose | Needed just to use rotated videos? |
| --- | --- | --- |
| `rotated_bg_sub_fc_video.mp4` | Centered, rotated, background-subtracted view | **Yes: start here** |
| `background_sub_ff_video.mp4` | Background-subtracted view in full-frame coordinates | No; useful for checking processing/alignment |
| `*_ff.mp4` | Full-frame trial video, retaining arena context | No; useful for interpreting movements and artifacts |
| `*.h5` | DeepLabCut tracking output | No; useful for reprocessing or checking eye positions |
| `1t_trajectories_data.pickle` | Processed analysis table at the trajectories-folder root | No; only for joining to the paper's analysis |
| `rotated_bg_fc_video_drawn_frames.mp4`, `area_calculation_diagostic_video.mp4`, `shell_trace.png` | Diagnostic/analysis products | No; not substitutes for the clean rotated MP4 |

The example trial contains these video/diagnostic products; contents may differ across trials. The [broader 1T share](https://www.dropbox.com/scl/fo/3vc6q20s6bihbi2tuc63s/APeF3aU7wNxdf148oroggIU?rlkey=uf66439yaeohm57virb9j4rf5&st=ldlo9gjk&dl=0) is also linked from this repository, but use the **trajectories share above** for this workflow. Cloning GitHub alone does **not** download the external trajectory videos. The short FAAM clips in `DATA/1T/fast_arm_aligned_motions/videos/` are selected behavioral excerpts, not the complete collection of rotated trial videos.

## 2. Understand the view before analyzing it

The generation code is in [`CODE/1T/1t-approaches.ipynb`](../CODE/1T/1t-approaches.ipynb), in the cells defining `given_xy_xy_get_bodyaxis_angle`, `given_a_xy_crop_img`, and `rotate_image`.

- **Center:** midpoint between the tracked left and right eyes, not the silhouette centroid.
- **Rotation:** based on the eye-derived body axis, not travel direction and not alignment to an individual arm. In image coordinates, the code computes `bodyaxis_angle = atan2(rey - ley, rex - lex) - pi/2`, then passes `degrees(bodyaxis_angle) - 90` to OpenCV's rotation function. Do not assume a different head-up convention when combining these videos with another dataset.
- **Processing:** the notebook cleans/smooths eye tracks before centering and rotation (including a 29-frame, degree-5 Savitzky–Golay filter). These are processed views, not untouched camera recordings.
- **Output:** the writer requests **600 × 600 pixels at 10 fps**, grayscale content encoded in an MP4. Read each file's actual metadata rather than assuming all downloads match.
- **Borders/background:** cropping and rotation introduce black padding. Background subtraction can leave residual structures and remove faint animal details. These are not segmentation masks or guaranteed clean silhouettes.
- **Timing:** use zero-based frame indices and the file's measured fps for time within the exported clip. Do not equate clip time zero with the start of the original experiment without checking its metadata.
- **Frame count:** the notebook stores several tracking arrays with `[:-1]` after computing frame differences, and the rotated writer iterates over those arrays. Consequently a rotated video can be one frame shorter than its source. Check counts and offsets before joining tracking or labels; do not silently truncate mismatched data.

The crop stabilizes position and orientation, so it removes the arena-relative translation/rotation you would need to infer swimming/crawling trajectories or orientation relative to flow. Keep the matching full-frame video/tracks for those questions. Inspect trials for tracking slips, abrupt rotation, clipping of arms, poor contrast, and background artifacts before annotating or measuring them. The notebook's `inBox` flag controls inclusion in its aggregate images, **not** whether a frame is written to the rotated MP4; exported videos are not automatically restricted to valid in-arena moments.

## 3. Open and verify one video

First open the downloaded MP4 in a local player such as VLC. Scrub through the start, middle, and end. A failed Dropbox browser preview does not by itself mean the downloaded file is broken.

If FFmpeg is installed, inspect the metadata and decode the whole file to check for errors:

```bash
ffprobe -v error -select_streams v:0 \
  -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames,duration \
  -of json trajectories/khorne/Food_eaten/0/rotated_bg_sub_fc_video.mp4

ffmpeg -v error \
  -i trajectories/khorne/Food_eaten/0/rotated_bg_sub_fc_video.mp4 \
  -f null -
```

For the example file checked on **2026-09-17**, FFprobe reported MPEG-4 video, 600 × 600 pixels, 10 fps, **5,999 frames**, and **599.9 seconds**. Full-file decoding completed without reported errors. These are example-file results, not an audit of every trial or a total dataset size.

## 4. Read frames in Python without loading a whole video into RAM

Python is optional for viewing. For analysis, create a dedicated environment; no GPU or DeepLabCut installation is needed for reading these existing MP4s:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install opencv-python-headless
```

On Windows, use `py -m venv .venv` and activate with `.venv\Scripts\Activate.ps1` in PowerShell (or `.venv\Scripts\activate.bat` in Command Prompt). The headless OpenCV package supports video reading and image writing but not `cv2.imshow`; view saved images with your usual image viewer. Record your installed versions with `python -m pip freeze > environment-used.txt`.

Save the following as `inspect_rotated.py` in `my-octopus-data/`, then run `python inspect_rotated.py`. It scans only the target rotated videos, reads frames sequentially, writes a trial manifest, and saves one representative frame per trial. It leaves the MP4s unchanged. Run it on your one-trial download first; scanning a full collection decodes every frame and takes longer.

```python
from pathlib import Path
import csv
import math
import cv2

root = Path("trajectories")
files = sorted(root.glob("*/*/*/rotated_bg_sub_fc_video.mp4"))
if not files:
    raise SystemExit("No rotated videos found: check root and ZIP extraction layout.")

out = Path("inspection")
out.mkdir(exist_ok=True)
with (out / "video_manifest.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "animal", "condition", "trial", "relative_path", "fps", "width",
        "height", "reported_frames", "decoded_frames", "decoded_seconds", "status"
    ])
    for path in files:
        animal, condition, trial, _ = path.relative_to(root).parts
        cap = cv2.VideoCapture(str(path))
        try:
            if not cap.isOpened():
                raise RuntimeError(f"Cannot open {path}")
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            reported = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if not math.isfinite(fps) or fps <= 0:
                raise RuntimeError(f"Invalid fps for {path}: {fps}")
            decoded = 0
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                # OpenCV decodes to BGR; convert if your analysis wants grayscale.
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if decoded == reported // 2:
                    preview = out / animal / condition / trial / "middle.png"
                    preview.parent.mkdir(parents=True, exist_ok=True)
                    if not cv2.imwrite(str(preview), gray):
                        raise RuntimeError(f"Cannot write {preview}")
                # Add per-frame analysis here. Time within this clip = decoded / fps.
                decoded += 1
            status = "OK" if decoded == reported and decoded > 0 else "CHECK_FRAME_COUNT"
            writer.writerow([
                animal, condition, trial, path.relative_to(root).as_posix(),
                fps, width, height, reported, decoded, decoded / fps, status
            ])
            print(path, decoded, "frames", status)
        finally:
            cap.release()
```

Inspect `inspection/video_manifest.csv` and the saved images. `OK` means the reported and decoded frame counts agree; it does **not** certify tracking quality or temporal alignment. An early decoder failure can look like end-of-file in OpenCV, so investigate any mismatch with FFmpeg and try downloading the file again. Re-running the script replaces the manifest and matching preview images.

## 5. Optional compatibility copies

If your annotation tool/browser cannot read the original MPEG-4 codec, make a separate H.264 copy with FFmpeg:

```bash
mkdir -p working/khorne/Food_eaten/0
ffmpeg -n -i trajectories/khorne/Food_eaten/0/rotated_bg_sub_fc_video.mp4 \
  -map 0:v:0 -an -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart \
  working/khorne/Food_eaten/0/rotated_h264.mp4
```

`-n` refuses to overwrite an existing output. This is a **lossy compatibility copy**, not a replacement for the downloaded original. No new frame rate, resizing, or trimming is requested; still verify fps/frame count afterward. Keep annotations keyed to the original trial and zero-based frame number, and record any subsequent trimming/resampling offsets. Avoid exporting the whole collection to PNG unless your tool requires it: it can greatly increase disk use.

## 6. If you need tracking data or want to regenerate the videos

For simply using the existing rotated MP4s, **stop here**: you have workable videos and trial identifiers.

For deeper analysis, keep the matching `.h5`, trial metadata, and full-frame files. The optional `1t_trajectories_data.pickle` is a pandas analysis table, not a video archive. Load pickle/HDF files only from trusted sources; pickle loading can execute code. Older serialized pandas objects may need a compatible environment, and stored `subdir` paths may refer to the author's computer and need explicit remapping to your local root.

The notebooks are research workflows, not a one-click installer. If you need to regenerate or change the crop/background/rotation:

1. Work on a **copy** of one complete trial first; do not overwrite the shared exports.
2. Inspect `CODE/1T/1t-approaches.ipynb`. Its `data_root` is `../../DATA/1T/trajectories`, relative to the notebook working directory. Either reproduce that layout or change the path explicitly. Set `animals` and `experiments` to your downloaded subset.
3. Review the tracking columns rather than picking an arbitrary `.h5`: the notebook selects eye coordinates by column position, with different positions for `Food_eaten` versus the other conditions. Verify those columns and the correspondence of tracking rows to video frames before processing.
4. The rotation cell reads `background_sub_ff_video.mp4` and writes `rotated_bg_sub_fc_video.mp4`. It is guarded by per-animal `mean_frames_<animal>.png` / `std_frames_<animal>.png` cache checks and `rerun`; existing cached images can skip generation even when a trial output is missing. Conversely, forcing a rerun can overwrite existing rotated outputs.
5. `Create_food_eaten_bg_sub_videos.ipynb` contains the food-eaten background-subtraction workflow; it is not a general recipe for every condition. Review its paths and assumptions before use.
6. The original generation cells accumulate videos/frames in memory and can require substantial RAM. Do not “Run All” over the full dataset as an initial setup step. Scope to one trial, validate results against the existing export, then plan batch processing.

Changing the rotation convention, smoothing, background subtraction, or frame selection creates a new derivative dataset. Record those changes and preserve the source-to-output frame mapping so collaborators can compare results.

## Validation scope

This guide was checked against the repository's generation code and the live Dropbox trajectories layout. The single example `khorne/Food_eaten/0/rotated_bg_sub_fc_video.mp4` was downloaded, fully decoded with FFmpeg and the Python example, and visually sampled. The whole collection and notebook regeneration were **not** rerun or audited.
