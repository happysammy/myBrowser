import json
import base64
from cryptography.fernet import Fernet
from myBrowser.src.utils.config_loader import get_config_path
import getpass

class EVMAddress:
    def __init__(self, index, address, private_key=None, mnemonic=None, encryption_key=None):
        self.index = index
        self.address = address
        self._private_key = private_key
        self._mnemonic = mnemonic
        if private_key and mnemonic and encryption_key:
            self.set_encrypted_secrets(private_key, mnemonic, encryption_key)

    def set_encrypted_secrets(self, private_key, mnemonic, encryption_key):
        """加密并保存私钥和助记词"""
        fernet = Fernet(base64.urlsafe_b64encode(encryption_key.encode()[:32].ljust(32, b'\0')))
        self._private_key = fernet.encrypt(private_key.encode()).decode()
        self._mnemonic = fernet.encrypt(mnemonic.encode()).decode()

    def get_private_key(self, encryption_key):
        """解密并返回私钥"""
        fernet = Fernet(base64.urlsafe_b64encode(encryption_key.encode()[:32].ljust(32, b'\0')))
        return fernet.decrypt(self._private_key.encode()).decode()

    def get_mnemonic(self, encryption_key):
        """解密并返回助记词"""
        fernet = Fernet(base64.urlsafe_b64encode(encryption_key.encode()[:32].ljust(32, b'\0')))
        return fernet.decrypt(self._mnemonic.encode()).decode()

    def to_dict(self):
        """将地址信息转换为字典格式"""
        return {
            "index": self.index,
            "address": self.address,
            "private_key": self._private_key,
            "mnemonic": self._mnemonic
        }

class EVMAddressManager:
    def __init__(self, filename='addresses.json'):
        self.filename = get_config_path(filename)
        self.addresses = []
        self.encryption_key = None  # 存储加密密钥
        self.load_addresses()
        self.decrypt_addrs = []

    def ensure_encryption_key(self):
        """确保加密密钥已被设置"""
        if not self.encryption_key:
            self.encryption_key = getpass.getpass(prompt='Enter encryption key: ')

    def add_address(self, index, address, private_key, mnemonic):
        """添加地址，首次使用时要求输入加密密钥"""
        self.ensure_encryption_key()
        new_address = EVMAddress(index, address, private_key, mnemonic, self.encryption_key)
        self.addresses.append(new_address)
        self.save_addresses()
        print(f"Address {index} added successfully.")

    def get_address_info(self, index):
        """获取地址信息，包括解密的私钥和助记词"""
        if type(index) == int:
            index = str(index)
        if len(self.decrypt_addrs) == 0:
            self.get_all_addr_info()

        for addr in self.decrypt_addrs:
            if addr['index'] == index:
                return addr
            else:
                return None

    def get_all_addr_info(self):
        self.ensure_encryption_key()
        decrypt_addrs = []
        for addr in self.addresses:
            private_key = addr.get_private_key(self.encryption_key)
            mnemonic = addr.get_mnemonic(self.encryption_key)
            decrypt_addrs.append({"index": addr.index, "address": addr.address,
                                  "private_key": private_key, "mnemonic": mnemonic})
        self.decrypt_addrs = decrypt_addrs


    def save_addresses(self):
        """将地址列表保存到JSON文件"""
        with open(self.filename, 'w') as f:
            json.dump([addr.to_dict() for addr in self.addresses], f)

    def load_addresses(self):
        """从JSON文件加载地址列表"""
        try:
            with open(self.filename, 'r') as f:
                addresses_data = json.load(f)
                for addr_data in addresses_data:
                    self.addresses.append(EVMAddress(**addr_data))
        except FileNotFoundError:
            print("Addresses file not found. Starting with an empty list.")

    def parse_addresses(self, filename="import_addr_examples.json"):
        file = get_config_path(filename)
        with open(file, "r") as f:
            wallets = json.load(f)
            i = 0
            for w in wallets['wallets']:
                self.add_address(str(i), w['addr'], w['private'], w['words'])
                i += 1

# 使用示例
if __name__ == "__main__":
    manager = EVMAddressManager()
    #manager.add_address(1, "0x123...", "my_private_key", "my_mnemonic_phrase")
    # manager.get_address_info(1)
    print(manager.get_address_info(0))
    #manager.parse_addresses()


