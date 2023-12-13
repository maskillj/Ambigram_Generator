# Ambigram Generator

## What is an Ambigram?
An ambigram is a word, number, or other figure that looks the same or can still be read when viewed (or rotated) upside down [source: https://www.dictionary.com/e/pop-culture/ambigram/]

## About the Project
This project uses a Cycle-GAN (Generative Adversarial Network) to produce ambigrams based on custom-generated datasets. Generation of the datasets for training the Cycle-GAN is undertaken by the **gen_ambigram_training** function as defined in **Data_Generator.py**. The model's architecture and training is given in **Ambigram_Generator.py**.
This implementation follows that described on the TensorFlow website: https://www.tensorflow.org/tutorials/generative/cyclegan. Notable changes pertain to the preprocessing of images of the words, an increased number of training epochs, and a reduction in the important of identity loss in the training loop.

## How to Use
### Step 1: Download the fonts listed in Fonts 1.zip and Fonts 2.zip
These are used to generate the dataset for each of the words in the ambigram.
### Step 2: Run the gen_ambigram_training function with your desired words
This function takes two string arguments for each orientation of the ambigram. For instance, to generate the ambigram of John and Mary, run gen_ambigram_training('John".'Mary')
### Step 3: Run the Ambigram_Generator.py
This file both constructs and traings the Cycle-GAN based on the chosen ambigram words. Please note that some edits may be needed to the location of the dataset images based on your own internal folder system, and that dataset_directory expects the name of a parent folder containing the folder holding the images, not the folder holding the images itself.
Training using the implementation rovided is very slow. For this reason, running Ambigram_Generator.py on GPUs and/or over a Virtual Machine is strongly recommended. 
### Step 4: Generate ambigrams
Ambigrams can be generated corresponding to each of the fonts in the training data. They can be generated using the **generate_images** function, as below:

```python 
for inp in dataset.take(5):
    generate_images(generator_f, inp)
```
