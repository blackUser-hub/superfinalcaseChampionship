import pandas as pd
import json
from sentence_transformers import SentenceTransformer

# Чтение CSV файла
data = pd.read_csv("data.csv")

# Загрузка модели для эмбеддингов
model = SentenceTransformer('all-MiniLM-L6-v2')

# Генерация текстов из колонок
data['combined_text'] = data.apply(
    lambda row: f"{row['genre']} {row['style']} {row['colors_theme']} {row['tematics']} {row['mood']}", axis=1
)

# Генерация эмбеддингов
embeddings = model.encode(data['combined_text'].tolist())

# Добавление эмбеддингов в формате JSON в одну колонку
data['embedding'] = embeddings.tolist()

# Преобразование эмбеддинга в строку JSON
data['embedding'] = data['embedding'].apply(lambda x: json.dumps(x))

# Сохранение в новый CSV файл
data.to_csv('embedding.csv', index=False)

print("Файл сохранён:  embedding.csv")
