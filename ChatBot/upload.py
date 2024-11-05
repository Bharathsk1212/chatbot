# upload.py
import requests
from PIL import Image
import torch
from torchvision import models, transforms
import wikipedia
import json

# Load the pre-trained ResNet model from PyTorch (ResNet18)
resnet_model = models.resnet18(pretrained=True)
resnet_model.eval()  # Set the model to evaluation mode

# Define the image transformation pipeline
image_transform = transforms.Compose([
    transforms.Resize(256),          # Resize the image to 256x256 pixels
    transforms.CenterCrop(224),      # Crop the center 224x224 pixels
    transforms.ToTensor(),           # Convert the image to a PyTorch tensor
    transforms.Normalize(            # Normalize the tensor
        mean=[0.485, 0.456, 0.406],  # These are the ImageNet means
        std=[0.229, 0.224, 0.225]    # These are the ImageNet standard deviations
    )
])

# Load ImageNet class labels
def load_imagenet_labels():
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    response = requests.get(url)
    return json.loads(response.text)

class_labels = load_imagenet_labels()  # Load class labels

# Function to classify an uploaded image
def classify_image(uploaded_file):
    try:
        # Open the image file
        img = Image.open(uploaded_file)

        # Apply the transformation to the image
        img_tensor = image_transform(img)

        # Add a batch dimension (as the model expects a batch of inputs)
        img_tensor = img_tensor.unsqueeze(0)

        # Perform inference (i.e., classification)
        with torch.no_grad():
            outputs = resnet_model(img_tensor)

        # Get the predicted class index (highest score)
        _, predicted_idx = outputs.max(1)

        # Return the human-readable class label
        return class_labels[predicted_idx.item()]

    except Exception as e:
        return f"Error in image classification: {str(e)}"

# Function to search for information on Wikipedia based on the label
def search_wikipedia(label):
    try:
        # Get a summary of the label from Wikipedia
        # return wikipedia.summary(label, sentences=2)
        return f""
    except Exception as e:
        return f"No additional information found for {label}."
