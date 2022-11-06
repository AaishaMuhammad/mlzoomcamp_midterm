# Importing libraries

import numpy as np
import pandas as pd
import xgboost as xgb
import bentoml
import warnings

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

# Suppressing warnings
warnings.filterwarnings("ignore")

# Read data
data = "./data/Data_MaanCummings_2011_ AmNat52931_ByPop.txt"
df = pd.read_table(data)

# Renaming the DataFrame columns to make working with the data easier.
columns = ['pop', 'pop_number', 'n_tox', 'toxicity', 'toxicity_se', 'toxicity_normalised',
'toxicity_norm_se', 'viewer', 'background', 'noise', 'v_or_d', 'vs_lumin_cont', 'vs_chrom_cont', 'vs_conspic', 'vi_brightness',
'vi_bright_se', 'vi_bright_normalised', 'bird_lumin_cont', 'bird_chrom_cont', 'bird_conspic_cont']
df.columns = columns

# Filling NaN values with 0s and dropping duplicate values
df = df.fillna(0).drop_duplicates()

# Data splitting into training and test data with 80/20 split. 
df_full_train, df_test = train_test_split(df, test_size=0.2, shuffle=True, random_state=2)
df_full_train.reset_index(drop=True)


# Selecting target variable
y_full_train = np.log1p(df_full_train['toxicity'].values)

# Dropping target variable from dataset
del df_full_train['toxicity']

# Also removing variations of the target variable that are present in the data from research. 
del df_full_train['n_tox']
del df_full_train['toxicity_se']
del df_full_train['toxicity_normalised']
del df_full_train['toxicity_norm_se']

# Lastly we remove these four columns as it had better results in experimentation and/or they would not logically be available to the model. 
del df_full_train['pop_number']
del df_full_train['bird_lumin_cont']
del df_full_train['bird_chrom_cont']
del df_full_train['bird_conspic_cont']
del df_full_train['vi_bright_se']
del df_full_train['vi_bright_normalised']

# Parameters that have been tuned to give the best results with XGBoost
xgb_params = {
    # 'num_boost_round': 86,
    'colsample_bytree': 0.8,
    'eval_metric': 'rmse',
    'learning_rate': 0.1,
    'max_depth': 3,
    'min_child_weight': 5,
    'objective': 'reg:squarederror',
    'random_state': 10
}

# Initializing the dictionary vectorizer
dv = DictVectorizer()

# Performing one-hot encoding with dv
dict_full_train = df_full_train.to_dict(orient='records')
x_full_train = dv.fit_transform(dict_full_train)

# Making DMatrix out of data for the XGBoost model to use
features = dv.get_feature_names()
dfull_train = xgb.DMatrix(x_full_train, label=y_full_train)

# Training the final model
model = xgb.train(xgb_params, dfull_train, num_boost_round=86)

# Saving the model with BentoML
bentoml.xgboost.save_model(
    'frog_toxicity_model',
    model,
    custom_objects={
        'dictVectorizer': dv
    }
)