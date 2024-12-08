import uvicorn
import pandas as pd
import json
import numpy as np
import faiss
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse

app = FastAPI()

# Загрузка данных и индекса
data_path = "data_with_single_embedding.csv"
index_path = "faiss_index.bin"

# Загрузка данных
data = pd.read_csv(data_path)
data['embedding'] = data['embedding'].apply(json.loads)  # Конвертация эмбеддингов из JSON
embeddings_np = np.vstack(data['embedding'].values).astype('float32')

# Загрузка FAISS индекса
index = faiss.read_index(index_path)

print(f"Индекс содержит {index.ntotal} записей, данные загружены.")


def find_similar(index, query_vector, k=4):
    """
    Найти ближайшие соседи с использованием FAISS.
    """
    distances, indices = index.search(query_vector, k)
    return indices[0], distances[0]


def render_html(image_id, recommendations):
    """
    Генерация HTML страницы с основной картинкой и рекомендациями.
    """
    # Данные основной картинки
    main_image = data.loc[data['Id'] == image_id].iloc[0]
    main_image_base64 = main_image['photo']

    # Рекомендации
    recommended_images = [
        {
            "id": data.loc[idx, "Id"],
            "photo": data.loc[idx, "photo"],
            "genre": data.loc[idx, "genre"],
            "style": data.loc[idx, "style"],
            "colors_theme": data.loc[idx, "colors_theme"],
            "tematics": data.loc[idx, "tematics"],
            "mood": data.loc[idx, "mood"],
        }
        for idx in recommendations
    ]

    # HTML-код
    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Recommendation System</title>
        <style>
            body {{
                background: linear-gradient(135deg, #1e1e1e, #333333);
                color: #fff;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
            }}
            .main-image, .recommendation {{
                display: inline-block;
                margin: 10px;
                border-radius: 8px;
                box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            }}
            img {{
                border-radius: 8px;
                width: 200px;
                height: 200px;
            }}
            .info {{
                margin-top: 10px;
                padding: 10px;
                border: 1px solid #555;
                border-radius: 8px;
                background: #444;
                text-align: left;
                font-size: 14px;
                line-height: 1.5;
            }}
            .recommendations {{
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
            }}
            .recommendation a {{
                text-decoration: none;
                color: inherit;
                display: block;
                text-align: center;
            }}
            .recommendation:hover {{
                transform: scale(1.05);
                transition: transform 0.3s ease;
            }}
        </style>
    </head>
    <body>
        

        <!-- Основная картинка -->
        <div class="main-image">
            
            <img src="data:image/jpeg;base64,{main_image_base64}" alt="Main Image">
            <div class="info">
                <p><strong>Жанр:</strong> {main_image['genre']}</p>
                <p><strong>Стиль:</strong> {main_image['style']}</p>
                <p><strong>Цветовая гамма:</strong> {main_image['colors_theme']}</p>
                <p><strong>Тематика:</strong> {main_image['tematics']}</p>
                <p><strong>Настроение:</strong> {main_image['mood']}</p>
            </div>
        </div>

        
        <div class="recommendations">
    """

    for rec in recommended_images:
        html += f"""
        <div class="recommendation">
            <a href="/?image_id={rec['id']}">
                <img src="data:image/jpeg;base64,{rec['photo']}" alt="Recommended Image">
                <div class="info">
                    <p><strong>Жанр:</strong> {rec['genre']}</p>
                    <p><strong>Стиль:</strong> {rec['style']}</p>
                    <p><strong>Цветовая гамма:</strong> {rec['colors_theme']}</p>
                    <p><strong>Тематика:</strong> {rec['tematics']}</p>
                    <p><strong>Настроение:</strong> {rec['mood']}</p>
                </div>
            </a>
        </div>
        """

    html += """
        </div>
    </body>
    </html>
    """
    return html


@app.get("/", response_class=HTMLResponse)
async def recommend(image_id: str = Query(..., description="UUID изображения")):
    """
    Основной маршрут для получения рекомендаций по ID изображения.
    """
    # Проверка на наличие ID
    if image_id not in data['Id'].values:
        raise HTTPException(status_code=404, detail=f"ID {image_id} не найден")

    # Получение вектора для запрашиваемого изображения
    query_row = data[data['Id'] == image_id]
    query_vector = np.array(query_row['embedding'].values[0]).reshape(1, -1)

    # Поиск похожих изображений
    similar_indices, distances = find_similar(index, query_vector, k=5)

    # Исключить текущее изображение из рекомендаций
    similar_indices = [idx for idx in similar_indices if data.loc[idx, "Id"] != image_id]

    # Генерация HTML ответа
    return render_html(image_id, similar_indices[:4])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
