from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import pickle as pkl

import os
region = os.environ['ACCOUNT_REGION']
key = os.environ['ACCOUNT_KEY']

credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(
    endpoint='https://image-recognition-6258-project.cognitiveservices.azure.com/',
    credentials=credentials
)

# image_path = "../../images/cure-or-guassian-blur/01950.jpg"
image_path = "../../images/cure-or-nochallenge-3d1-iphone/4_1_5_066_01_0.jpg"

# Specify the features you want to extract
features = [VisualFeatureTypes.objects]

# Call the API to analyze the image
with open(image_path, "rb") as image_stream:
    results = client.analyze_image_in_stream(image_stream, visual_features=features)

# Extract object recognition results
if "objects" in dir(results):
    objects = results.objects
    for obj in objects:
        print(f"Object: {obj.object_property} with confidence {obj.confidence * 100}%")

# Save results
with open("./data/results.pkl", "wb") as f:
    pkl.dump(results, f)
