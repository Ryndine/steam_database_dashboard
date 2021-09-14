drop table if exists games_countries;

create table games_countries
(
    steamid int,
    appid int,
    loccountrycode text,
    primary key (steamid, appid)
) without rowid;

insert into games_countries
    select pl.steamid, g.appid, pl.loccountrycode
    from player_locations pl
    inner join games_1 g using (steamid)