from neupy import algorithms, layers
import numpy as np
from neupy import environment
from sklearn.gaussian_process import GaussianProcess
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

f = open('pair_k_results', 'r')
index = 0
parameters = []
scores = []
for line in f:
    pair = line.split()
    parameters.append(int(pair[0]))
    scores.append(int(pair[1]))
    index = index + 1
f.close()
    

environment.reproducible()


def vector_2d(array):
    return np.array(array).reshape((-1, 1))

def gaussian_process(x_train, y_train, x_test):
    x_train = vector_2d(x_train)
    y_train = vector_2d(y_train)
    x_test = vector_2d(x_test)

    # Train gaussian process
    gp = GaussianProcess(corr='squared_exponential', theta0=1e-1, thetaL=1e-3, thetaU=1)

    # noise = 0.1
    # rbf = ConstantKernel(1.0) * RBF(length_scale=1.0)
    # gp = GaussianProcessRegressor(kernel=rbf, alpha=noise**2)

    gp.fit(x_train, y_train)

    # Get mean and standard deviation for each possible number of hidden units
    # y_mean, y_std = gp.predict(x_test, return_std=True)
    # y_std = vector_2d(y_std)

    y_mean, y_var = gp.predict(x_test, eval_MSE=True)
    y_std = np.sqrt(vector_2d(y_var))
    
    return y_mean, y_std

def next_parameter_by_ei(y_min, y_mean, y_std, x_choices):
    # Calculate expecte improvement from 95% confidence interval
    expected_improvement = y_min - (y_mean - 1.96 * y_std)
    expected_improvement[expected_improvement < 0] = 0

    max_index = expected_improvement.argmax()
    # Select next choice
    next_parameter = x_choices[max_index]

    return next_parameter


def hyperparam_selection(k_range, n_iter=49):
    # To be able to perform gaussian process we need to have at least 2 samples.
    if index == 0:
        f = open("kvalue","w+")
        f.write("%d\r\n", 5)
        f.close()
        return
    if index == 1:
        f = open("kvalue","w+")
        f.write("%d\r\n", 10)
        f.close()
        return

    min_k_range, max_k_range = k_range
    k_range_choices = np.arange(min_k_range, max_k_range + 1)

    y_min = min(scores)
    y_mean, y_std = gaussian_process(parameters, scores, k_range_choices)

    k_next = next_parameter_by_ei(y_min, y_mean, y_std, k_range_choices)

    if k_next in parameters:
        k_optimal = np.argmin(scores)
        print("Found optimal k value:%d", k_optimal) 
        f = open("koptimal","w+")
        f.write("%d\r\n", min_score_index)
        f.close()
    else:
        print "k_next: %d" % k_next
        f = open("kvalue","w+")
        f.write("%d\r\n", k_next)
        f.close()
        return
    
hyperparam_selection(
    k_range=[2, 50],
    n_iter=49,
)