select
	project_id,
    channel_id,
    message_id, 
    user_id,
    reply_users
from NETWORK_ANALYTICS.NETWORK_ANALYTICS.base_slack_conversatios_history
inner join NETWORK_ANALYTICS.NETWORK_ANALYTICS.BASE_SUPERSPACE_PROJECT on BASE_SLACK_CONVERSATIOS_HISTORY.CHANNEL_ID = BASE_SUPERSPACE_PROJECT.SLACK_CHANNEL_ID
left join NETWORK_ANALYTICS.NETWORK_ANALYTICS.base_slack_users using(user_id)
QUALIFY ROW_NUMBER() OVER(PARTITION BY message_id ORDER BY extraction_date DESC) = 1