# PokemonBattlerBot
Package runs with Python3 

# Required Packages
Install requests, docopt, websockets, and aiohttp. Sample command

pip3 install --user requests 

# MacOS Notes
If you have an SSL certification error with Python3 on Mac, you can fix it with 
the following command
/Applications/Python\ 3.7/Install\ Certificates.command

# Accounts
I believe you have to make an account before you start testing with the bot. I 
recommend making the accounts in a way that the user name matches the password. 

# Models
The models directory is for storing models for future use only. Don't commit
short-term models here.

# Sample Commands

python bot.py USCBot9 USCBot9 USCBot10 --iterations=20 --modeltype=random --notraining --printstats

python bot.py USCBot10 USCBot10 USCBot9 --iterations=20 --modeltype=dqn --notraining --printstats --load_model=F:\GitHub\PokemonBattlerBot\models\Bot1_LongTermReward_Epsilon9_Iteration265.model --challenge

# Current Accounts
USCBot1
USCBot2
USCBot9
USCBot10