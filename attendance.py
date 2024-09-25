import cv2 
import face_recognition


myImage = face_recognition.load_image_file('ImageAttendance/Nicolas Satria Dermawan.jpg')
myImage = cv2.cvtColor(myImage, cv2.COLOR_BGR2RGB)

resized_image = cv2.resize()

megawatiImg = face_recognition.load_image_file('ImageAttendance/Megawati.jpg')
megawatiImg = cv2.cvtColor(megawatiImg, cv2.COLOR_BGR2RGB)

faceloc = face_recognition.face_locations(myImage)[0]
encodemyface = face_recognition.face_encodings(myImage)[0]
cv2.rectangle(myImage,(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]), (255,0,255),2)

facelocmega = face_recognition.face_locations(megawatiImg)[0]
encodemyfacemega = face_recognition.face_encodings(megawatiImg)[0]
cv2.rectangle(megawatiImg,(facelocmega[3],facelocmega[0]),(facelocmega[1],facelocmega[2]), (255,0,255),2)

results = face_recognition.compare_faces([encodemyface],encodemyfacemega)
facedis = face_recognition.face_distance([encodemyface],encodemyfacemega)
print(results,facedis)
cv2.putText(megawatiImg,f'{results} {round(facedis[0],2)}', (50, 50), cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

cv2.imshow('Muka Niko', myImage)
cv2.imshow('Muka Megawati', megawatiImg)
cv2.waitKey(0)