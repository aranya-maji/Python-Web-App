from flask import Flask, render_template, request
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,f1_score,precision_score, recall_score
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import os
import csv
from csv import writer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
app = Flask(__name__)

formal_peach = (255/255, 218/255, 185/255)
mycolor = [formal_peach, "#4682B4"]
sns.set_palette(mycolor)

#read csv file
df = pd.read_csv('survey lung cancer.csv')
# replacing gender from MALE/FEMALE to 0/1
df.GENDER = df.GENDER.replace({"M": 0, "F": 1})

# Define and train the Random Forest model
model = RandomForestClassifier()
X = df.drop('LUNG_CANCER', axis=1)
y = df.LUNG_CANCER
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,shuffle = False)
model.fit(X_train, y_train)
y_predict = model.predict(X_test)

#GENERATING ACCURACY , PRECISION , RECALL SCORE
@app.route('/')
def index():
    y_predict = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_predict) * 100
    precision = precision_score(y_test,y_predict, pos_label='YES')*100
    recall =  recall_score(y_test,y_predict, pos_label='YES')*100

    return render_template('index.html', accuracy=accuracy , precision=precision ,  recall=recall)


#PLOTTING HEATMAP
Z = df.drop('LUNG_CANCER',axis=1)
sns.heatmap(Z.corr())
plt.title("HEATMAP")
plt.savefig(os.path.join('static', 'image1', 'plot15.png'), bbox_inches='tight')
plt.close()




#PLOT WITH AGE
df.groupby('GENDER').size().plot(kind='pie',  textprops={'fontsize': 20},autopct='%1.0f%%')
plt.title('Percentage of the affected people Male(0) Vs Female(1)')
plt.savefig(os.path.join('static', 'image1', 'plot.png'))
plt.close()



#PLOT WITH SMOKING
plt.figure(figsize=(8,6))
sns.countplot(x ='SMOKING', data = df, hue = 'LUNG_CANCER')
plt.title("Smoking Vs.Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot1.png'))
plt.close()



#PLOT WITH ANXEITY
plt.figure(figsize=(8,6))
sns.countplot(x ='ANXIETY', data=df, hue = 'LUNG_CANCER')
plt.title("Anxiety Vs.Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot2.png'))
plt.close()


#PLOT WITH CHRONIC DISEASES
plt.figure(figsize=(8,6))
sns.countplot(x='CHRONIC DISEASE', data=df, hue = 'LUNG_CANCER')
plt.title("CHRONIC DISEASE Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot3.png'))
plt.close()



#PLOT WITH ALCOHOL CONSUMPTION
plt.figure(figsize=(8,6))
sns.countplot(x='ALCOHOL CONSUMING', data=df, hue = 'LUNG_CANCER')
plt.title("ALCOHOL CONSUMING Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot4.png'))
plt.close()


#PLOT WITH YELLOW FINGERS
plt.figure(figsize=(8,6))
sns.countplot(x='YELLOW_FINGERS', data=df, hue = 'LUNG_CANCER')
plt.title("YELLOW FINGERS Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot5.png'))
plt.close()



#PLOT WITH PEER PRESSURE
plt.figure(figsize=(8,6))
sns.countplot(x='PEER_PRESSURE', data=df, hue = 'LUNG_CANCER')
plt.title("PEER PRESSURE Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot6.png'))
plt.close()



#PLOT WITH FATIGUE
plt.figure(figsize=(8,6))
sns.countplot(x='FATIGUE ', data=df, hue = 'LUNG_CANCER')
plt.title("FATIGUE Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot7.png'))
plt.close()



#PLOT WITH ALLERGY
plt.figure(figsize=(8,6))
sns.countplot(x='ALLERGY ', data=df, hue = 'LUNG_CANCER')
plt.title("ALLERGY Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot8.png'))
plt.close()



#PLOT WITH WHEEZING
plt.figure(figsize=(8,6))
sns.countplot(x='WHEEZING', data=df, hue = 'LUNG_CANCER')
plt.title("WHEEZING Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot9.png'))
plt.close()



#PLOT WITH COUGHING
plt.figure(figsize=(8,6))
sns.countplot(x='COUGHING', data=df, hue = 'LUNG_CANCER')
plt.title("COUGHING Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot10.png'))
plt.close()


#PLOT WITH SHORTNESS OF BREATH
plt.figure(figsize=(8,6))
sns.countplot(x='SHORTNESS OF BREATH', data=df, hue = 'LUNG_CANCER')
plt.title("SHORTNESS OF BREATH Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot11.png'))
plt.close()


#PLOT WITH SWALLOWING DIFFICULTY
plt.figure(figsize=(8,6))
sns.countplot(x='SWALLOWING DIFFICULTY', data=df, hue = 'LUNG_CANCER')
plt.title("SWALLOWING DIFFICULTY Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot12.png'))
plt.close()



#PLOT WITH CHEST PAIN
plt.figure(figsize=(8,6))
sns.countplot(x='CHEST PAIN', data=df, hue = 'LUNG_CANCER')
plt.title("CHEST PAIN Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot13.png'))
plt.close()



#GENERATING CONFUSION MATRIX
sns.set(rc = {'axes.grid':False})
ConfusionMatrixDisplay.from_predictions(y_test, y_predict)
plt.title("CONFUSION MATRIX")
plt.savefig(os.path.join('static', 'image1', 'plot16.png'))
plt.close()



#GENERATING IMPORTANCE OF EACH FEATURE[SYMPTOM]
Symptoms_importance = pd.DataFrame(  {"Symptoms": list(X.columns), "importance": model.feature_importances_}).sort_values("importance", ascending=False)
sns.barplot(x=Symptoms_importance.Symptoms, y=Symptoms_importance.importance)
plt.xlabel("Symptoms ")
plt.ylabel("Importance score")
plt.title("The symptoms and their importance in building this model")
plt.xticks( rotation=45, horizontalalignment="right", fontweight="light", fontsize="x-large")
print(Symptoms_importance)
plt.savefig(os.path.join('static', 'image1', 'plot17.png'),bbox_inches='tight')




#PLOT WITH AGE
df['AGE'] = pd.to_numeric(df['AGE'], errors='coerce')  
df = df.dropna(subset=['AGE'])
df['LUNG_CANCER'] = df['LUNG_CANCER'].map({'YES': 1, 'NO': 0})
bins = [0, 60,999]  
labels = ["Less Than 60", "More Than 60"]
df['AGE_GROUP'] = pd.cut(df['AGE'], bins=bins, labels=labels)
grouped_data = df.groupby('AGE_GROUP')['LUNG_CANCER'].sum()
plt.figure(figsize=(8, 8))
plt.pie(grouped_data, labels=grouped_data.index, autopct='%1.1f%%', startangle=140,colors = mycolor)
plt.axis('equal') 
plt.title("AGE Vs. Lung Cancer")
plt.savefig(os.path.join('static', 'image1', 'plot14.png'))

@app.route('/')
def plot14():
    return render_template('index.html', plt=encoded_image)






#TAKING DATA FROM USER AND PREDICTING
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        
        # Get user input from the form
        feature1 = int(request.form['feature1'])
        feature2 = int(request.form['feature2'])
        feature3 = int(request.form['feature3'])
        feature4 = int(request.form['feature4'])
        feature5 = int(request.form['feature5'])
        feature6 = int(request.form['feature6'])
        feature7 = int(request.form['feature7'])
        feature8 = int(request.form['feature8'])
        feature9 = int(request.form['feature9'])
        feature10 = int(request.form['feature10'])
        feature11 = int(request.form['feature11'])
        feature12 = int(request.form['feature12'])
        feature13 = int(request.form['feature13'])
        feature14 = int(request.form['feature14'])
        feature15 = int(request.form['feature15'])

        prediction = model.predict(np.array([[feature1, feature2 , feature3 ,feature4 , feature5, feature6 , feature7 , feature8 , feature9 , feature10 , feature11 , feature12, feature13 , feature14 , feature15  ]]))[0]

        result = 'Cancer Detected' if prediction == 'YES' else 'No Cancer Detected'
        if (feature1 == 1):
            x = "F"
        else:
            x = "M"
        List = [x, feature2 , feature3 ,feature4 , feature5, feature6 , feature7 , feature8 , feature9 , feature10 , feature11 , feature12, feature13 , feature14 , feature15 , prediction ]
        with open('survey lung cancer.csv', 'a') as f_object:

            writer_object = writer(f_object)
            writer_object.writerow(List)
            f_object.close()


        return render_template('result.html', result=result)



if __name__ == '__main__':
    app.run(host = '127.0.0.1' , port = 5000,debug=True)
