import os
import sys
import subprocess
from datetime import datetime
import time

def main(argv):
	if len(argv) != 6:
		print('Usage: python bot_manager.py <iterations> <bot1> <bot1_password> '
			'<bot2> <bot2_password>')
		return 

	iterations = int(argv[1])
	bot1 = argv[2]
	bot1_password = argv[3]
	bot2 = argv[4]
	bot2_password = argv[5]

	logdir = os.path.join(os.path.dirname(__file__), 'logs')
	if not os.path.exists(logdir):
		os.mkdir(logdir)

	bot_script = os.path.join(os.path.dirname(__file__), 'bot.py')
	for iteration in range(iterations):
		datestring = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
		log1path = os.path.join(logdir, '{}_Iteration{}.txt'.format(datestring, 
			iteration))
		log2path = os.path.join(logdir, '{}_Iteration{}.txt'.format(datestring, 
			iteration))
		with open(log1path, 'w') as log1, open(log2path, 'w') as log2:
			try:
				process1 = subprocess.Popen(['python', bot_script, bot1, bot1_password, 
					bot2], stdout=log1, stderr=log1)
				time.sleep(10)
				process2 = subprocess.Popen(['python', bot_script, bot2, 
					bot2_password, bot1, '--challenge'], stdout=log2, stderr=log2)
				process1.communicate()
				process2.communicate()
			except KeyboardInterrupt:
				process1.kill()
				process2.kill()

if __name__ == '__main__':
	main(sys.argv)
