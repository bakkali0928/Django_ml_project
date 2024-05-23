import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import pickle
from .models import PredResults
import joblib

# Load the model and encoder
with open(r'C:\Users\lenovo\projetML\model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open(r'C:\Users\lenovo\projetML\encoder.pkl', 'rb') as encoder_file:
    encoder = joblib.load(encoder_file)

# Check if the loaded object is an instance of OneHotEncoder
if not isinstance(encoder, OneHotEncoder):
    raise TypeError("Loaded encoder object is not an instance of OneHotEncoder")


def index(request):
    return render(request, 'predict.html')


def predict_chances(request):
    if request.POST.get('action') == 'post':
        # Retrieve input from the form
        age = float(request.POST.get('age'))
        height = float(request.POST.get('height'))
        weight = float(request.POST.get('weight'))
        fcvc = float(request.POST.get('fcvc'))
        ncp = float(request.POST.get('ncp'))
        ch2o = float(request.POST.get('ch2o'))
        faf = float(request.POST.get('faf'))
        tue = float(request.POST.get('tue'))

        gender = request.POST.get('gender')
        family_history = request.POST.get('family_history')
        caec = request.POST.get('caec')
        mtrans = request.POST.get('mtrans')
        calc = request.POST.get('calc')
        scc = request.POST.get('scc')
        smoke = request.POST.get('smoke')
        favc = request.POST.get('favc')

        # Encode categorical features
        categorical_data = {
            'Gender': [gender],
            'family_history_with_overweight': [family_history],
            'CAEC': [caec],
            'MTRANS': [mtrans],
            'CALC': [calc],
            'SCC': [scc],
            'SMOKE': [smoke],
            'FAVC': [favc]
        }

        categorical_df = pd.DataFrame(categorical_data)
        categorical_encoded = encoder.transform(categorical_df)
        # Define categorical columns
        categorical_cols = [
            'Gender', 'family_history_with_overweight', 'CAEC', 'MTRANS', 'CALC', 'SCC', 'SMOKE', 'FAVC'
        ]

        # Ensure the order of one-hot encoded columns matches the order during training
        encoded_feature_names = encoder.get_feature_names_out(categorical_cols)
        categorical_encoded_df = pd.DataFrame(categorical_encoded, columns=encoded_feature_names)

        # Combine continuous and categorical data
        features = np.concatenate(([
            age, height, weight, fcvc, ncp, ch2o, faf, tue
        ], categorical_encoded_df.values[0]))

        # Make prediction
        prediction = model.predict([features])
        result = prediction[0]

        # Save the prediction to the database
        PredResults.objects.create(
            age=age,
            height=height,
            weight=weight,
            fcvc=fcvc,
            ncp=ncp,
            ch2o=ch2o,
            faf=faf,
            tue=tue,
            gender=gender,
            family_history=family_history,
            caec=caec,
            mtrans=mtrans,
            calc=calc,
            scc=scc,
            smoke=smoke,
            favc=favc,
            classification=result
        )

        return JsonResponse({
            'result': result,
            'age': age,
            'height': height,
            'weight': weight,
            'fcvc': fcvc,
            'ncp': ncp,
            'ch2o': ch2o,
            'faf': faf,
            'tue': tue,
            'gender': gender,
            'family_history': family_history,
            'caec': caec,
            'mtrans': mtrans,
            'calc': calc,
            'scc': scc,
            'smoke': smoke,
            'favc': favc
        })


def view_results(request):
    data = {"dataset": PredResults.objects.all()}
    return render(request, "results.html", data)
