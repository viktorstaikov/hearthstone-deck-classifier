drop table if exists decks;
create table decls (
  id integer primary key autoincrement,
  title text not null unique,
  cardname text not null unique,
  cardcount integer,
  class text not null unique,
  archetype text not null unique,
  season text not null unique,
  gamemode text not null unique
);