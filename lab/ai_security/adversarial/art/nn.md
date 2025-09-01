
# Using Adversarial Robustness Toolbox (ART) with PyTorch

## 1. Setup Workspace

```bash
mkdir ~/workspace/art1
mkdir art1
cd art1
```

## 2. Create a Virtual Environment

Using **uv** (a modern Python package/dependency manager):

```bash
uv venv .venv
source .venv/bin/activate
```

> Activates a clean Python 3.12 virtual environment inside `.venv`.

## 3. Initialize Project

```bash
uv init
```

This creates:

* `pyproject.toml` → project config
* `uv.lock` → lock file
* `README.md` & `main.py`

## 4. Install Dependencies

Install ART and required libraries:

```bash
uv add adversarial-robustness-toolbox
uv add torch
uv add packaging
uv add torchvision
```

> The `packaging` library is required due to ART internals.

## 5. Example Code

Use `main.py` and adapt from the official [get\_started\_pytorch.py](https://github.com/Trusted-AI/adversarial-robustness-toolbox/blob/main/examples/get_started_pytorch.py):

```python
"""
The script demonstrates a simple example of using ART with PyTorch. The example train a small model on the MNIST dataset
and creates adversarial examples using the Fast Gradient Sign Method. Here we use the ART classifier to train the model,
it would also be possible to provide a pretrained model to the ART classifier.
The parameters are chosen for reduced computational requirements of the script and not optimised for accuracy.
"""

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import PyTorchClassifier
from art.utils import load_mnist


# Step 0: Define the neural network model, return logits instead of activation in forward method


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv_1 = nn.Conv2d(in_channels=1, out_channels=4, kernel_size=5, stride=1)
        self.conv_2 = nn.Conv2d(in_channels=4, out_channels=10, kernel_size=5, stride=1)
        self.fc_1 = nn.Linear(in_features=4 * 4 * 10, out_features=100)
        self.fc_2 = nn.Linear(in_features=100, out_features=10)

    def forward(self, x):
        x = F.relu(self.conv_1(x))
        x = F.max_pool2d(x, 2, 2)
        x = F.relu(self.conv_2(x))
        x = F.max_pool2d(x, 2, 2)
        x = x.view(-1, 4 * 4 * 10)
        x = F.relu(self.fc_1(x))
        x = self.fc_2(x)
        return x


# Step 1: Load the MNIST dataset

(x_train, y_train), (x_test, y_test), min_pixel_value, max_pixel_value = load_mnist()

# Step 1a: Swap axes to PyTorch's NCHW format

x_train = np.transpose(x_train, (0, 3, 1, 2)).astype(np.float32)
x_test = np.transpose(x_test, (0, 3, 1, 2)).astype(np.float32)

# Step 2: Create the model

model = Net()

# Step 2a: Define the loss function and the optimizer

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Step 3: Create the ART classifier

classifier = PyTorchClassifier(
    model=model,
    clip_values=(min_pixel_value, max_pixel_value),
    loss=criterion,
    optimizer=optimizer,
    input_shape=(1, 28, 28),
    nb_classes=10,
)

# Step 4: Train the ART classifier

classifier.fit(x_train, y_train, batch_size=64, nb_epochs=3)

# Step 5: Evaluate the ART classifier on benign test examples

predictions = classifier.predict(x_test)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on benign test examples: {}%".format(accuracy * 100))

# Step 6: Generate adversarial test examples
attack = FastGradientMethod(estimator=classifier, eps=0.2)
x_test_adv = attack.generate(x=x_test)

# Step 7: Evaluate the ART classifier on adversarial test examples

predictions = classifier.predict(x_test_adv)
accuracy = np.sum(np.argmax(predictions, axis=1) == np.argmax(y_test, axis=1)) / len(y_test)
print("Accuracy on adversarial test examples: {}%".format(accuracy * 100))
```

## 6. Run the Example

```bash
python fgsm.py
```

✅ Expected output (similar to your run):

```
Accuracy on benign test examples: ~97%
Accuracy on adversarial test examples: ~39%
```

---

⚡ **Tip:** You can try different attacks (e.g., `ProjectedGradientDescent`, `CarliniL2Method`) by replacing `FastGradientMethod`.


# **FastGradientMethod - Fast Gradient Sign Method (FGSM)**

### The Big Idea: The "Wrong Way" on a Map

Imagine you have a machine learning model that's very good at identifying images. You can think of its understanding as a landscape with hills and valleys.

  * **A Valley** represents a **correct classification** with high confidence (low error/loss). For example, when you give it a picture of a cat, you land deep in the "cat" valley.
  * **A Hill** represents a boundary between classifications. The peak of the hill is where the model is most confused.
  * **The Goal:** We want to take our image that's deep in the "cat" valley and push it just over the nearest hill into, say, the "dog" valley, with the *least possible effort*.

FGSM finds the *fastest* way to go uphill (i.e., increase the model's error) and takes one big step in that direction.
