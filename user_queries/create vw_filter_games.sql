drop view if exists vw_filter_games;

create view vw_filter_games as
select *
from vw_games
where genre = 'Action'
    or genre = 'Free to Play'
    or genre = 'Strategy'
    or genre = 'Adventure'
    or genre = 'Indie'
    or genre = 'RPG'
    or genre = 'Casual'
    or genre = 'Simulation'
    or genre = 'Racing'
    or genre = 'Massively Multiplayer'
    or genre = 'Sports'
    or genre = 'Early Access'