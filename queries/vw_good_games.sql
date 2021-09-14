drop view if exists [vw_good_games];
create view [vw_good_games] 
as 
select * from app_id_info where rating >= 90;