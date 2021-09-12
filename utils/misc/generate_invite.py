import random

letters = ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


async def create_invite(id):
    ref_hex = hex(id)[2:]
    one_rand_int = random.choice(letters)
    while True:
        two_rand_int = random.choice(letters)
        if one_rand_int != two_rand_int:
            ref_1, ref_2 = one_rand_int + ref_hex, two_rand_int + ref_hex
            return ref_1, ref_2
