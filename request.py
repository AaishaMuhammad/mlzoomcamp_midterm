# This script will not run until the bento has been built and is actively running.
# IF deploy to cloud is currently active, the URL can be changed. 


# Importing requests library
import requests

# Specifiying URL for queries
# url = "http://localhost:3000/predict" # <-- uncomment this to run on local deploy
url = "https://toxicity-predictor-3zykgobfea-uc.a.run.app/predict" # <-- uncomment this to run on cloud deploy


# Making some dictionary's with dummy data for ease of querying. Change these values to change your request.
# Ensure data entered is within range described in README.md!
dict1 = {
  "pop": "AG",
  "viewer": "bird",
  "background": "heli",
  "noise": "sp",
  "v_or_d": "d",
  "vs_lumin_cont": 0.663722415,
  "vs_chrom_cont": 0.233671337,
  "vs_conspic": 0.555260377,
  "vi_brightness": 3689.650359
}

dict2 = {
  "pop": "BCG",
  "viewer": "bird",
  "background": "heli",
  "noise": "sp",
  "v_or_d": "d",
  "vs_lumin_cont": 0.484848,
  "vs_chrom_cont": 0.233671337,
  "vs_conspic": 0.555260377,
  "vi_brightness": 3789.650359
}

dict3 = {
  "pop": "SO",
  "viewer": "crab",
  "background": "leaf",
  "noise": "sp",
  "v_or_d": "d",
  "vs_lumin_cont": 0.784848,
  "vs_chrom_cont": 0.233671337,
  "vs_conspic": 0.634560377,
  "vi_brightness": 3489.650359
}

dict4 = {
  "pop": "SO",
  "viewer": "bird",
  "background": "bark",
  "noise": "sp",
  "v_or_d": "v",
  "vs_lumin_cont": 1.484848,
  "vs_chrom_cont": 0.765371337,
  "vs_conspic": 0.555260377,
  "vi_brightness": 1298.650359
}


# Specifying which dictionary should be sent
query = dict3

# Running basic checks to ensure data is within acceptable range of values.
pop_ids = ["AG", "TALA", "AL", "BCG", "BCO", "CA", "CO", "SC", "SH", "PoSo", "SO"]
viewers = ["pumilio", "bird", "crab", "snake"]
bgs = ['bark', 'heli', 'leaf']
noises = ["sp", "fix"]
vords = ["v", "d"]

if query["pop"] not in pop_ids:
    print("Invalid Population")
    quit()

if query["viewer"] not in viewers:
    print("Invalid viewer")
    quit()

if query["background"] not in bgs:
    print("Invalid background")
    quit()

if query["noise"] not in noises:
    print("Invalid noise")
    quit()

if query["v_or_d"] not in vords:
    print("Invalid VorD")
    quit()

if query["vs_lumin_cont"] < 0.000000000 or query["vs_lumin_cont"] > 1.000000000:
    print("Invalid vs_lumin_cont")
    quit()

if query["vs_chrom_cont"] < 0.000000000 or query["vs_chrom_cont"] > 1.000000000:
    print("Invalid vs_chrom_cont")
    quit()

if query["vs_conspic"] < 0.000000000 or query["vs_conspic"] > 1.000000000:
    print("Invalid vs_conspic")
    quit()

if query["vi_brightness"] < 3000.000000000 or query["vi_brightness"] > 17000.000000000:
    print("Invalid vi_brightness")
    quit()

# Sending request and printing response
response = requests.post(url, json=query).json()
print(f"The estimated toxicity of this frog is {response}")