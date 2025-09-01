
# Using Adversarial Robustness Toolbox (ART) with PyTorch

## 1. Setup Workspace

```bash
cd ~/workspace
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
```

> The `packaging` library is required due to ART internals.

## 5. Example Code

Use `main.py` and adapt from the official [get\_started\_pytorch.py](https://github.com/Trusted-AI/adversarial-robustness-toolbox/blob/main/examples/get_started_pytorch.py):

```python
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

from art.estimators.classification import PyTorchClassifier
from art.attacks.evasion import FastGradientMethod

# Define simple CNN
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=5)
        self.fc1 = nn.Linear(1024, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = torch.relu(torch.max_pool2d(self.conv1(x), 2))
        x = torch.relu(torch.max_pool2d(self.conv2(x), 2))
        x = x.view(-1, 1024)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Load MNIST dataset
transform = transforms.Compose([transforms.ToTensor()])
trainset = torchvision.datasets.MNIST(root='./data', train=True,
                                      download=True, transform=transform)
testset = torchvision.datasets.MNIST(root='./data', train=False,
                                     download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=64,
                                          shuffle=True)
testloader = torch.utils.data.DataLoader(testset, batch_size=64,
                                         shuffle=False)

# Define loss and optimizer
model = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Wrap with ART classifier
classifier = PyTorchClassifier(
    model=model,
    clip_values=(0, 1),
    loss=criterion,
    optimizer=optimizer,
    input_shape=(1, 28, 28),
    nb_classes=10,
)

# Train the model
for epoch in range(1):
    for images, labels in trainloader:
        classifier.fit(images, labels, batch_size=64, nb_epochs=1)

# Evaluate benign accuracy
x_test, y_test = next(iter(testloader))
acc_benign = classifier.evaluate(x_test, y_test)[1]
print(f"Accuracy on benign test examples: {acc_benign * 100:.2f}%")

# Generate adversarial examples with FGSM
attack = FastGradientMethod(estimator=classifier, eps=0.2)
x_test_adv = attack.generate(x=x_test)

# Evaluate adversarial accuracy
acc_adv = classifier.evaluate(x_test_adv, y_test)[1]
print(f"Accuracy on adversarial test examples: {acc_adv * 100:.2f}%")
```

## 6. Run the Example

```bash
python main.py
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
