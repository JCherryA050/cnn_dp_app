from keras.preprocessing.image import load_img
# Standard Imports
import numpy as np

# Importing all relevant packages for modeling in keras

from tensorflow.keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from tensorflow.keras.models import load_model
from PIL import Image

# Import packages for showing the performance metrics
from glob import glob
import cv2
import os

# Setting the random seed for reproducability
np.random.seed(123)

def getPrediction(filename):

    image = load_img('./static/uploads/'+filename)
    image_name = filename.replace('.png','')

    height_num = image.height/50
    width_num = image.width/50
    
    for i in range(0,int(height_num)):
        for j in range(0,int(width_num)):

            # Setting the points for cropped image
            left = 0 + 50*j
            top = 0 + 50*i
            right = 50 + 50*j
            bottom = 50 + 50*i

            # Cropped image of above dimension
            # (It will not change original image)
            im1 = image.crop((left, top, right, bottom))
            
            # Shows the image in image viewer
            # os.mkdir('./test/9037_split')
            im1.save('./split/'+image_name+'_'+str(right)+'_'+str(bottom)+'.png')

    data = glob('./split/*.png')
    model = load_model('./models/denseNet201.h5')

    def make_prediction(img_path,target_size):
        img = load_img(img_path,target_size=target_size)
        img_array = img_to_array(img)
        img_batch = np.expand_dims(img_array,axis=0)
        # img_preprocessed = preprocess_input(img_array)
        return float(model.predict(img_batch/255))
     
    predictions = []
    for path in data:
        predictions.append(make_prediction(path,(50,50)))
    predictions_array = np.array(predictions)
    normalized_predictions = (predictions_array - min(predictions_array))/(max(predictions_array) - min(predictions_array))
    # Separating file name from the path of the file
    files = []
    for datum in data:
            files.append(os.path.basename(datum))

    # removing the .png from the file names and isolating the x, y positions of the images
    x = []
    y = []
    for file in files:
        # isolating the x and y coordinates of the image and converting to int type
        x.append(int(file.split('_')[1]))
        y.append(int(file.split('_')[2].replace('.png','')))

    # Initialize the full image space
    full_slide = Image.new('RGB',(max(x)-min(x),max(y)-min(y)),color='#f2f2f5')
    count = 0
    for datum in data:
        # Isolate the file name
        file = os.path.basename(datum)

        # grab the location of the image from the file
        x = int(file.split('_')[1])
        y = int(file.split('_')[2].replace('.png',''))

        # Load the image in using the cv library
        img = Image.new('RGB',(50,50),color=(int(255*predictions_array[count]),int(255*predictions_array[count]),int(255*predictions_array[count])))
        
        # paste the image into the image space
    #     full_slide.paste(img,(x-51,y-51))
    #     # paste the image into the image space
        full_slide.paste(img,(x-50,y-50))
        count+=1
    
    image_file_name = 'new_image.png'
    smaller_map = full_slide.resize((400,400))
    smaller_image = image.resize((400,400))
    image_and_heatmap = Image.new('RGB',(800,400))
    image_and_heatmap.paste(smaller_map,(0,0))
    image_and_heatmap.paste(smaller_image,(400,0))
    image_and_heatmap.save('./static/uploads/new_image.png',)
    return image_file_name
