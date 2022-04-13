import random


class OneParticipant:
    def __init__(self, prime, alpha):
        self.__private_key = random.randrange(0, prime - 1)
        self.__public_key = (alpha ** self.__private_key) % prime
        self.__prime = prime
        self.__share_key = 1

    def get_pubkey(self):
        return self.__public_key

    def cal_share_key(self, another_key):
        self.__share_key = (another_key ** self.__private_key) % self.__prime
        return self.__share_key
