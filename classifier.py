# notebook: https://colab.research.google.com/drive/1t2rpYMVUTzW5-4u0DiEAvSPNm3AqHCzR?usp=sharing#scrollTo=i2VEZ0L7VHMT

import timm
import torch.nn as nn
import torch
import torchvision.transforms as T
from PIL import Image

# will's model-loading code
model = timm.create_model('efficientnet_b0', pretrained=True)
in_features = model.classifier.in_features
model.classifier = nn.Linear(in_features, 1)

# load device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# load weights
model.load_state_dict(torch.load('efficientnet_model_epoch_10.pt', map_location=device))
model = model.to(device)
model.eval()

# preprocessing transform (same as training)
desired_dim = 128
curr_dim = (1700, 2200)
transform_dim = (desired_dim, int(desired_dim / curr_dim[0] * curr_dim[1]))

transform = T.Compose([
    T.Resize(transform_dim),
    T.ToTensor(),
    T.Normalize(mean=[0.5], std=[0.5])
])

def classify(pages):
    with torch.no_grad():
        # preprocess all pages
        batch = torch.stack([transform(page) for page in pages]).to(device)
        
        # run inference
        outputs = model(batch)
        probs = torch.sigmoid(outputs)
        preds = (probs > 0.5).int().squeeze()
        
        # return as list of booleans
        return [bool(pred.item()) for pred in preds]
        