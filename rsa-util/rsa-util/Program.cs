using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Intel.PSD.CryptoExtensions
{
    


    class Program
    {
        //These are the primes that form our modulus.
        //static readonly long p = 1163;
        //static readonly long q = 1601;

        /// <summary>
        /// The RSA modulus
        /// </summary>
        static readonly long N = 1861963;  

        /// <summary>
        /// The public exponent.
        /// </summary>
        static readonly long E = 3;

        /// <summary>
        /// The private exponent.
        /// </summary>
        static readonly long D = 1239467;

        /// <summary>
        /// We only support 4 character plaintext words.
        /// </summary>
        static readonly uint REQ_WORD_LEN = 4;

        /// <summary>
        /// The maximum number of words to encrypt or decrypt in one call.
        /// </summary>
        static readonly uint MAX_WORDS = 25;

        /// <summary>
        /// Perform modular exponentiation.
        /// </summary>
        /// <param name="x">The base.</param>
        /// <param name="y">The exponent.</param>
        /// <param name="n">The modulus.</param>
        /// <returns></returns>
        static long power(long x, long y, long n)
        {
            // Initialize result 
            long res = 1;

            // Update x if it is more  
            // than or equal to p 
            x = x % n;

            while (y > 0)
            {
                // If y is odd, multiply  
                // x with result 
                if ((y & 1) == 1)
                {
                    res = (res * x) % n;
                }

                // y must be even now 
                // y = y / 2 
                y = y >> 1;
                x = (x * x) % n;
            }
            return res;
        }

        /// <summary>
        /// Perform basic RSA encryption.
        /// </summary>
        /// <param name="m">The plaintext message.</param>
        /// <returns>The ciphertext.</returns>
        static long encrypt(long m)
        {            
            return power(m, E, N);
        }

        /// <summary>
        /// Performs basic RSA decryption.
        /// </summary>
        /// <param name="c">The ciphertext.</param>
        /// <returns>The decrypted plaintext.</returns>
        static long decrypt(long c)
        {            
            return power(c, D, N);

        }

        /// <summary>
        /// Mapping between characters and numbers used to encode a string.
        /// </summary>
        static readonly Dictionary<char, long> charDigits = new Dictionary<char, long>
        {
            {'`', 0 }, { 'A', 1}, { 'B', 2 }, { 'C', 3 },
            {'D', 4 }, {'E', 5 }, {'F', 6 },  {'G', 7 },
            {'H', 8 }, {'I', 9 }, {'J', 10 }, {'K', 11 },
            {'L', 12 },{'M', 13 },{'N', 14 }, {'O', 15 },
            {'P', 16 },{'Q', 17 },{'R', 18 }, {'S', 19 },
            {'T', 20 },{'U', 21 },{'V', 22 }, {'W', 23 },
            {'X', 24 }, {'Y', 25 },{'Z', 26 }
        };

        /// <summary>
        /// Mapping between integers and characters. Used to decode a number into a string.
        /// </summary>
        static readonly char[] baseChars = new char[] {'`', 'A','B','C',
                                            'D','E','F','G',
                                            'H','I','J','K',
                                            'L','M','N','O',
                                            'P','Q','R','S',
                                            'T','U','V','W',
                                            'X','Y','Z'
                                        };

        /// <summary>
        /// We are using a 27 character alphabet and therefore performing base 27 arithmetic during encode/decode.
        /// </summary>
        static readonly long MOD = 27;
        static readonly long MOD2 = MOD * MOD;
        static readonly long MOD3 = MOD2 * MOD;
        static readonly long MOD4 = MOD3 * MOD;

        /// <summary>
        /// Encode a word as an integer suitable for RSA encryption/decryption.
        /// </summary>
        /// <param name="s">Word to encode. This must be 4 or 5 characters.</param>
        /// <returns>The numerically encoded word.</returns>
        static long encode(string s)
        {
            char[] arr = s.ToUpper().ToCharArray();

            long enc = 0;

            //We handle 5 char words different than 4 char words.
            if (arr.Length == 4)
            {
                enc = (charDigits[arr[0]] * MOD3) +
                       (charDigits[arr[1]] * MOD2) +
                       (charDigits[arr[2]] * MOD) +
                       charDigits[arr[3]];

            }
            else //NOTE: If the word has more than 5 chars, only the first 5 will be encoded.
            {
                enc = (charDigits[arr[0]] * MOD4) +
                        (charDigits[arr[1]] * MOD3) +
                        (charDigits[arr[2]] * MOD2) +
                        (charDigits[arr[3]] * MOD) +
                    charDigits[arr[4]];

            }

            return enc;
        }
        /// <summary>
        /// Decode a base 27 integer into a word.
        /// </summary>
        /// <param name="a">The integer to decode.</param>
        /// <returns>The decoded word.</returns>
        static string decode(long a)
        {
            string s = String.Empty;
            
            do
            {
                s = baseChars[a % MOD] + s;
                a = a / MOD;
            }
            while (a > 0);


            return s;
        }
        
        /// <summary>
        /// A simple class to hold the parsed command line params.
        /// </summary>
        class Args
        {
            /// <summary>
            /// What action to perform.
            /// </summary>
            public enum Verb
            {
                /// <summary>
                /// Do nothing.
                /// </summary>
                None,

                /// <summary>
                /// Encrypt the word.
                /// </summary>
                Encrypt,

                /// <summary>
                /// Decrypt the word.
                /// </summary>
                Decrypt
            }

            /// <summary>
            /// The words to either encrypt or decrypt.
            /// </summary>
            public string[] Words;

            /// <summary>
            /// The action to perform on the word.
            /// </summary>
            public Verb Action;

            /// <summary>
            /// Ctor to initialize the Args instance to a sane state.
            /// </summary>
            public Args()
            {
                Words = null; //We will initialize this when we know how many words we have.

                Action = Verb.None;
            }
        }
        /// <summary>
        /// Parses the command line arguments. It expects at least 2 arguments, the action and a list of words.
        /// </summary>
        /// <param name="args">The args string[] parameter passed to Main.</param>
        /// <returns>An instance of Args containing the command line info.</returns>
        static Args ParseCmdLine(string[] args)
        {
            
            Args a = new Args();
            
            if ( (args.Length >= 2) && (args.Length <= (MAX_WORDS + 1) ) ) //The verb and up to MAX_WORDS words.
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

                //Allocate enough strings for what was provided on the command line.
                a.Words = new string[args.Length - 1];

                for (var i = 1; i < args.Length; i++)
                {
                    a.Words[i-1] = args[i].ToUpper().Trim();
                }
            }


            return a;
        }

        /// <summary>
        /// Encrypt the words using basic RSA and display the intermediate values as well as the result.
        /// </summary>
        /// <param name="ms">The words to encrypt. Each of these must be 4 characters in length.</param>
        static void DoEncryption(string[] ms)
        {
            foreach (string m in ms)
            {
                if (m.Length != REQ_WORD_LEN)
                {
                    throw new ArgumentException("Plaintext is of incorrect length.");
                }

                long enc = encode(m);

                long c = encrypt(enc);

                string s = decode(c);

                Console.WriteLine("Plaintext = {0}, encoding = {1}, encryption = {2}, decoding = {3}.", m, enc, c, s);
            }
        }

        /// <summary>
        /// Decrypt the words using basic RSA and display the intermediate values as well as the result.
        /// </summary>
        /// <param name="cs">The words to decrypt. These must be at least 4 characters in length.</param>
        static void DoDecryption(string[] cs)
        {
            foreach (string c in cs)
            {
                if (c.Length < REQ_WORD_LEN) //NOTE: We do not test for equality, as ciphertext may be 5 characters.
                {
                    throw new ArgumentException("Ciphertext is of incorrect length.");
                }

                long enc = encode(c);

                long dec = decrypt(enc);

                string s = decode(dec);

                Console.WriteLine("Ciphertext = {0}, encoding = {1}, decryption = {2}, decoding = {3}.", c, enc, dec, s);
            }
        }

        static void PrintUsage()
        {
            Console.WriteLine("Usage: rsa-util.exe <E | D> <words>. Use 'E' to encrypt, 'D' to decrypt.");
            Console.WriteLine();
            Console.WriteLine("Up to " + MAX_WORDS.ToString() + " words may be encrypted/decrypted per call.");
            Console.WriteLine();
            Console.WriteLine("Plaintext words must be 4 characters long.");
            Console.WriteLine();
            Console.WriteLine("Ciphertext words may be either 4 or 5 characters long.");
            Console.WriteLine();
            Console.WriteLine("Characters must be alphabetic only and are case insensitive.");
        }

        static void Main(string[] args)
        {
            try
            {
                Args a = ParseCmdLine(args);

                if (a.Action == Args.Verb.Encrypt)
                {
                    DoEncryption(a.Words);
                }
                else if (a.Action == Args.Verb.Decrypt)
                {
                    DoDecryption(a.Words);
                }
                else
                {
                    PrintUsage();

                }
            }
            catch(Exception)
            {
                Console.WriteLine("An unexpected error has occurred. Please make sure you are invoking the utility correctly");
                Console.WriteLine();

                PrintUsage();

            }
        }
    }
}
