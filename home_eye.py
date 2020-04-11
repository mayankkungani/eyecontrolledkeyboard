import dlib
import cv2
import numpy as np
from math import hypot
from playsound import playsound
import time
from rules import rules
from ao import omg
from num import num
from pz import omgpz
import config

#global text
def home():
	font=cv2.FONT_HERSHEY_PLAIN
	#global text
	
	option_window=np.zeros((950,1000,3),np.uint8)

	option_window[:]=(100,0,50)
	#video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
	#video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

	cap= cv2.VideoCapture(0)
	#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 950)
	#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1000)
	board=np.zeros((600,1000,3),np.uint8)
	keyboard_type=np.zeros((950,1000,3),np.uint8)

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
			


	def recta(output_index,light):
		#output_index=self.output_index

		if output_index==0:
			x=(200,440)  #rules
			y=(250,490)


		elif output_index==2:
			x=(700,440) # 0-9
			y=(750,490)
		


		elif output_index==1:
			x=(495,670) #a-0
			y=(445,720)

		else:
			x=(495,200) #p-z
			y=(445,250)

		if light is True:
			cv2.rectangle(option_window,x,y,(255,255,255),255,-1)
		else:	
			cv2.rectangle(option_window,x,y,(255,0,0),255,-1)

	#text settings

		cv2.putText(option_window,"Rules",(190,460),font,3,(0,0,0),3) 
		cv2.putText(option_window,"0-9",(690,460),font,3,(0,0,0),3)
		cv2.putText(option_window,"A-O",(425,695),font,3,(0,0,0),3)
		cv2.putText(option_window,"P-Z",(425,225),font,3,(0,0,0),3)



	#counters

	frames=0
	output_index=0
	blinking_frames=0
	#text=""

	while True:

		_,frame=cap.read(0)
		frames +=1
		#keyboard[:]=(0,0,0)
		gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
		faces=detector(gray)
		#active_letter=keys_set_1[letter_index]


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

				if blinking_frames==3:
					#text += active_letter
					playsound("get-outta-here.mp3")
					if output_index==0:
						rules()

					elif output_index==1:
						cap.release()
						cv2.destroyAllWindows()
						omg()
						home()
					elif output_index==2:
						cap.release()
						cv2.destroyAllWindows()
						num()
						home()
					else:
						cap.release()
						cv2.destroyAllWindows()
						omgpz()
						home()


					#time.sleep(1)
				#	print(keys_set_1[letter_index])
				#	print(text)
				#	print(active_letter)
			else:
				blinking_frames=0


			
			
			gaze_ratio_left_eye=get_eye_gaze_ratio([36,37,38,39,40,41],landmarks)
			gaze_ratio_right_eye=get_eye_gaze_ratio([42,43,44,45,46,47],landmarks)

			gaze_ratio=(gaze_ratio_left_eye+gaze_ratio_right_eye)/2
			cv2.putText(frame,str(gaze_ratio),(50,300),font,2,(0,0,255),3)
			if gaze_ratio<0.1:

				cv2.putText(frame,"right",(50,200),font,2,(0,0,255),3)
			elif gaze_ratio>1:
				cv2.putText(frame,"left",(50,200),font,2,(0,0,255),3)
			

		#print(frames)
		if frames==26:
			output_index=output_index+1
			frames=0
		if output_index==4:
			output_index=0


		for i in range(4):
			if i==output_index:
				light=True
			else:
				light=False
			recta(i,light) #note i
			#print(i,light)
		#print(light,output_index)





			

			#threshold_eye=cv2.resize(threshold_eye,None,fx=8,fy=8)
		#keyboard1=cv2.resize(keyboard,None,fx=0.5,fy=0.5)
			#cv2.imshow("t",threshold_eye)
			#cv2.imshow("left",left_side_threshold)
		
			#cv2.imshow("right",right_side_threshold)

		#joint_keyboard=np.vstack((board,keyboard))
		#joint_keyboard1=cv2.resize(joint_keyboard,None,fx=0.5,fy=0.5)	
		
		#final_keyboard=np.concatenate((joint_keyboard1,frame),axis=)
		option_window2=cv2.resize(option_window,(600,700))
		ff=cv2.resize(frame,(600,700))
		#cv2.imshow("fdd",ff)
		#cv2.imshow("f",frame)
		#cv2.imshow("keyboardfirst",keyboard_type)
		#cv2.imshow("keyboard",keyboard1)
		#cv2.imshow("board",board)
		#cv2.imshow("key",joint_keyboard1)
		joined_frames=np.hstack((ff,option_window2))
		cv2.imshow("home",joined_frames)
		key = cv2.waitKey(1)
		if key==27: #pressing esc key
			break
	    

	cap.release()
	cv2.destroyAllWindows()

home()