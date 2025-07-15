import matplotlib.pyplot as plt

def show_noise_map(noise):
    plt.imshow(noise, cmap='Greys')
    plt.title("Noise Map")
    plt.axis('off')
    plt.show()