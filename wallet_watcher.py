from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import TrtlServer
from models import Base, Bet
from pprint import pprint
engine = create_engine('sqlite:///trtlrace.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()
RPC_URL = "http://127.0.0.1:8070/json_rpc"
WALLET = TrtlServer(RPC_URL)
CONFIRMED_TXS = []
RACELENGTH = 30
WINNERS = [{'wins':0},{'wins':0},{'wins':0},{'wins':0},{'wins':0},{'wins':0},{'wins':0},{'wins':0}]

def round_down(value, base=RACELENGTH):
    return int(value) - int(value) % int(base)

def get_winner(height,race_num):
    blockhash = WALLET.getBlockHashes({'firstBlockIndex':height,'blockCount':1})
    inthash = int(blockhash['blockHashes'][0],16)
    return (inthash % 8)

def insert_winner(race,pot):
    race_winner = get_winner(height,race)
    winner = Winner(
        race_id=race,
        winner=race_winner,
        pot=pot
    )


def get_pot(race):
    pot = session.query(
        func.sum(Bet.amount)).filter_by(race_id=race).scalar()  

def run():
    while True:
        status = WALLET.getStatus()
        height = status['blockCount']
        race_start = round_down(WALLET.getStatus()['blockCount'])
        race = height // RACELENGTH
        blocks_left = RACELENGTH - (height - race_start)
        if blocks_left == 1: # we want a gap block, where no more bets are read in
            continue
        if blocks_left == 30: # race ended, find winner and pay out
            pot = get_pot(race)
            insert_winner(race,pot)
        transactionData = WALLET.getTransactions({'firstBlockIndex':race_start-1}) # include bets from previous gap block
        for item in transactionData['result']['items']:
            for tx in item['transactions']:
                if tx['paymentId']=='':
                    continue
                if tx['transaction_hash'] in CONFIRMED_TXS:
                    continue
                if tx['unlockTime']==0:
                    CONFIRMED_TXS.append({'txid': tx['transaction_hash'],'parsed':False})

        for tx in CONFIRMED_TXS:
            if tx['parsed']:
                continue
            data = WALLET.getTransaction({'transactionHash':tx})

            # remove invalid bets
            try:
                turtle = int(data['paymentId'][-1:])
                # bet was invalid
                if turtle > 7:
                    continue
            except ValueError: # bet was invalid
                continue 

            bet = Bet(
                race_id = race,
                bet_on = turtle,
                amount = data['amount'],
                payment_id = data['paymentId']
            )
            tx['parsed'] = True

        print(tx)

def test_winners():
    status = WALLET.getStatus()
    height = status['blockCount']
    for i in range(1,height-1):
        winner = get_winner(i,1)
        print("turtle %d has won race %d" % (winner,i))
        WINNERS[winner]['wins'] = WINNERS[winner]['wins']+1
    pprint(WINNERS)

if __name__ == "__main__":
    test_winners()