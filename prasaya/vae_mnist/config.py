import torch

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyperparameters
latent_size = 2
batch_size = 128
num_epochs = 2
learning_rate = 1e-3

# Visualization
interpolation_steps = 10
num_interpolation_pairs = 5

# Paths
data_dir = '/tmp/data_mnist'
plot_dir = '/tmp/vae_plots_mnist'