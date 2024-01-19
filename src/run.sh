for ((i=$2; i<=$3; i++)); do
	caseName=$1
	aux="../benchmarks/${caseName}/${caseName}"
	plPath="../pls/${caseName}/${caseName}_iter_$i.pl"
	outputPath="../outputs"
	python3 drawDensityGraph.py -aux $aux -plPath $plPath -output $outputPath
done


