python downloadRainData

f95 convert_rfe_bin2asc.f -o convert_rfe_bin2asc

BINFILES=$(find . -name all_products.bin\*)

for BINFILE in ${BINFILES}
do
	./convert_rfe_bin2asc ${BINFILE} ${BINFILE}.txt
	rm ${BINFILE}
done

python makeRainDBF $1
