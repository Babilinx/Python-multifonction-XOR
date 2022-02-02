# The random and string libraries are used to generate a random string with flexible criteria
import string
import random
import sys
import os
import tqdm


def help():  # simple help message
    print("""\n
    Simple python XOR encryption/decryption by Babilinx\n\n
    name.py [fonction] [text you want to use] [file to use] [output filename] [-o] {key}

    fonctions:
    -h          Show this help message
    -setup      Setup all of requirements in the folder where the file is.
    -e          Encrypt the text you are used in second position with the key what is enter if it's enter,
                else it generate a key and print it
    -d          Decrypt the text you are used in second position with the key what is enter
    -eFile      Encrypt a file you are used in second position with the key what is enter if it's enter,
                else it generate a key and print it (you also can use -o option)
    -dFile      Decrypt a file you are used in second position with the key's file (ex: C:\...\...\keys\keyname.txt)
    -o          Write/read the key into a file""")


def key_gen(txt):
    key = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase +
                  string.digits + '^!\$%&/()=?{[]}+~#-_.:,;<>') for i in range(len(txt)))
    return key  # key generator with the length of {key} equals to {txt} length


def xor(txt, key):
    try:
        txt = sys.argv[2]
    except IndexError:
        print("\nArgumentError: Try '-h' to show help menu")
        pass
    output = []
    for i in range(len(txt)):
        xor_num = ord(txt[i]) ^ ord(key[i % len(key)])
        output.append(chr(xor_num))
    return ''.join(output)  # xor {txt} with the key {key}


try:
    fonc = sys.argv[1]
except IndexError:
    print("FatalError")
    help()
    sys.exit()


if fonc == "-h":
    help()

if fonc == "-e" or fonc == "-d":
    try:
        txt = sys.argv[2]
    except IndexError:
        print("\nArgumentError: Try '-h' to show help menu")
    try:
        key = sys.argv[3]
    except IndexError:
        key_statut = False  # True if the key was enteer as sys.argv[3]
        key = key_gen(txt)
    try:
        if fonc == "-e":
            print(f"\nkey = {key}")
        print(f"\ntext = {xor(txt, key)}")
    except NameError:
        pass
    if sys.argv[4] == "-o":
        key_name = input("Enter the key name: ")
        if not os.path.isdir("keys"):
            os.mkdir("keys")
        os.chdir("keys")
        with open(key_name, "a") as f_key_name:
            f_key_name.write(key)

if fonc == "-t":
    txt = sys.argv[2]
    key = sys.argv[3]
    t = xor(txt, key)
    print(t)
    print(xor(t, key))

if fonc == "-eFile":
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(input_file, "rb") as f_input_file:
        print(f"[+] Reading {input_file} ...")
        filesize = os.path.getsize(input_file)
        try:
            if sys.argv[4] != "-o":
                try:
                    key = sys.argv[4]
                except IndexError:
                    print("KeyError: Please enter a key\n")
                    key_gen_question = input(
                        f"Do you want to generate a key wich have the lenght of the file ?({filesize/1024}kb) [Y|n] ")
                    if key_gen_question == "y" or key_gen_question == "Y":
                        print("[*] Generating the key, it can take a long...")
                        key = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase +
                                      string.digits + '^!\$%&/()=?{[]}+~#-_.:,;<>') for u in range(filesize))
                    else:
                        print("Try '-h' to show help menu")
                        sys.exit()
        except IndexError:
            print("FatalError: Try '-h' to show help menu")
            sys.exit()
        try:
            if sys.argv[4] == "-o":
                key_name = input("Enter the key name: ")
                if not os.path.isdir("keys"):
                    os.mkdir("keys")
                os.chdir("keys")
                with open(key_name + ".txt", "w") as f_key_name:
                    print("[*] Generating the key, it can take a long...")
                    key = ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase +
                                  string.digits + '^!\$%&/()=?{[]}+~#-_.:,;<>') for u in range(filesize))
                    f_key_name.write(key)
        except IndexError:
            print("FatalError: Try '-h' to show help menu")
            sys.exit()

        with open(output_file, "wb") as f_output_file:
            print(f"[+] Creating {output_file} ...")
            i = 0
            progress = tqdm.tqdm(range(filesize), unit="o", unit_scale=True, unit_divisor=1024)
            while f_input_file.peek():
                if not i % 20:
                    progress.update(20)
                c = ord(f_input_file.read(1))
                j = i % len(key)
                b = bytes([c ^ ord(key[j])])
                f_output_file.write(b)
                i += 1
            print("\n[+] Done")

if fonc == "-dFile":
    try:
        input_file = sys.argv[2]
    except IndexError:
        print("ArgumentError: Try '-h' to show help menu")
    try:
        output_file = sys.argv[3]
    except IndexError:
        print("ArgumentError: Try '-h' to show help menu")

    with open(input_file, "rb") as f_input_file:
        print(f"[+] Reading {input_file} ...")
        filesize = os.path.getsize(input_file)

        try:
            if sys.argv[5] == "-o":
                try:
                    key_file = sys.argv[4]
                    if not os.path.isdir("keys"):
                        print("DirectorryError: Directorry 'keys' don't exist, use '-setup'")
                        sys.exit()
                    os.chdir("keys")
                    with open(key_file, "rt") as f_key_file:
                        key = f_key_file
                        print(f_key_file)

                except IndexError:
                    print(f"\nArgumentError: Try '-h' to show help menu")

            else:
                print(
                    f"\nArgumentError: name '{sys.argv[4]}' is not defined\nTry '-h' to show help menu")

        except IndexError:
            key = sys.argv[4]

        with open(output_file, "wb") as f_output_file:
            print(f"[+] Creating {output_file} ...")
            i = 0
            progress = tqdm.tqdm(range(filesize), unit="o", unit_scale=True, unit_divisor=1024)
            while f_input_file.peek():
                if not i % 20:
                    progress.update(20)
                c = ord(f_input_file.read(1))
                j = i % len(key)
                b = bytes([c ^ ord(key[j])])
                f_output_file.write(b)
                i += 1
            print("\n[+] Done")
            sys.exit()

if fonc == "-setup":
    os.mkdir("keys")

else:
    print(f"\nArgumentError: name '{fonc}' is not defined\nTry '-h' to show help menu")
