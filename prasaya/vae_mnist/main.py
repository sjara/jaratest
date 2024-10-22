import os
import torch
from config import device, plot_dir, num_interpolation_pairs
from model import VAE
from data_loader import get_data_loaders
from train import train
from visualize import save_reconstructed_images, save_latent_space_plot, generate_interpolations, interpolate_specific_digits

def main():
    # Create plot directory if it doesn't exist
    os.makedirs(plot_dir, exist_ok=True)

    # Get data loaders
    train_loader, test_loader, test_dataset = get_data_loaders()

    # Initialize and train the model
    model = VAE().to(device)
    trained_model = train(model, train_loader)

    # Save reconstructed images
    save_reconstructed_images(trained_model, test_loader)

    # Save latent space plot
    save_latent_space_plot(trained_model, test_loader)

    # Generate and save interpolations
    generate_interpolations(trained_model, test_dataset, num_interpolation_pairs)

    interpolate_specific_digits(trained_model, test_dataset, digit1=8, digit2=4)

    print(f"All plots have been saved in the '{plot_dir}' directory.")

if __name__ == "__main__":
    main()