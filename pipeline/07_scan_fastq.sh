#!/bin/sh
# 无比对 k-mer 定点扫描：并行处理所有 FASTQ，每文件独立产出计数
# 管线: gzip -dc | awk 取序列行 | grep -F 多模式精确匹配 | 计数
# 只匹配 FASTQ 第 2/4 行（序列行），避免质量行的 ASCII 巧合
set -u
BASE=/Users/leotang/test/mva-hackathon
PAT=$BASE/pipeline/centered_patterns.txt
OUT=$BASE/pipeline/scan_out
mkdir -p $OUT

for fq in $BASE/data/*.fastq.gz; do
  b=$(basename "$fq" .fastq.gz)
  [ -s "$OUT/$b.counts" ] && { echo "skip $b"; continue; }
  (
    gzip -dc "$fq" 2>/dev/null \
      | awk 'NR%4==2' \
      | grep -oF -f "$PAT" \
      | sort | uniq -c > "$OUT/$b.counts.tmp" \
      && mv "$OUT/$b.counts.tmp" "$OUT/$b.counts" \
      && echo "done $b"
  ) &
done
wait
echo "ALL_SCANS_COMPLETE"
ls -la $OUT/
