# Introducion

Midterm project I built for the Machine Learning Zoomcamp by Alexey Grigorev. Learn more about the free bootcamp by following any of the links below. 

- https://mlzoomcamp.com
- https://github.com/alexeygrigorev/mlbookcamp-code/tree/master/course-zoomcamp

For this midterm, we were required to pick out a dataset of our choosing, and then make and train a ML model using it. We were also required to deploy it either to a cloud service or to our local systems.

I also built an independent frontend app using Streamlit that can be used to query the model in a fun, intuitive way without the hassle of running Python scripts over and over again. 

## About the project

In 2011, a research was published in The American Naturalist, detailing how the colour and brightness of a certain species of Poison Frog are indicators for their toxicity levels. 

Poisonous or toxic organisms often present bold colourations and flashy patterns instead of subdued tones that would promote camouflage. This might seem disandvantageous at first, as such organisms are more likely to be noticed by whatever species predate them. However, this is actually a defense mechanism - the bold colours serve as an advertisement for their toxicity, shouting out "Do not eat me!" to any potential predators. Thus even when noticed, predators will move past them as they have learnt that the bright colours and loud patterns mean the prey is unsuitable for consumption. 

There have been theories in the past of how the colour of the frog may relate to its toxicity. A lot of these were disproved, with evidence to the contrary having also been found. This study focused on the inherent reflectance of the frog's colour, independent of who the viewer was, in relation to its toxicity levels. By this new metric, and with a wider range of colour morphs, the study found a strong correlation between the conspiciousness of a frog and its toxicity level. 

This project hopes to build a model that will be able to predict the toxicity of the poison frog based on its colours and brightness alone. 

## Dataset Information

The data I use throughout this project was sourced from [Google's Dataset search](https://datasetsearch.research.google.com/). It is available for download from several websites. The version I used is from [Zenodo](https://zenodo.org/record/5010072#.Y2bE9HbP1D_). There may be minor differences in data from other websites. 

The [research](https://www.journals.uchicago.edu/doi/10.1086/663197) that uses and explains this data was published in [The American Naturalist](https://www.journals.uchicago.edu/toc/an/current) Volume 179, in January of 2012. 

There is no need to download the data to run this repository as the data files have been supplied in the [data folder](/tree/main/data).

## Ready-to-use cloud deploy

Below there is a complete guide to installing and running both the ML Model and the Streamlit app locally. However, if you'd like to check out the final product first, this Streamlit app is connected to the cloud deployed model.

__insert linkhere__

## Files & Folders

There are mutliple files and folders provided in the main repository. Below, I organise them loosely, but each of the files and their purpose has been explained extensively in the appropriate sections. 

1. Setup
    - `requirements.txt` - for setting up the virtual environment. 
    - `data` folder - contains the main working data file.
2. EDA & Model Experimentation
    - `notebook.ipynb` - main working notebook, containing EDA, feature analysis, model training and tuning, and finalising a best model. 
3. Model Training & Saving
    - `train.py` - isolated Python script to train the best model and save it as a BentoML model. 
4. Serving Model
    - `predict.py` - Python script that loads up and serves the model after saving it.
    - `bentofile.yaml` - Bentofile provided to build the BentoML package.
5. Getting Results from Model
    - `app.py` - Streamlit app for deploying a front-end service that makes requests to served model. 
    - `request.py` - isolated Python script that can make requests to model through the command line. 

## My work explained

The working notebook `notebook.ipynb` contains everything that was done to obtain the model, from EDA to final model. Here's a summary of it all.

- Basic data setup
    
    The data provided was organised for use in research and was not the most intuitive to work with. I renamed the columns according to the guide provided with the data. This [guide](/tree/main/data/README_for_Data_MaanCummings_2011_ AmNat52931_ByInd.txt) is committed along with the data in the `data` folder. 

- Basic data analysis

    I performed basic EDA to check for missing data and duplicate values, and to learn more about the different features.

- Data correction

    EDA revealed an abnormally large amount of missing data in some of the columns - up to 93% of that column contained `NaN` values. These three features were dropped. The rest of the data had a smattering of missing values - these were filled in with zeros. Lastly, EDA revealed several rows which were exact duplicates - these were dropped. 

- Further data analysis

    After doing the data correction, I split the data into train/validation/test sets, with a 80/10/10 ratio. Then I used the Pandas Profiler library to get a more in-depth look at all of the data. This allowed me to look at different metrics, correlation graphs, scatter plots, and more for different features just by changing values on a HTML interface.

- Baseline model

    After this I was ready to train my first model. There were two columns that contained normalised values of the other data columns. These were dropped as they would not realistically be available to a model in production. Once that was done, I trained a baseline model with LinearRegression.

    The model (and all subsequent models until the very end) was trained on the training dataset and tested against the validation dataset. The metric of scoring used was `RMSE`.

- Experiments

    I conducted some experiments to try and improve the models performance. I tried dropping features which EDA indicated to have lower correlation, and tried some scaling with the numerical data. The best performance out of these was by using Standard Scaling and by dropping no features. 

- Decision tree model

    Next I trained a decision tree model with default parameters and data. This was used as a baseline for the decision tree models. Then I performed the same experiments as with the Linear Regression model, and found that no method of scaling nor dropping any features could improve the baseline. 

    After that I hyper-tuned the models parameters with GridSearch CV. 

- XGBoost model

    Lastly I trained a XGBoost model on default parameters and data. This baseline was stored as well, and already performed better than previous models. I then conducted some experiments to refine this model, both using the previous experiments and some new ones tailered to XGBoost. Lastly, I set up a GridSearch that exhaustively tunes multiple XGBoost parameters. 

    ___This is a time consuming and resource heavy process. If you do decide to run the notebook at any point, it might be better to skip the section which is performing this tuning.___

    After GridSearch returned optimal parameters, some further digging had to be done to choose parameters that were not overfitted. After I did that I checked these parameters against validation data one last time, obtaining the lowest RMSE score so far at 0.018. This was chosen as the final model. 

- Training the final model

    Now that the best performing model had been selected, I trained it one last time, but this time on the combined train and validation data and scored it against the test data - hitherto untouched. This model was then saved using BentoML. 

    ___In the notebook, you will notice the code for saving the model is commented out. This is because we will use `train.py` to train and save the model instead.___

## Setup Prerequisites

All of the setup instructions below assume you have a working Python install ready. It also assumes you have Docker installed. 

If you do not have any of these, please follow the respective guides to install and set them up before following any steps below. 

- [Python Installation](https://docs.python.org/3/using/index.html)
- [Docker Installation](https://docs.docker.com/engine/install/)
- [Setting up Docker and Windows Linux Subsystem - For Windows Users](https://andrewlock.net/installing-docker-desktop-for-windows/)

## Setting up local environment

__Any code instructions listed throughout this guide are for a Windows system. Where possible, links to tutorials detailing the same or similar steps in other OS have been provided.__

To run this repository on your local system, you will need to setup a Python virtual environment. I use the built-in Python `venv` for this. [Python documentation](https://docs.python.org/3/library/venv.html) has an extensive guide on creating these environments. 

1. Create a new folder and navigate to it. 

2. Create a virtual environment. 
    ```
    python -m venv /path/to/venv/directory
    ```

3. Activate the new virtual environment.
    
    ```
    .\Scripts\Activate.ps1
    ```
    Make sure you are in the virtual environment directory before running this command.

4. Clone the project repository.

    ```
    git clone https://github.com/AaishaMuhammad/mlzoomcamp_midterm

    ```

After ensuring you are navigated to the directory containing all the files,

7. Install all required packages.
    
    ```
    pip install -r requirements.txt
    ```

<br>

## Training & deploying the model

Make sure you have followed all the previous steps before attempting these. You will need to be in the activated virtual environment and have all dependencies installed for this part to work. 

1. Run the training script.

    ```
    python train.py
    ```

2. Build a Bento with BentoML.

    ```
    bentoml build
    ```

This part may take some time to run. After it has finished,

3. Containerize the Bento.

    ```
    bentoml containerize toxicity_predictor:latest
    ```

This step may also take some time to finish. Wait for it to finish before progressing further. 

4. Run the docker container.
    
    After the previous command finished, you will notice at the end it outputs a unique code, something similar to `toxicity_predictor:xiizeo24z6nb43cl`. Replace the 'unique key' in the below command with the portion after 'toxicity_prediction:' that your system generated. This key generated is unique to every time `bentoml containerize` is run and cannot be generalised in any way. 

    ```
    docker run -it --rm -p 3000:3000 toxicity_predictor:'unique-key' serve --production
    ```

    Alternatively, the `bentoml containerize`, upon finishing, will display a Docker run command that should be identical to the one above. You can copy and run that command instead if it is identical. 

Congratulations! The toxicity predictor model is now up and running on your local system.

## Running Streamlit front-end

Make sure you've followed all the previous steps and the the predictor service is up and running before attempting to launch the front-end service. 

1. Configure Streamlit

    - Navigate to `app.py` and launch it in your code editor. 
    - Comment out the current URL definition - this one queries the active Cloud deploy of the model. 
    - Uncomment the fist URL definition - this will make the app query your version of the model running on `localhost`. 

<br>

2. Launch Streamlit.

    ```
    streamlit run app.py
    ```

And that's it! The app is fully configured and will launch in your web browser immediately. It refreshes live as you change the inputs and will immediately deliver a fresh prediction. 

## Testing model manually

If (for some absurd reason :D) you do not want to interactively use the service through the Streamlit app, you can also use it via a provided requests script. 

1. Customise request.

    Open the `request.py` file in your code editor. You will notice four dictionaries already defined. These are to make it easier to test the model. Change these values as desired and then save the file. 

<br>

__NOTE: Due to the specific nature of the data used in training this model, it performs accurately only if the data is within specific bounds. Below is the acceptable range of values.__

- `'pop'`: `'AG'`, `'TALA'`, `'AL'`, `'BCG'`, `'BCO'`, `'CA'`, `'CO'`, `'SC'`, `'SH'`, `'PoSo'`, '`SO'`

- `'viewer'`: `'pumilio'`, `'bird'`, `'crab'`, `'snake'`

- `'background'`: `'bark'`, `'heli'`, `'leaf'`

- `'noise'`: `'sp'`, `'fix'`

- `'v_or_d'`: `'v'`, `'d'`

- `'vs_lumin_cont'`: Float value between `0` and `1.0`

- `'vs_chrom_cont'`: Float value between `0` and `1.0`

- `'vs_conspic'`: Float value between `0` and `1.0`

- `'vi_brightness'`: Float value between `3000.0` and `17000.0`

2. Configure request.
    
    At the top of the file there are two URL defintions. Comment out the cloud deploy definition and uncomment the local deploy one. 

    The script will now query your model running on `localhost`.

3. Run request.

    ```
    python request.py
    ```

And that is it! The output will be printed onto the terminal. 

<br>

## Deploying model to the cloud

In a real-world production scenario, we will have to deploy the model to some cloud service to allow it to be queried from external services. Right now, we can only query it from another app running either on our local system or at least on the same network. Once it is deployed to the cloud, external apps can also access it - like my Streamlit app can query my model deployed on Google Cloud. 

This guide will take you over the steps required to deploy to Google Cloud Run. Before following these steps, make sure you have an active Google Cloud account. You will need to have activated and verified Billing Options as well. 

This will also require an active installation of Gcloud CLI. A detailed guide on installing and running this can be found on [Google Documentation](https://cloud.google.com/sdk/docs/install). 

__None of the steps followed here will incur a charge on their own, and billing options merely require activation for verification purposes. Ensure you deactivate unnecessary processes to prevent accidental billing.__

0. Prerequisites

    Before attempting any of the steps below, make sure you have finished all the previous steps and have a ready Docker container. If your container is currently running on the local system, you may deactivate it - it is not needed for this section. 

    To check if your Docker container is ready, run:

    ```
    docker images
    ```

    You should see a docker image similar to `toxicity_detector:'unique-tag'` in the list. 

1. Create a project in Google Cloud.

    Start by navigating to the [Google Cloud console](https://console.cloud.google.com/projectselector2/home/dashboard) and creating a new project. Make sure billing options are activated for this project. 

2. Enable Artifact Registry.

    We need the artifact registry to get our Docker container over to Google Cloud Run. Enable the API by following [this link](https://console.cloud.google.com/apis/enableflow?apiid=artifactregistry.googleapis.com) and completing the steps. 

_The user may require special permissions to run Docker. If at any point you run into permission issues, try again from an administrative user._

3. Create artifact repository.

    Navigate to the Artifact Registry and open the Repositories page. 

    Create a new repository and name it `'toxicity-predictor'`. Make sure you have the format configured to `'Docker'` and choose a region. I used `'us-central1'` for my deploy. 

4. Set up Docker authentication.

    You need to configure Docker to use Google Cloud to authenticate requests when pushing or pulling Docker images. Run the following command in your terminal to update the Docker configuration:

    ```
    gcloud auth configure-docker us-central1-docker.pkg.dev
    ```

    If you used another region and not 'us-central1', change that part of the command to match your region.

5. Tag Docker image.

    Before we can push the Docker image, we need to tag it so we can push it to a specific location:

    ```
    docker tag toxicity_predictor:'your_unique_tag'  us-central1-docker.pkg.dev/'your_project_id'/toxicity-predictor/toxicity_predictor:latest
    ```
    
    Use the above command after changing `'your_unique_tag'` to the tag shown when you ran `'docker images'`. Also change `'your_project_id'` to whatever ID you specified when creating your Google Cloud project. 

    If you used another region and not 'us-central1', change that part of the command to match your region. 

6. Push the Docker image.

    Now we can push our Docker image onto the Artifact Registry. Run:

    ```
    docker push us-central1-docker.pkg.dev/'your_project_id'/toxicity-predictor/toxicity_predictor:latest
    ```

    Making sure to replace `'your_project_id'` with your project ID, and also the region if 'us-central1' was not used. 

_If you would like a more in-depth reading about the above, or need to find help for a different OS, consult [these docs](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)._

<br>

Now that we have pushed the Docker image onto Artifact Registry, it is available for us to use in a Cloud Run project. 

7. Create Google Cloud Run service.

    Navigate to the Google Cloud Run [dashboard](https://console.cloud.google.com/run). Click on __Create Service__. 

    On the left side, select the option to 'Deploy one revision from an existing container image'. Navigate to and select the Docker image we just pushed.

8. Specify details.
    
    Fill in the rest of the form with required detials, such as project name and region. Use the same region and pick a convenient name like 'toxicity-predictor' as you cannot change this part. 

    Set CPU allocation and autoscaling as needed. Keep these options lower to remain in the free tier if desired. 

9. Set authentication.
    
    Make sure you pick the authentication option, __Allow unauthenticated invocations__. This will allow us to query it with the Streamlit app and the `request.py` script.

10. Create service.

    Once you've set up everything, click Create and wait for the deployment to finish. This can take a moment to process everything. 

11. Configure Streamlit app and `request.py`.

    After the service is deployed, you will see a displayed URL in the header. Copy this URL. 

    - Configure Streamlit app
        
        Navigate to `app.py`. Remove the active URL and paste your deploy's link in place. Save the file and run,

        ```
        streamlit run app.py
        ```

        The app will now query your cloud deploy of the model. 
    
    - Configure `request.py`

        Navigate to `request.py`. Remove the active URL and paste your deloy's link in place. Save the file, customise the request as needed, and run,

        ```
        python request.py
        ```

        The script will now query your cloud deploy of the model. 

12. Delete Docker image from repository.

    After the Google Cloud Run service is deployed, we can safely delete the image from the Artifact Registry.

    Navigate back to the Registry and from there to Repositories. Select the 'toxicity-prediction' repository and click on 'Delete'. Make sure you confirm the deletion and wait for it to finish deleting. 