echo "start"
kvalue=`cat kvalue`

while true
do
	echo "start train $kvalue"
	THEANO_FLAGS=floatX=float32,device=cuda,optimizer=fast_run python2 train.py dest_mlp_tgtcls_1_cswdtx_alexandre
	echo "train done, start push to kaggle"
	kaggle competitions submit -c pkdd-15-predict-taxi-service-trajectory-i -f it002000000.csv -m "$kvalue"
	sleep 30
	echo "echo get result from kaggle"
	python getResultKaggle.py
	
	mkdir "kvalue$kvalue"
	mv output/* "kvalue$kvalue"
	mv model_data/* "kvalue$kvalue"

	echo "slect next hyper parameter"
	python selectHyperpara.py
	koptimal=`cat koptimal`
	if [[ ! -z "$koptimal" ]]; then
	   echo "found k optimal:$koptimal"
	   break
	fi	
done


