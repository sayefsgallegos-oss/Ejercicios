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
  foto_tarjeta     text,
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
  grupo   text,
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

-- =====================================================================
-- RESERVA TU CLASE
-- =====================================================================

-- Horarios en que hay profesores (día 0 = lunes ... 6 = domingo; hora de inicio 0-23)
create table if not exists public.disponibilidad (
  id          bigint generated always as identity primary key,
  nivel       text not null check (nivel in ('primaria','secundaria')),
  dia_semana  int  not null check (dia_semana between 0 and 6),
  hora        int  not null check (hora between 0 and 23),
  cupos       int  not null default 1 check (cupos >= 0),
  activo      boolean not null default true,
  unique (nivel, dia_semana, hora)
);

create table if not exists public.reservas_clase (
  id            bigint generated always as identity primary key,
  creado        timestamptz not null default now(),
  fecha         date not null,
  hora          int  not null check (hora between 0 and 23),
  nivel         text not null check (nivel in ('primaria','secundaria')),
  grado         text not null check (char_length(grado) <= 60),
  condicion     text not null check (char_length(condicion) <= 60),
  programa      text check (char_length(programa) <= 80),
  apoderado     text not null check (char_length(apoderado) between 2 and 120),
  alumno        text not null check (char_length(alumno) between 2 and 120),
  celular       text not null check (char_length(celular) between 6 and 20),
  pagina        text check (char_length(pagina) <= 200),
  utm_source    text check (char_length(utm_source) <= 120),
  utm_medium    text check (char_length(utm_medium) <= 120),
  utm_campaign  text check (char_length(utm_campaign) <= 160),
  -- seguimiento interno
  estado        text not null default 'reservada' check (estado in ('reservada','confirmada','dictada','cancelada','no asistió')),
  profesor      text,
  notas         text
);

-- Antes de guardar: el horario debe existir, estar en el futuro y tener cupo.
create or replace function public.validar_reserva_clase() returns trigger
language plpgsql security definer set search_path = public as $$
declare v_cupos int; v_usados int;
begin
  select cupos into v_cupos from disponibilidad
   where nivel = new.nivel and dia_semana = extract(isodow from new.fecha)::int - 1 and hora = new.hora and activo;
  if v_cupos is null then raise exception 'horario_no_disponible'; end if;
  if (new.fecha + make_time(new.hora, 0, 0)) < (now() at time zone 'America/Lima') then raise exception 'horario_pasado'; end if;
  -- evita que dos personas tomen el último cupo al mismo tiempo
  perform pg_advisory_xact_lock(hashtext(new.nivel || new.fecha::text || new.hora::text));
  select count(*) into v_usados from reservas_clase
   where nivel = new.nivel and fecha = new.fecha and hora = new.hora and estado <> 'cancelada';
  if v_usados >= v_cupos then raise exception 'horario_lleno'; end if;
  return new;
end $$;

drop trigger if exists antes_de_reservar on public.reservas_clase;
create trigger antes_de_reservar before insert on public.reservas_clase
  for each row execute function public.validar_reserva_clase();

-- La web solo puede saber CUÁNTAS reservas hay por horario (nunca nombres ni celulares).
create or replace function public.horarios_ocupados(desde date, hasta date)
returns table (fecha date, hora int, nivel text, total int)
language sql stable security definer set search_path = public as $$
  select r.fecha, r.hora, r.nivel, count(*)::int
    from reservas_clase r
   where r.fecha between desde and least(hasta, desde + 31) and r.estado <> 'cancelada'
   group by r.fecha, r.hora, r.nivel;
$$;

alter table public.disponibilidad enable row level security;
alter table public.reservas_clase enable row level security;

drop policy if exists "web lee disponibilidad" on public.disponibilidad;
create policy "web lee disponibilidad" on public.disponibilidad for select to anon using (activo);

drop policy if exists "web crea reservas de clase" on public.reservas_clase;
create policy "web crea reservas de clase" on public.reservas_clase
  for insert to anon with check (estado = 'reservada' and profesor is null and notas is null);

revoke all on public.reservas_clase from anon;
grant insert on public.reservas_clase to anon;
grant select on public.disponibilidad to anon;
revoke all on function public.horarios_ocupados(date, date) from public;
grant execute on function public.horarios_ocupados(date, date) to anon;

-- Foto para las tarjetas de programas (Propuesta A)
alter table public.programas add column if not exists foto_tarjeta text;

-- Grupo del equipo: 'direccion' o 'administracion'
alter table public.equipo add column if not exists grupo text;

-- Mateverano: cursos del programa y enlace propio en el menú
alter table public.programas add column if not exists cursos jsonb not null default '[]';
alter table public.programas add column if not exists en_menu boolean not null default false;
alter table public.programas add column if not exists grados_desde int not null default 0;
alter table public.programas drop constraint if exists programas_formulario_check;
alter table public.programas add constraint programas_formulario_check check (formulario in ('individual','grupal','sos','home','verano'));
