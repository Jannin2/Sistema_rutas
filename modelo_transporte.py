import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv("dataset_transporte.csv")


df["Linea_cod"] = LabelEncoder().fit_transform(df["Linea"])
df["Origen_cod"] = LabelEncoder().fit_transform(df["Estacion_Origen"])
df["Destino_cod"] = LabelEncoder().fit_transform(df["Estacion_Destino"])


X = df[["Linea_cod", "Origen_cod", "Destino_cod", "Tiempo_estimado"]]
y = df["Retraso"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)


modelo = DecisionTreeClassifier()
modelo.fit(X_train, y_train)


y_pred = modelo.predict(X_test)
print("Precisión:", accuracy_score(y_test, y_pred))
print("Reporte:\n", classification_report(y_test, y_pred))
