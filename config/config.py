project_name = 'PROJECT_NAME'
domain = ''

admin = {
    'admin_name': 'ADMIN_NAME',
    'admin_mail': 'ADMIN_NAME',               # email registered to send email.
    'admin_mobile': 'ADMIN_MOBILE_NO',
    'time_zone': 'ADMIN_TIMEZONE'             # Admin timezone. default UTC.
}

# leave blank if fb account kit login not required
fb_account_kit = {
    'api_version': "v1.0"
    'app_id': 'APP_ID'
    'app_secret': 'APP_SECRET'
    'me_endpoint_url': 'https://graph.accountkit.com/v1.0/me'
    'token_exchange_url': 'https://graph.accountkit.com/v1.0/access_token'
}

application_config = {
    'webapp2_extras.sessions' = {
        'secret_key': 'VERY_SECRET_KEY',
    }
}
