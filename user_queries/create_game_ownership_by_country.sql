drop table if exists game_ownership_by_country;

create table game_ownership_by_country
(
    loccountrycode text,
    appid int,
    owners int,
    primary key (loccountrycode, appid)
) without rowid;

insert into game_ownership_by_country
    select loccountrycode, appid, count(steamid) 
    from games_countries 
    group by loccountrycode, appid;