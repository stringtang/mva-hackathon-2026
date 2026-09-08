# Pitch video build

Reproducible build of the 3-minute Track 2 pitch video. Final render: **2:53**, 1920×1080, 25 fps.

- `slides/s1–s7.html` + `style.css` — slide source
- `slides/s1–s7.png` — rendered slides
- `narration.txt` — voiceover script, one block per slide

Voice: **OpenAI `gpt-4o-mini-tts`, voice `nova`**, with the instruction *"Calm, measured, unhurried narration for a scientific presentation to an expert panel. Neutral and clear; no dramatization; even pacing; brief natural pauses at sentence ends."* No music, no dramatisation, no patient-identifying content. (An earlier build used macOS `say`/Samantha; the OpenAI voice replaced it for naturalness.)

```sh
# render slides
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
for i in 1 2 3 4 5 6 7; do
  "$CHROME" --headless --disable-gpu --hide-scrollbars \
    --screenshot="slides/s$i.png" --window-size=1920,1080 \
    --default-background-color=0e1621 "file://$PWD/slides/s$i.html"
done

# narration — one POST per block of narration.txt (needs OPENAI_API_KEY)
# POST https://api.openai.com/v1/audio/speech
#   {"model":"gpt-4o-mini-tts","voice":"nova","input":"<block N>",
#    "response_format":"wav","instructions":"<see above>"}  -> audio_openai/nN.wav

# mux and concatenate
for i in 1 2 3 4 5 6 7; do
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 audio_openai/n$i.wav)
  ffmpeg -loop 1 -i slides/s$i.png -i audio_openai/n$i.wav -c:v libx264 -tune stillimage \
    -pix_fmt yuv420p -r 25 -c:a aac -b:a 192k -shortest -t "$d" seg$i.mp4
done
printf "file 'seg%d.mp4'\n" 1 2 3 4 5 6 7 > concat.txt
ffmpeg -f concat -safe 0 -i concat.txt -c copy mva_track2_pitch.mp4
```

Audio and the final `.mp4` are git-excluded; the deliverable is the hosted video URL.
