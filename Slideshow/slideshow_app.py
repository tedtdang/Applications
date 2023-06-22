import cv2
from pathlib import Path as p
import streamlit as st
import time

# Set up Streamlit app
st.set_page_config(page_title='Slideshow')

# Set up slideshow
image_files = list(p.cwd().glob('Images/*.[jp][pn]g'))
num_images = len(image_files)
current_image_index = 0

# Create sidebar for user input
with st.sidebar:
    # Add slider for image selection
    image_index = st.slider('Select an image:', 1, num_images, value=current_image_index+1)

    # Check if user has selected a new image
    if image_index != current_image_index+1:
        current_image_index = image_index-1

    # Add checkbox to toggle slideshow
    slideshow_enabled = st.checkbox('Toggle slideshow', value=True)

# Create main screen for displaying images
main_screen = st.empty()

# Loop over images
while True:
    if slideshow_enabled:
        # Load current image and display it on the main screen
        image = cv2.imread(str(image_files[current_image_index]))
        main_screen.image(image, channels='BGR')

        # Update current image index
        current_image_index = (current_image_index + 1) % num_images

        # Wait for 2 seconds before loading next image
        time.sleep(5)
    else:
        # Load selected image and display it on the main screen
        image = cv2.imread(str(image_files[current_image_index]))
        main_screen.image(image, channels='BGR')

        # Break out of loop
        break