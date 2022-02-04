# The random and string libraries are used to generate a random string with flexible criteria
import string
import random
import sys
import os
import tqdm


def help():  # simple help message
    print("""\n
    Simple python XOR encryption/decryption by Babilinx\n\n
    name.py [fonction] [text you want to use] [file to use] {key} [-f] [filename] [-o] [filename]

    fonctions:
    -h          Show this help message
    -e          Encrypt the text you are used in second position with the key
                what is enter if it's enter,
                else it generate a key and print it
    -d          Decrypt the text you are used in second position with the key
                what is enter
    -eFile      Encrypt a file you are used in second position with the key
                what is enter if it's enter,
                else it generate a key and print it (you also can use -f option)
    -dFile      Decrypt a file you are used in second position with the key's file
                (ex: C:\...\...\keys\keyname.txt)
    -f          Write/read keys on a file.
    -o          Write outputs in a file.

    See more on README file on GitHub ! """)


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


# check if the user have enter an arguments
try:
    fonc = sys.argv[1]
except IndexError:
    print("FatalError")
    help()
    sys.exit()

# help menu
if fonc == "-h":
    help()
# encrypt fonction
elif fonc == "-e":
    # check if the user enter an argument
    try:
        txt = sys.argv[2]
    except IndexError:
        print("\nArgumentError: Try '-h' to show help menu")
        sys.exit()
        # check if the user enter a key, if not it generate one
    try:
        key = sys.argv[3]
    except IndexError:
        # generate the key
        key = key_gen(txt)
    # print the key and encrypted text
    print("\nkey = {}".format(key))
    print("\ntext = {}".format(xor(txt, key)))
    # check for f fonction
    try:
        if sys.argv[4] == "-f":
            try:
                # try to catch filename
                key_name = sys.argv[5]
            except IndexError:
                key_name = input("Enter the key filename: ")
            # check if keys dirrectory exists
            if not os.path.isdir("keys"):
                # if not, it will create it if the user is okey
                if input("Error: Dirrectory 'keys' don't exists.\nDo you want to create it ? [y|n] ") == "y":
                    # create it
                    os.mkdir("keys")
            # go to dir keys
            os.chdir("keys")
            # write the key in the key_file
            with open(key_name, "a") as f_key_name:
                f_key_name.write(key)
    # if not f fonction, just pass
    except IndexError:
        pass

# decrypt fonction
elif fonc == "-d":
    # check if the user enter an argument
    try:
        txt = sys.argv[2]
    except IndexError:
        print("\nArgumentError: Try '-h' to show help menu")
        sys.exit()
    # check if the user enter the key
    try:
        key = sys.argv[3]
    except IndexError:
        print("\nArgumentError: Try '-h' to show help menu")
    # check for f fonction
    try:
        if sys.argv[4] == "-f":
            try:
                # try to catch filename
                key_name = sys.argv[5]
            except IndexError:
                key_name = input("Enter the key's filename: ")
            # check if keys dirrectory exists
            if not os.path.isdir("keys"):
                # if not, it will create it if the user is okey
                if input("Error: Dirrectory 'keys' don't exists.\nDo you want to create it ? [y|n] ") == "y":
                    # create it
                    os.mkdir("keys")
                    # exiting because the key file can't exists
                    sys.exit()
            # go to dir keys
            os.chdir("keys")
            # read the key in the key_file
            with open(key_name, "r") as f_key_name:
                key = f_key_name.read()
    # if not f fonction, just print the key and pass
    except IndexError:
        print(f"key = {key}")
        pass

    # check for -o fonction
    try:
        if sys.argv[6] == "-o":
            try:
                filename = sys.argv[7]
                # open the file and write the decrypt text
                with open(filename, "w") as f:
                    f.write(xor(txt, key))
            except IndexError:
                print("FileNotExist: Try '-h' to show help menu")
    # in not o fonction, just pass
    except IndexError:
        pass


elif fonc == "-eFile":
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    with open(input_file, "rb") as f_input_file:
        print(f"[+] Reading {input_file} ...")
        filesize = os.path.getsize(input_file)
        try:
            if sys.argv[4] != "-f":
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

elif fonc == "-dFile":
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
                print(f"\nArgumentError: name '{sys.argv[4]}' is not defined\nTry '-h' to show help menu")

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


else:
    print(f"\nArgumentError: name '{fonc}' is not defined\nTry '-h' to show help menu")
