# SETUP
## NOTES

	"`" is the default perfix, if you are self-hosting the bot and have a custom prefix set, replace it with that
	to report any bugs, contact @sadanslargehole on discord <@521819891141967883>
# MESSAGES IN PRIVATE CHANNELS WILL BE LOGGED BY DEFAULT IF BLACKLIST MODE IS ON, AND SAID CHANNELS ARE NOT BLACKLISTED
## Step One
Do you want whitelist or blacklist mode?
- Whitelist mode makes it so you have to choose for what channels unpins are logged.
	- you can mark and un-mark channels for logging with `` `wlist <add | rm> [channelID]``.
- blacklist mode makes it so all channels are logged unless you mark them as ignored
	- you can mark and un-mark a channel as blacklisted with `` `blist <add|rm> [channelID]``
- To set your mode run `` `mode set <blist|wlist>``
## Step Two
- setup the logging channel
	- the bot can automatically setup a logging channel for you if you want
	- to do this run `` `log setup``. This will create a channel with the following defaults
		- @everyone will be denied the ability to speak
		- any role with manage messages, manage server, or manage channels will be allowed to speak
		- the description and name will be automatically setup
		- move the channel to where you want it
		- change any permissions that are necessary
	- to use your own channel run `` `log setup [channelID]``
## Step 3
- enable the bot
	- run `` `enable``
