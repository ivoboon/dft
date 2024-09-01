import dft

def main():
		# Initialised the Signal class
		num_samples = 1000
		signal = dft.Signal(num_samples, 1)

		# Constructs a signal
		signal.add_shift(1)
		signal.add_normal_noise(0, 1, 0.5)
		signal.add_signal(1, 3, 0)
		signal.add_signal(3, 8, 5)

		# Performs DFT
		signal.DFT()

		# Applies a band-stop filter
		signal.band_stop_filter(10, 500)

		# Performs IDFT
		signal.IDFT()

		# Plots results
		signal.plot_combined_samples()


if __name__ == "__main__":
	main()