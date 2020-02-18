with open('./Debug_R15167_ПАРАМ.ci', 'rb') as readFile:
    ss = readFile.read()
    # ss = strToWrite.encode(encoding='cp1251')
    ss = ss.replace(b'READY', b'\x00')

with open('./Debug_R15167_ПАРАМ.ci', 'wb') as writeFile:
    ss = writeFile.write(ss)