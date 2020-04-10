#! /usr/bin/env python3
# coding: utf-8

import hashlib
import json
import uuid
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.transactions = []

        previous_hash = hashlib.sha256(f'{uuid.uuid4()}'.encode()).hexdigest()
        self.new_block(previous_hash, self.proof_of_work(previous_hash))

    def new_block(self, previous_hash, proof):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash_block(self.last_block)
        }

        self.chain.append(block)
        self.transactions = []
        return block

    def new_transactions(self, sender, recipient, amount):
        self.transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash_block(block):
        return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def valid_proof(last_proof, proof):
        return hashlib.sha256(f'{last_proof}{proof}'.encode()).hexdigest()[:4] == "0000"
