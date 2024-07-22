from keras.models import load_model 
import os

def get_model1():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'resnet50_3_class_modelv3.h5')
    return load_model(model_path)

def get_model2():
    model_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'resnet50_3_class_modelCovid.h5')
    return load_model(model_path)