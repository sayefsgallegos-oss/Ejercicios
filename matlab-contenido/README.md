# matLab · Contenido en código

Videos y piezas gráficas de matLab Perú generados con programación (Python + Cairo + NumPy + FFmpeg + Pillow).

## Entregables listos (`entregables/`)

| Carpeta | Contenido |
|---|---|
| `videos/reto_*.mp4` | Retos del día (saludos, porcentaje, potencias, consecutivos) |
| `videos/equis_ep1_balanza.mp4` | Serie "Equis busca su valor", episodio 1 |
| `videos/robots_reto_maquinas.mp4` | Matti y Numi presentan: el reto del día |
| `videos/robots_error404.mp4` | Error 404: Numi se equivocó |
| `videos/robots_novela_cap1.mp4` | La señal perdida, capítulo 1 |
| `videos/robots_novela_cap2.mp4` | La señal perdida, capítulo 2 |
| `videos/robots_novela_cap3.mp4` | La señal perdida, capítulo 3 |
| `carrusel_errores/` | Carrusel "Errores comunes" (5 láminas 1080×1350) |
| `campana_rescate/` | Campaña "Misión Rescate" (3 posts + 1 historia, flyer único y flyer A5 en PDF para imprenta, con QR a WhatsApp) |
| `campana_verano/` | Campaña "Verano 2027" (2 posts + 1 historia) |

## Personajes (`assets/robots_v2/`)

Poses recortadas con fondo transparente:

- `matti_emo*`, `matti_acc*`, `matti_prof*`, `matti_nov_*`: Matti (emociones, acción, profesor, novela)
- `numi_a*` … `numi_d*`: Numi (alegre, emociones, novela, retos)
- `equis*`: Equis · `carbon_cero_*`: Señor Cero (gris carbón) · `num_1`…`num_9` y `siete*`: habitantes de Matemópolis

`assets/robots/` tiene las poses originales y `assets/logo.png` el logo.

`mision.py` dibuja la tarjeta "Misión para ti" del final de cada capítulo; `assets/ganador_capN.png` es la captura del primero en acertar.

## Cómo generar un video

Requisitos: Python 3 con `pycairo`, `numpy`, `scipy`, `pillow`, `qrcode`, y `ffmpeg`.
Instalar las fuentes de `fuentes/` en el sistema (Fredoka, Nunito, Poppins).

```bash
python3 rr_novela_cap2.py              # video completo -> out/robots_novela_cap2.mp4
python3 rr_novela_cap2.py --frame 12   # un cuadro de prueba en el segundo 12
python3 campana_rescate.py             # flyers -> out/campana_rescate/
```

## Herramientas para poses nuevas generadas con IA

```bash
python3 -I quitar_croma.py hoja.png out/hoja_alpha.png magenta   # fondo magenta o verde liso
python3 -I quitar_negro.py hoja.png out/hoja_alpha.png           # fondo negro
python3 -I separar_poses.py out/hoja_alpha.png assets/robots_v2 nombre   # una pose por archivo
python3 -I recolorear.py pose.png pose_nueva.png carbon           # cambiar color del cuerpo
```

Pedir a la IA siempre **fondo de color liso** (magenta #FF00FF o verde #00FF00); los cuadritos "dibujados" y los fondos con brillo no se pueden recortar bien.
