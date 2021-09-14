drop view if exists vw_genre_achieve;

create view vw_genre_achieve AS
    select gg.genre, avg(percentage) achievements_percentages
    from games_genres gg
    inner join achievement_percentages ap
        on ap.appid = gg.appid
    group by gg.genre; 
