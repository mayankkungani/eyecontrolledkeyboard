
import dlib
import cv2
import numpy as np
from math import hypot
from playsound import playsound
import time
import config
#from home_eye import home





def omg():
	cap= cv2.VideoCapture(0)
	board=np.zeros((600,1000,3),np.uint8)


	board[:]=(255)
	detector =dlib.get_frontal_face_detector()
	predictor=dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

	def midpoint(p1,p2):
		return ((p1.x+p2.x)//2,(p2.y+p2.y)//2)

	font=cv2.FONT_HERSHEY_PLAIN


	def get_eye_gaze_ratio(eye_points, facial_landmarks):
				#gaze detection
		left_eye_region=np.array([(facial_landmarks.part(eye_points[0]).x,facial_landmarks.part(eye_points[0]).y),
								  (facial_landmarks.part(eye_points[1]).x,facial_landmarks.part(eye_points[1]).y),	
								  (facial_landmarks.part(eye_points[2]).x,facial_landmarks.part(eye_points[2]).y),
								  (facial_landmarks.part(eye_points[3]).x,facial_landmarks.part(eye_points[3]).y),
								  (facial_landmarks.part(eye_points[4]).x,facial_landmarks.part(eye_points[4]).y),
								  (facial_landmarks.part(eye_points[5]).x,facial_landmarks.part(eye_points[5]).y)],np.int32)
		height,width,_=frame.shape
		mask=np.zeros((480,640),np.uint8)


		cv2.polylines(frame,[left_eye_region],True,255,2)
		cv2.fillPoly(mask,[left_eye_region],255)
		eye=cv2.bitwise_and(gray,gray,mask=mask)

		min_x=np.min(left_eye_region[:,0])
		max_x=np.max(left_eye_region[:,0])
		min_y=np.min(left_eye_region[:,1])
		max_y=np.max(left_eye_region[:,1])

		gray_eye= eye[min_y:max_y,min_x:max_x]

		_,threshold_eye=cv2.threshold(gray_eye,70,255,cv2.THRESH_BINARY)
		height,width=threshold_eye.shape
		left_side_threshold=threshold_eye[0:height,0:width//2]
		left_side_white=cv2.countNonZero(left_side_threshold)

		right_side_threshold=threshold_eye[0:height,width//2:width]
		right_side_white=cv2.countNonZero(right_side_threshold)    #zeros are black
		gaze_ratio=0
		try:	
			gaze_ratio=left_side_white/right_side_white
		except ZeroDivisionError:
			pass

		return gaze_ratio
			


	keyboard=np.zeros((600,1000,3),np.uint8)
	keys_set_1={0:"a",1:"b",2:"c",3:"d",4:"e",
				5:"f",6:"g",7:"h",8:"i",9:"j",
				10:"k",11:"l",12:"m",13:"n",14:"o"}

	def letter(letter_index,text,letter_light):

		if letter_index<5:
			x=200*letter_index
			y=0

		elif 4<letter_index<10:
			letter_index=letter_index-5
			x=200*letter_index
			y=200

		elif 9<letter_index<15:
			letter_index=letter_index-10
			x=200*letter_index
			y=400		

		width=200
		height=200
		th=3 #thickness

		#cv2.rectangle(keyboard,(x+th,y+th),(x+width-th,y+height-th),(255,0,0),th)

		if letter_light is True:
			cv2.rectangle(keyboard,(x+th,y+th),(x+width-th,y+height-th),(255,255,255),-1)
		else:
		    cv2.rectangle(keyboard,(x+th,y+th),(x+width-th,y+height-th),(255,0,0),th)

		#text settings


		font_letter=cv2.FONT_HERSHEY_PLAIN
		
		font_scale=10
		font_th=4
		text_size=cv2.getTextSize(text,font_letter,font_scale,font_th)[0]
		width_text,height_text=text_size[0],text_size[1]
		text_x=int((width-width_text)/2)+x
		text_y=int((width-width_text)/2)+y+100
		cv2.putText(keyboard,text,(text_x,text_y),font_letter,font_scale,(255,0,0),font_th)



	#counters

	frames=0
	letter_index=0
	blinking_frames=0
	text=""

	while True:

		_,frame=cap.read(0)
		frames +=1
		keyboard[:]=(0,0,0)
		gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces=detector(gray)
		active_letter=keys_set_1[letter_index]


		for face in faces:
			#x,y=face.left(),face.top()
			#x1,y1=face.right(),face.bottom()
			#print(face)
			#cv2.rectangle(frame,(x,y),(x1,y1),(0,255,0))
			landmarks=predictor(gray,face)
			#print(landmarks.part(36))
			
			#left eye
			
			
			top=midpoint(landmarks.part(37),landmarks.part(38))
			bottom=midpoint(landmarks.part(41),landmarks.part(40))

			
			leftpoint=(landmarks.part(36).x,landmarks.part(36).y)
			rightpoint=(landmarks.part(39).x,landmarks.part(39).y)
			#hor_line=cv2.line(frame,leftpoint,rightpoint,(0,255,0),2)
			#ver_line=cv2.line(frame,top,bottom,(0,255,0),2)





		
			leftver_line_length = hypot((top[0]-bottom[0]),(top[1]-bottom[1]))
			lefthor_line_length = hypot((leftpoint[0]-rightpoint[0]),(leftpoint[1]-rightpoint[1]))
			ratio1=lefthor_line_length/leftver_line_length
			

			#right eye    

			leftpoint1=(landmarks.part(42).x,landmarks.part(42).y)
			rightpoint1=(landmarks.part(45).x,landmarks.part(45).y)

			topr=midpoint(landmarks.part(43),landmarks.part(44))
			bottomr=midpoint(landmarks.part(47),landmarks.part(46))
			#hor_line1=cv2.line(frame,leftpoint1,rightpoint1,(0,255,0),2)
			#ver_line1=cv2.line(frame,topr,bottomr,(0,255,0),2)
			

			rightver_line_length = hypot((topr[0]-bottomr[0]),(topr[1]-bottomr[1]))
			righthor_line_length = hypot((leftpoint1[0]-rightpoint1[0]),(leftpoint1[1]-rightpoint1[1]))
			ratio2=righthor_line_length/rightver_line_length
			ratio=(ratio2+ratio1)/2
			#cv2.putText(frame,str(ratio),(50,150),font,3,(255,0,0))

			#print(leftver_line_length)
			if ratio>4.8:
				#cv2.putText(frame,str(letter_index),(400,150),font,3,(255,0,0))
				cv2.putText(frame,"BLINKING",(50,150),font,3,(0,0,255))
				#print(keys_set_1[letter_index])
				blinking_frames+=1
				frames-=1

				if blinking_frames==5:
					config.text += active_letter
					playsound("get-outta-here.mp3")
					#time.sleep(1)
				#	print(keys_set_1[letter_index])
				#	print(text)
				#	print(active_letter)
			else:
				blinking_frames=0


			#print(text)
			
			gaze_ratio_left_eye=get_eye_gaze_ratio([36,37,38,39,40,41],landmarks)
			gaze_ratio_right_eye=get_eye_gaze_ratio([42,43,44,45,46,47],landmarks)

			gaze_ratio=(gaze_ratio_left_eye+gaze_ratio_right_eye)/2
			cv2.putText(frame,str(gaze_ratio),(50,300),font,2,(0,0,255),3)
			if gaze_ratio<0.1:

				cv2.putText(frame,"right",(50,200),font,2,(0,0,255),3)
			elif gaze_ratio>1:
				cv2.putText(frame,"left",(50,200),font,2,(0,0,255),3)
			

		if frames==15:
			letter_index =letter_index+1
			frames=0
		if letter_index==15:
			letter_index=0

		for i in range(15):
			if i==letter_index:
				light=True
			else:
				light=False
			letter(i,keys_set_1[i],light)

		cv2.putText(board,config.text,(50,150),font,4,0,3)    


			

			#threshold_eye=cv2.resize(threshold_eye,None,fx=8,fy=8)
		keyboard1=cv2.resize(keyboard,None,fx=0.5,fy=0.5)
			#cv2.imshow("t",threshold_eye)
			#cv2.imshow("left",left_side_threshold)
		
			#cv2.imshow("right",right_side_threshold)

		joint_keyboard=np.vstack((board,keyboard))
		joint_keyboard1=cv2.resize(joint_keyboard,(600,700))	
		
		#final_keyboard=np.concatenate((joint_keyboard1,frame),axis=)
		#cv2.imshow("f",frame)
		ff=cv2.resize(frame,(600,700))
		#cv2.imshow("keyboardfirst",keyboard_type)
		#cv2.imshow("keyboard",keyboard1)
		#cv2.imshow("board",board)
		#cv2.imshow("key",joint_keyboard1)

		joined_frames=np.hstack((ff,joint_keyboard1))
		cv2.imshow("a to o",joined_frames)


		key = cv2.waitKey(1)
		if key==27: #pressing esc key
			break
	    

	cap.release()
	cv2.destroyAllWindows()




#start=omg()
