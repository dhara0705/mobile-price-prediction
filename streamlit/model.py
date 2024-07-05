import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pickle

# Load the dataset
df = pd.read_csv('medical data.csv')

# Convert all columns to string
df = df.astype(str)

# Drop the 'Name' and 'DateOfBirth' columns
df = df.drop(['Name', 'DateOfBirth'], axis=1)

# Handle the 'Femal' value in the 'Symptoms' column
df['Symptoms'] = df['Symptoms'].replace('Femal', 'Female')

# Handle missing values in the 'Symptoms' column
df['Symptoms'] = df['Symptoms'].fillna('')

# Encode all columns (features) using LabelEncoder
le_dict = {}
for column in df.columns:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    le_dict[column] = le

# Split the data into features (X) and target (y)
X = df.drop('Symptoms', axis=1)
y = df['Symptoms']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Classification Report:\n{classification_report(y_test, y_pred)}")
print(f"Confusion Matrix:\n{confusion_matrix(y_test, y_pred)}")

# Save the trained model and LabelEncoders
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('label_encoders.pkl', 'wb') as f:
    pickle.dump(le_dict, f)

# Create the Streamlit app
st.title("Medical Disease Recommendation System")
st.write("Enter your symptoms to get a recommendation.")
st.write(f"Please enter {len(X.columns)} symptoms, comma-separated:")

# Create input fields for symptoms
symptoms = st.text_input("Symptoms (comma-separated):")

# Load the saved model and LabelEncoders
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('label_encoders.pkl', 'rb') as f:
    le_dict = pickle.load(f)

# Predict the disease when the submit button is clicked
if st.button("Submit"):
    symptoms_list = [symptom.strip() for symptom in symptoms.split(',')]
    
    # Ensure the input matches the features used in training
    input_data = {column: [''] for column in X.columns}
    if len(symptoms_list) == len(X.columns):
        for i, column in enumerate(X.columns):
            input_data[column] = [symptoms_list[i]]
    else:
        st.error(f"Please enter exactly {len(X.columns)} symptoms.")
        st.stop()
    
    # Add 'joint pain' to the list of symptoms if it is entered
    if 'joint pain' in symptoms_list:
        symptoms_list.remove('joint pain')
        input_data['joint pain'] = ['joint pain']
    
    symptom_df = pd.DataFrame(input_data)
    
    for column in symptom_df.columns:
        le = le_dict[column]
        try:
            # Ensure all symptoms are in the known labels
            for symptom in symptom_df[column]:
                if symptom not in le.classes_:
                    st.error(f"Error: '{symptom}' is not a known symptom.")
                    st.stop()
            symptom_df[column] = le.transform(symptom_df[column])
        except ValueError as e:
            st.error(f"Error: {e}")
            st.stop()
    
    prediction = model.predict(symptom_df)
    st.write(f"Recommended medicine: {prediction[0]}")