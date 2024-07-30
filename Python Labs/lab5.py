import datetime
import hashlib
import os
import string

today = None


def iterate(match: int, lower: int, upper: int) -> None:
    """
    match: The interger to terminate early on.
    lower: The lower boundary for iteration
    upper: The upper boundary for iteration that is inclusive 

    return: None
    """

    for i in range(lower, upper +1):
        if i ==  match:
            break
        if i % 2 == 0:
            print(i)

def update_date() -> None:
    """
    Updates global today
    """

    global today
    today = datetime.datetime.now()

def hash_file(file_name: str) -> str:
    """
    file_name: relative path to read a file

    return: md5 digest of file contents
    """

    with open(file_name, 'rb') as file_in:
        contents =  file_in.read()
    
    return hashlib.md5(contents).hexdigest()

def arg_split(split_val: int, *args: tuple) -> list:
    """
    split_val: An integer used for splitting the argument list.
    *args: A tuple of values to return if divisibe split_val

    return: list of arguments divisible by split_val
    """

    return [a for a in args if a%split_val == 0]

def hash_directory(path: str, recursive: bool = False, duplicate_check: bool = False):
    """
    path: The path of the directory to iterate over.
    recursive: Boolean to indicate whether to iterate over sub directories.
    duplicate_check: Boolean to indicate whether to check for duplicates.

    return: generator object for yielding file name and hex_digest. 
    """
    seen_hashes = set()

    if recursive:
        for root, dirs, files in os.walk(path):
            for file in files:

                file_name = file
                digest = hash_file(os.path.join(root, file_name))

                if duplicate_check:
                    yield file_name, digest, f"Duplicate: {'Yes' if digest in seen_hashes else 'No'}"
                else:
                    yield file_name, digest
                
                seen_hashes.add(digest)
        
    else:

        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                continue
            else:
                file_name = item
                digest = hash_file(os.path.join(path, file_name))

                if duplicate_check:
                    yield file_name, digest, f"Duplicate: {'Yes' if digest in seen_hashes else 'No'}"
                else:
                    yield file_name, digest
                seen_hashes.add(digest)

def rot13(input_string: str) -> str:
    """
    string: The string to conduct an ROT13 on.

    return: The result of an ROT13 on the input.
    """
    letters = string.ascii_lowercase
    rtnString = ""

    for s in input_string:
        index = letters.index(s.lower())
        offset = (index + 13) % 26
        rtnString += letters[offset] if s.islower() else letters[offset].upper()

    return rtnString

if __name__ == "__main__":
    # Task 1
    print("Starting Task 1:\n")
    iterate(23, 2, 25)
   
    # Task 2
    print("\nStarting Task 2:\n")
    print(f"Today is: {'unknown' if today is None else today}")
    update_date()
    print(f"Today is: {'unknown' if today is None else today}")
   
    # Task 3
    print("\nStarting Task 3:\n")
    response = arg_split(14, 13, 14, 28, 29, 42)
    print(f'Remaining arguments are: {response}')
  
    # Task 4
    print("\nStarting Task 4:\n")
    digest = hash_file('lab5.py')
    print(f'The MD5 digest of lab5.py is: {digest}')
  
    # Task 5
    # Use the root directory of the student share
    print("\nStarting Task 5:\n")
    for item in hash_directory('Z:/'): 
        print(item)
    # Use the root directory of the student share, but include sub directories
    for item in hash_directory('Z:/', recursive=True, duplicate_check=True):
        print(item)

    # Task 6
    print("\nStarting Task 6:\n")
    cipher_text = rot13("ThisIsATestOfTheEmergencyBroadcastSystem")
    clear_text = rot13(cipher_text)
    print(f"Cipher:\t{cipher_text}")
    print(f"Clear:\t{clear_text}")
