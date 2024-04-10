select sag.name, sag.price, 
case 
when sap.on_sale = true then round(sag.price - (sag.price * sale_percent),2)
else sag.price end as discount_price,
sap.publisher, sap.on_sale, sasp.sale_percent, sasp.start_date, sasp.end_date
from store_app_salepublisher sasp
join store_app_publishergame sapg on sapg.publisher_id = sasp.publisher_id
join store_app_publisher sap on sap.id = sapg.publisher_id
join store_app_games sag on sag.id = sapg.game_id;


-- select name, price, 
-- case when price = 0 then 1
-- else price end as custom_price
-- from store_app_games

select name, price, sale_price from store_app_games sag;