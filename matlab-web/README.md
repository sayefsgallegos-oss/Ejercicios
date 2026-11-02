# Web de matLab (matlab.com.pe)

Web en HTML puro, sin WordPress. Se publica en **Netlify**, guarda los formularios en **Supabase** y los cambios se suben con **GitHub**.

## ¿Qué archivo toco para cambiar…?

| Quiero cambiar… | Archivo |
|---|---|
| Teléfono, WhatsApp, correos, redes, libro de reclamaciones | `js/config.js` |
| Aviso de temporada (la franja roja debajo del carrusel) | `js/config.js` → `avisoTemporada` |
| Horarios, grados y precios S.O.S. de los formularios | `js/config.js` |
| Banners del carrusel | `js/datos.js` → `banners` *(o Supabase, tabla `banners`)* |
| Textos, video, beneficios o mensaje de WhatsApp de un programa | `js/datos.js` → `programas` *(o Supabase, tabla `programas`)* |
| Activar o quitar un programa | `activo: true/false` y `en_home: true/false` en el programa |
| **Profesores y equipo** (entran o salen) | `js/datos.js` → `equipo` *(o Supabase, tabla `equipo`)* |
| Textos fijos del inicio, Nosotros, S.O.S., Contáctanos | El `index.html` de cada carpeta |
| Colores de la marca | `css/estilos.css`, al inicio (`:root`) |
| Imágenes | Carpeta `img/` (usa formato `.webp`, máximo ~300 KB) |

### Agregar o quitar un profesor
1. Sube su foto cuadrada a `img/equipo/` (ej. `juan-perez.webp`).
2. En `js/datos.js`, dentro de `equipo`, copia una línea y cambia los datos:
   ```js
   { nombre: "Juan Pérez", cargo: "Profesor de Matemática", foto: "/img/equipo/juan-perez.webp", orden: 17, activo: true },
   ```
3. Si alguien se va, cambia su `activo: true` por `activo: false`.

### Cambiar un banner
Cada banner necesita 2 imágenes: escritorio (2560×947) y celular (1313×1563). Súbelas a `img/banners/` y edita la lista `banners` en `js/datos.js`.

## Estructura (las mismas URLs de la web anterior)

```
index.html                                   Inicio
programas/integrales-individuales/           Lista de programas individuales
  programa-anual-elite/                      Anual Élite
  programa-mensual-power/                    Mensual Power
programas/talleres-grupales/                 Lista de talleres grupales
  mateinnovando/                             Mateinnovando
  finanzas-para-jovenes/                     Taller Financiero
clases-de-emergencia/                        Clases S.O.S. (reserva en 2 pasos)
nosotros/                                    Nosotros + equipo
contactanos/                                 Contáctanos
registro-de-notas-matlab/                    Portal para Padres (en pausa)
css/estilos.css · js/config.js · js/datos.js · js/main.js
supabase/esquema.sql · supabase/datos-iniciales.sql
```

Todas las páginas de programa usan **la misma plantilla**: para crear un programa nuevo se copia la carpeta de uno existente, se cambia el `data-slug` y se agrega el programa en `datos.js`.

## Probar en tu computadora

```bash
cd matlab-web
python3 -m http.server 8000
```
Abre http://localhost:8000. En modo local los formularios **no se envían** (se ven en la consola del navegador), y Analytics/Pixel no se activan.

## Publicar en Netlify
1. Netlify → *Add new site* → *Import from GitHub* → elige el repositorio.
2. **Base directory:** `matlab-web` · **Build command:** (vacío) · **Publish directory:** `matlab-web`.
3. *Forms* → activar detección de formularios → *Form notifications* → correo a `administracionsb@matlab.com.pe` para los formularios `contacto` y `reserva-sos`.
4. Al final, *Domain management* → conectar `matlab.com.pe`.

Cada vez que se sube un cambio a GitHub, Netlify publica solo en ~1 minuto.

## Conectar Supabase
1. Crear proyecto en https://supabase.com (región São Paulo, la más cercana a Perú).
2. *SQL Editor* → pegar `supabase/esquema.sql` → *Run*. Luego `supabase/datos-iniciales.sql` → *Run*.
3. *Project Settings → API*: copiar **Project URL** y **anon public key** en `js/config.js` (`supabaseUrl`, `supabaseAnonKey`). Esa clave es pública a propósito: la seguridad está en las reglas (RLS) del esquema, que solo permiten a la web **crear** contactos y **leer** contenido.
4. Desde ese momento:
   - Los contactos llegan a la tabla **`leads`** (con programa, grado, horario, página y campaña de anuncio). Tu equipo puede marcar `estado` y `asesora`.
   - Las reservas S.O.S. llegan a **`reservas_sos`**.
   - Banners, programas y equipo se editan desde *Table Editor*, como una hoja de cálculo, sin tocar código.

## Medición
Se mantienen los mismos códigos de la web anterior (Google Analytics `G-15QK6CYNE1`, Tag Manager, Meta Pixel y Microsoft Clarity). **Solo se activan en `matlab.com.pe`**, para que las pruebas no ensucien las estadísticas. Además, se registra un evento **Lead** al enviar un formulario y **Contact** al hacer clic en WhatsApp.

## Pendientes
- [ ] Confirmar grados de Mateinnovando (`para_quien` en `datos.js`).
- [ ] Cargos del equipo (`cargo` en `datos.js`).
- [ ] Fase 2 S.O.S.: pago automático con Mercado Pago.
- [ ] Portal para Padres conectado al sistema interno.
