import cv2 as cv
import numpy as np

imgs = [0, 1, 2, 3, 4, 5, 6, 7] 

for n in imgs:
    img = cv.imread(f"./img/{n}.bmp")
    if img is None:
        print(f"Erro ao carregar a imagem '{n}.bmp.")
    else:
        h , w, _ = img.shape
        
        mask = np.zeros((h, w), dtype=np.uint8)
        
        for y in range(h):
            for x in range(w):
                b, g, r = img[y, x].astype(int)
                
                verdice = g - max(b, r)
                
                if (verdice <= 0):
                    valor = 255
                else:
                    escala = min(verdice, 100) / 100.0
                    valor = int(255 * (1.0 - escala))
                    valor = max(0, min(255, valor))

                mask[y, x] = valor
        
        mask = cv.GaussianBlur(mask, (3, 3), 0)
        cv.imwrite(f"{n}-out.bmp", mask)
        cv.imshow(f"{n} - out", mask)

cv.waitKey(0)
cv.destroyAllWindows()