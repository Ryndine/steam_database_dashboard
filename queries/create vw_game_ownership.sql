drop view if exists vw_genre_ownership_by_country;

create view vw_genre_ownership_by_country as
    select ccc.alpha3 countrycode, gg.genre, sum(owners) genre_owners
    from game_ownership_by_country gobc
    inner join games_genres gg
        on gobc.appid = gg.appid
    inner join countries_codes_and_coordinates ccc
        on gobc.loccountrycode = ccc.alpha2
    group by gobc.loccountrycode, gg.genre; 