# # UltraSound Occupancy Detection

This is an implementation of occupancy detection using python based on ultrasound waves.

## Django
this is a basic implementation of an IoT app to show the room is occupied or not. in updates every second with the value it receives by `detetcion.py`

## Detection
`detection.py`
run this so that it only calculates the motion score and send it as a request to Django app.

## GUI
`gui.py`
run this program so that you have a real-time FFT plot of the microphone.


## Image Processing
`cameramotiondetector.py`
this is a simple motion detector with image processing it subtract two frames and then smoothen the delta frame. if changes happen as a motion in will draw a contour.
