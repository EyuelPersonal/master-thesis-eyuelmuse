with
conversations AS (
    select *
    from network_analytics.network_analytics.base_slack_conversations
    QUALIFY ROW_NUMBER() OVER(PARTITION BY channel_id ORDER BY extraction_date DESC) = 1
),
conversation_history AS (
    select *
    from network_analytics.network_analytics.base_slack_conversatios_history
    QUALIFY ROW_NUMBER() OVER(PARTITION BY message_id ORDER BY extraction_date DESC) = 1
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
        conversation_history.channel_id,
        conversation_history.message_id, 
        conversation_history.user_id,
        conversation_history.reply_users
    from conversation_history
    left join conversations using(channel_id)
    inner join users using(user_id)
    inner join staff on users.name = staff.slack_name
    left join project on conversation_history.channel_id = project.slack_channel_id
    where project.slack_channel_id is null and conversations.is_private = true and reply_users is not null
    
)

select * from final