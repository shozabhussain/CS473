#!/usr/bin/env python3
# -*- coding: latin-1 -*-
blob = """
    �*�jc��(�:���7���E�?ֹ�$�Z���l�5ekJ㱻U���\�N�|KG�"m�_L�>T�_�kCu]w�ϻ��^@�� ��ϧ_���[z��`6�?�3H�M7u�R��	^ͽS��;
"""
from hashlib import sha256
if(sha256(blob.encode()).hexdigest() == "22418c4b6146fb5f3b025102ea8be3a0f266fc3793c28502d57d66ff8b89d3cb"):
	print("Prepare to be destroyed!")
elif(sha256(blob.encode()).hexdigest() == "f7e70395fd924cc9cb543c5f6e5c9e33858f68fcfd96027b7d38b56212dd8464"):
	print("I come in peace.")