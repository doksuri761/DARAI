import pickle
import tensorflow as tf
from keras import layers
from keras import models
from keras import optimizers
from keras import losses
from keras import metrics
from keras import activations
from keras.callbacks import TensorBoard
import datetime
import numpy as np

with open("kor-grade-dataset.pkl", "rb") as f:
    dataset = pickle.load(f)

# model = models.Sequential([
#     layers.Dense(8, activation=activations.relu, input_shape=(1,)),
#     layers.Dense(16, activation=activations.leaky_relu),
#     layers.Dense(256, activation=activations.sigmoid),
#     layers.Dense(1024, activation=activations.relu),
#     layers.Dense(256, activation=activations.leaky_relu),
#     layers.Dense(1024, activation=activations.sigmoid),
#     layers.Dense(256, activation=activations.relu),
#     layers.Dense(16, activation=activations.leaky_relu),
#     layers.Dense(8, activation='sigmoid')
# ])
model = models.load_model("model.h5")
model.summary()
logdir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = TensorBoard(log_dir=logdir)
model.compile(optimizer=optimizers.SGD(learning_rate=0.005), loss=[losses.mse, losses.MSE], metrics=[metrics.accuracy, metrics.mae, metrics.mse, metrics.mape, metrics.msle])
print("Training...")
model.fit(np.array(dataset[0]), np.array(dataset[1]), epochs=20, batch_size=128, verbose=1, callbacks=[tensorboard_callback])
model.save("model.h5")
# model = models.load_model("model.h5")
# model.fit(np.array(dataset[0]), np.array(dataset[1]), epochs=240, batch_size=128, verbose=1)
# for i in [81,67,51,35,24,17,12,9]:
#     print(model.predict(np.array([i])).argmax() + 1)
# model.save("model.h5")
