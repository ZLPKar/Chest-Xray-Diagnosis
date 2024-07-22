import os
import numpy as np
import shutil
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input

# Paths
model_path = r'C:\Users\zachp\OneDrive - University of Leicester\Computer science project\resnet50_3_class_modelv3.h5'
data_path = r'C:\Users\zachp\OneDrive - University of Leicester\Computer science project\test'
target_paths = {
    'Normal': r'C:\Users\zachp\OneDrive - University of Leicester\Computer science project\Normal',
    'Virus': r'C:\Users\zachp\OneDrive - University of Leicester\Computer science project\Viral',
    'Bacteria': r'C:\Users\zachp\OneDrive - University of Leicester\Computer science project\Bacterial'
}

# Load the model
model = load_model(model_path)

# Ensure target directories exist
for target_path in target_paths.values():
    os.makedirs(target_path, exist_ok=True)

# Prepare image for prediction (same as training preprocessing)
def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    # Apply rescaling as used during training
    return img_array / 255.0

# Predict and move images
for img_name in os.listdir(data_path):
    img_path = os.path.join(data_path, img_name)
    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):  # Check if the file is an image
        img_array = prepare_image(img_path)
        preds = model.predict(img_array)
        predicted_class = np.argmax(preds, axis=1)[0]
        max_prob = np.max(preds)

        # Print diagnostic information
        print(f'Image: {img_name}, Predicted Class Index: {predicted_class}, Max Probability: {max_prob}')

        # Move the images based on predicted class
        if predicted_class == 0:
            shutil.move(img_path, target_paths['Bacteria'])
        elif predicted_class == 1:
            shutil.move(img_path, target_paths['Normal'])
        elif predicted_class == 2:
            shutil.move(img_path, target_paths['Virus'])
