def log(content):
    f = open("log.txt", "a")
    f.write(content + "\n\n")
    f.close()