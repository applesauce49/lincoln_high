# Module to support Lincoln High RSA encryption game.

import functools
import operator
import random

# Generalized left fold.
def foldl(func, acc, xs):
    return functools.reduce(func, xs, acc)

# RSA encrypter/decrypter based on p, q, and e.
class rsa_encrypter():
    def __init__(self, p, q, e):
        #TODO: Use CRT private keys to improve performance.
        #self.p = p
        #self.q = q
        if not self.is_prime(p):
            raise Exception("p is not prime.")
            
        if not self.is_prime(q):
            raise Exception("q is not prime.")
            
        self.n = p * q
        self.e = e
        self.d = pow(e, -1, self.euler_phi(self.n))
        

    def is_prime(self, n):
        """"pre-condition: n is a nonnegative integer
        post-condition: return True if n is prime and False otherwise."""
        if n < 2: 
             return False;
        if n % 2 == 0:             
            return n == 2  # return False
        k = 3
        while k*k <= n:
             if n % k == 0:
                return False
             k += 2
        return True

    def euler_phi(self, n):
        y = n
        for i in range(2,n+1):
            if self.is_prime(i) and n % i  == 0 :
                y -= y/i
            else:
                continue
        return int(y)

    def encrypt(self, msg):
        if msg >= self.n:
            raise Exception("Message is larger than RSA modulus.")
            
        return pow(msg, self.e, self.n)
        
    def decrypt(self, ctext):
        if ctext >= self.n:
            raise Exception("Ciphertext is larger than RSA modulus.")
        return pow(ctext, self.d, self.n)


# Word encoder/decoder based on base 27 math.
class word_encoder():
    
    def __init__(self):
        self.base = 27
        self.letterCodes = list(range(1, self.base))
        self.asciiShift = 96

    def from_digits(self, digits):
        l = len(digits)
        mults = [pow(self.base, i) for i in list(range(0, l))]
        mults.reverse()
        return foldl(operator.add, 0,[d * m for d,m in zip(digits, mults)])
    
    def encode(self, w): 
        chars = [ord(c) for c in w.lower()]
        digits = [c - self.asciiShift for c in chars]
        return self.from_digits(digits)
   
    def to_digits(self, n):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % self.base))
            n //= self.base
        return digits[::-1]

    def decode(self, i):
        digits = self.to_digits(i);
        return ''.join([chr(d + self.asciiShift) for d in digits])
    

# Word encode and encrypt / decrypt and decode
class word_encrypter():
    def __init__(self, p, q, e):
        self.rsa = rsa_encrypter(p, q, e)
        self.enc = word_encoder()
    
    def encode_and_encrypt(self, w): 
        return self.enc.decode(self.rsa.encrypt(self.enc.encode(w)))
    
    def decrypt_and_decode(self, w): 
        return self.enc.decode(self.rsa.decrypt(self.enc.encode(w)))
    
    def verify_word(self, ew, dw, words): 
        return (self.decrypt_and_decode(ew) == dw) and (dw in words)
    
    
# The word list with associated ciphertexts along with some verification, query, and extraction routines.    
class word_list():
    def __init__(self, p, q, e):
        self.enc = word_encrypter(p, q, e)
        self.words = ["snit", "hype", "jock", "dude", "labs", "funk", "nosy", 
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

        self.words.sort()
            
        self.cts = [self.enc.encode_and_encrypt(w) for w in self.words]
            
    def verify_word_list(self):
        print("Word list is duplicate free: ", len(list(dict.fromkeys(self.words))) == len(self.words))

        print("Word count: ", len(self.words))
        
        dts = [self.enc.decrypt_and_decode(ct) for ct in self.cts]
        print("Decryptions successful: ", dts == self.words)


        matched = foldl(operator.and_, 
                        True, 
                        [self.enc.verify_word(self.cts[i], self.words[i], self.words) for i in range(0, len(self.words))]
                       )
        print("Lists match: ", matched)
    
    def print_word_list(self):
        [print(w) for w in self.words]
        
    def write_word_list(self, filepath):
        with open(filepath, 'w') as f:
            [f.write(w + "\n\n") for w in self.words]
            
    def print_ciphertext_list(self):
        [print(ct) for ct in self.cts]
    
    def write_ciphertext_list(self, filepath):
         with open(filepath, 'w') as f:
            [f.write(ct + "\n\n") for ct in self.cts]
         
    
    def word_in_words(self, w):
        return w in self.words
    
    def ct_in_ciphertexts(self, ct):
        return ct in self.cts
    

#### Example usage
# import lincoln_high
# import operator

# [p, q, e] = [1163, 1601, 3]

# wl = lincoln_high.word_list(p, q, e)

# wl.verify_word_list()

# print(wl.word_in_words("yolk"))
# print(wl.ct_in_ciphertexts("buywu"))


# wl.print_ciphertext_list()
# wl.write_ciphertext_list("ciphertext.txt")