# Reconstructing MNIST dataset using VAE

## How to run the code
- Install torch, tqdm, matplotlib
- Check `config.py` to update parameters and output path
- Run: `python main.py`
- Generates plots for:
    - latent space 
    - interpolation between 8 and 4
    - comparison between reconstructed image and image in testing dataset


## List of Files

- config.py -> Configuration file that user changeable hyperparameters and output directory
- data-loader.py -> Function to getch training and test data from MNIST dataset in torchvision
- main.py -> Run this file to run the project and control the training and evaluation flow
- train.py -> Use to run the training loop
- model.py -> Define the architecture of the VAE model
- visualize.py -> Functions to generate scatter plots and interpolations 


