from django.test import TestCase

# Create your tests here.
# import hashlib
# import datetime
#
#
# def getHash(f):
#     line = f.readline()
#     hash = hashlib.md5()
#     while (line):
#         hash.update(line)
#         line = f.readline()
#     return hash.hexdigest()
#
#
# print(getHash(open('1.txt', 'rb')))
# print(getHash(open('2.txt', 'rb')))

import os
os.remove("q.txt")
