# superfinalcaseChampionship
в папке bot лежит телеграмм бот нашей команды, сделанный для привлечения новой аудитории
  запуск: 
    python -m venv venv
    ./venv/Source/activate(для виндовс) source ./venv/bin/activate (для линукс)
    pip install -r requerements.txt
    запуск файла bot.py

в папке recomendation_system лежит рекомендательная система для генерированных картинок
  запуск: 
      python -m venv venv
      ./venv/Source/activate(для виндовс) source ./venv/bin/activate (для линукс)
      pip install -r requerements.txt
      uvicorn app:main --reload
      и нужно обратиться по url http://127.0.0.1:8000/?image_id=ff5fa2b7-d194-4910-a6b6-a4aa6c038407

в папке cofe_test лежит пример принципа работы теста для подбора кофе для пользователей
  запуск: 
  просто открыть index.html в браузере:)
