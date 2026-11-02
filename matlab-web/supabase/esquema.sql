-- =====================================================================
-- BASE DE DATOS DE LA WEB DE MATLAB (Supabase)
-- Cómo usarlo: en Supabase > SQL Editor > New query, pega TODO este
-- archivo y presiona "Run". Se puede ejecutar más de una vez.
-- =====================================================================

-- ---------- CONTACTOS (formularios "¡Te contactamos!") ----------
create table if not exists public.leads (
  id            bigint generated always as identity primary key,
  creado        timestamptz not null default now(),
  nombre        text not null check (char_length(nombre) between 2 and 120),
  apellido      text check (char_length(apellido) <= 120),
  celular       text not null check (char_length(celular) between 6 and 20),
  correo        text check (char_length(correo) <= 160),
  programa      text check (char_length(programa) <= 80),
  grado         text check (char_length(grado) <= 60),
  frecuencia    text check (char_length(frecuencia) <= 60),
  horario       text check (char_length(horario) <= 80),
  servicio      text check (char_length(servicio) <= 80),
  pagina        text check (char_length(pagina) <= 200),
  utm_source    text check (char_length(utm_source) <= 120),
  utm_medium    text check (char_length(utm_medium) <= 120),
  utm_campaign  text check (char_length(utm_campaign) <= 160),
  acepta        boolean not null default false,
  -- seguimiento interno (lo llena tu equipo, no la web)
  estado        text not null default 'nuevo' check (estado in ('nuevo','contactado','matriculado','no interesado')),
  asesora       text,
  notas         text
);

-- ---------- RESERVAS S.O.S. ----------
create table if not exists public.reservas_sos (
  id            bigint generated always as identity primary key,
  creado        timestamptz not null default now(),
  apoderado     text not null check (char_length(apoderado) between 2 and 120),
  correo        text not null check (char_length(correo) <= 160),
  celular       text not null check (char_length(celular) between 6 and 20),
  estudiante    text not null check (char_length(estudiante) between 2 and 120),
  grado         text not null check (char_length(grado) <= 60),
  dia           text not null check (char_length(dia) <= 20),
  horas         int  not null check (horas in (1, 2)),
  rango         text not null check (char_length(rango) <= 40),
  total         numeric(8,2) not null check (total >= 0),
  estado        text not null default 'pendiente' check (estado in ('pendiente','pagada','dictada','cancelada')),
  pagina        text check (char_length(pagina) <= 200),
  utm_source    text check (char_length(utm_source) <= 120),
  utm_medium    text check (char_length(utm_medium) <= 120),
  utm_campaign  text check (char_length(utm_campaign) <= 160),
  notas         text
);

-- ---------- CONTENIDO EDITABLE ----------
create table if not exists public.banners (
  id            bigint generated always as identity primary key,
  titulo        text not null,
  imagen        text not null,
  imagen_movil  text,
  link          text,
  orden         int not null default 0,
  activo        boolean not null default true
);

create table if not exists public.programas (
  id               bigint generated always as identity primary key,
  slug             text unique not null,
  nombre           text not null,
  tipo             text not null check (tipo in ('individual','grupal','sos')),
  etiqueta         text,
  url              text not null,
  resumen          text,
  descripcion      text,
  imagen           text,
  datos            jsonb not null default '[]',
  video_youtube    text,
  video_miniatura  text,
  beneficios       jsonb not null default '[]',
  libros           jsonb not null default '[]',
  para_quien       text,
  disponibilidad   text,
  whatsapp_mensaje text,
  formulario       text not null default 'individual' check (formulario in ('individual','grupal','sos','home')),
  en_home          boolean not null default false,
  activo           boolean not null default true,
  orden            int not null default 0
);

create table if not exists public.equipo (
  id      bigint generated always as identity primary key,
  nombre  text not null,
  cargo   text,
  foto    text not null,
  orden   int not null default 0,
  activo  boolean not null default true
);

-- =====================================================================
-- SEGURIDAD (Row Level Security)
-- La web (clave "anon") puede: LEER contenido activo y CREAR contactos/reservas.
-- NO puede leer, cambiar ni borrar contactos o reservas de nadie.
-- Tú los ves desde el panel de Supabase (Table Editor).
-- =====================================================================
alter table public.leads        enable row level security;
alter table public.reservas_sos enable row level security;
alter table public.banners      enable row level security;
alter table public.programas    enable row level security;
alter table public.equipo       enable row level security;

drop policy if exists "web crea leads" on public.leads;
create policy "web crea leads" on public.leads
  for insert to anon with check (acepta = true and estado = 'nuevo' and asesora is null and notas is null);

drop policy if exists "web crea reservas" on public.reservas_sos;
create policy "web crea reservas" on public.reservas_sos
  for insert to anon with check (estado = 'pendiente' and notas is null);

drop policy if exists "web lee banners" on public.banners;
create policy "web lee banners" on public.banners for select to anon using (activo);

drop policy if exists "web lee programas" on public.programas;
create policy "web lee programas" on public.programas for select to anon using (activo);

drop policy if exists "web lee equipo" on public.equipo;
create policy "web lee equipo" on public.equipo for select to anon using (activo);

-- La web solo necesita insertar en estas tablas (sin leer de vuelta)
revoke all on public.leads, public.reservas_sos from anon;
grant insert on public.leads, public.reservas_sos to anon;
grant select on public.banners, public.programas, public.equipo to anon;
