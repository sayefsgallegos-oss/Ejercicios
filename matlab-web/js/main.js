/* =====================================================================
   LÓGICA DE LA WEB DE MATLAB
   No necesitas tocar este archivo para cambiar textos: usa
   js/config.js y js/datos.js (o Supabase cuando esté conectado).
   ===================================================================== */
(function () {
  "use strict";

  const C = window.MATLAB_CONFIG;
  const $ = (sel, raiz = document) => raiz.querySelector(sel);
  const $$ = (sel, raiz = document) => Array.from(raiz.querySelectorAll(sel));
  const esc = (t) => String(t ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const enLocal = ["localhost", "127.0.0.1", ""].includes(location.hostname);
  const supabaseActivo = Boolean(C.supabaseUrl && C.supabaseAnonKey);

  /* ------------------------------------------------------------------
     ÍCONOS
     ------------------------------------------------------------------ */
  const ICONOS = {
    clases: '<rect x="8" y="8" width="32" height="22" rx="2"/><path d="M4 36h40l-3 4H7z"/><path d="M24 13v13M24 13c-3-2-7-2-10 0v13c3-2 7-2 10 0 3-2 7-2 10 0V13c-3-2-7-2-10 0"/>',
    reloj: '<circle cx="24" cy="24" r="19"/><path d="M24 11v13l9 7"/><path d="M24 6v2M24 40v2M6 24h2M40 24h2"/>',
    virtual: '<rect x="4" y="6" width="30" height="22" rx="2"/><path d="M13 34h12M19 28v6"/><circle cx="19" cy="15" r="4"/><path d="M12 25c1.5-3 4-4.5 7-4.5s5.5 1.5 7 4.5"/><circle cx="37" cy="31" r="4"/><path d="M30 44c1-4 4-6 7-6s6 2 7 6"/>',
    seguimiento: '<path d="M4 40l10-12 8 6 9-12"/><circle cx="35" cy="14" r="8"/><path d="M41 20l5 5"/><path d="M35 10v4l3 2"/>',
    grupo: '<circle cx="24" cy="15" r="6"/><path d="M13 38c1-7 5.5-10 11-10s10 3 11 10"/><circle cx="10" cy="19" r="4.5"/><path d="M2 36c.6-5 3.5-7.5 8-7.5"/><circle cx="38" cy="19" r="4.5"/><path d="M46 36c-.6-5-3.5-7.5-8-7.5"/>',
    check: '<circle cx="24" cy="24" r="19"/><path d="M15 24.5l6 6 12-13"/>',
    colegio: '<path d="M6 42V22l18-10 18 10v20"/><path d="M2 42h44"/><path d="M19 42V32h10v10"/><path d="M24 12V4h8v4h-8"/><rect x="10" y="26" width="5" height="5"/><rect x="33" y="26" width="5" height="5"/><circle cx="24" cy="22" r="3"/>',
  };
  const icono = (nombre) => `<svg viewBox="0 0 48 48" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${ICONOS[nombre] || ICONOS.check}</svg>`;

  const SOCIAL = {
    whatsapp: '<path d="M12 2.2a9.8 9.8 0 0 0-8.4 14.8L2.2 21.8l4.9-1.3A9.8 9.8 0 1 0 12 2.2z" fill="none" stroke="currentColor" stroke-width="1.9"/><path d="M8.6 7.3c.2-.4.4-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .6l-.5.7c-.1.2-.2.3 0 .6.5.8 1.1 1.5 1.9 2 .3.2.6.4 1 .5.2.1.4.1.6-.1l.7-.8c.2-.2.4-.2.6-.1l1.8.9c.2.1.4.2.4.3.1.2.1.9-.3 1.5-.4.6-1.4 1.1-2 1.1-.6 0-1.3.1-3.5-.9-2.6-1.2-4.2-3.9-4.3-4.1-.1-.2-1-1.3-1-2.6 0-1.2.6-1.8.9-2.1z"/>',
    facebook: '<path d="M14 8h3V4h-3c-2.8 0-4.5 1.8-4.5 4.6V11H7v4h2.5v7h4v-7h3l.5-4h-3.5V9c0-.6.4-1 1-1z"/>',
    instagram: '<rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.5" cy="6.5" r="1.3"/>',
    tiktok: '<path d="M16.5 3c.4 2.2 1.8 3.7 4 4v3.2c-1.5 0-2.9-.5-4-1.2V15a6 6 0 1 1-6-6h.6v3.3a2.8 2.8 0 1 0 2.2 2.7V3z"/>',
    youtube: '<path fill-rule="evenodd" d="M22 8.2a3 3 0 0 0-2.1-2.1C18 5.6 12 5.6 12 5.6s-6 0-7.9.5A3 3 0 0 0 2 8.2 31 31 0 0 0 1.6 12 31 31 0 0 0 2 15.8a3 3 0 0 0 2.1 2.1c1.9.5 7.9.5 7.9.5s6 0 7.9-.5a3 3 0 0 0 2.1-2.1c.4-1.2.4-3.8.4-3.8s0-2.6-.4-3.8zM10 15V9l5.2 3z"/>',
    correo: '<rect x="2.5" y="5" width="19" height="14" rx="2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 6.5l9 6.5 9-6.5" fill="none" stroke="currentColor" stroke-width="2"/>',
  };
  const social = (n) => `<svg viewBox="0 0 24 24" aria-hidden="true">${SOCIAL[n]}</svg>`;

  /* ------------------------------------------------------------------
     WHATSAPP
     ------------------------------------------------------------------ */
  const linkWhatsapp = (texto) => `https://wa.me/${C.whatsapp}?text=${encodeURIComponent(texto || C.mensajes.general)}`;

  /* ------------------------------------------------------------------
     DATOS (Supabase o respaldo local)
     ------------------------------------------------------------------ */
  async function leerTabla(tabla, orden = "orden") {
    const local = (window.MATLAB_DATOS[tabla] || []).filter((x) => x.activo !== false).sort((a, b) => (a[orden] ?? 0) - (b[orden] ?? 0));
    if (!supabaseActivo) return local;
    try {
      const r = await fetch(`${C.supabaseUrl}/rest/v1/${tabla}?select=*&activo=eq.true&order=${orden}.asc`, {
        headers: { apikey: C.supabaseAnonKey, Authorization: `Bearer ${C.supabaseAnonKey}` },
      });
      if (!r.ok) throw new Error(r.status);
      const filas = await r.json();
      return filas.length ? filas : local;
    } catch (e) {
      console.warn(`No se pudo leer "${tabla}" de Supabase, uso datos locales.`, e);
      return local;
    }
  }
  let _programas;
  const programas = () => (_programas ||= leerTabla("programas"));

  /* ------------------------------------------------------------------
     MEDICIÓN (Analytics, Tag Manager, Pixel, Clarity)
     Solo en el dominio real.
     ------------------------------------------------------------------ */
  const M = C.medicion;
  const medicionActiva = M.dominios.includes(location.hostname);
  function cargarScript(src) { const s = document.createElement("script"); s.async = true; s.src = src; document.head.appendChild(s); }
  if (medicionActiva) {
    if (M.googleTagManager) {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
      cargarScript(`https://www.googletagmanager.com/gtm.js?id=${M.googleTagManager}`);
    }
    if (M.googleAnalytics) {
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date());
      window.gtag("config", M.googleAnalytics);
      cargarScript(`https://www.googletagmanager.com/gtag/js?id=${M.googleAnalytics}`);
    }
    if (M.metaPixel) {
      /* eslint-disable */
      !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
      /* eslint-enable */
      window.fbq("init", M.metaPixel);
      window.fbq("track", "PageView");
    }
    if (M.clarity) {
      window.clarity = window.clarity || function () { (window.clarity.q = window.clarity.q || []).push(arguments); };
      cargarScript(`https://www.clarity.ms/tag/${M.clarity}`);
    }
  }
  function medir(evento, datos = {}) {
    if (!medicionActiva) { console.info("[medición de prueba]", evento, datos); return; }
    try {
      if (window.gtag) window.gtag("event", evento === "Lead" ? "generate_lead" : "contact", datos);
      if (window.fbq) window.fbq("track", evento, datos);
    } catch (e) { /* nada */ }
  }

  /* Guardar de dónde vino la visita (anuncios con ?utm_source=...) */
  const UTM = (() => {
    const p = new URLSearchParams(location.search);
    let guardado = {};
    try { guardado = JSON.parse(sessionStorage.getItem("matlab_utm") || "{}"); } catch (e) { /* sin almacenamiento */ }
    const nuevo = {};
    ["utm_source", "utm_medium", "utm_campaign"].forEach((k) => { if (p.get(k)) nuevo[k] = p.get(k); });
    if (Object.keys(nuevo).length) { guardado = nuevo; try { sessionStorage.setItem("matlab_utm", JSON.stringify(nuevo)); } catch (e) { /* nada */ } }
    return guardado;
  })();

  /* ------------------------------------------------------------------
     CABECERA Y PIE (iguales en todas las páginas)
     ------------------------------------------------------------------ */
  async function pintarCabecera() {
    const lugar = $("#cabecera");
    if (!lugar) return;
    const progs = await programas();
    const ruta = location.pathname;
    const item = (p) => `<li><a href="${esc(p.url)}">${esc(p.nombre === "Clase S.O.S." ? "Clases de Emergencia S.O.S." : p.nombre)}</a></li>`;
    const individuales = progs.filter((p) => p.tipo === "individual" || p.tipo === "sos").map(item).join("");
    const grupales = progs.filter((p) => p.tipo === "grupal").map(item).join("");
    const activo = (cond) => (cond ? ' class="activo"' : "");

    lugar.outerHTML = `
      <div class="barra-superior"><div class="contenedor"><a href="/registro-de-notas-matlab/">Portal para Padres</a></div></div>
      <header class="cabecera cuadricula" id="cabecera">
        <div class="contenedor">
          <a class="logo" href="/" aria-label="matLab - Inicio"><img src="/img/logo-matlab-14.webp" alt="matLab 14 años" width="465" height="294"></a>
          <button class="boton-menu" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu-principal"><span></span><span></span><span></span></button>
          <nav aria-label="Menú principal">
            <ul class="menu" id="menu-principal">
              <li class="cerrar-menu"><button class="boton-menu" aria-label="Cerrar menú" style="display:block">✕</button></li>
              <li><a href="/"${activo(ruta === "/" || ruta === "/index.html")}>Inicio</a></li>
              <li>
                <button class="menu-desplegar${ruta.startsWith("/programas") || ruta.startsWith("/clases-de-emergencia") ? " activo" : ""}" aria-expanded="false">Programas <i class="flecha"></i></button>
                <ul class="submenu">
                  <li><a class="sub-titulo" href="/programas/integrales-individuales/">Individuales <i class="flecha-der"></i></a><ul class="submenu">${individuales}</ul></li>
                  <li><a class="sub-titulo" href="/programas/talleres-grupales/">Grupales <i class="flecha-der"></i></a><ul class="submenu">${grupales}</ul></li>
                </ul>
              </li>
              <li><a href="/nosotros/"${activo(ruta.startsWith("/nosotros"))}>Nosotros</a></li>
              <li><a class="boton boton-verde" href="/contactanos/">Contáctanos</a></li>
            </ul>
          </nav>
        </div>
      </header>`;

    const cab = $("#cabecera");
    const menu = $("#menu-principal");
    const abrir = $(".contenedor > .boton-menu", cab);
    let fondo;
    const cerrarMenu = () => { menu.classList.remove("abierto"); abrir.setAttribute("aria-expanded", "false"); fondo?.remove(); fondo = null; document.body.style.overflow = ""; };
    abrir.addEventListener("click", () => {
      menu.classList.add("abierto"); abrir.setAttribute("aria-expanded", "true"); document.body.style.overflow = "hidden";
      fondo = document.createElement("div"); fondo.className = "fondo-menu"; fondo.addEventListener("click", cerrarMenu); cab.appendChild(fondo);
    });
    $(".cerrar-menu button", cab).addEventListener("click", cerrarMenu);
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") cerrarMenu(); });

    // En celular, los títulos de submenú abren/cierran en vez de navegar.
    const esMovil = () => matchMedia("(max-width: 960px)").matches;
    $$(".menu-desplegar, .sub-titulo", cab).forEach((b) => b.addEventListener("click", (e) => {
      if (b.classList.contains("sub-titulo") && !esMovil()) return;
      e.preventDefault();
      const li = b.parentElement; const abierto = li.classList.toggle("abierto");
      if (b.matches("button")) b.setAttribute("aria-expanded", String(abierto));
    }));
    document.addEventListener("click", (e) => { if (!esMovil() && !e.target.closest(".menu")) $$(".menu li.abierto", cab).forEach((li) => li.classList.remove("abierto")); });

    const sombra = () => cab.classList.toggle("con-sombra", window.scrollY > 40);
    window.addEventListener("scroll", sombra, { passive: true }); sombra();
  }

  function pintarPie() {
    const lugar = $("#pie");
    if (!lugar) return;
    const r = C.redes;
    lugar.outerHTML = `
      <footer class="pie">
        <div class="contenedor">
          <div class="pie-arriba">
            <div class="pie-marca"><img src="/img/logo-matlab.webp" alt="matLab" width="256" height="256" loading="lazy"><span>© ${new Date().getFullYear()} matLab · Todos los derechos reservados</span></div>
            <ul class="pie-menu">
              <li><a href="/">Inicio</a></li>
              <li><a href="/programas/integrales-individuales/">Programas individuales</a></li>
              <li><a href="/programas/talleres-grupales/">Talleres grupales</a></li>
              <li><a href="/clases-de-emergencia/">Clases S.O.S.</a></li>
              <li><a href="/nosotros/">Nosotros</a></li>
              <li><a class="boton boton-verde" href="/contactanos/">Contáctanos</a></li>
            </ul>
          </div>
          <div class="pie-abajo">
            <div>
              <a href="${esc(C.libroReclamaciones)}" target="_blank" rel="noopener">Libro de reclamaciones</a>
              <div class="pie-datos">WhatsApp: <a href="${linkWhatsapp(C.mensajes.general)}" data-medir="whatsapp" target="_blank" rel="noopener">${esc(C.telefonoVisible)}</a> · Empresas: <a href="mailto:${esc(C.correoEmpresas)}">${esc(C.correoEmpresas)}</a></div>
            </div>
            <div class="redes"><span>Síguenos en:</span>
              <a href="${esc(r.facebook)}" target="_blank" rel="noopener" aria-label="Facebook">${social("facebook")}</a>
              <a href="${esc(r.instagram)}" target="_blank" rel="noopener" aria-label="Instagram">${social("instagram")}</a>
              <a href="${esc(r.tiktok)}" target="_blank" rel="noopener" aria-label="TikTok">${social("tiktok")}</a>
              <a href="${esc(r.youtube)}" target="_blank" rel="noopener" aria-label="YouTube">${social("youtube")}</a>
            </div>
          </div>
        </div>
      </footer>`;
  }

  function pintarWhatsappFlotante() {
    const texto = document.body.dataset.whatsapp || C.mensajes.flotante;
    const a = document.createElement("a");
    a.className = "whatsapp-flotante";
    a.href = linkWhatsapp(texto);
    a.target = "_blank"; a.rel = "noopener";
    a.dataset.medir = "whatsapp";
    a.setAttribute("aria-label", "Escríbenos por WhatsApp");
    a.innerHTML = `${social("whatsapp")}<span>¡Contáctanos!</span>`;
    document.body.appendChild(a);
  }

  /* Enlaces con data-whatsapp="clave" o data-whatsapp-texto="..." */
  function activarEnlacesWhatsapp(raiz = document) {
    $$("[data-whatsapp], [data-whatsapp-texto]", raiz).forEach((a) => {
      if (a === document.body) return;
      const texto = a.dataset.whatsappTexto || C.mensajes[a.dataset.whatsapp] || C.mensajes.general;
      a.href = linkWhatsapp(texto); a.target = "_blank"; a.rel = "noopener"; a.dataset.medir = "whatsapp";
    });
  }
  document.addEventListener("click", (e) => {
    const a = e.target.closest("[data-medir='whatsapp']");
    if (a) medir("Contact", { canal: "whatsapp", pagina: location.pathname });
  });

  /* ------------------------------------------------------------------
     CARRUSEL
     ------------------------------------------------------------------ */
  async function pintarCarrusel() {
    const lugar = $("#carrusel");
    if (!lugar) return;
    const banners = await leerTabla("banners");
    if (!banners.length) { lugar.remove(); return; }
    lugar.innerHTML = `
      <div class="carrusel-pista">${banners.map((b, i) => `
        <a class="carrusel-slide" href="${esc(b.link || "#")}" aria-label="${esc(b.titulo)}" ${i ? 'aria-hidden="true" tabindex="-1"' : ""}>
          <picture>
            ${b.imagen_movil ? `<source media="(max-width: 700px)" srcset="${esc(b.imagen_movil)}">` : ""}
            <img src="${esc(b.imagen)}" alt="${esc(b.titulo)}" width="1920" height="710" ${i ? 'loading="lazy"' : 'fetchpriority="high"'}>
          </picture>
        </a>`).join("")}
      </div>
      ${banners.length > 1 ? `
        <button class="carrusel-flecha izq" aria-label="Anterior">❮</button>
        <button class="carrusel-flecha der" aria-label="Siguiente">❯</button>
        <div class="carrusel-puntos">${banners.map((_, i) => `<button aria-label="Ir al banner ${i + 1}"${i ? "" : ' class="activo"'}></button>`).join("")}</div>` : ""}`;

    if (banners.length < 2) return;
    const pista = $(".carrusel-pista", lugar);
    const slides = $$(".carrusel-slide", lugar);
    const puntos = $$(".carrusel-puntos button", lugar);
    let actual = 0, timer;
    const ir = (n) => {
      actual = (n + slides.length) % slides.length;
      pista.style.transform = `translateX(-${actual * 100}%)`;
      puntos.forEach((p, i) => p.classList.toggle("activo", i === actual));
      slides.forEach((s, i) => { s.setAttribute("aria-hidden", String(i !== actual)); s.tabIndex = i === actual ? 0 : -1; });
    };
    const reiniciar = () => { clearInterval(timer); if (!matchMedia("(prefers-reduced-motion: reduce)").matches) timer = setInterval(() => ir(actual + 1), 6000); };
    $(".izq", lugar).addEventListener("click", () => { ir(actual - 1); reiniciar(); });
    $(".der", lugar).addEventListener("click", () => { ir(actual + 1); reiniciar(); });
    puntos.forEach((p, i) => p.addEventListener("click", () => { ir(i); reiniciar(); }));
    lugar.addEventListener("mouseenter", () => clearInterval(timer));
    lugar.addEventListener("mouseleave", reiniciar);
    // deslizar con el dedo
    let x0 = null;
    lugar.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
    lugar.addEventListener("touchend", (e) => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 40) { ir(actual + (dx < 0 ? 1 : -1)); reiniciar(); }
      x0 = null;
    });
    reiniciar();
  }

  function pintarAviso() {
    const lugar = $("#aviso-temporada");
    if (!lugar) return;
    const a = C.avisoTemporada;
    if (!a || !a.activo) { lugar.remove(); return; }
    lugar.className = "aviso";
    lugar.innerHTML = `<div class="contenedor"><span>${a.texto}</span><a class="boton boton-blanco" href="${esc(a.link)}">${esc(a.boton)}</a></div>`;
  }

  /* ------------------------------------------------------------------
     TARJETAS DE PROGRAMAS
     ------------------------------------------------------------------ */
  async function pintarTarjetas() {
    for (const lugar of $$("[data-tarjetas]")) {
      const filtro = lugar.dataset.tarjetas; // "home" | "individual" | "grupal"
      const lista = (await programas()).filter((p) => filtro === "home" ? p.en_home : p.tipo === filtro || (filtro === "individual" && p.tipo === "sos"));
      lugar.innerHTML = lista.map((p) => `
        <article class="cuaderno aparece">
          ${filtro === "home" ? `<span class="etiqueta">${p.tipo === "grupal" ? "Grupal" : "Individual"}</span>` : ""}
          <h3>${esc(p.nombre)}</h3>
          <p>${esc(p.resumen)}</p>
          <a class="boton boton-rojo" href="${esc(p.url)}">¡Quiero saber más!</a>
        </article>`).join("");
    }
    const pedido = $("#a-pedido");
    if (pedido && C.programasAPedido?.length) {
      pedido.innerHTML = `¿Buscas otro programa? También dictamos <strong>${C.programasAPedido.map(esc).join(", ")}</strong>. <a href="${linkWhatsapp(C.mensajes.otroPrograma)}" data-medir="whatsapp" target="_blank" rel="noopener">Escríbenos por WhatsApp</a>`;
    }
  }

  /* ------------------------------------------------------------------
     VIDEOS DE YOUTUBE (se cargan solo al hacer clic: la web va más rápido)
     ------------------------------------------------------------------ */
  function htmlVideo(id, miniatura, titulo = "Ver video") {
    return `<button class="video" type="button" data-youtube="${esc(id)}" aria-label="${esc(titulo)}">
      <img src="${esc(miniatura || `https://i.ytimg.com/vi/${id}/hqdefault.jpg`)}" alt="" loading="lazy"><span class="play"></span></button>`;
  }
  document.addEventListener("click", (e) => {
    const v = e.target.closest(".video[data-youtube]");
    if (!v) return;
    const marco = document.createElement("div");
    marco.className = "video";
    marco.innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${encodeURIComponent(v.dataset.youtube)}?autoplay=1&rel=0" title="Video de matLab" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>`;
    v.replaceWith(marco);
  });
  function activarVideos() {
    $$("[data-video]").forEach((d) => { d.outerHTML = htmlVideo(d.dataset.video, d.dataset.miniatura, d.dataset.titulo); });
  }

  /* ------------------------------------------------------------------
     FORMULARIOS
     ------------------------------------------------------------------ */
  const opciones = (lista, placeholder) => `<option value="">${esc(placeholder)}</option>` + lista.map((o) => `<option>${esc(o)}</option>`).join("");
  const campo = (html, error = "Completa este campo") => `<div class="campo">${html}<div class="mensaje-error">${error}</div></div>`;

  async function htmlFormulario(tipo, programa) {
    const progs = await programas();
    let campos = "";
    const nombreCompleto = campo('<label class="solo-lectores" for="f-nombre">Nombres y apellidos</label><input id="f-nombre" name="nombre" placeholder="Nombres y apellidos" autocomplete="name" required>');
    const celular = campo('<label class="solo-lectores" for="f-celular">Celular</label><input id="f-celular" name="celular" type="tel" inputmode="tel" placeholder="Celular" autocomplete="tel" required pattern="[0-9+ ]{9,15}">', "Ingresa un celular válido (9 dígitos)");
    const grado = campo(`<label class="solo-lectores" for="f-grado">Grado</label><select id="f-grado" name="grado" required>${opciones(C.grados, "Grado*")}</select>`, "Elige el grado");

    if (tipo === "home") {
      campos = nombreCompleto + celular +
        campo(`<label class="solo-lectores" for="f-programa">Programa de interés</label><select id="f-programa" name="programa" required>${opciones([...progs.map((p) => p.nombre), "Otro programa"], "Programa de interés")}</select>`, "Elige un programa");
    } else if (tipo === "individual") {
      campos = nombreCompleto + celular + grado +
        campo(`<label class="solo-lectores" for="f-horario">Horario</label><select id="f-horario" name="horario" required>${opciones(C.horariosIndividuales, "Horario a elegir")}</select>`, "Elige un horario");
    } else if (tipo === "grupal") {
      campos = nombreCompleto + celular + grado +
        campo(`<label class="solo-lectores" for="f-frecuencia">Frecuencia</label><select id="f-frecuencia" name="frecuencia" required>${opciones(Object.keys(C.horariosGrupales), "Frecuencia de interés*")}</select>`, "Elige una frecuencia") +
        campo(`<label class="solo-lectores" for="f-horario">Horario</label><select id="f-horario" name="horario" required disabled><option value="">Horario de interés* (elige frecuencia)</option></select>`, "Elige un horario");
    } else if (tipo === "contacto") {
      campos =
        campo('<label class="solo-lectores" for="f-nombre">Nombres</label><input id="f-nombre" name="nombre" placeholder="Nombres" autocomplete="given-name" required>') +
        campo('<label class="solo-lectores" for="f-apellido">Apellidos</label><input id="f-apellido" name="apellido" placeholder="Apellidos" autocomplete="family-name" required>') +
        campo('<label class="solo-lectores" for="f-correo">Correo</label><input id="f-correo" name="correo" type="email" placeholder="Correo electrónico" autocomplete="email" required>', "Ingresa un correo válido") +
        celular +
        campo(`<label class="solo-lectores" for="f-servicio">Servicio</label><select id="f-servicio" name="servicio" required>${opciones(C.serviciosContacto, "Servicio de interés")}</select>`, "Elige un servicio");
    }
    return `
      <form class="formulario" novalidate data-tipo="${tipo}" ${programa ? `data-programa="${esc(programa)}"` : ""}>
        ${campos}
        <input class="trampa" name="sitio_web" tabindex="-1" autocomplete="off" aria-hidden="true">
        <label class="check"><input type="checkbox" name="acepta" required> <span>Acepto el uso de mis datos para que matLab me contacte.</span></label>
        <button class="boton boton-rojo" type="submit">Enviar</button>
        <div class="form-estado oculto" role="status" aria-live="polite"></div>
      </form>`;
  }

  async function enviarDatos(tabla, formNetlify, datos) {
    const intentos = [];
    if (supabaseActivo) {
      intentos.push(fetch(`${C.supabaseUrl}/rest/v1/${tabla}`, {
        method: "POST",
        headers: { apikey: C.supabaseAnonKey, Authorization: `Bearer ${C.supabaseAnonKey}`, "Content-Type": "application/json", Prefer: "return=minimal" },
        body: JSON.stringify(datos),
      }).then((r) => { if (!r.ok) throw new Error("Supabase " + r.status); }));
    }
    if (!enLocal) { // Netlify Forms: avisa por correo
      const cuerpo = new URLSearchParams({ "form-name": formNetlify });
      Object.entries(datos).forEach(([k, v]) => cuerpo.append(k, v == null ? "" : String(v)));
      intentos.push(fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: cuerpo.toString() })
        .then((r) => { if (!r.ok) throw new Error("Netlify " + r.status); }));
    }
    if (!intentos.length) { console.info("[modo prueba] Datos que se enviarían:", tabla, datos); return true; }
    const res = await Promise.allSettled(intentos);
    res.filter((x) => x.status === "rejected").forEach((x) => console.warn(x.reason));
    return res.some((x) => x.status === "fulfilled");
  }

  function validar(form) {
    let ok = true;
    $$(".campo", form).forEach((c) => {
      const el = $("input, select", c);
      const valido = el.disabled ? true : el.checkValidity() && String(el.value).trim() !== "";
      c.classList.toggle("error", !valido);
      if (!valido && ok) { el.focus(); ok = false; }
    });
    const acepta = $('[name="acepta"]', form);
    if (acepta && !acepta.checked) { if (ok) acepta.focus(); acepta.closest(".check").style.color = "#fff3a6"; ok = false; }
    else if (acepta) acepta.closest(".check").style.color = "";
    return ok;
  }

  function activarFormulario(form, programaObj) {
    // horarios dependientes (talleres grupales)
    const frec = $('[name="frecuencia"]', form);
    if (frec) frec.addEventListener("change", () => {
      const sel = $('[name="horario"]', form);
      const lista = C.horariosGrupales[frec.value] || [];
      sel.innerHTML = opciones(lista, lista.length ? "Horario de interés*" : "Horario de interés* (elige frecuencia)");
      sel.disabled = !lista.length;
    });
    $$("input, select", form).forEach((el) => el.addEventListener("input", () => el.closest(".campo")?.classList.remove("error")));

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if ($(".trampa", form).value) return; // robot
      if (!validar(form)) return;
      const fd = new FormData(form);
      const datos = {
        nombre: fd.get("nombre")?.trim(),
        apellido: fd.get("apellido")?.trim() || null,
        celular: fd.get("celular")?.trim(),
        correo: fd.get("correo")?.trim() || null,
        programa: fd.get("programa") || form.dataset.programa || null,
        grado: fd.get("grado") || null,
        frecuencia: fd.get("frecuencia") || null,
        horario: fd.get("horario") || null,
        servicio: fd.get("servicio") || null,
        pagina: location.pathname,
        utm_source: UTM.utm_source || null, utm_medium: UTM.utm_medium || null, utm_campaign: UTM.utm_campaign || null,
        acepta: true,
      };
      const boton = $('button[type="submit"]', form);
      const estado = $(".form-estado", form);
      boton.disabled = true; boton.textContent = "Enviando…";
      const ok = await enviarDatos("leads", "contacto", datos);
      boton.disabled = false; boton.textContent = "Enviar";
      estado.classList.remove("oculto", "ok", "mal");
      const textoWa = programaObj?.whatsapp_mensaje || C.mensajes.reservar;
      if (ok) {
        estado.classList.add("ok");
        estado.innerHTML = `<strong>¡Gracias, ${esc(datos.nombre.split(" ")[0])}!</strong><br>Una asesora te escribirá muy pronto.<br><a class="boton boton-verde" href="${linkWhatsapp(textoWa)}" data-medir="whatsapp" target="_blank" rel="noopener">¿Apurado? Escríbenos ya</a>`;
        $$(".campo, .check, button[type=submit]", form).forEach((el) => el.classList.add("oculto"));
        medir("Lead", { programa: datos.programa || datos.servicio || "", pagina: datos.pagina });
      } else {
        estado.classList.add("mal");
        estado.innerHTML = `No pudimos enviar tus datos. Por favor escríbenos por WhatsApp.<br><a class="boton boton-verde" href="${linkWhatsapp(textoWa)}" data-medir="whatsapp" target="_blank" rel="noopener">Abrir WhatsApp</a>`;
      }
    });
  }

  async function pintarFormularios() {
    for (const lugar of $$("[data-formulario]")) {
      const tipo = lugar.dataset.formulario;
      const prog = lugar.dataset.programa ? (await programas()).find((p) => p.slug === lugar.dataset.programa) : null;
      lugar.innerHTML = await htmlFormulario(tipo, prog?.nombre);
      activarFormulario($("form", lugar), prog);
    }
  }

  /* ------------------------------------------------------------------
     PÁGINA DE PROGRAMA (plantilla única)
     ------------------------------------------------------------------ */
  async function pintarPrograma() {
    const lugar = $("#programa");
    if (!lugar) return;
    const p = (await programas()).find((x) => x.slug === lugar.dataset.slug);
    if (!p) { lugar.innerHTML = '<div class="contenedor seccion pagina-simple"><h1 class="titulo">Programa no disponible</h1><p>Escríbenos por WhatsApp y te contamos.</p></div>'; return; }
    document.body.dataset.whatsapp = p.whatsapp_mensaje;
    const datos = p.datos || [];
    lugar.innerHTML = `
      <section class="hero-programa">
        <div class="contenedor">
          <div class="texto">
            <span class="etiqueta">${esc(p.etiqueta)}</span>
            <h1>${esc(p.nombre)}</h1>
            <p>${esc(p.descripcion)}</p>
            <a class="boton boton-rojo" href="#reservar">¡Reserva tu clase!</a>
          </div>
          <div class="imagen"><img src="${esc(p.imagen)}" alt="Alumno de ${esc(p.nombre)}" width="700" height="964" fetchpriority="high"></div>
        </div>
      </section>
      ${datos.length ? `<div class="barra-datos" style="--n:${datos.length}">${datos.map((d) => `<div class="dato">${icono(d.icono)}<span>${esc(d.texto)}</span></div>`).join("")}</div>` : ""}
      <section class="seccion cuadricula">
        <div class="contenedor cuerpo-programa">
          <div class="principal">
            <p class="frase">El aprendizaje se convierte en un emocionante viaje compartido.<br>¡Despierta la magia de los números con su <span class="amarillo">compañero de clase</span>!</p>
            ${p.video_youtube ? htmlVideo(p.video_youtube, p.video_miniatura, `Ver video de ${p.nombre}`) : ""}
            ${p.beneficios?.length ? `<ul class="checks chicos beneficios">${p.beneficios.map((b) => `<li>${esc(b)}</li>`).join("")}</ul>` : ""}
            ${p.libros?.length ? `<div class="libros"><div class="portadas">${p.libros.map((l) => `<img src="${esc(l.imagen)}" alt="Libro ${esc(l.titulo)}" loading="lazy">`).join("")}</div>
              <p>Programa desarrollado a partir de los libros ${p.libros.map((l) => `<strong>“${esc(l.titulo)}”</strong>`).join(" y ")} de Marco Loret de Mola.</p></div>` : ""}
            <div class="especificaciones">
              <h3>Especificaciones</h3>
              <div class="items">
                <div class="item">${icono("colegio")}<span>Para alumnos de<br><strong>${esc(p.para_quien)}</strong></span></div>
                <div class="item">${icono("reloj")}<span>Disponibilidad para<br><strong>${esc(p.disponibilidad)}</strong></span></div>
              </div>
            </div>
          </div>
          <aside class="lateral" id="reservar">
            <div class="caja-form">
              <h2>¡TE <span class="amarillo">CONTACTAMOS!</span></h2>
              <p>Déjanos tus datos para que una asesora se comunique contigo.</p>
              <div data-formulario="${esc(p.formulario)}" data-programa="${esc(p.slug)}"></div>
            </div>
            <div class="o-whatsapp"><p>O escríbenos directo al WhatsApp 👇</p>
              <a class="boton boton-verde" data-whatsapp-texto="${esc(p.whatsapp_mensaje)}">¡Quiero reservar ahora!</a></div>
          </aside>
        </div>
      </section>`;
    activarEnlacesWhatsapp(lugar);
  }

  /* ------------------------------------------------------------------
     EQUIPO (Nosotros) — cinta animada
     ------------------------------------------------------------------ */
  async function pintarEquipo() {
    const lugar = $("#equipo");
    if (!lugar) return;
    const equipo = await leerTabla("equipo");
    const tarjeta = (x, copia) => `
      <figure class="persona"${copia ? ' aria-hidden="true"' : ""}>
        <img src="${esc(x.foto)}" alt="${copia ? "" : esc(x.nombre)}" width="190" height="190" loading="lazy">
        <h3>${esc(x.nombre)}</h3>${x.cargo ? `<p>${esc(x.cargo)}</p>` : ""}
      </figure>`;
    // Se duplica la lista para que la cinta sea infinita.
    lugar.innerHTML = `<div class="equipo-pista" style="--duracion:${Math.max(20, equipo.length * 4)}s">${equipo.map((x) => tarjeta(x)).join("")}${equipo.map((x) => tarjeta(x, true)).join("")}</div>`;
  }

  /* ------------------------------------------------------------------
     CLASES S.O.S. — reserva en 2 pasos
     ------------------------------------------------------------------ */
  function pintarReservaSOS() {
    const lugar = $("#reserva-sos");
    if (!lugar) return;
    const S = C.sos;
    const dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"];
    lugar.innerHTML = `
      <div class="pasos-form"><span class="activo" data-paso-ind="1"><b>1</b> Datos</span><span data-paso-ind="2"><b>2</b> Confirmación</span></div>
      <form class="formulario" novalidate>
        <div data-paso="1">
          <div class="aviso-mediodia">Toda reserva de clase hecha después del mediodía se programa para el día siguiente.</div>
          ${campo('<label class="solo-lectores" for="s-apoderado">Nombres y apellidos del apoderado</label><input id="s-apoderado" name="apoderado" placeholder="Nombres y apellidos (apoderado)*" autocomplete="name" required>')}
          ${campo('<label class="solo-lectores" for="s-correo">Correo</label><input id="s-correo" name="correo" type="email" placeholder="Correo electrónico*" autocomplete="email" required>', "Ingresa un correo válido")}
          ${campo('<label class="solo-lectores" for="s-celular">Celular</label><input id="s-celular" name="celular" type="tel" inputmode="tel" placeholder="Celular de contacto*" autocomplete="tel" required pattern="[0-9+ ]{9,15}">', "Ingresa un celular válido")}
          ${campo('<label class="solo-lectores" for="s-estudiante">Nombre del estudiante</label><input id="s-estudiante" name="estudiante" placeholder="Nombre del estudiante*" required>')}
          ${campo(`<label class="solo-lectores" for="s-grado">Grado</label><select id="s-grado" name="grado" required>${opciones(C.grados, "Grado del estudiante*")}</select>`, "Elige el grado")}
          ${campo(`<label class="solo-lectores" for="s-dia">Día</label><select id="s-dia" name="dia" required>${opciones(dias, "Día de la clase*")}</select>`, "Elige el día")}
          ${campo(`<label class="solo-lectores" for="s-horas">Horas</label><select id="s-horas" name="horas" required>${`<option value="">¿Cuántas horas?*</option>` + S.precios.map((p) => `<option value="${p.horas}">${esc(p.etiqueta)} (S/ ${p.precio})</option>`).join("")}</select>`, "Elige la cantidad de horas")}
          ${campo('<label class="solo-lectores" for="s-rango">Rango de horas</label><select id="s-rango" name="rango" required disabled><option value="">Rango de horas* (elige día y horas)</option></select>', "Elige el rango de horas")}
          <input class="trampa" name="sitio_web" tabindex="-1" autocomplete="off" aria-hidden="true">
          <label class="check"><input type="checkbox" name="acepta" required> <span>Acepto el uso de mis datos para que matLab me contacte.</span></label>
          <button class="boton boton-rojo" type="button" data-siguiente>Siguiente</button>
        </div>
        <div data-paso="2" class="oculto">
          <div class="resumen"></div>
          <div class="dos-botones"><button class="boton boton-blanco" type="button" data-atras>Retroceder</button><button class="boton boton-rojo" type="submit">Confirmar reserva</button></div>
        </div>
        <div class="form-estado oculto" role="status" aria-live="polite"></div>
      </form>`;

    const form = $("form", lugar);
    const dia = $('[name="dia"]', form), horas = $('[name="horas"]', form), rango = $('[name="rango"]', form);
    const actualizarRangos = () => {
      const finde = ["Sábado", "Domingo"].includes(dia.value);
      const lista = dia.value && horas.value ? (finde ? S.rangos.finDeSemana : S.rangos.semana)[horas.value] || [] : [];
      rango.innerHTML = opciones(lista, lista.length ? "Rango de horas*" : "Rango de horas* (elige día y horas)");
      rango.disabled = !lista.length;
    };
    dia.addEventListener("change", actualizarRangos); horas.addEventListener("change", actualizarRangos);
    $$("input, select", form).forEach((el) => el.addEventListener("input", () => el.closest(".campo")?.classList.remove("error")));

    const paso = (n) => {
      $$("[data-paso]", form).forEach((d) => d.classList.toggle("oculto", d.dataset.paso !== String(n)));
      $$("[data-paso-ind]", lugar).forEach((d) => d.classList.toggle("activo", d.dataset.pasoInd === String(n)));
      lugar.scrollIntoView({ behavior: "smooth", block: "start" });
    };
    let reserva;
    $("[data-siguiente]", form).addEventListener("click", () => {
      if (!validar($('[data-paso="1"]', form))) return;
      const fd = new FormData(form);
      const precio = S.precios.find((p) => String(p.horas) === fd.get("horas"));
      reserva = {
        apoderado: fd.get("apoderado").trim(), correo: fd.get("correo").trim(), celular: fd.get("celular").trim(),
        estudiante: fd.get("estudiante").trim(), grado: fd.get("grado"), dia: fd.get("dia"),
        horas: Number(fd.get("horas")), rango: fd.get("rango"), total: precio.precio, estado: "pendiente",
        pagina: location.pathname, utm_source: UTM.utm_source || null, utm_medium: UTM.utm_medium || null, utm_campaign: UTM.utm_campaign || null,
      };
      $(".resumen", form).innerHTML = `<strong>¡Este es el resumen de tu reserva!</strong><dl style="margin-top:.8rem">
        <dt>Apoderado</dt><dd>${esc(reserva.apoderado)}</dd><dt>Estudiante</dt><dd>${esc(reserva.estudiante)}</dd>
        <dt>Grado</dt><dd>${esc(reserva.grado)}</dd><dt>Día</dt><dd>${esc(reserva.dia)}</dd>
        <dt>Horario</dt><dd>${esc(reserva.rango)} (${reserva.horas} h)</dd><dt>Celular</dt><dd>${esc(reserva.celular)}</dd></dl>
        <div class="total">Total: S/ ${reserva.total}</div>`;
      paso(2);
    });
    $("[data-atras]", form).addEventListener("click", () => paso(1));

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if ($(".trampa", form).value || !reserva) return;
      const boton = $('button[type="submit"]', form);
      boton.disabled = true; boton.textContent = "Enviando…";
      const ok = await enviarDatos("reservas_sos", "reserva-sos", reserva);
      boton.disabled = false; boton.textContent = "Confirmar reserva";
      const textoWa = `Hola, acabo de reservar una Clase S.O.S. 🚨 en la web:\n• Estudiante: ${reserva.estudiante} (${reserva.grado})\n• Día: ${reserva.dia}, ${reserva.rango} (${reserva.horas} h)\n• Total: S/ ${reserva.total}\n• Apoderado: ${reserva.apoderado}\n¿Cómo realizo el pago?`;
      const estado = $(".form-estado", form);
      estado.classList.remove("oculto", "ok", "mal");
      if (ok) {
        $('[data-paso="2"]', form).classList.add("oculto");
        estado.classList.add("ok");
        estado.innerHTML = `<strong>¡Reserva registrada!</strong><br>Último paso: envíanos el resumen por WhatsApp y una asesora te confirma el horario y te indica cómo pagar.<br><a class="boton boton-verde" href="${linkWhatsapp(textoWa)}" data-medir="whatsapp" target="_blank" rel="noopener">Enviar por WhatsApp</a>`;
        medir("Lead", { programa: "Clase S.O.S.", valor: reserva.total, pagina: location.pathname });
      } else {
        estado.classList.add("mal");
        estado.innerHTML = `No pudimos registrar la reserva, pero puedes enviarla directo por WhatsApp.<br><a class="boton boton-verde" href="${linkWhatsapp(textoWa)}" data-medir="whatsapp" target="_blank" rel="noopener">Enviar por WhatsApp</a>`;
      }
    });
  }

  /* ------------------------------------------------------------------
     EFECTOS: contadores y aparición al hacer scroll
     ------------------------------------------------------------------ */
  function activarEfectos() {
    const reducir = matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!("IntersectionObserver" in window)) { $$(".aparece").forEach((el) => el.classList.add("visible")); return; }
    const obs = new IntersectionObserver((entradas) => entradas.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add("visible");
      obs.unobserve(en.target);
    }), { threshold: .15 });
    $$(".aparece").forEach((el) => obs.observe(el));

    const obsNum = new IntersectionObserver((entradas) => entradas.forEach((en) => {
      if (!en.isIntersecting) return;
      const el = en.target, fin = Number(el.dataset.contar);
      obsNum.unobserve(el);
      if (reducir) { el.textContent = fin; return; }
      const t0 = performance.now(), dur = 1400;
      const paso = (t) => { const k = Math.min(1, (t - t0) / dur); el.textContent = Math.round(fin * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(paso); };
      requestAnimationFrame(paso);
    }), { threshold: .5 });
    if (!reducir) $$("[data-contar]").forEach((el) => { el.textContent = "0"; obsNum.observe(el); });
  }

  /* ------------------------------------------------------------------
     ARRANQUE
     ------------------------------------------------------------------ */
  async function iniciar() {
    await Promise.all([pintarCabecera(), pintarCarrusel(), pintarTarjetas(), pintarPrograma(), pintarEquipo()]);
    pintarPie();
    pintarAviso();
    activarVideos();
    await pintarFormularios();
    pintarReservaSOS();
    activarEnlacesWhatsapp();
    pintarWhatsappFlotante();
    activarEfectos();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar); else iniciar();
})();
