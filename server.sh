for i in $(seq 1 100); do python solarGraph.py --update && python solarGraph.py --render && rrdtool dump ../B2_A2_S2_temp.rrd && sleep 300 ;done
