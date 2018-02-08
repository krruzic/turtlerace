import random
import sys
import os
import binascii
import json

from jsonrpc_requests import Server

def gen_paymentids(address,num):
    SEED = os.environ.get("SECRET_KEY")
    rng = random.Random(address+SEED)
    results = []
    length = 31
    chunk_size = 65535
    chunks = []
    while length >= chunk_size:
        chunks.append(rng.getrandbits(chunk_size * 8).to_bytes(chunk_size, sys.byteorder))
        length -= chunk_size
    if length:
        chunks.append(rng.getrandbits(length * 8).to_bytes(length, sys.byteorder))
    result = b''.join(chunks)

    for i in range(0,num):
        results.append("".join(map(chr, binascii.hexlify(result+(i).to_bytes(2, byteorder='big')))))

    return results


class TrtlServer(Server):
    def dumps(self, data): 
        data['password'] = os.environ.get('WALLET_RPC_PASS')
        return json.dumps(data)
