# Secret Santa Slack Bot
The bot randomly assigns members of a channel to each other and sends the name of the assigned member within a direct message (along with some nice wishes).

## Requirements - Install
- Python
- slackclient: `pip install slackclient`

## Setup
1. Create a new App within your Slack workspace: https://api.slack.com/apps
2. Add a bot user to your App
3. Under the `Installed App` section copy the `Bot User OAuth Access Token`

## Usage
1. Create a channel. By default it should be: `secret-santa`
2. When you want to assign people run the application:
```bash
SLACK_API_TOKEN={your-slack-bot-access-token} python ./secret_santa.py
```

## Environment variables
`SLACK_API_TOKEN`: your slack bot access token - Required.
`CHANNEL_NAME`: the name of your secret santa channel - Optional. Default: secret-santa
`DRY_RUN`: only printing out the `user_id` pairs but not actually sending the messages

![](https://gph.is/1UTyrBr)
