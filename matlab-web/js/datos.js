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
    { titulo: "Mate Verano - ¡Asegura su cupo 2027! Cálculo mental, finanzas y razonamiento matemático", imagen: "/img/banners/verano.webp", imagen_movil: "/img/banners/verano-movil.webp", link: "/programas/talleres-grupales/mateverano/", orden: 0, activo: true },
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
      foto_tarjeta: "/img/opcion-a/prog-elite.webp",
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
      foto_tarjeta: "/img/opcion-a/prog-power.webp",
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
      foto_tarjeta: "/img/opcion-a/prog-mateinnovando.webp",
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
      foto_tarjeta: "/img/opcion-a/prog-financiero.webp",
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
      slug: "mateverano",
      nombre: "Mateverano",
      tipo: "grupal",
      etiqueta: "Talleres de verano",
      url: "/programas/talleres-grupales/mateverano/",
      resumen: "Talleres grupales de verano: razonamiento matemático, cálculo mental, finanzas y listos para el cole.",
      descripcion: "Complementa sus vacaciones con talleres en vivo para llegar con todo al próximo año. ¡Asegura su cupo 2027!",
      imagen: "/img/programas/mateverano.webp",
      foto_tarjeta: "/img/programas/mateverano.webp",
      datos: [
        { icono: "virtual", texto: "Clases 100% virtuales" },
        { icono: "grupo", texto: "Grupos pequeños" },
        { icono: "reloj", texto: "50 minutos por clase" },
        { icono: "clases", texto: "Turnos mañana, tarde y noche" },
      ],
      // Cursos del verano: aparecen en la página y en el formulario ("curso de interés")
      cursos: [
        { titulo: "Razonamiento Matemático", texto: "Herramientas efectivas para su pensamiento lógico.", form: "Razonamiento Matemático" },
        { titulo: "Cálculo Mental", texto: "Calcula con más rapidez, agilidad y seguridad.", form: "Cálculo Mental" },
        { titulo: "Finanzas", texto: "Aprende a ahorrar y administrar su dinero desde joven.", form: "Finanzas Verano" },
        { titulo: "Listos para el Cole", texto: "Refuerza sus bases para el próximo grado en solo un mes.", form: "Listos para el Cole" },
      ],
      video_youtube: "kUC_t1u_rYs",
      video_miniatura: "", // vacío = usa la miniatura de YouTube
      beneficios: [],
      libros: [],
      para_quien: "3.° de primaria a 5.° de secundaria",
      disponibilidad: "mañana, tarde y noche",
      whatsapp_mensaje: "Hola 😎!! Quisiera mas información sobre sus programas de verano ☀️⛱️",
      formulario: "verano",
      grados_desde: 2, // el formulario muestra desde 3er grado de primaria
      en_home: false, en_menu: true, activo: true, orden: 5,
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
      en_home: false, activo: true, orden: 6,
    },
  ],

  /* ---------- Testimonios de padres (capturas de WhatsApp) ----------
     Para agregar uno: sube la imagen vertical a img/testimonios/ y copia una línea. */
  testimonios: [
    { titulo: "¡Adri pasó de B a todo A!", imagen: "/img/testimonios/t01.webp", chat: "/img/testimonios/chat-01.webp", orden: 1, activo: true },
    { titulo: "¡Ignacio y Facu, más que felices con Matlab!", imagen: "/img/testimonios/t02.webp", chat: "/img/testimonios/chat-02.webp", orden: 2, activo: true },
    { titulo: "¡Nuestra Matlover mejoró sus notas!", imagen: "/img/testimonios/t03.webp", chat: "/img/testimonios/chat-03.webp", orden: 3, activo: true },
    { titulo: "¡Nuestros profes le ponen corazón a cada clase!", imagen: "/img/testimonios/t04.webp", chat: "/img/testimonios/chat-04.webp", orden: 4, activo: true },
    { titulo: "¡Gaby salió muy bien este bimestre!", imagen: "/img/testimonios/t05.webp", chat: "/img/testimonios/chat-05.webp", orden: 5, activo: true },
    { titulo: "¡Carlos contento con su profe Matlab!", imagen: "/img/testimonios/t06.webp", chat: "/img/testimonios/chat-06.webp", orden: 6, activo: true },
    { titulo: "¡Andre, mejorando cada bimestre!", imagen: "/img/testimonios/t07.webp", chat: "/img/testimonios/chat-07.webp", orden: 7, activo: true },
    { titulo: "¡Álvaro logró ingresar a la universidad!", imagen: "/img/testimonios/t08.webp", chat: "/img/testimonios/chat-08.webp", orden: 8, activo: true },
    { titulo: "¡Gracias por sus comentarios!", imagen: "/img/testimonios/t09.webp", chat: "/img/testimonios/chat-09.webp", orden: 9, activo: true },
    { titulo: "¡Resultados que hablan por sí solos!", imagen: "/img/testimonios/t10.webp", chat: "/img/testimonios/chat-10.webp", orden: 10, activo: true },
    { titulo: "¡Gracias por confiar en nosotros!", imagen: "/img/testimonios/t11.webp", chat: "/img/testimonios/chat-11.webp", orden: 11, activo: true },
    { titulo: "¡Nuestro Taller Financiero es un éxito!", imagen: "/img/testimonios/t12.webp", chat: "/img/testimonios/chat-12.webp", orden: 12, activo: true },
    { titulo: "Nuestros estudiantes, más que agradecidos", imagen: "/img/testimonios/t13.webp", chat: "/img/testimonios/chat-13.webp", orden: 13, activo: true },
    { titulo: "¡Nuestra metodología Matlab es la mejor!", imagen: "/img/testimonios/t14.webp", chat: "/img/testimonios/chat-14.webp", orden: 14, activo: true },
    { titulo: "¡Muchas gracias por la confianza!", imagen: "/img/testimonios/t15.webp", chat: "/img/testimonios/chat-15.webp", orden: 15, activo: true },
  ],

  /* ---------- Equipo (página Nosotros e inicio) ----------
     grupo: "direccion" (sale en las tarjetas grandes de la Propuesta A),
            "administracion" o "" (salen en la cinta animada).
     Para agregar a alguien: copia una línea, cambia nombre/cargo/foto.
     Para quitar a alguien: cambia activo: true por activo: false.
     (activo: false = ya no está en el equipo; queda guardado por si vuelve) */
  equipo: [
    { nombre: "Marco Loret de Mola", cargo: "Director General", grupo: "direccion", foto: "/img/equipo/marco-loret-de-mola.webp", orden: 1, activo: true },
    { nombre: "Nidia Arana", cargo: "Gerente", grupo: "direccion", foto: "/img/equipo/nidia-arana.webp", orden: 2, activo: true },
    { nombre: "Pierre Gallegos", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/pierre-gallegos.webp", orden: 3, activo: true },
    { nombre: "Cesar Vallejo", cargo: "", grupo: "", foto: "/img/equipo/cesar-vallejo.webp", orden: 4, activo: false },
    { nombre: "Leandro Salazar", cargo: "", grupo: "", foto: "/img/equipo/leandro-salazar.webp", orden: 5, activo: false },
    { nombre: "Valeria Caballero", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/valeria-caballero.webp", orden: 6, activo: true },
    { nombre: "Ana Paula Chavez", cargo: "", grupo: "", foto: "/img/equipo/ana-paula-chavez.webp", orden: 7, activo: false },
    { nombre: "Kiara Herrera", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/kiara-herrera.webp", orden: 8, activo: true },
    { nombre: "Alexandra Velásquez", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/alexandra-velasquez.webp", orden: 9, activo: true },
    { nombre: "Marilyn Mora", cargo: "", grupo: "", foto: "/img/equipo/marilyn-mora.webp", orden: 10, activo: false },
    { nombre: "Samantha Piedra", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/samantha-piedra.webp", orden: 11, activo: true },
    { nombre: "Daniela Alamo", cargo: "", grupo: "", foto: "/img/equipo/daniela-alamo.webp", orden: 12, activo: false },
    { nombre: "Verónica Alamo", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/veronica-alamo.webp", orden: 13, activo: true },
    { nombre: "Gustavo Alvarado", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/gustavo-alvarado.webp", orden: 14, activo: true },
    { nombre: "Bryan Urcia", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/bryan-urcia.webp", orden: 15, activo: true },
    { nombre: "Alexandra Vilca", cargo: "Administración", grupo: "administracion", foto: "/img/equipo/alexandra-vilca.webp", orden: 16, activo: true },
  ],
};
