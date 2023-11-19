from roboflow import Roboflow
import cv2
from pyzbar import pyzbar
import requests

#в папке есть три показательных изображения, но в принципе можно взять любой скрин
picpath = "final/cam 1/3.jpg"
error_count = 0

def addPallet(text1): # данный кусок кода закоментирован, т.к. у нас нет подключения к другому серверу, то есть никто не может дать нам данные, а мы не можем их никуда отправить, из-за этого возникает ошибка, но если бы подключение было, то оно бы работало полностью корректно
   ''' url = 'https://localhost:443' # адрес сервера, на котрый отправляем 
    response3 = requests.post(url, json=text1) # делайем пост запрос о создании палета
    if response3.status_code == 200: # проверяем запрос
        print("Данные успешно отправлены на сервер 2")
    else:
        print(f"Ошибка при отправке данных на сервер 2. Код ошибки: {response3.status_code}")
    return 0'''
def errorPallet(): # этот кусок также закоментирован, т.к. у нас нет подключения к серверу и из-за этого возникает ошибка, но при наличии подключения все будет работать корректно
    '''global error_count 
    response4 = requests.post(json={})
    if response4.status_code == 200: # проверяем запрос
        print("Данные успешно отправлены на сервер 2")
    else:
        print(f"Ошибка при отправке данных на сервер 2. Код ошибки: {response4.status_code}")
        error_count += 1
    return 0'''
#модель как-бы находится в интернете, но только из-за недостатка мощности домашнего пк. сетка с настроенными весами в репозитории
rf = Roboflow(api_key="xnUyH3z1mUbMPtiwz0Ra")
project = rf.workspace().project("pallet-detection-irbmw")
model = project.version(1).model

#ищем палеты
pallets = model.predict(picpath, confidence=40, overlap=30).json()
model.predict(picpath, confidence=40, overlap=30).save('pred.jpg')
cvpallets = []
for pallet in pallets['predictions']:
    cvpallets.append([ int(pallet['x'] - pallet['width'] /2), int(pallet['x'] + pallet['width'] /2), int(pallet['y'] - pallet['height'] /2), int(pallet['y'] + pallet['height'] /2)])
print(cvpallets)

#готовимся к скану кодов
screenshot = cv2.imread(picpath)
detector = cv2.QRCodeDetector()

for cvpallet in cvpallets:
    #print(cvpallet)
    # Получаем границы изображения
    x1, x2, y1, y2 = cvpallet[0], cvpallet[1], cvpallet[2], cvpallet[3]
    

    # Обрезаем изображение, учитывая границы
    croppedscreen = screenshot[y1:y2, x1:x2]	
    qrcodes = pyzbar.decode(croppedscreen)
    if qrcodes != []:
        print(str(qrcodes[0].data)[2:-2])
        addPallet(str(qrcodes[0].data)[2:-2])
    else:
        errorPallet()

    # Проверяем, что обрезанное изображение не пустое, и только тогда отображаем его
    #if croppedscreen.size != 0:
        #cv2.imshow('1',croppedscreen)
        
cv2.imshow('1',cv2.resize(screenshot, (1280,720)))
cv2.waitKey(0) # wait for ay key to exit window
cv2.destroyAllWindows() # close all windows