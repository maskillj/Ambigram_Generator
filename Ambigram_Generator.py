import tensorflow as tf
import tensorflow_datasets as tfds
import os
import time
import matplotlib.pyplot as plt
from IPython.display import clear_output
from tensorflow_examples.models.pix2pix import pix2pix
import matplotlib.pyplot as plt

dataset_directory = 'Image Dataset'  
batch_size = 32  
image_size = (256,256)  
dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_directory,
    shuffle=True,
    batch_size=batch_size,
    image_size=image_size
)
dataset_directory = 'Inverted Images Dataset'  
batch_size = 32
image_size = (256,256)  
rotated_dataset = tf.keras.preprocessing.image_dataset_from_directory(
    dataset_directory,
    shuffle=True,
    batch_size=batch_size,
    image_size=image_size
)
AUTOTUNE = tf.data.AUTOTUNE

def normalize(image):
    img = tf.cast(img, dtype=tf.float32)
    return (img / 127.5) - 1.0
def preprocess_image(image):
    image = normalize(image)
    return image

BUFFER_SIZE = 64
BATCH_SIZE = 32
IMG_WIDTH = 256
IMG_HEIGHT = 256
OUTPUT_CHANNELS = 3

def filter_batch_size(batch, batch_size=32):
    return tf.shape(batch)[0] == batch_size
filtered_dataset = dataset.filter(lambda x, y: filter_batch_size(x, batch_size=32))
filtered_rotated_dataset = rotated_dataset.filter(lambda x, y: filter_batch_size(x, batch_size=32))
generator_g = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')
generator_f = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')

discriminator_x = pix2pix.discriminator(norm_type='instancenorm', target=False)
discriminator_y = pix2pix.discriminator(norm_type='instancenorm', target=False)

example = next(iter(dataset))

def preprocess_image(image, label):
    image = tf.cast(image, tf.float32)
    return image, label

dataset = dataset.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
rotated_dataset = rotated_dataset.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
generator_g = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')
generator_f = pix2pix.unet_generator(OUTPUT_CHANNELS, norm_type='instancenorm')

for batch in dataset:
    upright_images = batch[0]
    upright_images = tf.squeeze(upright_images)
    print("Shape after squeeze:", upright_images.shape)
    if upright_images.shape[-1] == 3:
        to_flipped = generator_g(upright_images)
    else:
        print("Incorrect image shape")

for batch in rotated_dataset:
    rotated_images = batch[0]
    rotated_images = tf.squeeze(rotated_images)
    print("Shape after squeeze:", rotated_images.shape)
    if rotated_images.shape[-1] == 3:
        to_upright = generator_f(rotated_images)
    else:
        print("Incorrect image shape")

LAMBDA = 10
loss_obj = tf.keras.losses.BinaryCrossentropy(from_logits=True)
def discriminator_loss(real, generated):
    real_loss = loss_obj(tf.ones_like(real), real)
    generated_loss = loss_obj(tf.zeros_like(generated), generated)
    total_disc_loss = real_loss + generated_loss
    return total_disc_loss * 0.5
def generator_loss(generated):
    return loss_obj(tf.ones_like(generated), generated)
def calc_cycle_loss(real_image, cycled_image):
    loss1 = tf.reduce_mean(tf.abs(real_image - cycled_image))
    return LAMBDA * loss1
def identity_loss(real_image, same_image):
    loss = tf.reduce_mean(tf.abs(real_image - same_image))
    return LAMBDA * 0.1 * loss
generator_g_optimizer = tf.keras.optimizers.legacy.Adam(2e-4, beta_1=0.5)
generator_f_optimizer = tf.keras.optimizers.legacy.Adam(2e-4, beta_1=0.5)

discriminator_x_optimizer = tf.keras.optimizers.legacy.Adam(2e-4, beta_1=0.5)
discriminator_y_optimizer = tf.keras.optimizers.legacy.Adam(2e-4, beta_1=0.5)

checkpoint_path = "./checkpoints/train"

ckpt = tf.train.Checkpoint(generator_g=generator_g,
                           generator_f=generator_f,
                           discriminator_x=discriminator_x,
                           discriminator_y=discriminator_y,
                           generator_g_optimizer=generator_g_optimizer,
                           generator_f_optimizer=generator_f_optimizer,
                           discriminator_x_optimizer=discriminator_x_optimizer,
                           discriminator_y_optimizer=discriminator_y_optimizer)

ckpt_manager = tf.train.CheckpointManager(ckpt, checkpoint_path, max_to_keep=5)
if ckpt_manager.latest_checkpoint:
    ckpt.restore(ckpt_manager.latest_checkpoint)
    print ('Latest checkpoint restored!!')
EPOCHS = 50
def generate_images(model, test_input):
    prediction = model(test_input[0])
    plt.figure(figsize=(12, 12))
    display_list = [test_input[0], prediction[0]]
    title = ['Input Image', 'Predicted Image']
    for i in range(2):
        plt.subplot(1, 2, i+1)
        plt.title(title[i])
        plt.imshow(display_list[i] * 0.5 + 0.5)
        plt.axis('off')
        plt.show()

@tf.function
def train_step(real_x, real_y):
    with tf.GradientTape(persistent=True) as tape:

        fake_y = generator_g(real_x, training=True)
        cycled_x = generator_f(fake_y, training=True)

        fake_x = generator_f(real_y, training=True)
        cycled_y = generator_g(fake_x, training=True)

        same_x = generator_f(real_x, training=True)
        same_y = generator_g(real_y, training=True)

        disc_real_x = discriminator_x(real_x, training=True)
        disc_real_y = discriminator_y(real_y, training=True)

        disc_fake_x = discriminator_x(fake_x, training=True)
        disc_fake_y = discriminator_y(fake_y, training=True)

        gen_g_loss = generator_loss(disc_fake_y)
        gen_f_loss = generator_loss(disc_fake_x)

        total_cycle_loss = calc_cycle_loss(real_x, cycled_x) + calc_cycle_loss(real_y, cycled_y)

        total_gen_g_loss = gen_g_loss + total_cycle_loss + identity_loss(real_y, same_y)
        total_gen_f_loss = gen_f_loss + total_cycle_loss + identity_loss(real_x, same_x)

        disc_x_loss = discriminator_loss(disc_real_x, disc_fake_x)
        disc_y_loss = discriminator_loss(disc_real_y, disc_fake_y)

    generator_g_gradients = tape.gradient(total_gen_g_loss, 
                                        generator_g.trainable_variables)
    generator_f_gradients = tape.gradient(total_gen_f_loss, 
                                        generator_f.trainable_variables)

    discriminator_x_gradients = tape.gradient(disc_x_loss, 
                                            discriminator_x.trainable_variables)
    discriminator_y_gradients = tape.gradient(disc_y_loss, 
                                            discriminator_y.trainable_variables)

    generator_g_optimizer.apply_gradients(zip(generator_g_gradients, 
                                            generator_g.trainable_variables))

    generator_f_optimizer.apply_gradients(zip(generator_f_gradients, 
                                            generator_f.trainable_variables))

    discriminator_x_optimizer.apply_gradients(zip(discriminator_x_gradients,
                                                discriminator_x.trainable_variables))

    discriminator_y_optimizer.apply_gradients(zip(discriminator_y_gradients,
                                                discriminator_y.trainable_variables))

for epoch in range(EPOCHS):
    start = time.time()
    n = 0
    for image_x, image_y in zip(dataset, rotated_dataset):
        train_step(image_x[0], image_y[0])
        if n % 10 == 0:
            print('.', end='')
        n += 1
    clear_output(wait=True)
    if (epoch + 1) % 5 == 0:
        ckpt_save_path = ckpt_manager.save()
        print('Saving checkpoint for epoch {} at {}'.format(epoch+1, ckpt_save_path))
    print('Time taken for epoch {} is {} sec\n'.format(epoch + 1, time.time()-start))

def generate_images(model, test_input):
    input_data = test_input[0]
    predictions = model(input_data, training=False)

    if input_data.ndim == 4:
        batch_size = input_data.shape[0]
    else:
        raise ValueError(f"Unexpected shape of input_data: {input_data.shape}")

    for i in range(batch_size):
        plt.figure(figsize=(10, 10))

        input_image = input_data[i].numpy() if hasattr(input_data[i], 'numpy') else input_data[i]
        predicted_image = predictions[i].numpy() if hasattr(predictions[i], 'numpy') else predictions[i]

        if input_image.ndim != 3 or input_image.shape[-1] != 3:
            raise ValueError(f"Input image shape {input_image.shape} is not valid for display")

        if predicted_image.ndim != 3 or predicted_image.shape[-1] != 3:
            raise ValueError(f"Predicted image shape {predicted_image.shape} is not valid for display")

        for j, image in enumerate([input_image, predicted_image]):
            plt.subplot(1, 2, j+1)
            plt.title(['Input Image', 'Predicted Image'][j])
            plt.imshow(image * 0.5 + 0.5)
            plt.axis('off')

        plt.show()