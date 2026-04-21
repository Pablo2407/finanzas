from PIL import Image, ImageDraw, ImageFont

def crear_icono(tamanio, nombre):
    img = Image.new('RGB', (tamanio, tamanio), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Círculo verde
    margen = tamanio // 8
    draw.ellipse([margen, margen, tamanio-margen, tamanio-margen], fill='#4CAF50')
    
    # Símbolo de dinero
    font_size = tamanio // 2
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    texto = '$'
    bbox = draw.textbbox((0, 0), texto, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text(((tamanio-w)//2, (tamanio-h)//2), texto, fill='white', font=font)
    
    img.save(f'static/{nombre}')
    print(f'{nombre} creado!')

crear_icono(192, 'icon-192.png')
crear_icono(512, 'icon-512.png')