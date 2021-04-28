"""
Ohad Omrad
Python and Git
"""

"""
This python code needed to be ran at one time before the server is up in order to initial the bank system
"""

import Bank
import CacheManager

bank = Bank.Bank("MyBank")
bank.addAccount("ohad", Bank.Bank.genarateKey("123"), "456")
bank.addAccount("noam", Bank.Bank.genarateKey("1234"), "1234")
CacheManager.FileCacheManager.saveBank(bank)
print("Bank Initial Boot")