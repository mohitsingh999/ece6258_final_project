from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import pickle as pkl
from time import sleep

import os
region = os.environ['ACCOUNT_REGION']
key = os.environ['ACCOUNT_KEY']

credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(
    endpoint='https://image-recognition-6258-project.cognitiveservices.azure.com/',
    credentials=credentials
)

dirpath = "results/nlm_cureor_block_smoothless/"
result_file = os.path.join(dirpath, "rekognition_results.txt")
for dirname in ["03_underexposure_extrema/", "04_overexposure_extrema/", "05_blur_extrema/", "06_contrast_extrema/", "07_dirtylens1_extrema/", "08_dirtylens2_extrema/"]:
    challenge_dirpath = os.path.join(dirpath, dirname)
    for file in os.listdir(challenge_dirpath):
        image_path = os.path.join(challenge_dirpath, file)
        image_relpath = os.path.join(dirname, file)

        # Specify the features you want to extract
        features = [VisualFeatureTypes.objects]

        # Call the API to analyze the image
        with open(image_path, "rb") as image_stream:
            try:
                results = client.analyze_image_in_stream(image_stream, visual_features=features)
            except:
                print("Waiting a minute")
                sleep(60)  # Rate limit

        # Extract object recognition results
        if "objects" in dir(results):
            objects = results.objects
            result_string = " ".join([f"{obj.confidence} {obj.object_property}" for obj in objects])
            for obj in objects:
                print(f"Object: {obj.object_property} with confidence {obj.confidence * 100}%")

        with open(result_file, "a") as f:
            f.write(f"{image_relpath} {result_string}\r\n")
