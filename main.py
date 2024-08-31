import dft

def main():
	num_samples = 1000
	signal = dft.Signal(num_samples, 1)
	signal.add_shift(0)
	signal.add_normal_noise(0, 1, 0.5)
	signal.add_signal(1, 3, 0)
	signal.add_signal(3, 8, 5)
	signal.DFT()
	signal.band_stop_filter(10, 500)
	signal.IDFT()
	signal.plot_samples()
	signal.plot_samples_IDFT_samples()


if __name__ == "__main__":
	main()