f = open("i.txt")
s = f.read()
import base64

# Строка Base64
base64_string = s

# # Очистка строки
# base64_string = base64_string.strip().replace("\n", "")

# Исправление заполнения
missing_padding = len(base64_string) % 4
if missing_padding != 0:
    base64_string += "=" * (4 - missing_padding)

# Сохранение изображения
output_file = "rec3.jpg"  # Имя файла для сохранения
with open(output_file, "wb") as image_file:
    image_file.write(base64.b64decode(base64_string))

print(f"Изображение сохранено как {output_file}")
