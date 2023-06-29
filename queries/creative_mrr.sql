with mapping as(
	select
        BASE_SLACK_USERS.user_id,
        dim_staff.staff_id
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.dim_staff 
    INNER JOIN NETWORK_ANALYTICS.NETWORK_ANALYTICS.BASE_SLACK_USERS ON 
        BASE_SLACK_USERS.NAME = dim_staff.slack_name
    where is_current = true and extraction_date = '2023-02-16'

),

performance as (
	select
    	staff_id,
        avg(hours_logged) as avg_hours_logged
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.rpt_creative_performance
    group by 1

)

select
    user_id,
    coalesce(avg_hours_logged, 0) AS avg_hours_logged
from performance
inner join mapping using(staff_id)