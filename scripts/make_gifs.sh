#!/usr/bin/env bash
# Builds the README GIFs in docs/gifs/ from the videos embedded in the thesis slides.
#
# Usage: make_gifs.sh <ffmpeg> <media_dir> <out_dir>
#   ffmpeg     path to the ffmpeg binary (e.g. ffmpeg)
#   media_dir  the slides' media folder: unzip "FINAL SLIDE.pptx" and use ppt/media/
#   out_dir    where to write the GIFs (e.g. docs/gifs)
#
# Example:
#   unzip -q "FINAL SLIDE.pptx" -d slides
#   scripts/make_gifs.sh ffmpeg slides/ppt/media docs/gifs
set -euo pipefail
FF="$1"; M="$2"; OUT="$3"
mkdir -p "$OUT"
PAL="split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle"

# gif <input> <output> <filters before palette>
gif() {
  "$FF" -hide_banner -loglevel error -y -i "$1" -filter_complex "[0:v]$3,$PAL" -loop 0 "$OUT/$2"
}

# Web joint selector: 31 s screen recording -> 1.5x speed
gif "$M/media2.mp4" web_selector.gif "setpts=PTS/1.5,fps=10,scale=800:-1:flags=lanczos"

# Hand-taught points (left) vs generated dataset (right), 1.5x speed, first 11 s
"$FF" -hide_banner -loglevel error -y -i "$M/media3.mp4" -i "$M/media4.mp4" -filter_complex \
  "[0:v]setpts=PTS/1.5,fps=10,scale=202:360:force_original_aspect_ratio=increase:flags=lanczos,crop=202:360,trim=duration=11,setpts=PTS-STARTPTS[l];\
   [1:v]setpts=PTS/1.5,fps=10,scale=202:360:force_original_aspect_ratio=increase:flags=lanczos,crop=202:360,trim=duration=11,setpts=PTS-STARTPTS[r];\
   [l]pad=iw+8:ih:0:0:white[lp];[lp][r]hstack,$PAL" \
  -loop 0 "$OUT/motion_comparison.gif"

# Close-up of the iron working along a row: 33 s -> 3x speed
gif "$M/media1.mp4" soldering_closeup.gif "setpts=PTS/3,fps=10,scale=480:-1:flags=lanczos"

# Top-down soldering process: 21.5 s -> 2x speed
gif "$M/media5.mp4" soldering_topdown.gif "setpts=PTS/2,fps=10,scale=480:-1:flags=lanczos"

ls -la "$OUT"
