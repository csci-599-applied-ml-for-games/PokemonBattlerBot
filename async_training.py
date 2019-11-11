from threading import Thread

MIN_REPLAY_MEMORY_SIZE = 3000

GAME_INFO = []
class GameInfo():
	start_time = 0.0
	threads = []
	bots = []

def make_bot(un, pw, expected_opponent, team, challenge, 
	trainer, replay_memory, game_index, model_path=None, target_model_path=None):
	
	if trainer:
		if model_path:
			agent = DQNAgent(INPUT_SHAPE, epsilon=epsilon, random_moves=True, 
				training=False)
		else:
			agent = RandomAgent()
	else:
		agent = DQNAgent(INPUT_SHAPE, epsilon=epsilon, random_moves=True, 
			training=False, copy_target_model=False, 
			replay_memory=replay_memory)
		agent.load_model(model_path)
		if target_model_path == None:
			agent.target_model = load_model(target_model_path)
		else:
			agent.target_model.set_weights(agent.model.get_weights())

	bot = BotClient(name=un, password=pw, 
		expected_opponent=expected_opponent, team=team, 
		challenge=challenge, runType=RunType.Iterations, runTypeData=1, 
		agent=agent, trainer=trainer, save_model=False)
	GAME_INFO[game_index].bots.append(bot)
	bot.start()

if __name__ == '__main__':
	timeout = 1200
	epsilon = 1
	epsilon_decay = 0.99
	min_epsilon = 0.001

	replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

	#NOTE: get the account information
	un1, pw1 = ('USCBot9', 'USCBot9')
	un2, pw2 = ('USCBot10', 'USCBot10')

	#NOTE: start two threads for each game 
	game_index = 0
	GAME_INFO[game_index].start_time = time.time()
	GAME_INFO[game_index].bots = []

	bot1_thread = Thread(target=make_bot, args=(un1, pw1, un2, team, False,  
		False, replay_memory, game_index), daemon=True) #TODO: add the model_path and target_model_path
	bot1_thread.start()

	time.sleep(5) #NOTE: the challenger needs to come a little after the other bot is set up

	bot2_thread = Thread(target=make_bot, args=(un2, pw2, un1, team, False,  
		False, replay_memory, game_index), daemon=True) #TODO: add the model_path
	bot2_thread.start()
	
	#NOTE: wait until all games finish
	any_alive = True
	while any_alive:
		any_alive = False
		#NOTE: check if any bots have stalled for more than 20 minutes
		for game_info in GAME_INFO:
			if time.time() - game_info.start_time > timeout:
				for bot in game_info.bots:
					bot.kill() #TODO: define kill in bot.py
			else:
				for thread in game_info.threads:
					if thread.is_alive():
						any_alive = True

	#NOTE: train
	#NOTE: create/load DQN and target DQN in main thread
	#NOTE: train newly loaded model

	#NOTE: decay epsilon
	if epsilon > min_epsilon and len(replay_memory) > MIN_REPLAY_MEMORY_SIZE:
		epsilon *= min_epsilon

	#NOTE: check if we should update target models
	if target_update_counter > update_target_every:
		target_update_counter = 0
		#TODO: save new target model
	else:
		target_update_counter += 1

	#NOTE: check if we should move to the next epoch
	#TODO: implement checking for next epoch