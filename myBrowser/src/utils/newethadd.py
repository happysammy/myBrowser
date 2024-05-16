from web3.auto import w3
from web3 import Web3
from mnemonic import Mnemonic
import json


def generate_eth_address(num_addresses) -> list[dict]:
    """
    输入数量生成随机的eth地址
    :param num_addresses: 需要生成的数量
    :return:
    """
    addresses = []
    mnemonic = Mnemonic("english")
    for i in range(num_addresses):
        mnemonic_words = mnemonic.generate(strength=128)
        w3.eth.account.enable_unaudited_hdwallet_features()
        account = w3.eth.account.from_mnemonic(mnemonic_words)
        addr = account.address
        priv_key = Web3.toHex(account.privateKey)

        addresses.append({
            "address": addr,
            "private_key": priv_key,
            "mnemonic": mnemonic_words
        })

    return addresses


# 测试函数
generated_addresses = generate_eth_address(500)
print(json.dumps(generated_addresses))

# for address in generated_addresses:
#     print(address["address"], address["private_key"], address["mnemonic"])