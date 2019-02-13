# Time synchronization

Code for synchronizing detections by use of synchronization transmitters.
Check the notebook for the needed functions and a usage example.

**Preparation**
Get your receiver time first linearly corrected, by comparing receiver clock at read-out with computer clock. For VPS, this can be done within the Fathom or VUE software.

**The method**
Choose one receiver as the "base receiver", preferably a receiver in the middle of the array, that hears all of the other receivers. The base receiver is the time keeper, the clock of the other receivers will be synchronized with the base clock.
Go through the synchronization process for each other receiver. In this process, you compare the detection time of a receiver pair (base receiver versus receiver in process) detecting the same transmitter (synchronization tag of one of the pair). The goal is to model the spline: a function that reflects the deviation of the receiver clock from the base clock over time. The spline can be found by calculating detection time differences (between the receiver pair) for each position of the synchronization transmitter.
