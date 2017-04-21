import cv2
import sys

# Аргументы командной строки

#  ----
sys.argv[1] = "1.png"
sys.argv[2] = sys.argv[1]
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

# Загрузка изображения
img = cv2.imread(template_filename)

# 
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

