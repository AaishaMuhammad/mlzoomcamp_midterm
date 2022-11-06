# Importing libraries
import bentoml
from bentoml.io import JSON
from bentoml.io import NumpyNdarray
from pydantic import BaseModel

# Setting up data validation class
class toxicity_predictions(BaseModel):
    pop: str
    viewer: str
    background: str
    noise: str
    v_or_d: str
    vs_lumin_cont: float
    vs_chrom_cont: float
    vs_conspic: float
    vi_brightness: float


# Getting the model from BentoML and setting up runner
model_ref = bentoml.xgboost.get("frog_toxicity_model:latest")
dv = model_ref.custom_objects['dictVectorizer']
model_runner = model_ref.to_runner()
svc = bentoml.Service("toxicity_predictor", runners=[model_runner])

# Serving the model
@svc.api(input=JSON(pydantic_model=toxicity_predictions), output=NumpyNdarray())
def predict(toxicity_predictions):
    data = toxicity_predictions.dict()
    vector = dv.transform(data)
    prediction = model_runner.predict.run(vector)
    print(prediction)
    return prediction[0]