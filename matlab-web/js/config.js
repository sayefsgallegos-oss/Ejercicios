/* =====================================================================
   CONFIGURACIÓN GENERAL DE LA WEB DE MATLAB
   ---------------------------------------------------------------------
   Este es el archivo que más vas a tocar. Cambia aquí teléfonos,
   correos, redes, horarios y textos de temporada.
   Solo cambia lo que está entre comillas "..." y respeta las comas.
   ===================================================================== */
window.MATLAB_CONFIG = {

  /* ---------- Presentación de propuestas ----------
     true muestra abajo a la izquierda el botón para cambiar entre la
     Propuesta A (/opcion-a/) y la Propuesta B (resto de la web).
     Ponlo en false cuando el cliente elija. */
  mostrarSelectorPropuestas: true,

  /* ---------- Supabase (base de datos) ----------
     Cuando creemos el proyecto en Supabase, pega aquí la URL y la
     "anon public key" (Project Settings > API). Si quedan vacías, la web
     usa los datos de js/datos.js y los formularios se envían solo por
     Netlify (llegan al correo). */
  supabaseUrl: "",
  supabaseAnonKey: "",

  /* ---------- Contacto ---------- */
  whatsapp: "51920000506",            // con código de país, sin + ni espacios
  telefonoVisible: "920 000 506",
  correoEmpresas: "marketing@matlab.com.pe",
  libroReclamaciones: "https://forms.gle/8j8mwW6PbADgEfH57",
  redes: {
    facebook: "https://www.facebook.com/perumatlab",
    instagram: "https://www.instagram.com/matlab_peru/",
    tiktok: "https://www.tiktok.com/@matlab_peru",
    youtube: "https://www.youtube.com/@matlab_peru",
  },

  /* ---------- Mensajes de WhatsApp generales ----------
     (los de cada programa están en js/datos.js) */
  mensajes: {
    flotante: "¡Hola Matlab! Quiero información de sus programas.",
    reservar: "¡Hola! ¡Quiero reservar una clase para mi hijo!",
    general: "Hola vengo de la página web, quiero más información de sus programas 🧐.",
    empresas: "¡Hola! Quiero info de Matlab Empresarial.",
    otroPrograma: "Hola vengo de la página web, quiero información sobre otro programa: ",
  },

  /* ---------- Aviso de temporada (franja debajo del carrusel) ----------
     activo: true lo muestra, false lo oculta. */
  avisoTemporada: {
    activo: true,
    texto: "🚨 ¿Exámenes finales? Ayudamos a tu hijo a <strong>salvar el año</strong> con clases de emergencia.",
    boton: "Reserva tu clase S.O.S.",
    link: "/clases-de-emergencia/",
  },

  /* ---------- Programas que se dan solo a pedido ----------
     No tienen página, pero se mencionan para que pregunten por WhatsApp. */
  programasAPedido: ["Dúo Integral", "Bachillerato IB", "Cálculo Mental", "Razonamiento Matemático", "Listos para el Cole", "Cerrando Brechas"],

  /* ---------- Opciones de los formularios ---------- */
  grados: [
    "1er Grado de Primaria", "2do Grado de Primaria", "3er Grado de Primaria",
    "4to Grado de Primaria", "5to Grado de Primaria", "6to Grado de Primaria",
    "1ero de Secundaria", "2do de Secundaria", "3ero de Secundaria",
    "4to de Secundaria", "5to de Secundaria",
  ],
  horariosIndividuales: [
    "4 a 5 p.m. - Lunes y miércoles",
    "4 a 5 p.m. - Martes y jueves",
    "8 a 9 p.m. - Lunes y miércoles",
    "8 a 9 p.m. - Martes y jueves",
  ],
  horariosGrupales: {
    "Lunes a viernes": ["Diurno", "Tarde", "Noche"],
    "Sábado y domingo": ["Diurno", "Tarde"],
  },
  serviciosContacto: ["Programas Integrales", "Talleres Grupales", "Clases S.O.S.", "Capacitación para empresas", "Otras opciones"],

  /* ---------- Reserva de clases (botón "Reserva tu clase") ---------- */
  reservas: {
    // Respuestas posibles a "Condición del alumno"
    condiciones: [
      { valor: "Alumno nuevo", detalle: "Primera clase con nosotros." },
      { valor: "Ya es alumno", detalle: "Quiere reservar otra clase." },
      { valor: "Tiene examen pronto", detalle: "Necesita una clase urgente." },
    ],
    anticipacionHoras: 3,      // no se puede reservar con menos de 3 horas
    semanasAdelante: 3,        // cuántas semanas hacia adelante se pueden ver
    horaInicio: 7, horaFin: 21, // rango que muestra el calendario
    zonaHoraria: "America/Lima",
    /* Horarios en que hay profesores, por nivel.
       Día: 0 = lunes, 1 = martes ... 5 = sábado, 6 = domingo.
       Cada número es la hora de inicio (16 = clase de 4 a 5 p.m.).
       cupos = cuántos alumnos pueden reservar el mismo horario (profesores libres).
       Cuando Supabase esté conectado, esto se edita en la tabla "disponibilidad". */
    disponibilidad: {
      primaria:   { 0: [15, 16, 17, 18], 1: [9, 15, 16, 17, 18], 2: [15, 16, 17, 18], 3: [9, 15, 16, 17, 18], 4: [15, 16, 17], 5: [9, 10, 11] },
      secundaria: { 0: [16, 17, 18, 19], 1: [9, 16, 17, 18, 19], 2: [16, 17, 18, 19, 20], 3: [9, 16, 17, 18, 19], 4: [16, 17, 18], 5: [9, 10, 11, 12] },
    },
    cupos: { primaria: 2, secundaria: 2 },
  },

  /* ---------- Clases S.O.S. ---------- */
  sos: {
    precios: [
      { horas: 1, etiqueta: "1 hora", precio: 60 },
      { horas: 2, etiqueta: "2 horas", precio: 100 },
    ],
    rangos: {
      semana: { 1: ["04 - 05 p.m.", "05 - 06 p.m.", "06 - 07 p.m.", "07 - 08 p.m.", "08 - 09 p.m."],
                2: ["04 - 06 p.m.", "05 - 07 p.m.", "06 - 08 p.m.", "07 - 09 p.m."] },
      finDeSemana: { 1: ["09 - 10 a.m.", "10 - 11 a.m.", "12 - 01 p.m."],
                     2: ["11 - 01 p.m.", "12 - 02 p.m."] },
    },
  },

  /* ---------- Medición (Analytics, Pixel, etc.) ----------
     Solo se activan en el dominio real, para que las pruebas
     no ensucien las estadísticas. */
  medicion: {
    dominios: ["matlab.com.pe", "www.matlab.com.pe"],
    googleAnalytics: "G-15QK6CYNE1",
    googleTagManager: "GTM-WFNTQWBG",
    metaPixel: "1402980782027741",
    clarity: "ylmzq6ve7e",
  },
};
