# Module to support Lincoln High RSA encryption game.
import sys
import functools
import operator

from enum import Enum
# import random

class utils():
    # Generalized left fold.
    @staticmethod
    def foldl(func, acc, xs):
        return functools.reduce(func, xs, acc)
    

# RSA encrypter/decrypter based on p, q, and e.
class rsa_encrypter():
    def __init__(self, p, q, e):
        #TODO: Use CRT private keys to improve performance.
        #self.p = p
        #self.q = q
        if not self.__is_prime(p):
            raise Exception("p is not prime.")
            
        if not self.__is_prime(q):
            raise Exception("q is not prime.")
            
        self.__n = p * q
        self.__e = e
        self.__d = pow(e, -1, self.__euler_phi(self.__n))
        
    
    def __is_prime(self, n):
        """"pre-condition: n is a nonnegative integer
        post-condition: return True if n is prime and False otherwise."""
        if n < 2: 
             return False
        if n % 2 == 0:             
            return n == 2  # return False
        k = 3
        while k*k <= n:
             if n % k == 0:
                return False
             k += 2
        return True

    def __euler_phi(self, n):
        y = n
        for i in range(2,n+1):
            if self.__is_prime(i) and n % i  == 0:
                y -= y/i
            else:
                continue
        return int(y)

    def encrypt(self, msg):
        if msg >= self.__n:
            raise Exception("Message is larger than RSA modulus.")
            
        return pow(msg, self.__e, self.__n)
        
    def decrypt(self, ctext):
        if ctext >= self.__n:
            raise Exception("Ciphertext is larger than RSA modulus.")
        return pow(ctext, self.__d, self.__n)


# Word encoder/decoder based on base 27 math.
class word_encoder():
    
    def __init__(self):
        self.__base = 27
        self.__letterCodes = list(range(1, self.__base))
        self.__asciiShift = 96

    def __from_digits(self, digits):
        l = len(digits)
        mults = [pow(self.__base, i) for i in list(range(0, l))]
        mults.reverse()
        return utils.foldl(operator.add, 0,[d * m for d,m in zip(digits, mults)])
    
    def encode(self, w): 
        chars = [ord(c) for c in w.lower()]
        digits = [c - self.__asciiShift for c in chars]
        return self.__from_digits(digits)
   
    def __to_digits(self, n):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % self.__base))
            n //= self.__base
        return digits[::-1]

    def decode(self, i):
        digits = self.__to_digits(i)
        return ''.join([chr(d + self.__asciiShift) for d in digits])
    

# The word list with associated ciphertexts along with some verification, query, and extraction routines.    
class word_list():
    def __init__(self, p = 1163, q = 1601, e = 3):
        self.__rsa = rsa_encrypter(p, q, e)
        self.__enc = word_encoder()
    
        #self.__enc = word_encrypter(p, q, e)
        self.__words = ["snit", "hype", "jock", "dude", "labs", "funk", "nosy", 
                        "bomb", "math", "dare", "eeew", "prob", "foul", "tizz", "meow", 
                        "bark", "ditz", "dump", "goop", "guts", "lads", "gals", "icky", 
                        "yuch", "yeti", "wuss", "yawl", "zarf", "yups", "quip", "nill", 
                        "nerd", "pleb", "zoom", "zany", "okay", "mope", "loot", "joke", 
                        "howl", "fans", "doom", "dodo", "ahem", "brat", "chug", "conk", 
                        "clap", "bums", "blah", "clod", "epic", "ogle", "pout", "purr", 
                        "trek", "undo", "vote", "wavy", "woof", "yank", "zest", "burp", 
                        "kaas", "hiya", "clam", "meme", "cram", "grid", "barf", "food", 
                        "fool", "lame", "dumb", "dune", "lard", "bard", "carp", "card", 
                        "flag", "frag", "dead", "dear", "kill", "sail", "sale", "bled",
                        "note", "boat", "coat", "turf", "rude", "lurk", "mute", "deaf",
                        "sign", "sine", "tame", "prey", "pray", "flay", "slip", "flea",
                        "slit", "mace", "bear", "bare", "nice", "lice", "mice", "dice",
                        "case", "care", "lair", "fair", "fare", "hair", "hare", "flee",
                        "fear", "hear", "here", "peer", "pier", "bath", "wart", "glee",
                        "look", "book", "cook", "aloe", "amen", "lady", "lord", "king",
                        "duke", "earl", "boys", "toys", "blob", "grub", "leap", "rare",
                        "real", "read", "rule", "mule", "loop", "bond", "wand", "ward",
                        "dark", "cork", "milk", "mire", "dire", "fire", "find", "bind",
                        "kind", "pots", "mush", "dash", "clip", "roll", "bowl", "bass",
                        "lass", "tote", "coal", "tank", "shut", "take", "open", "rave",
                        "kite", "type", "pike", "pile", "pipe", "dart", "ammo", "curl",
                        "hurl", "girl", "junk", "dunk", "monk", "lump", "limp", "camp",
                        "damp", "liar", "lyre", "pool", "life", "knee", "head", "hand",
                        "eyes", "ears", "nose", "neck", "bite", "nail", "back", "bone",
                        "vain", "vane", "vein", "blue", "frog", "blog", "fork", "bale",
                        "bail", "hail", "hale", "hang", "rang", "cash", "lead", "iron",
                        "gold", "zinc", "oryx", "onyx", "ankh", "oxen", "echo", "done",
                        "lamb", "jinx", "czar", "scab", "opal", "ache", "ogre", "iris",
                        "oboe", "tofu", "udon", "serf", "surf", "brig", "wren", "wrap",
                        "yolk", "yoke", "arid", "ooze", "walk", "coda"
                    ]

        self.__words.sort()
            
        self.__cts = [self.encode_and_encrypt(w) for w in self.__words]
    
    def encode_and_encrypt(self, w): 
        undecoded_ct = self.__rsa.encrypt(self.__enc.encode(w))
        return (undecoded_ct, self.__enc.decode(undecoded_ct))
    
    def decrypt_and_decode(self, w): 
        return self.__enc.decode(self.__rsa.decrypt(self.__enc.encode(w)))
    
    def verify_word(self, ew, dw): 
        return (self.decrypt_and_decode(ew) == dw) and (dw in self.__words)
       
    def verify_word_list(self):
        print("Word list is duplicate free: ", len(list(dict.fromkeys(self.__words))) == len(self.__words))

        print("Word count: ", len(self.__words))
        
        dts = [self.decrypt_and_decode(ct[1]) for ct in self.__cts]
        print("Decryptions successful: ", dts == self.__words)


        matched = utils.foldl(operator.and_, 
                        True, 
                        [
                            self.verify_word(   self.__cts[i][1], 
                                                self.__words[i]) for i in range(0, 
                                                                            len(self.__words)
                                                                            )
                        ]
                       )
        print("Lists match: ", matched)
    
    def print_word_list(self):
        [print(w) for w in self.__words]
        
    def write_word_list(self, filepath):
        with open(filepath, 'w') as f:
            [f.write(w + "\n\n") for w in self.__words]
            
    def print_ciphertext_list(self):
        [print(ct) for ct in self.__cts]
    
    def write_ciphertext_list(self, filepath):
         with open(filepath, 'w') as f:
            [f.write(str(ct) + "\n\n") for ct in self.__cts]
         
    
    def verify_encrypt(self, w):
        is_present = w in self.__words
        enc = self.__enc.encode(w)
        ct = self.__rsa.encrypt(enc)
        dec = self.__enc.decode(ct)
        return (is_present, enc, ct, dec)
        
    def verify_decrypt(self, ct):
        cts = [ct[1] for ct in self.__cts]
        is_present = ct in cts
        enc = self.__enc.encode(ct)
        pt = self.__rsa.decrypt(enc)
        dec = self.__enc.decode(pt)
        return (is_present, enc, pt, dec)
        
    def ve(self, w):
        (is_present, enc, ct, dec) = self.verify_encrypt(w)
        print("Is present: %s, plaintext: %s, encoding: %d, encryption: %d, decoding: %s."%(is_present, w, enc, ct, dec))

    def vd(self, ct):
        (is_present, enc, pt, dec) = self.verify_decrypt(ct)
        print("Is present: %s, ciphertext: %s, encoding: %d, decryption: %d, decoding: %s."%(is_present, ct, enc, pt, dec))

    
def print_usage_and_exit():
    print("Usage: python lincoln_high.py <E|D> <word>")
    exit(1)

class Action(Enum):
    Encrypt = 1
    Decrypt = 2

    @classmethod
    def from_str(cls, str):
        s = str.upper()
        if s == "E":
            return Action.Encrypt
        elif s == "D":
            return Action.Decrypt
        else:
            raise Exception("Invalid action.")


def parse_command_line(args):
    action_str = args[1]
    word = args[2]
    return (Action.from_str(action_str), word)

# Main execution here.
if __name__ == "__main__":

#### Example usage
# import lincoln_high
# These are now the defaults in the word_list ctor.
# [p, q, e] = [1163, 1601, 3]

    args = sys.argv

    if len(args) != 3:
        print_usage_and_exit()

    try:
        (action, word) = parse_command_line(args)

        wl = word_list()

        if action == Action.Encrypt:
            wl.ve(word)
        else:
            wl.vd(word)

        # wl.verify_word_list()

    except Exception as e:
        print("Error: ", e)
        print_usage_and_exit()

    # wl.print_ciphertext_list()
    
    # wl.write_ciphertext_list("ciphertext.txt")
