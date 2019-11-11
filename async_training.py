import os
import time
import random
from threading import Thread

from bot import BotClient, RunType, RandomAgent, LOGS_DIR
from gamestate import GameState
from dqn import DQNAgent

BOT_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_SHAPE = (GameState.vector_dimension(),)

def start_game(bot1, bot1_password, bot1_team, 
	bot2, bot2_password, bot2_team, epoch, 
	epsilon, epsilon_decay):		
	
	if epoch == 0:
		agent = DQNAgent(INPUT_SHAPE, epsilon=epsilon, 
			epsilon_decay=epsilon_decay)
	else:
		if epoch_model_path == None:
			raise Exception('Had None as epoch_model_path on iteration other than 0')
		agent = DQNAgent(INPUT_SHAPE, epsilon_decay=epsilon_decay, 
			model_path=epoch_model_path, training=True)

	if epoch == 0:
		trainer_agent = random_agent
	else:
		if epoch_model_path == None:
			raise Exception('Had None as epoch_model_path on iteration other than 0')
		trainer_agent = DQNAgent(INPUT_SHAPE, model_path=epoch_model_path, 
			training=False)

	bot1_client = BotClient(name=bot1, password=bot1_password, 
		expected_opponent=bot2, team=bot1_team, 
		challenge=False, runType=RunType.Iterations, runTypeData=1, 
		agent=bot1_agent, trainer=False, save_model=False)
	bot1_thread = Thread(target=bot1_client.start, daemon=True)
	bot1_thread.start()

	time.sleep(5) #NOTE: the challenger needs to come a little after the other bot is set up

	bot2_client = BotClient(name=bot2, password=bot2_password, 
		expected_opponent=bot1, team=bot2_team, 
		challenge=True, runType=RunType.Iterations, runTypeData=1, 
		agent=bot2_agent, trainer=True, save_model=False)
	bot2_thread = Thread(target=bot2_client.start, daemon=True)
	bot2_thread.start()

	return bot1_thread, bot1_client, bot2_thread, bot2_client

if __name__ == '__main__':
	random.seed()

	TIMEOUT = 1200
	BOT_LIST = [('USCBot1', 'USCBot1', 'USCBot2', 'USCBot2'), 
		('USCBot9', 'USCBot9', 'USCBot10', 'USCBot10')]

	#TODO: argument setup
	num_games = 2
	epochs = 2
	epsilon_decay = 0.1

	with open(os.path.join(BOT_DIR, 'teams/PokemonTeam'), 'rt') as teamfd:
		team = teamfd.read()

	epoch_model_path = None
	random_agent = RandomAgent()
	for epoch in range(epochs):
		replay_memory = dequeue(REPLAY_MEMORY_SIZE)

		games = []
		for game in range(num_games):
			bot1, bot1_password, bot2, bot2_password = BOT_LIST[game]
			start_game()

			games.append((bot1_thread, bot1_client, bot1, bot1_password, 
				bot2_thread, bot2_client, bot2, bot2_password))

		while True:
			for game_index, (bot1_thread, bot1_client, bot1, bot1_password, 
				bot2_thread, bot2_client, bot2, bot2_password) in\
				enumerate(games):
				
				#NOTE: check if any bots need to be killed
				if ((bot1_client.last_action_time - time.time()) > TIMEOUT or
					(bot2_client.last_action_time - time.time()) > TIMEOUT):
					print('TIMING OUT!') #TODO: remove me

					bot1_client.kill()
					bot2_client.kill()
					bot1_thread.join()
					bot2_thread.join()
					
					games[game_index] = start_game(bot1, bot1_password, team,
						agent, bot2, bot2_password, team, trainer_agent)
			
			#train
			old_epoch = agent.current_epoch
			epoch = agent.update_epoch()
			if old_epoch < epoch:
				epoch_model_path = os.path.join(LOGS_DIR, f'Epoch{epoch}.model')
				agent.save_model(path=epoch_model_path)
				agent.restart_epoch()
				break

			time.sleep(10)

