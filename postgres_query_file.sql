-- select * from store_app_publisher
-- where id 
-- in(
-- select publisher_id
-- from store_app_publishergame
-- group by publisher_id 
-- having count(*) < 3
-- order by count(*) desc)

select substring(name, 1,1), ascii(substring(name, 1,1)) from store_app_games
order by 
