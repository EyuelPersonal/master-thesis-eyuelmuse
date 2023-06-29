with project AS (
    select *
    from NETWORK_ANALYTICS.NETWORK_ANALYTICS.dim_project
),

final AS (
    select
        distinct project_id,
        ended <= deadline AS is_ontime,
        datediff(day,deadline, ended) AS eded_to_deadline
    from project
    where status = 'CLOSED'
)

select * 
from final
where is_ontime is not null