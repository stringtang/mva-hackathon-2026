#!/bin/sh
BASE=/Users/leotang/test/mva-hackathon
PAT=$BASE/pipeline/centered_patterns.txt
OUT=$BASE/pipeline/scan_out
mkdir -p $OUT

# 1) 补下缺失的 L002_R2
cd $BASE/data
if [ ! -s WGS_EX2312012_HGWCNDSX7_S16_L002_R2_001.fastq.gz ]; then
  /opt/miniconda3/bin/hf download SageBio/mva-hackathon-2026-data \
    WGS_EX2312012_HGWCNDSX7_S16_L002_R2_001.fastq.gz \
    --repo-type dataset --local-dir . >> $BASE/pipeline/dl_retry.log 2>&1
  echo "DOWNLOAD_DONE rc=$?" >> $BASE/pipeline/dl_retry.log
fi

# 2) 扫描所有已落地的 FASTQ（幂等：已有 .counts 则跳过）
for fq in $BASE/data/*.fastq.gz; do
  b=$(basename "$fq" .fastq.gz)
  [ -s "$OUT/$b.counts" ] && continue
  (
    gzip -dc "$fq" 2>/dev/null | awk 'NR%4==2' \
      | grep -oF -f "$PAT" | sort | uniq -c > "$OUT/$b.counts.tmp" \
      && mv "$OUT/$b.counts.tmp" "$OUT/$b.counts"
  ) &
done
wait
echo "ALL_COMPLETE $(date)" > $BASE/pipeline/scan_out/_ALL_DONE
