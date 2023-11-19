from ultralytics import YOLO

#    ____                       __              ____   __  __                      
#   / __ )____ ______________  / /____   ____  / __/  / / / /___  ____  ___  __  __
#  / __  / __ `/ ___/ ___/ _ \/ / ___/  / __ \/ /_   / /_/ / __ \/ __ \/ _ \/ / / /
# / /_/ / /_/ / /  / /  /  __/ (__  )  / /_/ / __/  / __  / /_/ / / / /  __/ /_/ / 
#/_____/\__,_/_/  /_/   \___/_/____/   \____/_/    /_/ /_/\____/_/ /_/\___/\__, /  
#                                                                         /____/  
 
model = YOLO("yolov8n.pt")  # загрузите предварительно обученную модель YOLOv8n
 
#model.train(data='training_model\data.yaml')  # обучите модель
#model.val()  # оцените производительность модели на наборе проверки
#model.predict(source="test.png")  # предсказать по изображению
#model.export(format="onnx")  # экспортируйте модель в формат ONNX

