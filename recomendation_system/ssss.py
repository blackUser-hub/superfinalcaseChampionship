import pandas as pd
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Чтение CSV файла
data = pd.read_csv("ggggg.csv")

# Загрузка модели для эмбеддингов
model = SentenceTransformer('all-MiniLM-L6-v2')

# Генерация текстов из колонок
data['combined_text'] = data.apply(
    lambda row: f"{row['genre']} {row['style']} {row['colors_theme']} {row['tematics']} {row['mood']}", axis=1
)

# Генерация эмбеддингов
embeddings = model.encode(data['combined_text'].tolist())

# Преобразование эмбеддингов в формат numpy
embeddings_np = np.array(embeddings).astype('float32')

# Создание индекса FAISS
dimension = embeddings_np.shape[1]  # Размерность эмбеддингов
index = faiss.IndexFlatL2(dimension)  # Используется L2-норма
index.add(embeddings_np)

print(f"Индекс содержит {index.ntotal} записей")

# Сохранение индекса FAISS в файл
faiss.write_index(index, "faiss_index.bin")
print("Индекс сохранён: faiss_index.bin")

# Добавление эмбеддингов в формате JSON в одну колонку (для совместимости с CSV)
data['embedding'] = embeddings.tolist()
data['embedding'] = data['embedding'].apply(lambda x: json.dumps(x))

# Сохранение данных с эмбеддингами в CSV
data.to_csv('data_with_single_embedding.csv', index=False)
print("Файл сохранён: data_with_single_embedding.csv")