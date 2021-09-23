import os
### 词库去重
files = os.listdir('key/')
for file in files:
    with open('key/'+file, 'r', encoding='utf-8') as fp:
        word = fp.read().split('\n')
        print("词库({})去重前的数目：{}".format(file, len(word)))
        word = set(word)
        print("去重后的词库数目：{}".format(len(word)))
    with open('key/' + file, 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(word))