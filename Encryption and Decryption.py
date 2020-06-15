# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 23:59:41 2020

@author: Jay krishna
"""

from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join
import time
import random, struct, sys
def encrypt_file(key, input_file):
    chunksize=16*4*1024

    output_filename = input_file + '.aes'

    initial_vector = os.urandom(16) # urandom: best method :)

    encryptor = AES.new(key, AES.MODE_CBC, initial_vector)
    filesize = os.path.getsize(input_file)

    try:
        with open(input_file, 'rb') as in_file:
            try:
                with open(output_filename, 'wb') as out_file:
                    # put the initial_vector at the beginning of the file
                    # we need to read from this position to decrypt correctly later
                    out_file.write(struct.pack('<Q', filesize))
                    out_file.write(initial_vector)

                    # go block for block through the data
                    while True:
                        # read a block of data
                        chunk = in_file.read(chunksize)
                        # if chunk == 0, we are at the end
                        if len(chunk) == 0:
                            break
                        # else we need to fill the last block of bytes up to 16
                        elif len(chunk) % 16 != 0:
                            chunk += b' ' * (16 - len(chunk) % 16)
                        # encrypt this block and append it to the file
                        out_file.write(encryptor.encrypt(chunk))
            except PermissionError:
                print("\nCouldn't write ", output_filename)
    except PermissionError:
        print("\nCouldn't read ", input_file)


def main1():
    #secret_key = b'--> I am a random secret key <--'

    secret_key = input("Give me a secret key (16, 24 or 32 characters):").encode("utf-8")
    while len(secret_key) != 16 and len(secret_key) != 24 and len(secret_key) != 32:
        print("\nThere was an error! Please try again with 16, 24 or 32 characters:")
        secret_key = input("\nGive me a secret key (16, 24 or 32 characters):").encode("utf-8")

    path = input("\nGive me a path or file to encrypt:")
    while os.path.isdir(path) != True and os.path.isfile(path) != True:
        print("\nThere was an error! Please try again with a correct path or file to encrypt:")
        path = input("\nGive me a path or file to encrypt:")

    # path = directory?
    if os.path.isdir(path):
        files = []
        # traverse all subfolders and save path + filename
        for root, d_names, f_names in os.walk(path):
            for f in f_names:
                files.append(os.path.join(root, f))  # these are all files in all subfolders
        for file in files:
            # better skip already encrypted files
            if not file.endswith(".aes"):
                print("\nEncrypting ", file)
                encrypt_file(secret_key, file)
                # after encryption we could delete the file.. ;)
                # just remove the '#' in the next line
                #os.remove(file)

    # path is no directory, but must be a file
    else:
        # better skip already encrypted files
        if not path.endswith(".aes"):
            print("\nEncrypting ", path)
            encrypt_file(secret_key, path)
            # after encryption we could delete the file.. ;)
            # just remove the '#' in the next line
            #os.remove(path)

def decrypt_file(key, input_file):
    """ Decrypts a file using AES CBC mode with the
       given key.
   """
 
    # This the block size of data we read, decrypt and write.
    # It should be a multiple of 16 for AES.
    chunksize=16*4*1024
 
    # get rid of the .aes ending
    output_filename = os.path.splitext(input_file)[0]
 
    try:
        with open(input_file, 'rb') as in_file:
            # retrieve the original size of the encrypted data
            original_size = struct.unpack('<Q', in_file.read(struct.calcsize('Q')))[0]
            # retrieve the initialization vector
            initial_vector = in_file.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, initial_vector)
 
            # read block for block the encrypted data, decrypt and write
            # sometimes decrypted files are already in place and
            # in use by the system and not writeable e.g. Thumbs.db
            try:
                with open(output_filename, 'wb') as out_file:
                    while True:
                        chunk = in_file.read(chunksize)
                        if len(chunk) == 0:
                            break
                        out_file.write(decryptor.decrypt(chunk))
                    # restore original size
                    out_file.truncate(original_size)
            except PermissionError:
                print("\nCouldn't write ", output_filename)
    except PermissionError:
        print("\nCouldn't read ", input_file)
 
def main2():
    #secret_key = b'--> I am a random secret key <--'
    pass1=input("enter Your password")
    if(pass1==password):
 
        secret_key = input("Give me your secret key (16, 24 or 32 characters):").encode("utf-8")
        while len(secret_key) != 16 and len(secret_key) != 24 and len(secret_key) != 32:
            print("\nThere was an error! Please try again with 16, 24 or 32 characters:")
            secret_key = input("\nGive me your secret key (16, 24 or 32 characters):").encode("utf-8")
 
        path = input("\nGive me a path or file to decrypt:")
        while os.path.isdir(path) != True and os.path.isfile(path) != True:
            print("\nThere was an error! Please try again with a correct path or file to decrypt:")
            path = input("\nGive me a path or file to decrypt:")
 
        # path = directory?
        if os.path.isdir(path):
            files = []
            # traverse all subfolders and save path + filename
            for root, d_names, f_names in os.walk(path):
                for f in f_names:
                    files.append(os.path.join(root, f))  # these are all files in all subfolders
            for file in files:
                # better skip not encrypted files
                if file.endswith(".aes"):
                    print("\nDecrypting ", file)
                    decrypt_file(secret_key, file)
                    # after decryption we could delete the file.. ;)
                # just remove the '#' in the next line
                    os.remove(file)
 
    # path is no directory, but must be a file
        else:
            # better skip not encrypted files + dirty fix
            if path.endswith(".aes") and not path.endswith("Thumbs.db.aes"):
                print("\nDecrypting ", path)
                decrypt_file(secret_key, path)
            # after decryption we could delete the file.. ;)
            # but think about typing in the wrong key...
            # just remove the '#' in the next line
                os.remove(path)
if __name__ == '__main__':
    #while True:
     #   password = str(input("Setting up stuff. Enter a password that will be used for decryption: "))
      #  repassword = str(input("Confirm password: "))
       # if password == repassword:
        #        break
        #else:
          #  print("Passwords Mismatched!")
    #f = open("data.txt", "w+")
     #f.write(password)
      #f.close()
            #enc.encrypt_file("data.txt")
    #print("Please restart the program to complete the setup")
            #time.sleep(15)
            #print("Enter your choice")
   
           
    while True:
        ch=input("1.Encrypt 2.Decrypt Enter your choice")
        if(ch=='1'):
            #clear()
            main1()
            break
        if(ch=='2'):
            password='1@3$'
            main2()
            break
        else:
            print("Enter proper choice")
