import matplotlib.pyplot as plt
import torch
import os
from config import device, latent_size, plot_dir, interpolation_steps

def save_reconstructed_images(model, test_loader):
    model.eval()
    with torch.no_grad():
        for images, _ in test_loader:
            images = images.to(device)
            reconstructed, _, _ = model(images)
            break

    fig, axes = plt.subplots(4, 4, figsize=(15, 15))
    for i in range(4):
        for j in range(2):
            idx = i * 2 + j
            # Original image
            axes[i, j*2].imshow(images[idx].cpu().squeeze(), cmap='gray')
            axes[i, j*2].axis('off')
            axes[i, j*2].set_title('Original')
            # Reconstructed image
            axes[i, j*2+1].imshow(reconstructed[idx].cpu().view(28, 28), cmap='gray')
            axes[i, j*2+1].axis('off')
            axes[i, j*2+1].set_title('Reconstructed')

    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'reconstructed_images.png'))
    plt.close()

def save_latent_space_plot(model, test_loader):
    model.eval()
    with torch.no_grad():
        all_mu = []
        all_labels = []
        for images, labels in test_loader:
            images = images.to(device)
            _, mu, _ = model(images)
            all_mu.append(mu.cpu())
            all_labels.append(labels)

        all_mu = torch.cat(all_mu, dim=0)
        all_labels = torch.cat(all_labels, dim=0)

    plt.figure(figsize=(10, 10))
    for label in range(10):
        mask = all_labels == label
        plt.scatter(all_mu[mask, 0], all_mu[mask, 1], label=str(label))
    plt.legend()
    plt.title('MNIST Digits in Latent Space')
    plt.savefig(os.path.join(plot_dir, 'latent_space.png'))
    plt.close()

def interpolate_images(model, img1, img2, steps=interpolation_steps):
    model.eval()
    with torch.no_grad():
        # Encode images
        img1 = img1.unsqueeze(0).to(device)
        img2 = img2.unsqueeze(0).to(device)
        z1, _ = model.encoder(img1.view(1, -1)).split(latent_size, dim=1)
        z2, _ = model.encoder(img2.view(1, -1)).split(latent_size, dim=1)
        
        # Interpolate in latent space
        alphas = torch.linspace(0, 1, steps)
        z_interp = torch.zeros(steps, latent_size)
        for i, alpha in enumerate(alphas):
            z_interp[i] = alpha * z2 + (1 - alpha) * z1
        
        # Decode interpolated latent vectors
        interpolated_imgs = model.decoder(z_interp.to(device)).cpu()
        
    return interpolated_imgs, z_interp, z1.cpu(), z2.cpu()

def plot_interpolation(original1, original2, interpolated, z_interp, z1, z2, index):
    n = len(interpolated)
    fig = plt.figure(figsize=(20, 10))
    
    # Create grid spec for layout
    gs = fig.add_gridspec(3, n)
    
    # Plot original images
    ax_orig1 = fig.add_subplot(gs[0, 0])
    ax_orig1.imshow(original1.squeeze(), cmap='gray')
    ax_orig1.set_title('Original 1')
    ax_orig1.axis('off')
    
    ax_orig2 = fig.add_subplot(gs[0, -1])
    ax_orig2.imshow(original2.squeeze(), cmap='gray')
    ax_orig2.set_title('Original 2')
    ax_orig2.axis('off')
    
    # Plot interpolated images
    for i in range(n):
        ax = fig.add_subplot(gs[1, i])
        ax.imshow(interpolated[i].view(28, 28), cmap='gray')
        ax.set_title(f'α={i/(n-1):.2f}')
        ax.axis('off')
    
    # Plot latent space
    ax_latent = fig.add_subplot(gs[2, :])
    ax_latent.scatter(z_interp[:, 0], z_interp[:, 1], c='b', alpha=0.5)
    ax_latent.scatter(z1[:, 0], z1[:, 1], c='r', s=100, label='Original 1')
    ax_latent.scatter(z2[:, 0], z2[:, 1], c='g', s=100, label='Original 2')
    
    # Add latent vector values as annotations
    for i, (x, y) in enumerate(z_interp):
        ax_latent.annotate(f'({x:.2f}, {y:.2f})', (x, y), xytext=(5, 5), 
                           textcoords='offset points', fontsize=8, alpha=0.7)
    
    ax_latent.annotate(f'({z1[0, 0]:.2f}, {z1[0, 1]:.2f})', (z1[0, 0], z1[0, 1]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=10, color='r')
    ax_latent.annotate(f'({z2[0, 0]:.2f}, {z2[0, 1]:.2f})', (z2[0, 0], z2[0, 1]), 
                       xytext=(5, 5), textcoords='offset points', fontsize=10, color='g')
    
    ax_latent.set_title('Latent Space Interpolation')
    ax_latent.legend()
    ax_latent.set_xlabel('Latent Dimension 1')
    ax_latent.set_ylabel('Latent Dimension 2')
    
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f'interpolation_{index}.png'), dpi=300, bbox_inches='tight')
    plt.close()

def generate_interpolations(model, dataset, num_pairs):
    for i in range(num_pairs):
        img1, _ = dataset[i*2]
        img2, _ = dataset[i*2+1]
        interpolated_imgs, z_interp, z1, z2 = interpolate_images(model, img1, img2)
        plot_interpolation(img1, img2, interpolated_imgs, z_interp, z1, z2, i)


def interpolate_specific_digits(model, dataset, digit1, digit2, steps=interpolation_steps):
    # Filter the dataset to get the specified digits
    indices1 = [i for i, (_, label) in enumerate(dataset) if label == digit1]
    indices2 = [i for i, (_, label) in enumerate(dataset) if label == digit2]

    if not indices1 or not indices2:
        print(f"Digits {digit1} or {digit2} not found in the dataset.")
        return

    # Take one sample from each digit class
    img1, _ = dataset[indices1[0]]
    img2, _ = dataset[indices2[0]]

    # Perform interpolation
    interpolated_imgs, z_interp, z1, z2 = interpolate_images(model, img1, img2)
    
    # Plot the interpolation
    plot_interpolation(img1, img2, interpolated_imgs, z_interp, z1, z2, f"{digit1}_{digit2}")