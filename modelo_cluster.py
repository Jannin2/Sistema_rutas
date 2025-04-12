import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("dataset_transporte.csv")

# Seleccionar características numéricas
X = df[['Tiempo_estimado', 'Retraso']]

# Escalar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Crear modelo KMeans con 3 grupos
kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Guardar resultados
df.to_csv("dataset_cluster_resultado.csv", index=False)

# Visualizar los grupos (opcional)
plt.figure(figsize=(8,6))
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=df['Cluster'], cmap='viridis', s=100)
plt.xlabel("Tiempo estimado (escalado)")
plt.ylabel("Retraso (escalado)")
plt.title("Agrupamiento de rutas por características")
plt.grid()
plt.savefig("grafico_clusters.png")
plt.show()
