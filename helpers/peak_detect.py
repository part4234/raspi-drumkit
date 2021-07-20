# Smoothed z-score algorithm
# Ref: https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data
# Implementation: https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data/56451135#56451135

import numpy as np


class PeakDetect():
	def __init__(self, lag, threshold, influence):
		print(f'[PeakDetect] lag {lag}')
		print(f'[PeakDetect] threshold {threshold}')
		print(f'[PeakDetect] influence {influence}')

		self.y = []
		self.length = 0
		self.lag = lag
		self.threshold = threshold
		self.influence = influence
		self.signals = []
		self.filteredY = []
		self.avgFilter = []
		self.stdFilter = []

		self.strengths = []
		self.maxStrength = 0

	def thresholding_algo(self, new_value):
		self.y.append(new_value)
		self.length = len(self.y)

		# handle lag
		i = len(self.y) - 1
		if i < self.lag:
			return (0, 0)
		elif i == self.lag:
			self.signals = [0] * len(self.y)
			self.filteredY = np.array(self.y).tolist()
			self.avgFilter = [0] * len(self.y)
			self.stdFilter = [0] * len(self.y)
			self.avgFilter[self.lag - 1] = np.mean(self.y[0:self.lag]).tolist()
			self.stdFilter[self.lag - 1] = np.std(self.y[0:self.lag]).tolist()
			self.strengths = [0] * len(self.y)
			return (0, 0)

		# add new entry
		self.signals += [0]
		self.filteredY += [0]
		self.avgFilter += [0]
		self.stdFilter += [0]
		self.strengths += [0]

		if abs(self.y[i] - self.avgFilter[i - 1]) > self.threshold * self.stdFilter[i - 1]:
			if self.y[i] > self.avgFilter[i - 1]:
				self.signals[i] = 1
				# update max strength
				self.maxStrength = max(self.y[i], self.maxStrength)
			else:
				self.signals[i] = -1

			self.filteredY[i] = self.influence * self.y[i] + (1 - self.influence) * self.filteredY[i - 1]
			self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
			self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])
		else:
			self.signals[i] = 0
			self.filteredY[i] = self.y[i]
			self.avgFilter[i] = np.mean(self.filteredY[(i - self.lag):i])
			self.stdFilter[i] = np.std(self.filteredY[(i - self.lag):i])
			# update strength
			if self.signals[i-1] == 1:
				self.strengths[i] = self.maxStrength
				self.maxStrength = 0

		return (self.signals[i], self.strengths[i])
