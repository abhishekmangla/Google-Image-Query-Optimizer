# Google-Image-Query-Optimizer

This program takes in 2 image queries. The first one is the baseline image query. The second one is a query which is used to compare the first 
one against. The difference between simply querying Google Images and using this program is this program uses structural similarity of 
images using image manipulation in SciKit to figure out the best IMAGE REPRESENTATION of your query compared to all the responses retrieved, while
Google Images uses PageRank or essentially popularity indexes to give you the most relevant images to your query. That is why this 
program is an optimized version of Google Image Querying.

## Getting Started

You can install the package with pip3 install google-image-query-optimizer. 
You might want to prepend sudo to that line. 
You can now run the script with "google-image-query-optimizer".

If you do not install using pip, you can also download this repo and do the following:
You might have to install the following:
pip3 install numpy
pip3 install Pillow
pip3 install -U scikit-image

To run: python3 genart.py
### Prerequisites

pip3 install numpy
pip3 install Pillow
pip3 install -U scikit-image


## Example

Enter Google Image Query (GIQ): Iron Man
Image Identifier (second GIQ): professional classy


## Built With

* [SciKit](http://www.dropwizard.io/1.0.2/docs/) - Structural similarity
* [Hardikvasa](https://github.com/hardikvasa/google-images-download/blob/master/google-images-download.py) - Downloading images from Google
* [PIL](https://rometools.github.io/rome/) - helps with dealing with images, opening them, resizing etc.

## Authors

* **Abhishek Mangla**



