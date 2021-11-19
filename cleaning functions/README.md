# Steam Database Dashboard
[Ryan Mangeno](https://github.com/Ryndine) | [Anny Tritchler](https://github.com/tritchlin/) | [Melissa Cardenas](https://github.com/melcardenas28)

## User Queries
This folder contains all the sql queries for the database.

### Usage:
1) Create sql query in new file.
```
drop view if exists vw_pop_genres;
create view vw_pop_genres as
select pl.steamid, g.appid 
from player_locations pl
inner join games_1 g
    on pl.steamid = g.steamid
-- inner join games_genres gg
--     on g.appid = gg.appid
-- group by gg.genre, pl.loccountrycode
```
2) Refer to file [q_execute_scripts](https://github.com/Ryndine/steam_analysis_database/blob/main/q_execute_scripts.py).
	1) set the database location
	```
	# --- DATABASE LOCATION ---
	# steamdb = db_interface('steamdata.db')
	steamdb = db_interface('D:\steam\steamdata.db')
	```
	2) Using function 'exec_script', set perameter to query location. Run the function on the database.
	```
	steamdb.exec_script('user_queries\create vw_pop_genres.sql')
	```
