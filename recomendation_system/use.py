import faiss
import numpy as np
import pandas as pd
import json

def load_index(index_path):
    """
    Загрузить FAISS индекс из файла.
    """
    index = faiss.read_index(index_path)
    print(f"Загруженный индекс содержит {index.ntotal} записей")
    return index

def find_similar(index, query_vector, k=4):
    """
    Найти наиболее похожие элементы по запросу.
    
    Args:
        index: FAISS индекс.
        query_vector: Вектор запроса (numpy array).
        k: Количество ближайших соседей.
    
    Returns:
        indices: Индексы наиболее похожих элементов.
        distances: Дистанции до них.
    """
    distances, indices = index.search(query_vector, k)
    return indices[0], distances[0]

def load_data_with_ids(data_path):
    """
    Загрузить CSV файл с данными и преобразовать эмбеддинги из JSON в numpy.
    
    Returns:
        data: DataFrame с оригинальными данными.
        embeddings_np: numpy массив эмбеддингов.
    """
    data = pd.read_csv(data_path)
    data['embedding'] = data['embedding'].apply(json.loads)
    embeddings_np = np.vstack(data['embedding'].values).astype('float32')
    return data, embeddings_np

def main():
    # Пути к файлам
    index_path = "faiss_index.bin"
    data_path = "data_with_single_embedding.csv"

    # Загрузка индекса и данных
    index = load_index(index_path)
    data, embeddings_np = load_data_with_ids(data_path)

    # Запрос ID от пользователя
    input_id = input("Введите ID фотографии для поиска похожих: ").strip()

    # Проверка наличия ID
    if input_id not in data['Id'].values:
        print(f"ID {input_id} не найден в данных.")
        return

    # Получение вектора запроса по ID
    query_row = data[data['Id'] == input_id]
    query_vector = np.array(query_row['embedding'].values[0]).reshape(1, -1)

    # Поиск ближайших соседей
    similar_indices, distances = find_similar(index, query_vector, k=5)

    # Получение ID похожих записей
    similar_ids = data.iloc[similar_indices]['Id'].tolist()

    print(f"Запрос ID: {input_id}")
    print(f"Похожие ID: {similar_ids}")
    print(f"Дистанции: {distances}")

if __name__ == "__main__":
    main()
