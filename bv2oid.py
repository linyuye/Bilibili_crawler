XOR_CODE = 23442827791579
MASK_CODE = 2251799813685247
MAX_AID = 1 << 51
ALPHABET = "FcwAPNKTMug3GV5Lj7EJnHpWsx4tb8haYeviqBz6rkCy12mUSDQX9RdoZf"
ENCODE_MAP = 8, 7, 0, 5, 1, 3, 2, 4, 6
DECODE_MAP = tuple(reversed(ENCODE_MAP))
BASE = len(ALPHABET)
PREFIX = "BV1"
PREFIX_LEN = len(PREFIX)
CODE_LEN = len(ENCODE_MAP)
def av2bv(aid):
    bvid = [""] * 9
    tmp = (MAX_AID | aid) ^ XOR_CODE
    for i in range(CODE_LEN):
        bvid[ENCODE_MAP[i]] = ALPHABET[tmp % BASE]
        tmp //= BASE
    return PREFIX + "".join(bvid)

def bv2av(bvid) :
    assert bvid[:3] == PREFIX
    bvid = bvid[3:]
    tmp = 0
    for i in range(CODE_LEN):
        idx = ALPHABET.index(bvid[DECODE_MAP[i]])
        tmp = tmp * BASE + idx
    return (tmp & MASK_CODE) ^ XOR_CODE

print(bv2av("BV1yTLAzuEZB"))