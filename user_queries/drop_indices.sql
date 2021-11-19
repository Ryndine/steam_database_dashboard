drop index idx_appidinfo;

drop index idx_gamedev;
drop index idx_gamepub;
drop index idx_gamegen;
drop index idx_achperc;

drop index idx_games1_1;
drop index idx_games1_2;
-- probably don't drop index idx_games1_3 on games1(appid);

-- do this when you need to query friends.
    -- drop index idx_friends on friends(steamid_a, steamid_b);


