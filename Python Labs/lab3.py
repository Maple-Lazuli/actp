import string

def main():
    # Building dictionary
    nums_0_to_25: list = [_ for _ in range(0,26)]
    lower_letters: str = string.ascii_lowercase
    my_dictionary: dict = dict()
    for k,v in zip(lower_letters, nums_0_to_25):
        my_dictionary[k] = v

    # Generating File
    with open("mypairs.txt", "w") as file_out:
        for k in my_dictionary:
            file_out.write(f"{k}:{my_dictionary[k]}\n")

if __name__ == "__main__":
    main()