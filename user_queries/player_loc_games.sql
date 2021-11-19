select count(pl.steamid), g1.appid, pl.loccountrycode 
from player_locations as pl
inner join games_1 as g1
    on pl.steamid = g1.steamid
    group by pl.loccountrycode, g1.appid

-- select count(pl.steamid), pl.loccountrycode, pl.gameid
-- from player_locations as pl
-- group by pl.loccountrycode, pl.gameid