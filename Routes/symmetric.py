from flask import Blueprint, request, jsonify
import base64
from Crypto.Cipher import AES, DES, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

symmetric_bp = Blueprint('symmetric', __name__)

# ── GENERATE KEY + IV ─────────────────────────
@symmetric_bp.route('/api/symmetric/generate-key', methods=['POST'])
def generate_key():
    algo = request.json.get('algorithm', 'AES-256')

    if algo == 'AES-256':
        key = get_random_bytes(32)
        iv  = get_random_bytes(16)
    elif algo == 'AES-128':
        key = get_random_bytes(16)
        iv  = get_random_bytes(16)
    elif algo == 'DES':
        key = get_random_bytes(8)
        iv  = get_random_bytes(8)
    elif algo == '3DES':
        key = get_random_bytes(24)
        iv  = get_random_bytes(8)
    else:
        return jsonify({'error': 'Unknown algorithm'}), 400

    return jsonify({
        'key': key.hex(),
        'iv': iv.hex()
    })


# ── ENCRYPT ─────────────────────────
@symmetric_bp.route('/api/symmetric/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    algo = data.get('algorithm')
    key = bytes.fromhex(data.get('key'))
    iv  = bytes.fromhex(data.get('iv'))
    plaintext = data.get('plaintext', '').encode()

    if algo in ('AES-256', 'AES-128'):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    elif algo == 'DES':
        cipher = DES.new(key, DES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, DES.block_size))

    elif algo == '3DES':
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(plaintext, DES3.block_size))

    else:
        return jsonify({'error': 'Unknown algorithm'}), 400

    return jsonify({'result': base64.b64encode(ciphertext).decode()})


# ── DECRYPT ─────────────────────────
@symmetric_bp.route('/api/symmetric/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    algo = data.get('algorithm')
    key = bytes.fromhex(data.get('key'))
    iv  = bytes.fromhex(data.get('iv'))
    ciphertext = base64.b64decode(data.get('ciphertext'))

    if algo in ('AES-256', 'AES-128'):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    elif algo == 'DES':
        cipher = DES.new(key, DES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), DES.block_size)

    elif algo == '3DES':
        cipher = DES3.new(key, DES3.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)

    else:
        return jsonify({'error': 'Unknown algorithm'}), 400

    return jsonify({'result': plaintext.decode()})