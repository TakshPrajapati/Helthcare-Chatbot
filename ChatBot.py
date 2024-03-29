import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import difflib
import speech_recognition as sr
import pyttsx3
from translate import Translator
import warnings
warnings.filterwarnings("ignore")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
rate = engine.getProperty('rate')
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand(language):
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5
        r.energy_threshold = 300
        audio = r.listen(source, 0, 8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language=language)
        # print(f"User said: {query}\n")

    except Exception as e:
        print("Unable to Recognize your voice.")
        return "None"

    return query

def translate_to_language(text, source_language, dest_language):
    translator = Translator(to_lang=dest_language, from_lang=source_language)
    translated_text = translator.translate(text)
    return translated_text

def load_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except FileNotFoundError:
        print("Error: 'model.pkl' file not found.")
    except Exception as e:
        print(f"Error loading the model: {e}")
    return None

def get_user_input():
    print("Enter the language you want to continue with (en or hi):")
    lang = input("Enter 'en' for English or 'hi' for Hindi: ")

    print("Tell us your symptoms:")
    user_input = input("Enter your symptoms separated by commas: ")
    
    return lang, user_input

def process_user_input(lang, user_input):
    if user_input.lower() == 'none':
        print("You have not given any symptom.")
    else:
        if lang == "hi":
            translated_text = translate_to_language(user_input, "hi", "en")
            print("Translated text:", translated_text)
        elif lang == "en":
            translated_text = translate_to_language(user_input, "en", "en")
            print("Translated text:", translated_text)

        t1_one = string_replace(translated_text)
        string_cleaned = remove_space(t1_one)

        symptoms_str = string_cleaned
        symptoms_list = symptoms_str.split(',')
        similar_symptoms = []

        for i in symptoms_list:
            matches = difflib.get_close_matches(i, cols, n=1, cutoff=0.7)
            if matches:
                similar_symptoms.append(matches[0])
            else:
                similar_symptoms.append(i)

        if len(similar_symptoms) >= 3:
            print("Your symptoms: ", similar_symptoms)

            symptoms_weights = dict(zip(severity_data['Symptom'], severity_data['weight']))
            weights = [symptoms_weights.get(symptom, 0) for symptom in similar_symptoms]
            weights = weights + [0] * (17 - len(weights))
            return weights
        else:
            print("You have not entered a minimum of 3 symptoms.")
    
    return None

def run_chatbot(weights):
    disease = diagnose(weights)
    main = disease[0]
    print()
    print(f'You may have {main}.')
    speak(f"You may have {main}")
    print()
    info = get_disease_info(main)
    print("Medicine: ", info[2])
    speak("Medicine recommended for this disease is")
    speak(info[2])
    print("Doctor: ", info[1])
    speak("Doctor suggested for you with a link to the doctor")
    speak(info[1])
    print("Link: ", info[0])

if __name__ == "__main__":
    model_path = 'E:\Healthcare_ChatBot_with_VoiceCommand-master/model.pkl'
    dataset = pd.read_csv('Training.csv')
    doc_dataset = pd.read_csv('Doctor.csv')
    severity_data = pd.read_csv('Symptom-severity.csv')
    X = dataset.iloc[:, :132].values
    y = dataset.iloc[:, -1].values

    dimensionality_reduction = dataset.groupby(dataset['prognosis']).max()
    labelencoder = LabelEncoder()
    y = labelencoder.fit_transform(y)
    cols = dataset.columns
    cols = cols[:-1]
    cols = severity_data['Symptom'].unique()

    weights = None

    while weights is None:
        lang, user_input = get_user_input()
        weights = process_user_input(lang, user_input)
    
    run_chatbot(weights)

    
    """

dataset = pd.read_csv('Training.csv')
doc_dataset = pd.read_csv('Doctor.csv')
severity_data = pd.read_csv('Symptom-severity.csv')
X = dataset.iloc[:, :132].values
y = dataset.iloc[:, -1].values
#
#
dimensionality_reduction = dataset.groupby(dataset['prognosis']).max()
#print(dimensionality_reduction)


labelencoder = LabelEncoder()

y = labelencoder.fit_transform(y)
cols = dataset.columns
cols = cols[:-1]
cols = severity_data['Symptom'].unique()

for i, col in enumerate(severity_data['Symptom']):
   # print(f'{i+1}. {col}')
           query = takeCommand().lower()


def string_replace(string):
    return string.replace("and",",")
 
def remove_space(string):
    return string.replace(" ","")



#print(symptoms_binary)
def diagnose(weights):
    weights = np.array(weights).reshape(1, -1)
    prediction = model.predict(weights)
    disease = labelencoder.inverse_transform(prediction)[0]
    return prediction

def get_disease_info(disease):
    des = doc_dataset[doc_dataset['Prognosis'] == disease]['Description'].values[0]
    doc = doc_dataset[doc_dataset['Prognosis'] == disease]['Name'].values[0]
    med = doc_dataset[doc_dataset['Prognosis'] == disease]['Medicine'].values[0]
    return des,doc,med
def run_chatbot():
    disease = diagnose(weights)
    main= disease[0]
    print()
    print(f'You may have {main}.')
    speak(f"You may have {main}")
    print()
    info=get_disease_info(main)
    print("Medicine: ",info[2])
    speak("Medicine recommended for this diseases is")
    speak(info[2])
    print("Doctor: ",info[1])
    speak("Doctor suggested for you with link of the doctor")
    speak(info[1])
    print("Link: ", info[0])

print("Give Atleast 3 Symptoms: ")
speak("Enter the language you want to continue with english or hindi")
lang = input("Enter the language you want to continue with 'en' or 'hi': ")

speak("Tell us your symptoms")
string_one = takeCommand(lang).lower()
print(string_one)
if string_one == 'none':
    print("You have not given any symptom")
else:
    if lang == "hi":
        translated_text = translate_to_language(string_one, "hi", "en")
        print(translated_text)
    elif lang == "en":
        translated_text = translate_to_language(string_one, "en", "en")
        print(translated_text)

    t1_one = string_replace(translated_text)
    string_cleaned = remove_space(t1_one)
    print(string_cleaned)

    symptoms_str = input("Enter the symptoms separated by commas: ")

    symptoms_list = string_cleaned.split(',')

    symptoms_list2 = ['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills',
                      'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting',
                      'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain', 'anxiety',
                      'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
                      'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes',
                      'breathlessness', 'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin',
                      'dark_urine', 'nausea', 'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation',
                      'abdominal_pain', 'diarrhoea', 'mild_fever', 'yellow_urine', 'yellowing_of_eyes',
                      'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach', 'swelled_lymph_nodes', 'malaise',
                      'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes',
                      'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs',
                      'fast_heart_rate', 'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool',
                      'irritation_in_anus', 'neck_pain', 'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs',
                      'swollen_blood_vessels', 'puffy_face_and_eyes', 'enlarged_thyroid', 'brittle_nails',
                      'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts', 'drying_and_tingling_lips',
                      'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
                      'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
                      'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'foul_smell_of urine',
                      'continuous_feel_of_urine', 'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)',
                      'depression', 'irritability', 'muscle_pain', 'altered_sensorium', 'red_spots_over_body',
                      'belly_pain', 'abnormal_menstruation', 'dischromic _patches', 'watering_from_eyes',
                      'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum',
                      'lack_of_concentration', 'visual_disturbances', 'receiving_blood_transfusion',
                      'receiving_unsterile_injections', 'coma', 'stomach_bleeding', 'distention_of_abdomen',
                      'history_of_alcohol_consumption', 'fluid_overload.1', 'blood_in_sputum',
                      'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads',
                      'scurring', 'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails',
                      'blister', 'red_sore_around_nose', 'yellow_crust_ooze']

    similar_symptoms = []
    for i in symptoms_list:
        matches = difflib.get_close_matches(i, cols, n=1, cutoff=0.7)
        if matches:
            similar_symptoms.append(matches[0])
        else:
            similar_symptoms.append(i)

    if len(similar_symptoms)>=3:
        print("Your symptoms: ", similar_symptoms)

        symptoms_weights = dict(zip(severity_data['Symptom'], severity_data['weight']))

        # Convert the user input symptoms to weights and store in a list
        weights = [symptoms_weights.get(symptom, 0) for symptom in similar_symptoms]

        # Make sure the list has 17 elements by filling in zeros
        weights = weights + [0] * (17 - len(weights))
        print(weights)
        run_chatbot()
    else:
        print("You have not entered minimum 3 symptoms")

"""


