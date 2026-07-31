import numpy as np

def adaboost_fit(X, y, n_clf):
	n_samples, n_features = np.shape(X)
	w = np.full(n_samples, (1 / n_samples))
	clfs = []

	# Your code here

	for _ in range(n_clf) :
		min_error = np.inf
		proper_feature = 0 
		best_threshold = 0 
		best_polarity = 0 
		best_predications = []
		
		for f in range(n_features) :
			iCol_values = X[: , f]
			unique_values = np.unique(iCol_values)
			threshold = unique_values
			# print(unique_values)
			# threshold = np.zeros(2 * len(unique_values) - 1)
			# for u in range(len(unique_values) - 1) : 
			# 	threshold[u] = unique_values[u]
			# for i in range(len(unique_values) - 1) : 
			# 	mean = (unique_values[i] + unique_values[i + 1])/2
			# 	threshold[i] = mean
			# print(threshold)
			for t in threshold:
				for polarity in [1,-1] : 
					predicated_output = np.ones(n_samples)
					if polarity == 1:
						for index,i in enumerate(iCol_values) :
							if i < t:
								predicated_output[index] = -1
					else : 
						for index,i in enumerate(iCol_values) :
							if i >= t:
								predicated_output[index] = -1

					differ_predications = np.zeros(len(y))
					for index,i in enumerate(predicated_output) :
						if i != y[index] :
							differ_predications[index] = False
						else :
							differ_predications[index] = True
					sum_errors = 0 
					for index,i in enumerate(differ_predications):
						if i == False :
							sum_errors += w[index]

					if sum_errors < min_error :
						min_error = sum_errors
						proper_feature = f
						best_threshold = t
						best_polarity = polarity
						best_predications = np.copy(predicated_output)

		if min_error == 0:
			min_error = 1e-10
		alpha = 0.5 * np.log((1-min_error) / min_error)
		
		clf = {'polarity': best_polarity, 'threshold': float(best_threshold), 'feature_index': int(proper_feature), 'alpha': float(alpha)}
		clfs.append(clf)
		w = w * np.exp(-alpha * y * best_predications)
		w = w / np.sum(w)
		

	return clfs



# X = np.array([[1, 2], [2, 3], [3, 4], [4, 5]])
# y = np.array([1, 1, -1, -1])
# n_clf = 3

# clfs = adaboost_fit(X, y, n_clf)
# print(clfs)