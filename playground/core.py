import os
import subprocess
import io
import json
import configparser
from playground.constants import ACCOUNTS_FILE, CONFIG_FILE


class Blockchain():
    def __init__(self):
        main_chain = self.get_main_chain()
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)

        self.config = config 
        self.instance = self.start_ganache(main_chain)

    def start_ganache(self, main_chain):
        """ Start ganache with a fork of a main chain
        
        Arguments:
        - `main_chain`: a string that contains an URL for the main chain
    
        Returns:
        - `ganache`: a Subprocess instance
        """
        ganache_config = self.config['ganache']
        
        # construct the command
        cmd = ['ganache-cli']
        cmd.append('--fork {}'.format(main_chain))
        if ganache_config['accounts']:
            cmd.append('-a {}'.format(ganache_config['accounts']))
        if ganache_config['default_balance']:
            cmd.append('-e {}'.format(ganache_config['default_balance']))
        if ganache_config['port']:
            cmd.append('-p {}'.format(ganache_config['port']))
        if ganache_config['network_id']:
            cmd.append('-i {}'.format(ganache_config['network_id']))
        if ganache_config['mnemonic']:
            cmd.append('-m {}'.format(ganache_config['mnemonic']))
        
        ganache_cmd = ' '
        ganache_cmd = ganache_cmd.join(cmd)
        print('Starting Ganache')
        print(ganache_cmd)
        # start ganache
        ganache = subprocess.Popen(
                ganache_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        return ganache

    def terminate(self):
        """ Terminates the instance
        """
        self.instance.terminate()
    
    def read_output(self):
        """ Reads the output of a ganache Subprocess
    
        Arguments:
        - `ganache`: the instance
        """
        accounts = []
        keys = []
    
        for line in io.TextIOWrapper(self.instance.stdout, encoding='utf-8'): 
            line = line.rstrip()
            # add new account
            if line.endswith('({} ETH)'.format(self.config['ganache']['default_balance'])):
                account = line.split(' ')[1]
                accounts.append(account)
            # add new private key
            elif line.startswith('('):
                key = line.split(' ')[1]
                keys.append(key)
            
            # add all accounts and keys into a file
            if len(keys) == int(self.config['ganache']['accounts']):
                self.store_accounts_and_keys(accounts, keys)

            print(line)
    
    @staticmethod
    def store_accounts_and_keys(accounts, keys):
        accounts_dict = dict()
        for i in range(0, len(accounts)):
            accounts_dict[accounts[i]] = keys[i]

        with open(ACCOUNTS_FILE, 'w+', encoding='utf-8') as f:
            json.dump(accounts_dict, f)

    @staticmethod
    def get_main_chain():
        """ Get the URL of the main chain
    
        Returns:
        - `main_chain`: the string URL of the main chain
        """
        # get infura project details
        infura_project_id = os.environ.get('INFURA_PLAY_ID')
        if infura_project_id:
            main_chain = 'https://mainnet.infura.io/v3/{}'.format(infura_project_id)
        else:
            # if infura is not configured, try local host
            main_chain = 'http://localhost:8545'
        
        return main_chain 
