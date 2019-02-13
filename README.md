# Time synchronisation

Code for synchronising detections by use of synchronisation transmitters.   
For questions, feel free to open an issue or contact the author!

## Preparation 

If possible, get your receiver time first linearly corrected, by comparing receiver clock at read-out with computer clock. For VPS, this can be done within the Fathom or VUE software.

## The method 

Choose one receiver as the "base receiver", preferably a receiver in the middle of the array, that hears all of the other receivers. The base receiver is the time keeper, the clock of the other receivers will be synchronised with the base clock. Go through the synchronisation process for each receiver. In this process, you compare the detection time of 2 receivers in a receiver pair (base receiver versus receiver in process) detecting the same transmitter (synchronisation transmitter of one of the pair). The goal is to model the spline: a function that reflects the deviation of the receiver clock from the base clock over time. 

1. First run the function Time_sync_create_DTDs.py. 
This creates two DataFrames: 
- one contains the detection time difference (DTD) of the base-receiver synchronisation transmitter, on the base receiver versus the receiver in process.
- the other contains the DTD of the processed receiver synchronisation transmitter, on the base receiver versus the receiver in process.

2. Then run the function Model_spline_and_time_sync.py. 
Check the figures and play with the parameters of the functions to get a smooth spline that fits (but NOT overfits!) the DTDs as good as possible.

## Extra

If you have receivers without synchronisation transmitter, it is still possible to synchronise them: 
- Model the spline of the DTD of the base-receiver synchronisation transmitter between both receivers
- Convert the distance between both receivers in time-distance by use of soundspeed
- For the resulting spline, substract the time-distance from the base transmitter spline.
