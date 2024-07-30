
def main():
    for i in range(1, 13):
        if i == 3:
            continue
        if i == 11:
            break
        if i % 2 == 0:
            print(hex(i))
        else:
            print(i)

if __name__ == "__main__":
    main()
    