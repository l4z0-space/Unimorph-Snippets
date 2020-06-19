



findFeature={}
def readAppendix():
    with open("models/features.txt","r") as fileContent:

        for row in fileContent:
            rowWords = row.split(";")
            dimension = rowWords[0]
            feature = rowWords[1]
            label =(rowWords[2].rstrip()).upper()
            findFeature[label]=feature

DICT={}
def get_lemmas():
    it = 1
    with open("bulgarian.txt","r",encoding="utf8") as data, open('lemma.txt','a',encoding='utf-8') as outFile:
        for x in data:
            line = x.split()
            try:
                features = line[-1]
                lemma = line[0]
                POS = features.split(';')[0]

                try:
                    if DICT[lemma] == 1:
                        pass
                except KeyError:
                    DICT[lemma] = 1
                    feat_name = findFeature[POS]
                    line =(f"{lemma},{feat_name}")
                    print(line)
                    outFile.write(line+"\n")
            except IndexError:
                print("invalid line")

readAppendix()
get_lemmas()
