import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def add_layer(inputs, in_size, out_size, n_layer, activation_function=None):
    layer_name = 'layer%s' % n_layer
    with tf.name_scope('layer'):
        with tf.name_scope('weights'):
            weights = tf.Variable(tf.random_normal([in_size, out_size]), name='w')
            # 在layer中爲weights和biases設置變化圖表
            tf.summary.histogram(layer_name + '/weights', weights)

        with tf.name_scope('biases'):
            biases = tf.Variable(tf.random_normal([1, out_size]), name='b')
            # 在layer中爲weights和biases設置變化圖表
            tf.summary.histogram(layer_name + '/biases', biases)

        with tf.name_scope('wx_plus_b'):
            wx_plus_b = tf.add(tf.matmul(inputs, weights), biases)

        if activation_function is None:
            outputs = wx_plus_b
        else:
            outputs = activation_function(wx_plus_b)

            # 在layer中爲weights和biases設置變化圖表
            tf.summary.histogram(layer_name + '/outputs', outputs)

        return outputs

x_data = np.linspace(-1, 1, 300, dtype=np.float32)[:, np.newaxis]
noise = np.random.normal(0, 0.05, x_data.shape).astype(np.float32)
y_data = np.square(x_data) - 0.5 + noise

with tf.name_scope('inputs'):
    xs = tf.placeholder(tf.float32, [None, 1], name='x_in')
    ys = tf.placeholder(tf.float32, [None, 1], name='y_in')

# add hiden layer
l1 = add_layer(xs, 1, 10, n_layer=1, activation_function=tf.nn.relu)
# add output layer
prediction = add_layer(l1, 10, 1, n_layer=12, activation_function=None)
with tf.name_scope('loss'):
    loss = tf.reduce_mean(tf.reduce_sum(tf.square(ys - prediction), reduction_indices=[1]))
    # 設置loss的變化圖
    tf.summary.histogram('loss', loss)
with tf.name_scope('train'):
    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(loss)

init = tf.global_variables_initializer()
sess = tf.Session()

# 給所有訓練圖合並
merged = tf.summary.merge_all()
writer = tf.summary.FileWriter('logs/', sess.graph)
sess.run(init)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.scatter(x_data, y_data)
plt.ion()
plt.show()

for i in range(1000):
    sess.run(train_step, feed_dict={xs: x_data, ys: y_data})
    if i % 50 == 0:
        rs = sess.run(merged, feed_dict={xs: x_data, ys: y_data})
        writer.add_summary(rs, i)
        try:
            ax.lines.remove(lines[0])
        except Exception:
            pass
        prediction_value = sess.run(prediction, feed_dict={xs: x_data})
        lines = ax.plot(x_data, prediction_value, 'r-', lw=5)
        plt.pause(0.1)
        # print(sess.run(loss, feed_dict={xs:x_data, ys:y_data}))
