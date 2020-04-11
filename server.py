#! /usr/bin/env python3
# coding: utf-8
import argparse
import json

from uuid import uuid4

from flask import Flask, request, jsonify

from blockchain.blockchain import Blockchain

app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = blockchain.last_block['proof']

    proof = blockchain.proof_of_work(last_proof)
    blockchain.new_transactions("0", node_identifier, 1)

    previous_hash = Blockchain.hash_block(last_block)
    block = blockchain.new_block(previous_hash, proof)

    return jsonify({
        'message': 'New block forged',
        'block': block
    }), 200


@app.route('/transaction', methods=['POST'])
def new_transactions():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']
    if not all (k in values for k in required):
        return 'Missing values', 400

    index = blockchain.new_transactions(values['sender'], values['recipient'], values['amount'])
    response = {'message': f'Transaction will be added to block {index}'}
    return json.dumps(response), 201


@app.route('/chain', methods=['GET'])
def chain():
    return json.dumps({
        "chain": blockchain.chain,
        'length': len(blockchain.chain)
    }), 200


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="""The port to use""", default="5000")
    parser.add_argument("-a", "--address", help="""The address to listen on""", default="0.0.0.0")
    return parser.parse_args()


if __name__ == '__main__':
    arg = parse_arguments()
    app.run(host=arg.address, port=arg.port)
