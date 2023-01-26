import pickle
from pathlib import Path
from csv import DictWriter
from csv import writer

import streamlit as st
import streamlit_authenticator as stauth
import os
import av
import cv2
import csv
import numpy as np
from datetime import datetime
import face_recognition
import pandas as pd


face = pickle.load(open('face_list.csv','rb'))
known_faces_names=face['known_faces_names'].tolist()
known_face_encoding=face['known_face_encoding'].tolist()


df=pd.DataFrame(columns=['Name','Time'])



# st.set_page_config(page_title="Simple Auth", layout="wide")

st.title("Face Recognition Attendence System")

select=st.sidebar.selectbox(
    "Select a mode",['Default','For Student','For Teacher']
)

now = datetime.now()
current_date=now.strftime("%Y-%m-%d")
# f=open(current_date+'.csv','w+',newline='')
# lnwrite=csv.writer(f)


def CheckPresentOrNot(user_name):
	if os.path.isfile(current_date+'abhi.csv'):
		attendence=pd.read_csv(current_date+'abhi.csv')
		listA=attendence.values.tolist()
		# data=attendence.head()
		print(listA)
		for i in listA:
			if i[0]==user_name:
				return False
		
		return True
	else:
		return True


def FACERECON(user_name):
	selected_mode = st.selectbox(
    	"Select a mode",['Default','image','upload']
	)

	if selected_mode=='image':
		# students=known_faces_names.copy()

		face_location=[]
		face_encoding=[]
		face_names=[]
		s=True

		img=st.camera_input("Take")
		if img is not None:
			b=img.getvalue()
			cimg=cv2.imdecode(np.frombuffer(b,np.uint8),cv2.IMREAD_COLOR)
			st.write(type(cimg))
			st.write(cimg.shape)
			# _,frame=video_capture.read()
			small_frame=cimg
			rgb_small_frame=small_frame[:,:,::-1]

			if s:
				face_location=face_recognition.face_locations(rgb_small_frame)
				face_encodings=face_recognition.face_encodings(rgb_small_frame,face_location)
				face_names=[]
				for face_encoding in face_encodings:
					matches=face_recognition.compare_faces(known_face_encoding,face_encoding)
					# print(matches)
					name=""
					face_distance=face_recognition.face_distance(known_face_encoding , face_encoding)
					# print(face_distance)
					best_match_index=np.argmin(face_distance)
					print(best_match_index)
					if matches[best_match_index]:
						name=known_faces_names[best_match_index]

					face_names.append(name)
					if name in known_faces_names and name==user_name and CheckPresentOrNot(user_name):
						# students.remove(name)
						st.write(name)
						current_time=now.strftime("%H hr-%M min")
						# df.loc[len(df.index)]=[user_name,current_time]
						dic={'Name':user_name,'Time':current_time}
						st.write(current_time)
						# lnwrite.writerow([name,current_time])
						st.write("Attendence Marked")
						# st.dataframe(df)
						field_names=['Name','Time']
						
						if os.path.isfile(current_date+'abhi.csv'):
							print(df)
						else:
							with open(current_date+'abhi.csv','w') as f_object:
								writer_object=writer(f_object)
								writer_object.writerow(field_names)
								f_object.close()
						
						with open(current_date+'abhi.csv','a') as f_object:
							dictwriter_object=DictWriter(f_object,fieldnames=field_names)
							dictwriter_object.writerow(dic)
							f_object.close()
					else:
						st.write("Your Attendence is recorded or the user is not matching....")

						
		
	# f.close()					


		

	
    



def LOGIN():
	names=["ratan tata","bill gates","abhishek","divyanshu","ambuj","joshi","rana","sindhwal"]
	usernames=['ratan','bill','abhishek','divyanshu','ambuj','joshi','rana','sindhwal']

	file_path=Path(__file__).parent / "hashed_pw.pkl"
	with file_path.open("rb") as file:
		hashed_passwords=pickle.load(file)

	credentials = {
			"usernames":{
			usernames[0]:{
				"name":names[0],
				"password":hashed_passwords[0]
			},
			usernames[1]:{
				"name":names[1],
				"password":hashed_passwords[1]
			},
			usernames[2]:{
				"name":names[2],
				"password":hashed_passwords[2]
			},
			usernames[3]:{
				"name":names[3],
				"password":hashed_passwords[3]
			}

		}
	}
	authenticator=stauth.Authenticate(credentials,'some_cookie_name','some_signature_key',cookie_expiry_days=0)

	name,authentication_status,username=authenticator.login("Login","main")

	if authentication_status==False:
		st.error("Username/password is incorrect")

	if authentication_status==None:
		st.warning("Please enter your username and password")

	if authentication_status:
		st.write("Mark your attendence")
		authenticator.logout("Logout","sidebar")
		st.sidebar.title(f"Welcome {name}")

		FACERECON(name)


def SeeRecord():
	selected_mode = st.selectbox(
    	"Select a mode",['Default','See','upload']
	)

	if selected_mode=='upload':
		name=st.text_input("Enter")
		uploaded_file = st.file_uploader("Choose a file")
		if uploaded_file is not None:
			st.write(name)
			st.image(uploaded_file)
			uploaded_image=face_recognition.load_image_file(uploaded_file)
			uploaded_encoding=face_recognition.face_encodings(uploaded_image)[0]
			st.write(uploaded_image)
			known_face_encoding.append(uploaded_encoding)
			known_faces_names.append(name)
			
		for i in known_faces_names:
			st.write(i)

	elif selected_mode=="See":
		now = datetime.now()
		current_date=now.strftime("%Y-%m-%d")
		df=pd.read_csv(current_date+'abhi.csv')
		st.dataframe(df)


def LOGIN2():
	names=['AD','Ram']
	usernames=['aa','ram']
	hashed_passwords=['ab','ab']


	# file_path=Path(__file__).parent / "hashed_pw.pkl"
	# with file_path.open("rb") as file:
	# 	hashed_passwords=pickle.load(file)

	credentials = {
			"usernames":{
			usernames[0]:{
				"name":names[0],
				"password":hashed_passwords[0]
			},
			usernames[1]:{
				"name":names[1],
				"password":hashed_passwords[1]
			}
		}
	}
	authenticator=stauth.Authenticate(credentials,'some_cookie_name','some_signature_key',cookie_expiry_days=0)

	name,authentication_status,username=authenticator.login("Login","main")

	if authentication_status==False:
		st.error("Username/password is incorrect")

	if authentication_status==None:
		st.warning("Please enter your username and password")

	if authentication_status:
		st.write("Mark your attendence")
		authenticator.logout("Logout","sidebar")
		st.sidebar.title(f"Welcome {name}")

		SeeRecord()
		

if select=='For Student':
	LOGIN()

elif select=='For Teacher':
	LOGIN2()

else:
	st.write(df)

	


