import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
import tensorflow as tf
import seaborn as sns
sns.set()
# define a function to calculate the KL divergence of two probability  
#  don’t include any probabilities equal to 0 because the log of 0 is negative infinity.
def kl_divergence(p, q):
    return np.sum(np.where(p != 0, p * np.log(p / q), 0))
  
# KL divergence between a normal distribution with a
#  mean of 0 and a standard deviation of 2 
# and another one with a mean of 2 and  a standard deviation of 2
# is equal to 500.
x = np.arange(-10, 10, 0.001)
p = norm.pdf(x, 0, 2)
q = norm.pdf(x, 2, 2)
plt.title('KL(P||Q) = %1.3f' % kl_divergence(p, q))
plt.plot(x, p)
plt.plot(x, q, c='red')

# If we measure the KL divergence between the initial probability distribution and another distribution with a mean of 5 and 
# a standard deviation of 4, 
# we expect the KL divergence to be higher than in the previous example.
q = norm.pdf(x, 5, 4)
plt.title('KL(P||Q) = %1.3f' % kl_divergence(p, q))
plt.plot(x, p)
plt.plot(x, q, c='red')
# KL divergence is not symmetrical.  if we switch P for Q and vice versa, we get a different result.

# To begin, we create a probability distribution with a known mean (0) and variance (2). 
# Then, we create another distribution with random parameters.
x = np.arange(-10, 10, 0.001)
p_pdf = norm.pdf(x, 0, 2).reshape(1, -1)
np.random.seed(0)
random_mean = np.random.randint(10, size=1)
random_sigma = np.random.randint(10, size=1)
random_pdf = norm.pdf(x, random_mean, random_sigma).reshape(1, -1)

# Since gradient descent, we need to select values for the hyperparameters (i.e. step size, number of iterations).
learning_rate = 0.001
epochs = 100

p = tf.placeholder(tf.float64, shape=pdf.shape)
mu = tf.Variable(np.zeros(1))
sigma = tf.Variable(np.eye(1))
normal = tf.exp(-tf.square(x - mu) / (2 * sigma))
q = normal / tf.reduce_sum(normal)

kl_divergence = tf.reduce_sum(
    tf.where(p == 0, tf.zeros(pdf.shape, tf.float64), p * tf.log(p / q))
)

optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(kl_divergence)
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    
    history = []
    means = []
    variances = []
    
    for i in range(epochs):
        sess.run(optimizer, { p: pdf })
        
        if i % 10 == 0:
            history.append(sess.run(kl_divergence, { p: pdf }))
            means.append(sess.run(mu)[0])
            variances.append(sess.run(sigma)[0][0])
    
    for mean, variance in zip(means, variances):
        q_pdf = norm.pdf(x, mean, np.sqrt(variance))
        plt.plot(x, q_pdf.reshape(-1, 1), c='red')
    plt.title('KL(P||Q) = %1.3f' % history[-1])
    plt.plot(x, p_pdf.reshape(-1, 1), linewidth=3)
    plt.show()
    
    plt.plot(history)
    plt.show()
    
    sess.close()