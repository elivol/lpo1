import cv2
import sys
from math import pi, cos, sin

# Аргументы командной строки

#  ----
sys.argv.append("1.1.png")
sys.argv.append("2.1.png")
#  ----

# Инициализация переменных
template_filename = ""
source_filename = ""

# Запись аргументов в переменные
if len(sys.argv):
    template_filename = sys.argv[1]
    source_filename = sys.argv[2]
else:
    print("Введите аргументы")
    exit(0)

# Загрузка изображения, Изменение размера
img = cv2.imread(template_filename)
img_t = cv2.resize(img, (475, 310), interpolation=cv2.INTER_CUBIC)

img = cv2.imread(source_filename)
img_s = cv2.resize(img, (475, 310), interpolation=cv2.INTER_CUBIC)

# Бинаризация изображения-шаблона, определение контуров изображения-шаблона
imgray_t = cv2.cvtColor(img_t, cv2.COLOR_BGR2GRAY)
ret_t, thresh_t = cv2.threshold(imgray_t, 127, 255, 0)
im2_t, contours_t, hierarchy_t = cv2.findContours(thresh_t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Бинаризация изображения-источника, определение контуров изображения-источника
imgray_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
ret_s, thresh_s = cv2.threshold(imgray_s, 127, 255, 0)
im2_s, contours_s, hierarchy_s = cv2.findContours(thresh_s, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 1. Количество контуров
# (Анализ)
t_contours_count = len(contours_t)
s_contours_count = len(contours_s)

print(t_contours_count, ' ', s_contours_count)

# 2. Ориентация контуров

# Высчитать средний наклон 2х росписей
sum_angle_t = 0
sum_angle_s = 0
for i in range(t_contours_count):
    sum_angle_t += cv2.minAreaRect(contours_t[i])[-1]

for i in range(s_contours_count):
    sum_angle_s += cv2.minAreaRect(contours_s[i])[-1]

# Среднее отклонение ориентации
# (Анализ)
angle_mid_s = sum_angle_s/s_contours_count
angle_mid_t = sum_angle_t/t_contours_count

print(angle_mid_s, angle_mid_t)

# 3. Длина контуров
sum_len_t = 0
sum_len_s = 0
# Общая длина подписи-шаблона
for i in range(t_contours_count):
    sum_len_t += cv2.arcLength(contours_t[i], True)

# Общая длина проверяемой подписи
for i in range(s_contours_count):
    sum_len_s += cv2.arcLength(contours_s[i], True)

print(sum_len_t, sum_len_s)

# 4. Положение экстремумов подписи


cv2.drawContours(img_s, contours_s, -1, (0, 255, 0), 3)
cv2.drawContours(img_t, contours_t, -1, (0, 255, 0), 3)

cv2.imshow("t", img_t)
cv2.waitKey()


cv2.imshow("s", img_s)
cv2.waitKey()