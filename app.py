# Importing Streamlit library
import streamlit as st
from streamlit_image_select import image_select

# Importing requests library and specifying model URL
import requests
# url = "http://localhost:3000/predict" #<-- uncomment this to run on localhost
url = "https://toxicity-predictor-3zykgobfea-uc.a.run.app/predict" # <-- uncomment this to run on cloud

# Querying dictionary format
query = {
  "pop": "BCG",
  "viewer": "snake",
  "background": "heli",
  "noise": "sp",
  "v_or_d": "d",
  "vs_lumin_cont": 1.484848,
  "vs_chrom_cont": 0.233671337,
  "vs_conspic": 0.8373917171,
  "vi_brightness": 3689.650359
}



# Title and basic info
st.title("Frog Toxicity Predictor")
st.markdown("In 2011, there was a study done on Strawberry Poison-dart frogs, _Oophaga pumilio_, which aimed to prove that the individual toxicity of these frogs can be estimated fairly by their colour and brightness. I used the data from that study to train a machine learning model which, given accurate measurements, provides an estimated toxicity prediction.")
st.write("Use this frontend to interact with the predictor model in real time. Choose the values and watch the prediction update live.")
st.info("_Tip! Click on the menu in the upper left corner, click on 'Settings', and activate 'Wide mode' for a better viewing experience._")
st.write("")

with st.expander("Learn more about the data inputs"):
    st.write("The data this model requires is a bit complicated, as it was initally recorded in carefully controlled scenarios. This model therefore only performs accurately when these laboratory conditions are emulated.")
    st.write("With the thresholds and options set within this web interface, the model performs fairly accurately. Below are descriptions of what each of the fields mean. Key features have been highlighted in red.")

    st.write("_Features have been classified as 'key features' if adjusting just that feature drastically changes the prediction. This does not mean it is has a very high correlation, nor that 'non-key features' are unimportant._")
    st.write("            ")

    st.warning("__Toxicity__: The estimated toxicity of a frog. This score is obtained by extensive mathematical calculations which have been detailed in the [study](https://www.journals.uchicago.edu/doi/10.1086/663197).")
    st.error("__Colour Morph__: These frogs occur in lots of different morphs with mostly distinct colours and patterns. Each variety has inherently different toxicity levels.")
    st.info("__Viewer__: This specifies which supposed predator is viewing the frog. Some of the data gathered in this study was processed to emulate the frog being viewed through the eyes of various predators. This was based on the hypothesis that brighter, more contrasting colours are more of a deterrent to predators than duller, muted ones. Specifying this minorly affects how important some features are to the final prediction.")
    st.info("__Background__: To prevent any of the data being skewed inaccurately by background reflectance, shadows, or any other background interference, all data was gathered with the frogs placed on one of three substrates. This also minorly affects how important some features are to the final prediction.")
    st.info("__Noise__: Most of the lighting data was filtered to some degree or another for background noise. This was filtered either at a mean constant or changed to match the species. Specifying which metric was used also minorly affects feature importance.")
    st.info("__Reflectance__: All the lighting measurements were taken either from the frogs back or frontal portion. To account for the differences in reflectance this may cause, this has been carefully recorded. This only minorly affects some feature's importance.")
    st.error("__Luminance contrast__: This is the contrast in the brightness, or luminance, of colours along a frog's back. This value is measured and then transformed such to be viewer specific.")
    st.error("__Colour contrast__: This is the spectral contrast, or contrast in the colours themselves, of the colours on a frog's back. This value is measured and then transformed such to be viewer specific.")
    st.error("__Conspicuousness__: This value is a measurement of a few different types of contrast and reflectance values, including both colour and luminance contrasts.")
    st.error("__Brightness__: This value is measured in a few different ways to obtain the general reflectance and brightness of a frog. This is processed to be viewer-independent.")

    st.write("The above is a simplification of what all the data values indicate to allow easy usage of this prediction tool. [The full study](https://www.journals.uchicago.edu/doi/10.1086/663197) contains a lot more information and detail if you're interested in learning more.")


# Specifying columns
col1, col2 = st.columns([2,2], gap='medium')

# Image selector to select colour morhps
with col1: 
    img = image_select(
    "Choose a colour morph",
    ["./st_images/aguacate.jpg",
    "./st_images/allobates.jpg",
    "./st_images/almirante.jpg",
    "./st_images/bastimentos_g.jpg",
    "./st_images/bastimentos_o.jpg",
    "./st_images/cayoagua.jpg",
    "./st_images/colon.jpg",
    "./st_images/cristobal.jpg",
    "./st_images/pastores.jpg",
    "./st_images/popa.jpg",
    "./st_images/solarte.jpg"
    ],

    captions=['Aguacate morph',
    'Allobates talamancae',
    'Almirante morph',
    'Bastimentos green morph',
    'Bastimentos orange morph',
    'Cayo Agua morph',
    'Colon morph',
    'Cristobal morph',
    'Pastores morph',
    'Popa morph',
    'Solarte morph']
    )

# Selector to set viewer
with st.sidebar: 
    viewer = st.selectbox(
        "Viewer",
        ('Frog', 'Bird', 'Crab', 'Snake')
    )
    st.write("         ")


# Selector to set background
with st.sidebar:
    bg = st.selectbox(
        'Background medium',
        ('Bark Litter', 'Lobster-claw Flowers', 'Leaf Litter')
    )
    st.write("         ")


# Radio buttons to choose noise specification
with st.sidebar:
    noise = st.radio(
        "Noise filtering metric",
        ['Constant', 'Species Specific']
    )
    st.write("         ")


# Radio button to specify reflectance value
with st.sidebar:
    vord = st.radio(
        "Reflectance",
        ['Ventral', 'Dorsal']
    )
    st.write("         ")


# Slider to specify float value for lumin_cont
with st.sidebar:
    lumin_cont = st.slider(
        "Luminance contrast",
        min_value=0.000000000,
        max_value=1.000000000
    )
    st.write("         ")


# Slider to specify float value for chrom_cont
with st.sidebar:
    chrom_cont = st.slider(
        "Colour contrast",
        min_value=0.000000000,
        max_value=1.000000000
    )
    st.write("         ")


# Slider to specify conspiciousness
with st.sidebar:
    conspic = st.slider(
        "Overall conspicuousness",
        min_value=0.000000000,
        max_value=1.000000000
    )
    st.write("         ")



with st.sidebar:
    bright = st.slider(
        "Total brightness",
        min_value=3000.000000000,
        max_value=17000.000000000
    )


frog_ids = {
    "./st_images/aguacate.jpg": "AG",
    "./st_images/allobates.jpg": "TALA",
    "./st_images/almirante.jpg": "AL",
    "./st_images/bastimentos_g.jpg": "BCG",
    "./st_images/bastimentos_o.jpg": "BCO",
    "./st_images/cayoagua.jpg": "CA",
    "./st_images/colon.jpg": "CO",
    "./st_images/cristobal.jpg": "SC",
    "./st_images/pastores.jpg": "SH",
    "./st_images/popa.jpg": "PoSo",
    "./st_images/solarte.jpg": "SO"
}

viewer_ids = {
    'Frog': 'pumilio',
    'Bird': 'bird',
    'Crab': 'crab',
    'Snake': 'snake'
}

bg_ids = {
    'Bark Litter': 'bark',
    'Lobster-claw Flowers': 'heli',
    'Leaf Litter': 'leaf'
}

noise_ids = {
    'Constant': 'fix', 
    'Species Specific': 'sp'
}

vord_ids = {
    'Ventral': 'v',
    'Dorsal': 'd'
}

query["pop"] = frog_ids[img]
query["viewer"] = viewer_ids[viewer]
query["background"] = bg_ids[bg]
query["noise"] = noise_ids[noise]
query["v_or_d"] = vord_ids[vord]
query["vs_lumin_cont"] = lumin_cont
query["vs_chrom_cont"] = chrom_cont
query["vs_conspic"] = conspic
query["vi_brightness"] = bright


response = requests.post(url, json=query).json()
# response = "placeholder"

with col2:
    st.header("Prediction:")
    st.info(response)



st.markdown("Photo credits to: [Arthur Anker](https://www.flickr.com/photos/artour_a), [Paul Bertner](https://rainforests.smugmug.com/), [Naska Photographie](https://www.instagram.com/naska_photographie/) and Wikimedia Commons.")