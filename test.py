import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from flask import Flask, request, jsonify

# Step 1: Data Collection
# Example: Load a dataset from a CSV file
data = pd.read_csv('sustainability_data.csv')

# Step 2: Data Preprocessing
# Handle missing values
data = data.dropna()

# Normalize the data
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# Split the data
X = data_scaled[:, :-1]  # Features
y = data_scaled[:, -1]   # Target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 3: Model Building with PyTorch
class SustainabilityModel(nn.Module):
    def __init__(self):
        super(SustainabilityModel, self).__init__()
        self.fc1 = nn.Linear(X_train.shape[1], 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

model = SustainabilityModel()

# Loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Training loop
num_epochs = 100
loss_values = []
for epoch in range(num_epochs):
    model.train()
    inputs = torch.tensor(X_train, dtype=torch.float32)
    targets = torch.tensor(y_train, dtype=torch.float32).view(-1, 1)
    
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()
    
    loss_values.append(loss.item())
    if (epoch+1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

# Evaluation
model.eval()
with torch.no_grad():
    inputs = torch.tensor(X_test, dtype=torch.float32)
    targets = torch.tensor(y_test, dtype=torch.float32).view(-1, 1)
    outputs = model(inputs)
    test_loss = criterion(outputs, targets)
    print(f'Test Loss: {test_loss.item():.4f}')

# Step 4: Visualization
# Plot the training loss
plt.figure(figsize=(10, 5))
plt.plot(range(num_epochs), loss_values)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

# Example: Visualize the predictions vs. actual values
plt.figure(figsize=(10, 5))
plt.scatter(y_test, outputs.numpy())
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Predictions vs. Actual Values')
plt.show()

# Step 5: Deployment on PythonAnywhere using Flask
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    inputs = torch.tensor(data['inputs'], dtype=torch.float32)
    with torch.no_grad():
        outputs = model(inputs)
    return jsonify({'prediction': outputs.numpy().tolist()})

if __name__ == '__main__':
    app.run()
