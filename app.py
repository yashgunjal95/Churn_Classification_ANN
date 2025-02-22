import numpy as np
import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder,OneHotEncoder, StandardScaler
import pickle
import tensorflow as tf

model = tf.keras.models.load_model('model.h5')

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pickle.load(file)

with open('onehot_encoder_geography','rb') as file:
    onehot_encoder_geography = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

## Steamlit 
st.title("Customer Churn Prediction")


geography = st.selectbox('Geography',onehot_encoder_geography.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.slider('Age',18,92)
balance = st.number_input('Balance')
credit_score = st.number_input('Credit_score')
estimated_salary = st.number_input('Estimated salary')
tenure = st.slider('Tenure',0,10)
num_of_products = st.slider("Number of Products", 1,4)
has_cr_card = st.selectbox('Has credit card',[0,1])
is_active_member = st.selectbox("Is active member",[0,1])

## Example input data
input_data = {
    'CreditScore' : [credit_score],
    #'Geography' : ,
    'Gender' : [label_encoder_gender.transform([gender])[0]],
    'Age' : [age],
    'Tenure' : [tenure],
    'Balance' : [balance],
    'NumOfProducts' : [num_of_products],
    'HasCrCard' : [has_cr_card],
    'IsActiveMember' : [is_active_member],
    'EstimatedSalary' : [estimated_salary]
}

input_data = pd.DataFrame(input_data)

geo_encoded = onehot_encoder_geography.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded,columns=onehot_encoder_geography.get_feature_names_out(['Geography']))
input_data = pd.concat([input_data.reset_index(drop=True), geo_encoded_df], axis=1)

input_data_scaled = scaler.transform(input_data)

prediction = model.predict(input_data_scaled)
prediction_prob = prediction[0][0]

st.write(f"Churn Probabilty : {prediction_prob}")

if prediction_prob > 0.5:
    st.write("This Customer is likely to churn. ")
else:
    st.write("This Customer is unlikely to churn. ")