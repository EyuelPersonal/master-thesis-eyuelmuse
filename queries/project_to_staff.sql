with 
project_to_staff AS (
    select *
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.int_bridge_project_to_staff
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
        project_to_staff.project_id,
        slack.user_id,
        project_to_staff.mapping_type
    from project_to_staff
    inner join project using(project_id)
    left join staff using(staff_id)
    left join slack on staff.slack_name = slack.name
)

select *
from final where user_id is not null