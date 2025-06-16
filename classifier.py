# notebook: https://colab.research.google.com/drive/1t2rpYMVUTzW5-4u0DiEAvSPNm3AqHCzR?usp=sharing#scrollTo=i2VEZ0L7VHMT

import timm
import torch.nn as nn
import torch

# will's model-loading code
model = timm.create_model('efficientnet_b0', pretrained=True)
in_features = model.classifier.in_features
model.classifier = nn.Linear(in_features, 1)

# load weights

# load device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)