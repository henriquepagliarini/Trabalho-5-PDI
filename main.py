import cv2 as cv
import numpy as np

imgs = [1, 4, 5, 7] 
fundo_path = 'fundo.webp'

img_bg_original = cv.imread(fundo_path)
if img_bg_original is None:
    print(f"Erro ao carregar {fundo_path}.")
    img_bg_original = np.zeros((720, 1280, 3))

for n in imgs:
    img_fg = cv.imread(f"./img/{n}.bmp")
    if img_fg is None:
        print(f"Erro ao carregar a imagem '{n}.bmp.")
        continue
    
    h, w, _ = img_fg.shape
    img_bg = cv.resize(img_bg_original, (w, h))
    
    img_fg = img_fg.astype(np.float32)
    img_bg = img_bg.astype(np.float32)
    
    mask = np.zeros((h, w), dtype=np.uint8)
    out = np.zeros((h, w, 3), dtype=np.uint8)
    
    for y in range(h):
        for x in range(w):
            b, g, r = img_fg[y, x]
            verdice = g - max(b, r)
            
            if (verdice <= 0):
                valor = 255
            else:
                escala = min(verdice, 100) / 100.0
                valor = int(255 * (1.0 - escala))
                valor = max(0, min(255, valor))

            mask[y, x] = valor

            b_fg, g_fg, r_fg = img_fg[y, x]
            px_fg = [b_fg, g_fg, r_fg]
            
            if (0 < valor < 255):
                media = (b_fg + r_fg) / 2.0
                if g_fg > media:
                    px_fg = [b_fg, media, r_fg]
            
            fg = valor / 255.0
            bg = 1.0 - fg
            
            px_bg = img_bg[y, x]
            
            out[y, x] = (np.array(px_fg, dtype=np.float32) * fg) + (px_bg * bg)

    out = np.clip(out, 0, 255).astype(np.uint8)
    cv.imwrite(f"{n}-out.bmp", out)
    cv.imshow(f"{n} - out", out)
    cv.waitKey(0)
    cv.destroyAllWindows()