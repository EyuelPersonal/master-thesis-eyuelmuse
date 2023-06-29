with 
time_entry AS (
    select *
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.base_superspace_time_entry
    QUALIFY row_number() OVER(partition by project_id, staff_id order by date desc) = 1
),

staff AS (
    select *
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.dim_staff
    where is_current = TRUE
),

project AS (
    select *
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.dim_project
    where status = 'CLOSED'
),

slack AS (
    select *
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.base_slack_users
    QUALIFY row_number() OVER(partition by user_id order by extraction_date desc) = 1
),

final AS (
    select
        time_entry.project_id,
        slack.user_id
    from time_entry
    inner join project using(project_id)
    left join staff using(staff_id)
    left join slack on staff.slack_name = slack.name
)

select * 
from final where user_id is not null