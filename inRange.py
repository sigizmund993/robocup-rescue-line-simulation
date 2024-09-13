import numpy as np
import cv2
# создаем пустую функцию 
def nothing(args):pass

# создаем окно для отображения результата и бегунки
cv2.namedWindow("setup")
cv2.createTrackbar("b1", "setup", 0, 255, nothing)
cv2.createTrackbar("g1", "setup", 0, 255, nothing)
cv2.createTrackbar("r1", "setup", 50, 255, nothing)
cv2.createTrackbar("b2", "setup", 219, 255, nothing)
cv2.createTrackbar("g2", "setup", 219, 255, nothing)
cv2.createTrackbar("r2", "setup", 215, 255, nothing)

fn = "frame.png" # путь к файлу с картинкой
img = cv2.imread(fn) # загрузка изображения

while True:
    r1 = cv2.getTrackbarPos('r1', 'setup')
    g1 = cv2.getTrackbarPos('g1', 'setup')
    b1 = cv2.getTrackbarPos('b1', 'setup')
    r2 = cv2.getTrackbarPos('r2', 'setup')
    g2 = cv2.getTrackbarPos('g2', 'setup')
    b2 = cv2.getTrackbarPos('b2', 'setup')
    # собираем значения из бегунков в множества
    min_p = (0, 0, 50)
    max_p = (215, 215, 215)
    # применяем фильтр, делаем бинаризацию
    img_g = cv2.inRange(img, min_p, max_p)

    cv2.imshow('img', img_g)
    ready = cv2.bitwise_and(img, img, mask = img_g)
    cv2.imshow('results', ready)
    if cv2.waitKey(33) & 0xFF == ord('q'):
         break

cv2.destroyAllWindows()