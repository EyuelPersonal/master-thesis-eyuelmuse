with
conversations AS (
    select *
    from network_analytics.network_analytics.base_slack_conversations
    QUALIFY ROW_NUMBER() OVER(PARTITION BY channel_id ORDER BY extraction_date DESC) = 1

),
conversation_members AS (
    select *
    from network_analytics.network_analytics.base_slack_conversation_members
    QUALIFY ROW_NUMBER() OVER(PARTITION BY channel_id, user_id ORDER BY extraction_date DESC) = 1

),
users AS (
    select *
    from network_analytics.network_analytics.base_slack_users
    where is_bot = FALSE and is_app_user = FALSE
    QUALIFY ROW_NUMBER() OVER(PARTITION BY user_id ORDER BY extraction_date DESC) = 1

),
staff AS (
    select * 
    from network_analytics.network_analytics.dim_staff
    where position in ('DESIGN_DIRECTOR', 'SPECIALIST', 'PROJECTMANAGER')
    
),
project AS (
    select slack_channel_id
    from network_analytics.network_analytics.base_superspace_project

),
final AS (
    select
        channel_id,
        array_agg(conversation_members.user_id) as members,
        array_size(members) as total_members
    from conversation_members
    left join conversations using(channel_id)
    inner join users using(user_id)
    inner join staff on users.name = staff.slack_name
    left join project on conversation_members.channel_id = project.slack_channel_id
    where project.slack_channel_id is null and conversations.is_private = true
    group by 1
    having total_members > 1
    
)

select * from final