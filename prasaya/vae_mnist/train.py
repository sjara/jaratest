import torch
from tqdm import tqdm
from config import device, num_epochs, learning_rate
from model import VAE, loss_function

def train_vae(model, train_loader, optimizer):
    model.train()
    train_loss = 0
    for images, _ in tqdm(train_loader, desc="Training"):
        images = images.to(device)

        reconstructed, mu, logvar = model(images)
        loss = loss_function(reconstructed, images, mu, logvar)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()

    return train_loss / len(train_loader.dataset)

def train(model, train_loader):
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(num_epochs):
        avg_loss = train_vae(model, train_loader, optimizer)
        print(f'Epoch [{epoch+1}/{num_epochs}], Average loss: {avg_loss:.4f}')

    return model