#!/bin/sh
# 带失速检测的断点续传：速度低于 20KB/s 持续 45s 即中断，循环重连从断点续
DEST=/Users/leotang/test/mva-hackathon/data/WGS_EX2312012_HGWCNDSX7_S16_L002_R2_001.fastq.gz
URL="https://huggingface.co/datasets/SageBio/mva-hackathon-2026-data/resolve/main/WGS_EX2312012_HGWCNDSX7_S16_L002_R2_001.fastq.gz"
TARGET=10911120034
LOG=/Users/leotang/test/mva-hackathon/pipeline/fetch_l002r2.log
: > "$LOG"
i=0
while [ "$i" -lt 400 ]; do
  i=$((i+1))
  sz=$(stat -f%z "$DEST" 2>/dev/null || echo 0)
  [ "$sz" -ge "$TARGET" ] && { echo "COMPLETE $sz" >> "$LOG"; break; }
  echo "[try $i] 起点 $sz ($((sz*100/TARGET))%)" >> "$LOG"
  curl -sL -C - --max-time 900 --connect-timeout 30 \
       --speed-limit 20000 --speed-time 45 \
       -H "Authorization: Bearer $(cat ~/.cache/huggingface/token)" \
       -o "$DEST" "$URL" >> "$LOG" 2>&1
done
final=$(stat -f%z "$DEST" 2>/dev/null || echo 0)
if [ "$final" -ge "$TARGET" ]; then echo "DONE_OK $final" >> "$LOG"; else echo "DONE_INCOMPLETE $final/$TARGET" >> "$LOG"; fi
