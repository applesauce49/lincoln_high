using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Intel.PSD.CryptoExtensions
{
    


    class Program
    {
        //static readonly long p = 1163;
        //static readonly long q = 1601;
        static readonly long n = 1861963;
        static readonly long e = 3;
        static readonly long d = 1239467;

        static long power(long x, long y, long p)
        {
            // Initialize result 
            long res = 1;

            // Update x if it is more  
            // than or equal to p 
            x = x % p;

            while (y > 0)
            {
                // If y is odd, multiply  
                // x with result 
                if ((y & 1) == 1)
                {
                    res = (res * x) % p;
                }

                // y must be even now 
                // y = y / 2 
                y = y >> 1;
                x = (x * x) % p;
            }
            return res;
        }

        static long encrypt(long m)
        {
            return power(m, e, n);
        }

        static long decrypt(long c)
        {
            return power(c, d, n);

        }

        static Dictionary<char, long> charDigits = new Dictionary<char, long>
        {
            {'`', 0 }, { 'A', 1}, { 'B', 2 }, { 'C', 3 },
            {'D', 4 }, {'E', 5 }, {'F', 6 },  {'G', 7 },
            {'H', 8 }, {'I', 9 }, {'J', 10 }, {'K', 11 },
            {'L', 12 },{'M', 13 },{'N', 14 }, {'O', 15 },
            {'P', 16 },{'Q', 17 },{'R', 18 }, {'S', 19 },
            {'T', 20 },{'U', 21 },{'V', 22 }, {'W', 23 },
            {'X', 24 }, {'Y', 25 },{'Z', 26 }
        };

        static char[] baseChars = new char[] {'`', 'A','B','C',
                                            'D','E','F','G',
                                            'H','I','J','K',
                                            'L','M','N','O',
                                            'P','Q','R','S',
                                            'T','U','V','W',
                                            'X','Y','Z'
                                        };

        static readonly long mod = 27;
        static readonly long mod2 = mod * mod;
        static readonly long mod3 = mod2 * mod;
        static readonly long mod4 = mod3 * mod;

        static long encode(string s)
        {
            char[] arr = s.ToUpper().ToCharArray();

            long enc = 0;

            if (arr.Length == 5)
            {
                enc = (charDigits[arr[0]] * mod4) + 
                        (charDigits[arr[1]] * mod3) + 
                        (charDigits[arr[2]] * mod2) + 
                        (charDigits[arr[3]] * mod) + 
                    charDigits[arr[4]];
                

            }
            else
            {
                enc = (charDigits[arr[0]] * mod3) +
                       (charDigits[arr[1]] * mod2) +
                       (charDigits[arr[2]] * mod) +
                       charDigits[arr[3]];
                   
            }

            return enc;
        }

        static string decode(long a)
        {
            string s = String.Empty;

            const long targetBase = 27;

            do
            {
                s = baseChars[a % targetBase] + s;
                a = a / targetBase;
            }
            while (a > 0);


            return s;
        }

       
        

        class Args
        {
            public enum Verb
            {
                None,
                Encrypt,
                Decrypt
            }
            public string Word;
            public Verb Action;

            public Args()
            {
                Word = String.Empty;
                Action = Verb.None;
            }
        }

        static Args ParseCmdLine(string[] args)
        {
            
            Args a = new Args();

            

            if (args.Length == 2) //The verb and word
            {

                string verb = String.Empty;

                string action = args[0].ToUpper().Trim();

                if (action == "E")
                {
                    a.Action = Args.Verb.Encrypt;
                }
                else if (action == "D")
                {
                    a.Action = Args.Verb.Decrypt;
                }
                else
                {
                    a.Action = Args.Verb.None;
                }

                a.Word = args[1].ToUpper().Trim();

            }


            return a;
        }

        static void DoEncryption(string m)
        {
            long enc = encode(m);

            long c = encrypt(enc);

            string s = decode(c);

            Console.WriteLine("Plaintext = {0}, encoding = {1}, decryption = {2}, decode = {3}", m, enc, c, s);

        }

        static void DoDecryption(string c)
        {            
            long enc = encode(c);

            long dec = decrypt(enc);

            string s = decode(dec);
                        
            Console.WriteLine("Ciphertext = {0}, encoding = {1}, decryption = {2}, decode = {3}", c, enc, dec, s);
        }

        static void Main(string[] args)
        {
            Args a = ParseCmdLine(args);

            if (a.Action == Args.Verb.Encrypt)
            {
                DoEncryption(a.Word);
            }
            else if (a.Action == Args.Verb.Decrypt)
            {
                DoDecryption(a.Word);
            }
            else
            {
                Console.WriteLine("Usage: lincoln-high <E | D> <word>. Use 'E' to encrypt, 'D' to decrypt.");

            }
        }
    }
}
