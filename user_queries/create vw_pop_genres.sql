drop view if exists vw_pop_genres;

create view vw_pop_genres as
select pl.steamid, g.appid 
from player_locations pl
inner join games_1 g
    on pl.steamid = g.steamid
-- inner join games_genres gg
--     on g.appid = gg.appid
--group by gg.genre, pl.loccountrycode