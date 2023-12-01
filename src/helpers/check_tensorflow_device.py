import tensorflow as tf

[print (device) for device in tf.config.list_physical_devices()]

print (f'Has GPU? {len(tf.config.list_physical_devices("GPU")) > 0}')
