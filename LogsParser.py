from pyparsing import Word, alphas, nums, ZeroOrMore, Suppress, Optional


class Log(object):
    
    def __init__(self):
        self.__api_name = Word(alphas + '_')
        self.__date = Word(nums + '-')
        self.__time = Word(nums + ':')
        self.__key = Word(alphas + nums)
        self.__ip = Word(nums + '.')
        self.__link = Word(alphas + nums + ':' + '/' + '.' + '_' + '?' + '&')

    def ShowFullInfo(self, LOG):
        self.__LOG_full = Suppress(self.__api_name + '|') + self.__date + self.__time + Suppress('[' + self.__key + ']' + 'INFO:') + self.__ip + self.__link
        print(self.__LOG_full.parseString(LOG))
    
    def CheckCompletedPurchase(ip):
        return 0

if __name__ == "__main__":
    try:
        LOG = Log()
        logsFile = open("logs.txt", "r")
        s = logsFile.readline()
        for log in logsFile:
            LOG.ShowFullInfo(log)

    finally:
        logsFile.close()


   




