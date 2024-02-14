import tensorflow as tf
import pandas as pd
from PIL import Image
import numpy as np
from tqdm import tqdm
import keras
import cv2
from Application import annotate_realtime

# train_labels_raw = pd.read_csv("datasets/CFV-Dataset/train.csv")
# # train_labels = train_labels.loc[:, ["image_path", "angle"]]
test_labels_raw = pd.read_csv("../../Forest/datasets/CFV-Dataset/test.csv")
print(tf.config.list_physical_devices())

# store images
train_x = []
test_x = []

# store angles
train_y = []
test_y = []


# for i, row in tqdm(train_labels_raw.iterrows(), total=train_labels_raw.shape[0]):
#     image_path = row['image_path']
#     angle = row['angle']
#     x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
#     if x1 == 0:
#         continue
#
#     image = np.array(Image.open(f"datasets/CFV-Dataset/images/{image_path}", 'r').crop((x1, y1, x2, y2))
#                      .resize((128, 128)))
#     train_x.append(image)
#     train_y.append(angle)
# train_x = (np.array(train_x) / 255).astype(np.float32)
# train_y = (np.array(train_y) / 360).astype(np.float32)
#
# train_dataset = tf.data.Dataset.from_tensor_slices((train_x, train_y))
# train_dataset = train_dataset.batch(32)
#
#
for i, row in tqdm(test_labels_raw.iterrows(), total=test_labels_raw.shape[0]):
    image_path = row['image_path']
    angle = row['angle']
    x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
    if x1 == 0:
        continue

    image = np.asarray(Image.open(f"../datasets/CFV-Dataset/images/{image_path}", 'r').crop((x1, y1, x2, y2))
                       .resize((128, 128)))
    test_x.append(image)
    test_y.append(angle)

test_x = (np.array(test_x) / 255).astype(np.float32)
test_y = (np.array(test_y) / 360).astype(np.float32)
test_dataset = tf.data.Dataset.from_tensor_slices((np.array(test_x), np.array(test_y)))
test_dataset = test_dataset.batch(32)
#
#
#
#
# model = Sequential([
#     layers.InputLayer(input_shape=(128, 128, 3)),
#     layers.Conv2D(16, 3, padding='same', activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Conv2D(32, 3, padding='same', activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Conv2D(64, 3, padding='same', activation='relu'),
#     layers.MaxPooling2D(),
#     layers.Flatten(),
#     layers.Dense(128, activation='relu'),
#     layers.Dense(64, activation='relu'),
#     layers.Dense(1, activation='sigmoid')
# ])
#
# model.compile(optimizer='adam',
#               loss=losses.MeanSquaredError(),
#               metrics=['accuracy'])
#
# model.summary()
#
# epochs = 500
#
# model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
#     filepath="Pretrained_networks/angle_model/best_weight.h5",
#     save_weights_only=True,
#     monitor='val_loss',
#     mode='min',
#     save_best_only=True)
#
# history = model.fit(
#     train_dataset,
#     validation_data=test_dataset,
#     epochs=epochs,
#     callbacks=[model_checkpoint_callback]
# )
# model.save('Pretrained_networks/angle_model/angle_model.keras')
# model.save_weights('Pretrained_networks/angle_model/angle_model_weights.h5')
#
# acc = history.history['accuracy']
# val_acc = history.history['val_accuracy']
#
# loss = history.history['loss']
# val_loss = history.history['val_loss']
#
# epochs_range = [i for i in range(1, epochs+1)]
#
# plt.figure(figsize=(8, 8))
# plt.subplot(1, 2, 1)
# plt.plot(epochs_range, acc, label='Training Accuracy')
# plt.plot(epochs_range, val_acc, label='Validation Accuracy')
# plt.legend(loc='lower right')
# plt.title('Training and Validation Accuracy')
#
# plt.subplot(1, 2, 2)
# plt.plot(epochs_range, loss, label='Training Loss')
# plt.plot(epochs_range, val_loss, label='Validation Loss')
# plt.legend(loc='upper right')
# plt.title('Training and Validation Loss')
# plt.show()

angle_estimator = keras.models.load_model("angle_model/angle_model.keras")
angle_estimator.load_weights("../Pretrained_networks/angle_model/angle_model_weights.h5")
# score = angle_estimator.evaluate(test_x, test_y, verbose=0)

# img = Image.open("download.jpg")
# img = img.resize((128, 128))
# img = np.asarray(img)
# img = np.array([img])

angles = angle_estimator.predict(test_x)
cnt = 0

for a in angles.tolist():
    angle = a[0] * 360
    print(annotate_realtime.distancesEstimation())
    # draw
    length = 25
    start_point = (64, 64)
    # Convert the angle to radians
    angle_rad = np.radians(90 - angle)

    # Calculate the end point
    end_point = (int(start_point[0] + length * np.cos(angle_rad)),
                 int(start_point[1] + length * np.sin(angle_rad)))

    # Draw the arrowed line
    img = test_x[cnt]
    cv2.arrowedLine(img, start_point, end_point, (0, 255, 0), thickness=2)
    cv2.imshow('pic', img)
    cv2.waitKey(0)
    cnt += 1