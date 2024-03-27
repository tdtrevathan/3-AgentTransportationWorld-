import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
import tensorflow

import numpy
import seaborn
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from tabulate import tabulate
from matplotlib import pyplot

#IMPORTANT DISREGARD THE WARNINGS IN THE OUTPUT, THEY DO NOT IMPEDE THE APPLICATION

def f2_score(precision, recall):
    beta = 2
    if precision == 0 or recall == 0:
        return 0
    f2 = (1 + beta**2) * (precision * recall) / ((beta**2 * precision) + recall)
    return f2

#SETUP

tensorflow.autograph.set_verbosity(1)

fashion_mnist = tensorflow.keras.datasets.fashion_mnist;

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

train_images = train_images / 255.0
test_images = test_images / 255.0

#---------------------------------------------------------------

#GET USER INPUT

number_of_convolutional_layers = int(input("Number of Convolutional Layers: "))
number_of_filters = int(input("Number of Neurons in First Layer: "))

number_of_layers = int(input("Number of Dense Layers: "))

epochs = int(input('Number of Epochs: '))
learning_rate = float(input("Learning Rate: "))

print('Choose the Loss Function:')
print('Sparse Categorical Cross Entropy = 1')
print('Mean Squared Error = 0')
print()
loss_function = bool(int(input("Choice: ")))

#---------------------------------------------------------------

#CREATE MODEL BASED ON INPUTS

model = tensorflow.keras.Sequential()

# Add convolutional layers
model.add(tensorflow.keras.layers.Conv2D(number_of_filters, kernel_size=(3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(tensorflow.keras.layers.MaxPooling2D(pool_size=(2, 2)))

print('Input the Neurons for the Convolutional Layers')
for i in range(number_of_convolutional_layers):
    number_of_filters = int(input(f"Number of Neurons in Convolutional Layer {i+1}: "))
    model.add(tensorflow.keras.layers.Conv2D(number_of_filters , kernel_size=(3, 3), activation='relu'))
    model.add(tensorflow.keras.layers.MaxPooling2D(pool_size=(2, 2)))

model.add(tensorflow.keras.layers.Flatten())

# Add dense layers
print('Input the Neurons for the Dense Layers')
for i in range(number_of_layers):
    number_of_nodes = int(input(f"Number of Neurons in Dense Layer {i+1}: "))
    model.add(tensorflow.keras.layers.Dense(number_of_nodes, activation='relu'))

# Add final layer
model.add(tensorflow.keras.layers.Dense(10, activation='softmax'))

#setup optimizer
optimizer = tensorflow.keras.optimizers.Adam(learning_rate=learning_rate)

# setup compile, fit, and evaluate based on loss function
if loss_function:
    print('sparse')
    model.compile(optimizer,
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    training_results = model.fit(train_images, train_labels, epochs=epochs)
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=3)
else:
    print('mse')
    model.compile(optimizer, loss='mean_squared_error', metrics=['accuracy'])

    # Convert labels to one-hot encoding
    train_labels_one_hot = tensorflow.keras.utils.to_categorical(train_labels)
    test_labels_one_hot = tensorflow.keras.utils.to_categorical(test_labels)

    # Train the model
    training_results = model.fit(train_images, train_labels_one_hot, epochs=epochs)
    test_loss, test_acc = model.evaluate(test_images, test_labels_one_hot, verbose=3)

#---------------------------------------------------------------

# SEUTUP OUTPUTS

#TRAINING DATA GRAPHS

#obtain training result data
training_results = training_results.history

# Extracting the loss and accuracy for training
loss_values = training_results['loss']
accuracy_values = training_results['accuracy']

# Extracting the validation loss and accuracy
val_loss_values = training_results.get('val_loss', [])
val_accuracy_values = training_results.get('val_accuracy', [])

#----------------------------

#TEST DATA REPORT AND CONFUSION MATRIX

#get predictions for report and confusion matrix
predictions = model.predict(test_images)
predicted_classes = numpy.argmax(predictions, axis=1)

#create report
report = classification_report(test_labels, predicted_classes, target_names=class_names, output_dict=True, digits=3)

#create confusion matrix
conf_matrix = confusion_matrix(test_labels, predicted_classes)

#plot confusion matrix
pyplot.figure(figsize=(10, 7))

# Using seaborn to create the heatmap
seaborn.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', xticklabels=class_names, yticklabels=class_names)

# Extract just the classes part of the report, omitting 'accuracy', 'macro avg', and 'weighted avg'
classes_report = {k: v for k, v in report.items() if k not in ['accuracy', 'macro avg', 'weighted avg']}

# Find the class with the lowest precision
lowest_precision = 1.0  # Start with 1.0 as the max possible precision
lowest_class = None
for class_label, metrics in classes_report.items():
    if metrics['precision'] < lowest_precision:
        lowest_precision = metrics['precision']
        lowest_class = class_label

#Calculate f2 scores
lowest_f2 = 1.0

for class_label, metrics in classes_report.items():
    report[class_label]['f2-score'] = f2_score(metrics['precision'],metrics['recall'])

column_values = [report[class_name]['f2-score'] for class_name in class_names]
lowest_f2_value = min(column_values)

#Get lowest f2 score
for class_label, metrics in classes_report.items():
    if metrics['f2-score'] == lowest_f2_value:
        lowest_f2_class = class_label

#Setup table to report data
table_data = []
for class_name in class_names:
    precision = report[class_name]['precision']
    recall = report[class_name]['recall']
    f1_score = report[class_name]['f1-score']
    f2_score = report[class_name]['f2-score']
    table_data.append([class_name, precision, recall, f1_score, f2_score])

#--------------------------------------------------

#Show confusion matrix
pyplot.xlabel('Predicted labels')
pyplot.ylabel('True labels')
pyplot.title('Confusion Matrix')
pyplot.show()


# Plotting training and validation loss
pyplot.figure(figsize=(12, 5))


epochs = range(1, len(loss_values) + 1)

pyplot.subplot(1, 2, 1)
pyplot.plot(epochs, loss_values, 'bo', label='Training loss')
if val_loss_values:
    pyplot.plot(epochs, val_loss_values, 'b', label='Validation loss')
pyplot.title('Training and validation loss')
pyplot.xlabel('Epochs')
pyplot.ylabel('Loss')
pyplot.legend()

# Plotting training and validation accuracy
pyplot.subplot(1, 2, 2)
pyplot.plot(epochs, accuracy_values, 'bo', label='Training accuracy')
if val_accuracy_values:
    pyplot.plot(epochs, val_accuracy_values, 'b', label='Validation accuracy')
pyplot.title('Training and validation accuracy')
pyplot.xlabel('Epochs')
pyplot.ylabel('Accuracy')
pyplot.legend()

pyplot.tight_layout()
pyplot.show()

#show table
print('\nTest accuracy:', test_acc)
print()
print(f'Class with lowest precision: {lowest_class}')
print(f'Class with the lowest f2 value: {lowest_f2_class}')
print(tabulate(table_data, headers=["Class", "Precision", "Recall", "F1-score", "F2-score"], tablefmt="grid"))