drop view if exists vw_games;

create view vw_games as
select 
    g.appid,
    g.Title, 
    gd.Developer,
    gg.Genre,
    gp.Publisher
from app_id_info g
inner join games_developers gd
    on g.appid = gd.appid
inner join games_genres gg
    on gd.appid = gg.appid
inner join games_publishers gp
    on gg.appid = gp.appid
