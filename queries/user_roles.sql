select
    BASE_SLACK_USERS.user_id,
    dim_staff.position,
    dim_staff.role,
    dim_staff.job_category
from NETWORK_ANALYTICS.NETWORK_ANALYTICS.dim_staff 
INNER JOIN NETWORK_ANALYTICS.NETWORK_ANALYTICS.BASE_SLACK_USERS ON 
    BASE_SLACK_USERS.NAME = dim_staff.slack_name
where is_current = true and extraction_date = '2023-02-16'