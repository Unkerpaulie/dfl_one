from faker import Faker

fake = Faker()

# print("start")
exclude = ["zip", "tar", "binary", "get_words_list", "image", "pystruct"]
# start = 300
# counter = 0

with open("fake_reference.txt", "a") as f:
    for func in fake.__dir__():
        if not func.startswith("_") and func not in exclude:
        # counter += 1
        # if counter > start:
            f.write("    ++++++++      \n")
            try:
                f.write(f"{func}: {eval('fake.'+func+'()')}\n")
            except:
                f.write(f"{func}: not callable\n")
    # if counter > start + 20:
    #     break