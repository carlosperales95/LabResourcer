#!/bin/bash

ES_SPARKDOMAIN="spark://fs0"
ES_SPARKPORT="7077"
ES_SPARKPATH=$(realpath ~/scratch/spark)

spark_dp = $ES_SPARKDOMAIN:$ES_SPARKPORT
print "path: %s" %(spark_dp)
bash $ES_SPARKPATH/sbin/start-master.sh
bash $ES_SPARKPATH/sbin/start-slave.sh  "$spark_dp"
bash $ES_SPARKPATH/bin/spark-submit --master "$spark_dp" examples/src/main/python/pi.py
bash $ES_SPARKPATH/sbin/stop-slave.sh "$spark_dp"


#cat > spark-env
