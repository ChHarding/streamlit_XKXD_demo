import streamlit as st
import requests
import bs4
import random
import plotly.graph_objects as go

# streamlit run streamlit_app_example2.py


# same function for fetching a URL as in the previous example
def get_xkcd_image_URL(n):   
    ''' return url to image of comics number n (int)'''
    url = 'http://xkcd.com' # base url
    n_str = str(n)
    url += f"/{n_str}/" # full comic page URL

    # Download the page.
    res = requests.get(url)
    res.raise_for_status() # will stop if request did not get code 200 (e.g. if it got 404)

    # Use BSoup to find the URL of the comic image.
    soup = bs4.BeautifulSoup(res.text,  "html.parser")  
    comicElem = soup.select('#comic img') # grab the img tag inside the id=comic div
    if comicElem == []:
        print('Could not find comic image.')
        return None
    else:
        imgURL = "http:" + comicElem[0].get('src') # get the link URL
        return imgURL

# Set the page configuration to wide mode
st.set_page_config(layout="wide")

# Streamlit app
st.title("XKCD Image Viewer") # web page title


# Sidebar for slider and button
with st.sidebar:
    # Slider to select the number of images
    # slider value is returned and stored in the variable num_images
    num_images = st.slider("How many XKCD images?", min_value=1, max_value=10, value=1)

    # Button to show images
    show_images = st.button("Show images")

    
# This will show in the main window!
if show_images:
    # with creates a context manager that will automatically close the spinner when the block of code is done
    bar = st.progress(0, "Scraping ...")
    with bar:
        image_urls = []
        for i in range(num_images):
            random_comic_number = random.randint(0, 2000)
            img_url = get_xkcd_image_URL(random_comic_number)
            if img_url is not None:
                image_urls.append(img_url)
            else:
                st.write(f"Could not find image for comic number {random_comic_number}.")
            bar.progress((i+1) * 1/num_images, # bar value in 0.0 to 1.10 
                         f"{i+1} of {num_images}") 
        bar.empty() # removes bar


    # with the spinner closed, create a container
    with st.container(height=800):
        for img_url in image_urls:
            st.image(img_url)