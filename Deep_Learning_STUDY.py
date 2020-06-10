import numpy as np
import torch

'''
x_data = [1.0, 2.0, 3.0]
y_data = [2.0, 4.0, 6.0]

w1 = 1.0
w2 = 1.0
b = 1.0

def forward(x):
    return x*x*w2 + x*w1 + b


def loss(x, y):
    y_pred = forward(x)
    return (y_pred - y) * (y_pred - y)

def gradient1(x, y):
    return 2 * x * ( x*x*w2 + w1 + b - y )

def gradient2(x, y):
    return 2 * x * x * ( x*x*w2 + w1 + b - y )

print("predict (Before training)", 4, forward(4))

for epoch in range(300):
    for x_val, y_val in zip(x_data, y_data):
        grad1 = gradient1(x_val, y_val)
        grad2 = gradient2(x_val, y_val)
        w1 = w1 - 0.01 * grad1
        w2 = w2 - 0.01 * grad2

        print("\tgrad: ", x_val, y_val, grad1, grad2)
        l = loss (x_val, y_val)
    print("progress: ", epoch+1, "trials", "w1=", w1, "w2=", w2, "loss=", l)
print("predic (after training)", "4 hours", forward(4))
'''

t = np.array([0., 1., 2., 3., 4., 5., 6.])
print(t)

print('Rank  of t: ', t.ndim)
print('Shape of t: ', t.shape)
