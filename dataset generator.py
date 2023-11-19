import cv2

# Открываем видеофайл с помощью OpenCV
video = cv2.VideoCapture('dataset.mp4')

# Читаем кадры из видеофайла
success, frame = video.read()

# Пока кадры читаются успешно, сохраняем их как изображения
frame_count = 0
while success:
    # Сохраняем кадр в файл с названием "кадр_номер_{}.jpg"
    if frame_count % 299 == 0:
        cv2.imwrite(f"{frame_count}.jpg", frame)

    # Читаем следующий кадр
    success, frame = video.read()

    # Увеличиваем счетчик кадров
    frame_count += 300

# Закрываем видеофайл
video.release()

