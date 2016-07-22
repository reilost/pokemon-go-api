import base64
import time
import re
import random
from datetime import datetime
import threading
import argparse
import os
import platform
import sys

import config
import login
import public
from getpass import getpass
import public_proto_pb2
#try:
import pokemon_pb2
import logic
import dirty
import api
	#config.pub=False
#except:
	#config.pub=True

def get_acces_token(usr,pws,type):
	access_token=None
	ltype=None
	if 'goo' in type:
		print '[!] Using google as login..'
		google_data=None
		if platform.system() == 'Windows':
			google_data= login.login_google(usr,pws)
			if google_data is not None:
				access_token=google_data['id_token']
		else:
			access_token= login.login_google_v2(usr,pws)
		if access_token is not None:
			ltype='google'
	else:
		print '[!] I am a poketrainer..'
		access_token= login.login_pokemon(usr,pws)
		ltype='ptc'
	return access_token,ltype
	
def main():

	poke_type = os.environ.get('POKE_TYPE', None)
	poke_username = os.environ.get('POKE_USERNAME', None)
	poke_password = os.environ.get('POKE_PASSWORD', None)
	poke_location = os.environ.get('POKE_LOCATION', None)
	print poke_location
	access_token, ltype = get_acces_token(poke_username, poke_password, poke_type)
	if access_token is not None:
		if config.debug:
			print '[!] using:',config.pub
		if config.pub:
			public.start_work(access_token,ltype, poke_location)
		else:
			dirty.start_private_show(access_token,ltype, poke_location)
	else:
		print '[-] access_token bad'

if __name__ == '__main__':
	sys.dont_write_bytecode = True
	main()