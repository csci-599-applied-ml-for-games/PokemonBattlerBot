import showdown 

print(showdown.__file__)

username1 = 'USCBot1'
password1 = 'USCBot1'

class BotClient(showdown.Client):
	async def on_private_message(self, pm):
		if pm.recipient == self:
			print(pm.content)
			await pm.reply(pm.content)

BotClient(name=username1, password=password1).start()