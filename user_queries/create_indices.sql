-- create unique index idx_appidinfo on app_id_info(appid);

-- create index idx_gamedev on games_developers(appid);
-- create index idx_gamepub on games_publishers(appid);
-- create index idx_gamegen on games_genres(appid);
-- create index idx_achperc on achievement_percentages(appid);

-- create index idx_games1_1 on games_1(steamid);
-- create unique index idx_games1_2 on games_1(steamid, appid);
create unique index if not exists idx_playerloc on player_locations(steamid);
-- probably don't create index idx_games1_3 on games1(appid);

-- do this when you need to query friends.
    -- create unique index idx_friends on friends(steamid_a, steamid_b);

    