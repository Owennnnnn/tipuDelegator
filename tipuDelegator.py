from beem import Steem
from beem.nodelist import NodeList
from beem.account import Account
import time
import json

f = open('keys.json')

loaded_json = json.load(f)
user = loaded_json['user']
tipu = 'tipu'
active = loaded_json['active_key']
if(user == 'INSERT_USERNAME' or active == 'INSERT_ACTIVE_KEY'):
	print('Error : Add user and keys into keys.json')
	quit()

nodelist = NodeList()
nodelist.update_nodes()
nodes = nodelist.get_steem_nodes()
steem = Steem(node=nodes, keys=[active])
f.close()

def getTotalDelegated():
	totalDelegated = 0.0
	currentDelegations = account.get_vesting_delegations()
	if currentDelegations:
		for i in currentDelegations:
			amount = i['vesting_shares']['amount']
			totalDelegated += float(amount)
		return totalDelegated / (10 ** 6)
				
while True:
	account = Account(user, blockchain_instance=steem)
	if(steem.vests_to_token_power(account.balances['total'][2] - getTotalDelegated()) > 0.1):
		currentDelegations = account.get_vesting_delegations()
		otherDelegationShares = 0.0
		if currentDelegations:
			for i in currentDelegations:
				if(i['delegatee'] != 'tipu'):
					print(i)
					amount = i['vesting_shares']['amount']
					otherDelegationShares = float(amount) + otherDelegationShares
			otherDelegationShares = otherDelegationShares / (10 ** 6)
		bal = account.balances['total'][2]
		bal = str(bal).split()
		ballance = bal[0]
		amountToDelegate = float(float(ballance) - float(otherDelegationShares)) - 1
		print(amountToDelegate)
		account.delegate_vesting_shares(tipu, str(amountToDelegate) + ' VESTS')
		print(user, 'delegated', amountToDelegate, 'shares to tipu')
	else:
		print(user, 'Didn\'t delegate to tipu')
	print('zzz...')
	time.sleep(60*60)
