import math
import matplotlib.pyplot as plt
import random

class Signal():
	"""
	A class that represents a signal, on which you can perform DFT, IDFT, and band-stop filter
	"""

	def __init__(self, num_samples: int, duration: float) -> None:
		"""
		Initialises the class with the number of samples and the number of signals based on Nyquist limit.
		Initialises the samples array with zeroes.
		Initialises the duration, and makes a time array based on the dt.
		Initialises flags that determine whether or not a certain function has run already.
		"""
		self.num_samples = num_samples
		self.num_signals = self.num_samples // 2 + 1
		self.samples = [0] * num_samples
		self.duration = duration
		self.time = []
		for n in range(num_samples):
			self.time.append(n * self.duration / self.num_samples)
		self.DFT_flag = False
		self.IDFT_flag = False
	

	def add_signal(self, amp: float, freq: float, phase: float) -> None:
		"""
		Adds a sinusoidal signal to the samples.
		"""
		for n in range(self.num_samples):
			self.samples[n] += amp * math.sin(2 * math.pi * freq * self.time[n] + phase)


	def add_shift(self, shift: float) -> None:
		"""
		Adds a shift to the samples.
		"""
		for n in range(self.num_samples):
			self.samples[n] += shift


	def add_normal_noise(self, mu: float, sigma: float, amplitude: float) -> None:
		"""
		Adds random normal noise to the samples.
		"""
		for n in range(self.num_samples):
			self.samples[n] += amplitude * random.gauss(mu, sigma)


	def DFT(self) -> None:
		"""
		Perform the discrete Fourier transform on the samples.
		It computes the real and imaginary parts, and normalises them.
		The normalised values are used to compute the magnitude and phase of the different frequencies.
		Finally, it sets the DFT flag.
		"""
		self.real = []
		self.imag = []
		self.real_norm = []
		self.imag_norm = []
		self.mag = []
		self.phase = []
		for k in range(self.num_signals):
			real_k = 0
			imag_k = 0
			for n in range(self.num_samples):
				real_k += self.samples[n] * math.cos(2 * math.pi * k * n / self.num_samples)
				imag_k -= self.samples[n] * math.sin(2 * math.pi * k * n / self.num_samples)
			self.real.append(real_k)
			self.imag.append(imag_k)
			real_norm_k = real_k * 2 / self.num_samples
			imag_norm_k = imag_k * 2 / self.num_samples
			self.real_norm.append(real_norm_k)
			self.imag_norm.append(imag_norm_k)
			mag_k = math.sqrt(real_norm_k ** 2 + imag_norm_k ** 2)
			phase_k = math.atan2(imag_norm_k, real_norm_k)
			self.mag.append(mag_k)
			self.phase.append(phase_k)
		
		self.real_norm[0] /= 2
		self.real_norm[-1] /= 2
		self.mag[0] = math.sqrt(self.real_norm[0] ** 2 + self.imag_norm[0] ** 2)
		self.mag[-1] = math.sqrt(self.real_norm[-1] ** 2 + self.imag_norm[-1] ** 2)
		self.phase[0] = math.atan2(self.imag_norm[0], self.real_norm[0])
		self.phase[-1] = math.atan2(self.imag_norm[-1], self.real_norm[-1])

		self.DFT_flag = True
	
	
	def IDFT(self) -> None:
		"""
		This function will only run if the DFT flag has been set.
		Performs the inverse Discrete Fourier Transform on the signal.
		It uses the computed magnitudes and phases to reconstruct the original signal.
		Finally, it sets the IDFT flag.
		"""
		if self.DFT_flag:
			self.IDFT_samples = []
			for n in range(self.num_samples):
				IDFT_n = 0
				for k in range(self.num_signals):
					IDFT_n += self.mag[k] * math.cos(2 * math.pi * k * n / self.num_samples + self.phase[k])
				self.IDFT_samples.append(IDFT_n)
			
			self.IDFT_flag = True
		else:
			print('DFT not executed')

	
	def band_stop_filter(self, lower_limit: int, upper_limit: int) -> None:
		"""
		This function will only run if the DFT flag has been set.
		Performs a band-stop filter on the magnitudes of the frequencies based on a lower limit and an upper limit.
		"""
		if self.DFT_flag:
			if (
				lower_limit <= upper_limit
				and 0 <= lower_limit < self.num_signals
				and 0 <= upper_limit < self.num_signals
			):
				self.mag[lower_limit:upper_limit + 1] = [0] * (1 + upper_limit - lower_limit)
			else:
				print('Incorrect frequency limits')
		else:
			print('DFT not executed')


	def plot_samples(self) -> None:
		"""
		Plots the samples of the original signal.
		"""
		plt.plot(self.time, self.samples)
		plt.show()


	def plot_freq(self) -> None:
		"""
		This function will only run if the DFT flag has been set.
		Plots the magnitudes of the different frequencies.
		"""
		if self.DFT_flag:
			plt.plot(list(range(self.num_signals)), self.mag)
			plt.show()
		else:
			print('DFT not executed')


	def plot_IDFT_samples(self) -> None:
		"""
		This function will only run if the DFT flag has been set.
		Plots the samples of the inverse Fourier transform.
		"""
		if self.IDFT_flag:
			plt.plot(self.time, self.IDFT_samples)
			plt.show()
		else:
			print('IDFT not executed')


	def plot_samples_IDFT_samples(self) -> None:
		"""
		This function will only run if the IDFT flag has been set.
		Plots a combination of the original samples and the samples of the inverse Fourier transform.
		"""
		if self.IDFT_flag:
			plt.plot(self.time, self.samples)
			plt.plot(self.time, self.IDFT_samples)
			plt.show()
		else:
			print('IDFT not executed')