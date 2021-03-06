import streamlit as st 
import cv2
from PIL import Image,ImageEnhance
import numpy as np 
import os

st.set_option('deprecation.showfileUploaderEncoding', False)
#st.write(st.config.get_option("server.enableCORS"))


try:
	face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
	eye_cascade=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')
	smile_cascade= cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_smile.xml')
except Exception:
	st.write("Error loading cascade classifiers")


def detect_faces(our_image):
	newimg = np.array(our_image.convert('RGB'))
	new_img = cv2.resize(newimg, (500, 509))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# Detect faces
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	# Draw rectangle around the faces
	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

	return (img,faces)   
def detect_eyes(our_image):
	newimg = np.array(our_image.convert('RGB'))
	new_img = cv2.resize(newimg, (500, 509))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
	for (ex,ey,ew,eh) in eyes:
	        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

	return img

def detect_smiles(our_image):
	newimg = np.array(our_image.convert('RGB'))
	new_img = cv2.resize(newimg, (500, 509))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# Detect Smiles
	smiles = smile_cascade.detectMultiScale(gray, 1.2, 25)
	# Draw rectangle around the Smiles
	for (x, y, w, h) in smiles:
	    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
	return img
def cartoonize_image(our_image):
	newimg = np.array(our_image.convert('RGB'))
	new_img = cv2.resize(newimg, (500, 509))
	img = cv2.cvtColor(new_img,1)
	gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
	# Edges
	gray = cv2.medianBlur(gray, 5)
	edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
	#Color
	color = cv2.bilateralFilter(img, 9, 300, 300)
	#Cartoon
	cartoon = cv2.bitwise_and(color, color, mask=edges)

	return cartoon

def canonize_image(our_image):
	newimg = np.array(our_image.convert('RGB'))
	new_img = cv2.resize(newimg, (500, 509))
	img = cv2.cvtColor(new_img,1)
	img = cv2.GaussianBlur(img, (11, 11), 0)
	canny = cv2.Canny(img, 100, 150)
	return canny




def main():
	"""Face Detection App"""

	st.title("Face Detection App")
	st.text("Build with Streamlit and OpenCV")

	activities = ["Detection","About"]
	choice = st.sidebar.selectbox("Select Activty",activities)

	if choice == 'Detection':
		st.subheader("Face Detection")

		image_file = st.file_uploader("Upload Image",type=['jpg','png','jpeg','webp'])

		if image_file is not None:
			our_image= Image.open(image_file)
			st.text('Original Image')
			
	
		enhance_type= st.sidebar.radio('Enhance Type',['Original','Gray-Scale','Contrast','Brightness'])
		
		if enhance_type == 'Gray-Scale':		
			new_img = np.array(our_image.convert('RGB'))
			img =cv2.cvtColor(new_img,1)
			gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
			#st.write(new_img)
			st.image(gray)
		elif enhance_type == 'Contrast':			
			c_rate=st.sidebar.slider('Contrast',0.5,3.5)
			enhancer=ImageEnhance.Contrast(our_image)
			img_output=enhancer.enhance(c_rate)
			st.image(img_output)
		elif enhance_type == 'Brightness':			
			c_rate=st.sidebar.slider('Brightness',0.5,3.5)
			enhancer=ImageEnhance.Brightness(our_image)
			img_output=enhancer.enhance(c_rate)
			st.image(img_output)


		# Face detection
		task =['Faces','Smiles','Eyes','Canonize','Cartoonize']
		feature_choice=st.sidebar.selectbox('Find Features',task)
		if st.button('Process'):

			if feature_choice =='Faces':
				result_img,result_faces = detect_faces(our_image)
				st.image(result_img)

				st.success("Found {} faces".format(len(result_faces)))
	
			elif feature_choice == 'Smiles':
				result_img = detect_smiles(our_image)
				st.image(result_img)


			elif feature_choice == 'Eyes':
				result_img = detect_eyes(our_image)
				st.image(result_img)

			elif feature_choice == 'Cartoonize':
				result_img = cartoonize_image(our_image)
				st.image(result_img)

			elif feature_choice == 'Canonize':
				result_canny = canonize_image(our_image)
				st.image(result_canny)





	elif choice == 'About':
		st.text("Here is my email ID")
		st.success("samriddhi100mit@gmal.com")

		

if __name__ == '__main__':
		main()	

