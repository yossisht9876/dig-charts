from flask import Flask, request, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from prometheus_client import generate_latest, CollectorRegistry, CONTENT_TYPE_LATEST, Gauge, Counter, Histogram

from torchvision import models, transforms
from torch.autograd import Variable
import torchvision.models as models
from PIL import Image

# All the 1000 imagenet classes
class_labels = 'imagenet_classes.json'

# Read the json
with open('imagenet_classes.json', 'r') as fr:
    json_classes = json.loads(fr.read())

app = Flask(__name__)

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total number of HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Duration of HTTP requests in seconds', ['method', 'endpoint'])
PREDICTION_COUNT = Counter('image_prediction_total', 'Total number of image predictions', ['label'])

# Allow CORS
CORS(app)

# Path for uploaded images
UPLOAD_FOLDER = 'data/uploads/'

# Allowed file extensions
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        REQUEST_COUNT.labels(method='POST', endpoint='/upload').inc()
        import time
        start_time = time.time()

        # Check if the post request has the file part
        if 'file' not in request.files:
            return "No file part"
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Send uploaded image for prediction
            predicted_image_class = predict_img(UPLOAD_FOLDER + filename)
            PREDICTION_COUNT.labels(label=predicted_image_class).inc()
            print("predicted_image_class", predicted_image_class)

            end_time = time.time()
            REQUEST_LATENCY.labels(method='POST', endpoint='/upload').observe(end_time - start_time)
            return json.dumps(predicted_image_class)
    return "Invalid request method"

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), content_type=CONTENT_TYPE_LATEST)

def predict_img(img_path):
    # Choose which model architecture to use from list above
    architecture = models.squeezenet1_0(pretrained=True)
    architecture.eval()

    # Normalization according to https://pytorch.org/docs/0.2.0/torchvision/transforms.html#torchvision.transforms.Normalize
    normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                     std=[0.229, 0.224, 0.225])
        
    # Preprocessing according to https://pytorch.org/tutorials/beginner/data_loading_tutorial.html
    preprocess = transforms.Compose([
       transforms.Resize(256),
       transforms.CenterCrop(224),
       transforms.ToTensor(),
       normalize
    ])

    # Path to uploaded image
    path_img = img_path

    # Read uploaded image
    read_img = Image.open(path_img)

    # Convert image to RGB if it is a .png
    if path_img.endswith('.png'):
        read_img = read_img.convert('RGB')

    img_tensor = preprocess(read_img)
    img_tensor.unsqueeze_(0)
    img_variable = Variable(img_tensor)

    # Predict the image
    outputs = architecture(img_variable)

    # Couple the ImageNet label to the predicted class
    labels = {int(key): value for (key, value) in json_classes.items()}
    predicted_label = labels[outputs.data.numpy().argmax()]
    print("\n Answer: ", predicted_label)

    return predicted_label

if __name__ == "__main__":
    app.run(debug=True, port=5000)

