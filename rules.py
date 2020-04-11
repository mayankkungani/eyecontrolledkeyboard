import cv2

import numpy as np

def rules():

	option_window=np.zeros((1200,1000,3),np.uint8)


	option_window[:]=(179,0,100)

	font=cv2.FONT_HERSHEY_PLAIN


	cv2.putText(option_window,"Rules",(50,50),font,3,(0,0,0),3) 
	cv2.putText(option_window,"Blink your eye for 2-3 sec ultil sound pops ",(50,100),font,2,(0,0,0),3) 
	cv2.putText(option_window,"on any page to go back plz press ESC button",(50,150),font,2,(0,0,0),3)
	cv2.imshow("home",option_window)
	key = cv2.waitKey(5000)


#rules()