import matplotlib.pyplot as plt 
import numpy as np 
import os 
import PIL 
import tensorflow as tf 
import pathlib 
from PIL import Image   
import glob  
from tensorflow import keras 
from tensorflow.keras import layers 
from tensorflow.keras.models import Sequential 


data_dir = "C:/Users/s/Downloads/flower_photos/flower_photos"
datagen = tf.keras.preprocessing.image.ImageDataGenerator()
data = datagen.flow_from_directory(data_dir)
data_dir = pathlib.Path(data_dir) 
data_dir_path = pathlib.Path(data_dir) 


# Training split 
train_ds = tf.keras.utils.image_dataset_from_directory( 
	data_dir, 
	validation_split=0.2, 
	subset="training", 
	seed=123, 
	image_size=(180, 180), 
	batch_size=32) 
# Testing or Validation split 
val_ds = tf.keras.utils.image_dataset_from_directory( 
	data_dir, 
	validation_split=0.2, 
	subset="validation", 
	seed=123, 
	image_size=(180,180), 
	batch_size=32) 
class_names = train_ds.class_names 
print(class_names)
import matplotlib.pyplot as plt 

plt.figure(figsize=(10, 10)) 

for images, labels in train_ds.take(1): 
	for i in range(25): 
		ax = plt.subplot(5, 5, i + 1) 
		plt.imshow(images[i].numpy().astype("uint8")) 
		plt.title(class_names[labels[i]]) 
		plt.axis("off") 

plt.show()

num_classes = len(class_names) 

model = Sequential([ 
	layers.Rescaling(1./255, input_shape=(180,180, 3)), 
	layers.Conv2D(16, 3, padding='same', activation='relu'), 
	layers.MaxPooling2D(), 
	layers.Conv2D(32, 3, padding='same', activation='relu'), 
	layers.MaxPooling2D(), 
	layers.Conv2D(64, 3, padding='same', activation='relu'), 
	layers.MaxPooling2D(), 
	layers.Flatten(), 
	layers.Dense(128, activation='relu'), 
	layers.Dense(num_classes) 
]) 
model.compile(optimizer='adam', 
			loss=tf.keras.losses.SparseCategoricalCrossentropy( 
				from_logits=True), 
			metrics=['accuracy']) 
model.summary() 
epochs=10
history = model.fit( 
train_ds, 
validation_data=val_ds, 
epochs=epochs 
) 
#Accuracy 
acc = history.history['accuracy'] 
val_acc = history.history['val_accuracy'] 

#loss 
loss = history.history['loss'] 
val_loss = history.history['val_loss'] 

#epochs 
epochs_range = range(epochs) 


plt.figure(figsize=(8, 8)) 
plt.subplot(1, 2, 1) 
plt.plot(epochs_range, acc, label='Training Accuracy') 
plt.plot(epochs_range, val_acc, label='Validation Accuracy') 
plt.legend(loc='lower right') 
plt.title('Training and Validation Accuracy') 

plt.subplot(1, 2, 2) 
plt.plot(epochs_range, loss, label='Training Loss') 
plt.plot(epochs_range, val_loss, label='Validation Loss') 
plt.legend(loc='upper right') 
plt.title('Training and Validation Loss') 
plt.show() 


from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Assuming you have the true labels and predicted labels from your validation set
y_true = []
y_pred = []

# Get the true and predicted labels for the entire validation set
for images, labels in val_ds:
    predictions = model.predict(images)
    predicted_labels = np.argmax(predictions, axis=1)
    
    y_true.extend(labels.numpy())
    y_pred.extend(predicted_labels)



