# KickBot
KickBot checks for registation/unregistration events on TELOS and posts updates to Slack

Install KickBot - A Telos BP Reg/UnReg monitor

Integrates with Slack
	-Pushes a message to a specific Slack channel
	
## Prerequisites
- Ubuntu 18.04
- Python2.7
- Python modules (see py script below)
- nodeos running locally
- Slack "incoming webhook" application enabled on target Slack account
		https://api.slack.com/incoming-webhooks
- Slack unique Webhook URL (embeds access token, target slack team & channel, and Bot meta)


## Installation Procedure

`sudo apt install python-pip`

`sudo pip install requests`

- Copy the get_producers.sh and get_producer_status.py scripts to a local folder with access to teclos
		*** Preferably /ext/kickbot
- Update py script with your specific Slack Webhook key
- Update py script variable "net_ver" to applicable network name (i.e. Stagenet, Testnet, Mainnet)

`chmod 755 get_producers.sh`

## Run
`./get_producers.sh`

- 1st time run will only create a state db
- subsequent runs will chack against state and push a status message to Slack on reg & unreg events

## Automate as a cron job

`sudo crontab -e `

*setup a cron job to run every minute*

`* * * * * /ext/kickbot/get_producers.sh  >>/ext/kickbot/kick.log 2>&1`
