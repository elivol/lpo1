import cv2
import sys

# Проверка аргументов кс
print("Введите аргументы: 1-изоражение-шаблон, 2-изображение-источник")

template_filename = input()
source_filename = input()

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

print("----------------\nРасчет критериев\n----------------")
print("Количество контуров первой подписи: ", t_contours_count)
print("Количество контуров второй подписи: ", s_contours_count)

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

print("Ориентация контуров первой подписи: ", angle_mid_t)
print("Ориентация контуров второй подписи: ", angle_mid_t)

# 3. Длина контуров
sum_len_t = 0
sum_len_s = 0
# Общая длина подписи-шаблона
for i in range(t_contours_count):
    sum_len_t += cv2.arcLength(contours_t[i], True)

# Общая длина проверяемой подписи
for i in range(s_contours_count):
    sum_len_s += cv2.arcLength(contours_s[i], True)

print("Общая длина контуров первой подписи: ", sum_len_t)
print("Общая длина контуров второй подписи: ", sum_len_s)

# 4. Положение экстремумов подписи
# Поиск  экстремумов по оси Y:
# a) для шаблона
contours_t = contours_t[1:]
y_max_t = []
y_min_t = []
for i in range(t_contours_count-1):
    cnt = contours_t[i]
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:,:,1].argmax()][0])
    y_max_t.append(topmost[1])
    y_min_t.append(bottommost[1])

print("Экстремумы контуров первой подписи по оси Y: y(max)=", max(y_max_t), ", y(min)=", min(y_min_t))

# b) для источника
y_max_s = []
y_min_s = []
contours_s = contours_s[1:]
for i in range(s_contours_count-1):
    cnt = contours_s[i]
    topmost = tuple(cnt[cnt[:,:,1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])
    y_max_s.append(topmost[1])
    y_min_s.append(bottommost[1])

print("Экстремумы контуров второй подписи по оси Y: y(max)=", max(y_max_s), ", y(min)=", min(y_min_s))

# Поиск экстремумов по оси X
# a) для шаблона:
x_max_t = []
x_min_t = []
for i in range(t_contours_count-1):
    cnt = contours_t[i]
    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    x_max_t.append(rightmost[0])
    x_min_t.append(leftmost[0])

print("Экстремумы контуров первой подписи по оси X: x(max)=", max(x_max_t), ", x(min)=", min(x_min_t))

# b) для источника
x_max_s = []
x_min_s = []
for i in range(s_contours_count-1):
    cnt = contours_s[i]
    leftmost = tuple(cnt[cnt[:,:,0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    x_max_s.append(rightmost[0])
    x_min_s.append(leftmost[0])

print("Экстремумы контуров второй подписи по оси X: x(max)=", max(x_max_s), ", x(min)=", min(x_min_s))

print("------------------\nПроверка критериев\n------------------")
count_crit = 0
# Количество контуров
if abs(t_contours_count-s_contours_count) <= 20:
    print(""""Количество контуров": критерий выполняется!""")
else:
    print(""""Количество контуров": критерий НЕ выполняется!""")
    count_crit += 1

# Длина контуров
if abs(sum_len_t-sum_len_s)/max(sum_len_s, sum_len_t) <= 0.2:
    print(""""Общая длина контуров": критерий выполняется!""")
else:
    print(""""Общая длина контуров": критерий НЕ выполняется!""")
    count_crit += 1


# Ориентация контуров
if abs(angle_mid_t-angle_mid_s) <= 10:
    print(""""Ориентация контуров": критерий выполняется!""")
else:
    print(""""Ориентация контуров": критерий НЕ выполняется!""")
    count_crit += 1

# Экстремумы контуров
if abs(max(y_max_t)-max(y_max_s)) <= 25:
    print(""""Экстремум по оси Y(max)": критерий выполняется!""")
else:
    print(""""Экстремум по оси Y(max)": критерий НЕ выполняется!""")
    count_crit += 1

if abs(min(y_min_t)-min(y_min_s)) <= 25:
    print(""""Экстремум по оси Y(min)": критерий выполняется!""")
else:
    print(""""Экстремум по оси Y(min)": критерий НЕ выполняется!""")
    count_crit += 1

if abs(max(x_max_t)-max(x_max_s)) <= 25:
    print(""""Экстремум по оси X(max)": критерий выполняется!""")
else:
    print(""""Экстремум по оси X(max)": критерий НЕ выполняется!""")
    count_crit += 1

if abs(min(x_min_t)-min(x_min_s)) <= 25:
    print(""""Экстремум по оси X(min)": критерий выполняется!""")
else:
    print(""""Экстремум по оси X(min)": критерий НЕ выполняется!""")
    count_crit += 1

print("----\nИтог\n----")
print("Выполнено критериев: ", 7-count_crit, " из 7")
if count_crit <= 1:
    print("Роспись подлинная!")
elif 1 < count_crit < 3:
    print("Вероятно, роспись подлинная")
else:
    print("Роспись поддельная!")
