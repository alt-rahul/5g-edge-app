import matplotlib.tri as tri
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

og_live = pd.read_csv(r'C:\Users\rahul\Documents\Python\Work\WINLAB\5g-edge-app\data\samples\trial\live_metrics.csv')
og_initial = pd.read_csv(r'C:\Users\rahul\Documents\Python\Work\WINLAB\5g-edge-app\data\samples\trial\intial_statement.csv')
og_verbose = pd.read_csv(r'C:\Users\rahul\Documents\Python\Work\WINLAB\5g-edge-app\data\samples\trial\verbose_statements.csv')

live = og_live.drop(columns=['Unnamed: 0'])

def normalize(diction : dict):
    diction = (diction)/(diction.max())
    return diction

norm = live.dropna()
norm = norm.iloc[:, 3:]
norm = norm.drop(columns=['Current Time'])
norm = normalize(norm)

x = norm['GPU Utilization (%)'].values
y = norm['Memory Utilization (%)'].values
z = norm['Memory Clock Utilization'].values


fig = plt.figure(figsize=(10, 12))
ax = fig.add_subplot(111, projection='3d')

triangular = tri.Triangulation(x, y)
surface = ax.plot_trisurf(triangular, z, cmap='viridis', edgecolor='none', alpha=0.8)
fig.colorbar(surface, ax=ax)

# linespace = np.linspace(0, 1, len(x))
linespace = [0,1]
X, Y = np.meshgrid(linespace, linespace)
ax.plot_surface(X, Y, np.zeros_like(X), color='gray', alpha=0.2)
ax.plot_surface(X,np.zeros_like(X),  Y, color='gray', alpha=0.2)
ax.plot_surface(np.zeros_like(X), X, Y, color='gray', alpha=0.2)

ax.set_box_aspect([1, 1, 1])
plt.tight_layout()
plt.show()