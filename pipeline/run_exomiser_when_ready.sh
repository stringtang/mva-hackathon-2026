#!/bin/sh
# 等 phenotype 数据包下载完成 → 解包 → 运行 Exomiser 全基因组无偏分析
set -e
BASE=/Users/leotang/test/mva-hackathon
EXODIR=$BASE/refs/exomiser
JAVA=/opt/homebrew/opt/openjdk@21/bin/java

rm -f $EXODIR/2512_hg38.zip   # 已解包，释放 22G

i=0
while [ ! -f $EXODIR/download.status ]; do
  i=$((i+1))
  if [ $i -gt 240 ]; then echo "TIMEOUT waiting for phenotype download"; exit 1; fi
  sleep 60
done
echo "phenotype 包下载完成，校验并解包..."
unzip -t $EXODIR/2512_phenotype.zip > /dev/null || { echo "ZIP CORRUPT"; exit 1; }
unzip -q -o $EXODIR/2512_phenotype.zip -d $EXODIR/data
rm -f $EXODIR/2512_phenotype.zip
ls $EXODIR/data

echo "启动 Exomiser（human-only exome 分析，无偏全基因组输入）..."
cd $EXODIR/exomiser-cli-15.1.0
mkdir -p $BASE/pipeline/exomiser/results
$JAVA -Xmx16G -jar exomiser-cli-15.1.0.jar analyse \
  --sample $BASE/pipeline/exomiser/proband-phenopacket.yml \
  --analysis $BASE/pipeline/exomiser/analysis-exome-humanonly.yml \
  --output-directory $BASE/pipeline/exomiser/results \
  --output-filename run1-exome-humanonly
echo "EXOMISER RUN COMPLETE"
ls -la $BASE/pipeline/exomiser/results/
