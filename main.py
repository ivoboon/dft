import dft

def main():
	# Initialises the Signal class
	num_samples = 1000
	signal = dft.Signal(num_samples, 1)

	# Constructs a signal with a shift
	signal.add_shift(1)
	signal.add_normal_noise(0, 1, 0.5)
	signal.add_signal(1, 3, 0)
	signal.add_signal(3, 8, 5)

	# Performs the discrete Fourier transform
	signal.DFT()

	# Shows the different frequencies
	signal.plot_freq()

	# Applies a band-stop filter on the random noise above our highest main frequency
	signal.band_stop_filter(10, 500)

	# Shows the new frequencies
	signal.plot_freq()

	# Performs the inverse discrete Fourier transform and plots the original signal combined with the attenuated signal
	signal.IDFT()
	signal.plot_samples_IDFT_samples()


if __name__ == "__main__":
	main()