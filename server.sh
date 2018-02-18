while [ 1 ]
do
	python solarGraph.py --update
	python solarGraph.py --render
	#rrdtool dump ../B2_A2_S2_temp.rrd
	date
        sleep 300
done


