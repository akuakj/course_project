import json
import numpy as np

with open('data/voice_database.json') as f:
    data = json.load(f)

people = list(data['voices'].values())
vectors = [np.array(p['vector_data']) for p in people]

for i in range(len(vectors)):
    for j in range(len(vectors)):
        a, b = vectors[i], vectors[j]
        sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
        name_i = people[i]['full_name'][:12]
        name_j = people[j]['full_name'][:12]
        print(f'{name_i} vs {name_j}: {sim:.3f}')