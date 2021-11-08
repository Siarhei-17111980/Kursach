import cv2    # импортируем библиотеку

img = cv2.imread('images/face1.jpeg')   # читаем изображение

img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))  # уменьшаем размер изображения в 2 раза

img_1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # переводим изображение в серый цвет

neuron = cv2.CascadeClassifier('haar_face.xml')  # используем натренированную нейронную сеть

faces = neuron.detectMultiScale(img_1, scaleFactor=1.3, minNeighbors=1)  # находим лица при помощи нейронной сети

print(f'Найдено {len(faces)} лиц')  # определяем количество распознанных лиц

for (x, y, w, h) in faces:    # пробегаемся по распознанным лицам и рисуем квадрат по их координатам
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness=2)

cv2.imshow('Faces', img)    # результат работы

cv2.waitKey(0)   # время показа результата в милисекундах

cv2.destroyAllWindows()