# Pitch video build

Reproducible build of the 3-minute Track 2 pitch video. Final render: **2:59**, 1920×1080, 25 fps.

- `slides/s1–s7.html` + `style.css` — slide source
- `slides/s1–s7.png` — rendered slides
- `narration.txt` — voiceover script, one block per slide

Voice: macOS `say`, **Samantha** (en_US), 152 wpm — deliberately flat and unhurried. No music, no dramatisation, no patient-identifying content.

```sh
# render slides
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i in 1 2 3 4 5 6 7; do
  "$CHROME" --headless --disable-gpu --hide-scrollbars \
    --screenshot="slides/s$i.png" --window-size=1920,1080 \
    --default-background-color=0e1621 "file://$PWD/slides/s$i.html"
done

# narration (see build notes for the split script)
say -v Samantha -r 152 -o audio/nN.aiff "<block N>"
ffmpeg -i audio/nN.aiff audio/nN.wav

# mux and concatenate
for i in 1 2 3 4 5 6 7; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 audio/n$i.wav)
  ffmpeg -loop 1 -i slides/s$i.png -i audio/n$i.wav -c:v libx264 -tune stillimage \
    -pix_fmt yuv420p -r 25 -c:a aac -b:a 192k -shortest -t "$d" seg$i.mp4
done
printf "file 'seg%d.mp4'\n" 1 2 3 4 5 6 7 > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy mva_track2_pitch.mp4
```

Audio and the final `.mp4` are git-excluded; the deliverable is the hosted video URL.
