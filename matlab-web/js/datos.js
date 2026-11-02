/* =====================================================================
   CONTENIDO DE LA WEB (respaldo local)
   ---------------------------------------------------------------------
   Cuando Supabase esté conectado, estos mismos datos se editan desde
   el panel de Supabase (tablas: banners, programas, equipo) y este
   archivo solo se usa si Supabase no responde.
   ===================================================================== */
window.MATLAB_DATOS = {

  /* ---------- Carrusel del inicio ---------- */
  banners: [
    { titulo: "matLab Power - Refuerza las mates paso a paso", imagen: "/img/banners/power.webp", imagen_movil: "/img/banners/power-movil.webp", link: "/programas/integrales-individuales/programa-mensual-power/", orden: 1, activo: true },
    { titulo: "matLab Élite - Alcanza su máximo potencial todo el año", imagen: "/img/banners/elite.webp", imagen_movil: "/img/banners/elite-movil.webp", link: "/programas/integrales-individuales/programa-anual-elite/", orden: 2, activo: true },
    { titulo: "matLab Finanzas - Construye su futuro financiero", imagen: "/img/banners/finanzas.webp", imagen_movil: "/img/banners/finanzas-movil.webp", link: "/programas/talleres-grupales/finanzas-para-jovenes/", orden: 3, activo: true },
  ],

  /* ---------- Programas ----------
     tipo: "individual" | "grupal" | "sos"
     formulario: "individual" (grado + horario) | "grupal" (grado + frecuencia + horario)
     datos: la barra amarilla. iconos disponibles: clases, reloj, virtual, seguimiento, grupo, check */
  programas: [
    {
      slug: "anual-elite",
      nombre: "Anual Élite",
      tipo: "individual",
      etiqueta: "Programa integral",
      url: "/programas/integrales-individuales/programa-anual-elite/",
      resumen: "Ayuda a tu hijo a consolidar sus bases matemáticas con un acompañamiento personalizado durante todo el año.",
      descripcion: "Ayuda a tu hijo a consolidar sus bases matemáticas con un acompañamiento personalizado durante todo el año.",
      imagen: "/img/programas/elite.webp",
      datos: [
        { icono: "clases", texto: "Dos o más clases por semana" },
        { icono: "reloj", texto: "50 minutos por cada clase" },
        { icono: "virtual", texto: "Clases 100% virtuales" },
        { icono: "seguimiento", texto: "Seguimiento completo" },
      ],
      video_youtube: "IduzZnSBPvs",
      video_miniatura: "/img/videos/elite.webp",
      beneficios: [
        "Evaluación de entrada para identificar oportunidades.",
        "Desarrollo de plan de trabajo a la medida del alumno.",
        "Acompañamiento durante todo su proceso de estudios.",
        "Informes en línea sobre el avance del programa.",
        "Reunión virtual con su profesor de colegio.",
        "Reuniones con nuestros tutores especializados de Matlab.",
      ],
      libros: [],
      para_quien: "primaria y secundaria",
      disponibilidad: "tarde y noche",
      whatsapp_mensaje: "Hola vengo de la página web, quiero más información del Programa Anual Élite 😎.",
      formulario: "individual",
      en_home: true, activo: true, orden: 2,
    },
    {
      slug: "mensual-power",
      nombre: "Mensual Power",
      tipo: "individual",
      etiqueta: "Programa integral",
      url: "/programas/integrales-individuales/programa-mensual-power/",
      resumen: "Dale a tu hijo el acompañamiento necesario para absolver sus dudas y que se convierta en un crack en matemáticas.",
      descripcion: "Dale a tu hijo el acompañamiento necesario para absolver sus dudas y que se convierta en un crack en matemáticas.",
      imagen: "/img/programas/power.webp",
      datos: [
        { icono: "clases", texto: "Una o más clases por semana" },
        { icono: "reloj", texto: "50 minutos por cada clase" },
        { icono: "virtual", texto: "Clases 100% virtuales" },
        { icono: "check", texto: "Eliges la cantidad de clases" },
      ],
      video_youtube: "_LgBJIqqOJc",
      video_miniatura: "/img/videos/power.webp",
      beneficios: [
        "Evaluación de entrada para identificar oportunidades.",
        "Desarrollo de plan de trabajo a la medida del alumno.",
        "Acompañamiento durante todo su proceso de estudios.",
        "Informes en línea sobre el avance del programa.",
        "Reunión virtual con su profesor de colegio.",
        "Reuniones con nuestros tutores especializados de Matlab.",
      ],
      libros: [],
      para_quien: "primaria y secundaria",
      disponibilidad: "tarde y noche",
      whatsapp_mensaje: "Hola vengo de la página web, quiero más información del Programa Mensual Power 💪.",
      formulario: "individual",
      en_home: true, activo: true, orden: 1,
    },
    {
      slug: "mateinnovando",
      nombre: "Mateinnovando",
      tipo: "grupal",
      etiqueta: "Taller grupal",
      url: "/programas/talleres-grupales/mateinnovando/",
      resumen: "Potencia el talento matemático y financiero de tu hijo con la alianza estratégica que tenemos con todos los Innova Schools.",
      descripcion: "Desarrollado a partir de una alianza estratégica con Innova Schools, que integra la metodología de MatLab con los temas, contenidos y necesidades de aprendizaje de sus estudiantes.",
      imagen: "/img/programas/mateinnovando.webp",
      datos: [
        { icono: "clases", texto: "2 clases por semana" },
        { icono: "reloj", texto: "50 minutos por cada clase" },
        { icono: "virtual", texto: "Clases 100% virtuales" },
        { icono: "grupo", texto: "Grupos pequeños" },
      ],
      video_youtube: "WaxA54UBkpQ",
      video_miniatura: "/img/videos/mateinnovando.webp",
      beneficios: [
        "Grupos pequeños.",
        "Explicación didáctica.",
        "Temas acorde al grado.",
        "Participación activa.",
      ],
      libros: [],
      para_quien: "alumnos de Innova Schools",   // PENDIENTE: confirmar grados
      disponibilidad: "tarde y noche",
      whatsapp_mensaje: "Hola vengo de la página web, quiero más información del Programa Mateinnovando👌.",
      formulario: "grupal",
      en_home: true, activo: true, orden: 3,
    },
    {
      slug: "taller-financiero",
      nombre: "Taller Financiero",
      tipo: "grupal",
      etiqueta: "Taller grupal",
      url: "/programas/talleres-grupales/finanzas-para-jovenes/",
      resumen: "Asegura el futuro financiero de tus hijos potenciando su educación financiera desde hoy.",
      descripcion: "Asegura el éxito financiero de tus hijos potenciando sus conocimientos de educación financiera.",
      imagen: "/img/programas/financiero.webp",
      datos: [
        { icono: "clases", texto: "Una o dos clases por semana" },
        { icono: "reloj", texto: "50 minutos por cada clase" },
        { icono: "virtual", texto: "Clases 100% virtuales" },
        { icono: "grupo", texto: "Grupos pequeños" },
      ],
      video_youtube: "x-whJ-qQg38",
      video_miniatura: "/img/videos/financiero.webp",
      beneficios: [
        "Grupos pequeños.",
        "Explicación didáctica.",
        "Temas acorde al grado.",
        "Participación activa.",
      ],
      libros: [
        { titulo: "Tu éxito financiero con Manzanitas", imagen: "/img/libros/manzanitas.webp" },
        { titulo: "Los Tec X. Una visión financiera", imagen: "/img/libros/los-tec-x.webp" },
      ],
      para_quien: "2do de primaria a 5to de secundaria",
      disponibilidad: "tarde y noche",
      whatsapp_mensaje: "Hola vengo de la página web, quiero más información del Taller Financiero 💰.",
      formulario: "grupal",
      en_home: true, activo: true, orden: 4,
    },
    {
      slug: "clase-sos",
      nombre: "Clase S.O.S.",
      tipo: "sos",
      etiqueta: "Clases de emergencia",
      url: "/clases-de-emergencia/",
      resumen: "¿Examen mañana? Clases individuales de emergencia para salvar el examen.",
      descripcion: "",
      imagen: "/img/programas/sos.webp",
      datos: [], beneficios: [], libros: [],
      video_youtube: "Le_YwBzSggw",
      video_miniatura: "/img/videos/sos.webp",
      whatsapp_mensaje: "Hola vengo de la página web, quiero más información de su Clase de Emergencia S.O.S 🚨.",
      formulario: "sos",
      en_home: false, activo: true, orden: 5,
    },
  ],

  /* ---------- Equipo (página Nosotros) ----------
     Para agregar a alguien: copia una línea, cambia nombre/cargo/foto.
     Para quitar a alguien: cambia activo: true por activo: false. */
  equipo: [
    { nombre: "Marco Loret de Mola", cargo: "Director General", foto: "/img/equipo/marco-loret-de-mola.webp", orden: 1, activo: true },
    { nombre: "Nidia Arana", cargo: "", foto: "/img/equipo/nidia-arana.webp", orden: 2, activo: true },
    { nombre: "Pierre Gallegos", cargo: "", foto: "/img/equipo/pierre-gallegos.webp", orden: 3, activo: true },
    { nombre: "Cesar Vallejo", cargo: "", foto: "/img/equipo/cesar-vallejo.webp", orden: 4, activo: true },
    { nombre: "Leandro Salazar", cargo: "", foto: "/img/equipo/leandro-salazar.webp", orden: 5, activo: true },
    { nombre: "Valeria Caballero", cargo: "", foto: "/img/equipo/valeria-caballero.webp", orden: 6, activo: true },
    { nombre: "Ana Paula Chavez", cargo: "", foto: "/img/equipo/ana-paula-chavez.webp", orden: 7, activo: true },
    { nombre: "Kiara Herrera", cargo: "", foto: "/img/equipo/kiara-herrera.webp", orden: 8, activo: true },
    { nombre: "Alexandra Velásquez", cargo: "", foto: "/img/equipo/alexandra-velasquez.webp", orden: 9, activo: true },
    { nombre: "Marilyn Mora", cargo: "", foto: "/img/equipo/marilyn-mora.webp", orden: 10, activo: true },
    { nombre: "Samantha Piedra", cargo: "", foto: "/img/equipo/samantha-piedra.webp", orden: 11, activo: true },
    { nombre: "Daniela Alamo", cargo: "", foto: "/img/equipo/daniela-alamo.webp", orden: 12, activo: true },
    { nombre: "Verónica Alamo", cargo: "", foto: "/img/equipo/veronica-alamo.webp", orden: 13, activo: true },
    { nombre: "Gustavo Alvarado", cargo: "", foto: "/img/equipo/gustavo-alvarado.webp", orden: 14, activo: true },
    { nombre: "Bryan Urcia", cargo: "", foto: "/img/equipo/bryan-urcia.webp", orden: 15, activo: true },
    { nombre: "Alexandra Vilca", cargo: "", foto: "/img/equipo/alexandra-vilca.webp", orden: 16, activo: true },
  ],
};
