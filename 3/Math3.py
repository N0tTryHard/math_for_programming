import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QTextEdit
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

# Генерация ключей RSA
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()


def rsa_encrypt(text, public_key):
    encrypted_text = public_key.encrypt(
        text.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_text.hex()


def rsa_decrypt(encrypted_text, private_key):
    encrypted_text_bytes = bytes.fromhex(encrypted_text)
    decrypted_text = private_key.decrypt(
        encrypted_text_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_text.decode('utf-8')


class RSAEncryptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.decrypted_text = None
        self.input_text_decrypt = None
        self.encrypted_text = None
        self.input_text_encrypt = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('RSA Шифрование')

        main_layout = QHBoxLayout()

        encrypt_frame = QFrame(self)
        encrypt_layout = QVBoxLayout(encrypt_frame)

        decrypt_frame = QFrame(self)
        decrypt_layout = QVBoxLayout(decrypt_frame)

        main_layout.addWidget(encrypt_frame)
        main_layout.addWidget(decrypt_frame)

        self.setLayout(main_layout)

        # Ввод сообщения для зашифровки
        input_label_encrypt = QLabel("Ввод сообщения для зашифровки", encrypt_frame)
        encrypt_layout.addWidget(input_label_encrypt)
        self.input_text_encrypt = QTextEdit(encrypt_frame)
        encrypt_layout.addWidget(self.input_text_encrypt)

        # Зашифрованное сообщение
        encrypted_label = QLabel("Зашифрованное сообщение", encrypt_frame)
        encrypt_layout.addWidget(encrypted_label)
        self.encrypted_text = QTextEdit(encrypt_frame)
        self.encrypted_text.setReadOnly(True)
        encrypt_layout.addWidget(self.encrypted_text)

        # Кнопка зашифровать
        encrypt_button = QPushButton("Зашифровать", encrypt_frame)
        encrypt_button.clicked.connect(self.encrypt)
        encrypt_layout.addWidget(encrypt_button)

        # Ввод сообщения для расшифровки
        input_label_decrypt = QLabel("Ввод сообщения для расшифровки", decrypt_frame)
        decrypt_layout.addWidget(input_label_decrypt)
        self.input_text_decrypt = QTextEdit(decrypt_frame)
        decrypt_layout.addWidget(self.input_text_decrypt)

        # Расшифрованное сообщение
        decrypted_label = QLabel("Расшифрованное сообщение", decrypt_frame)
        decrypt_layout.addWidget(decrypted_label)
        self.decrypted_text = QTextEdit(decrypt_frame)
        self.decrypted_text.setReadOnly(True)
        decrypt_layout.addWidget(self.decrypted_text)

        # Кнопка расшифровать
        decrypt_button = QPushButton("Расшифровать", decrypt_frame)
        decrypt_button.clicked.connect(self.decrypt)
        decrypt_layout.addWidget(decrypt_button)

    def encrypt(self):
        text = self.input_text_encrypt.toPlainText()
        encrypted_text = rsa_encrypt(text, public_key)
        self.encrypted_text.setPlainText(encrypted_text)

    def decrypt(self):
        encrypted_text = self.input_text_decrypt.toPlainText()
        decrypted_text = rsa_decrypt(encrypted_text, private_key)
        self.decrypted_text.setPlainText(decrypted_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RSAEncryptionApp()
    ex.show()
    sys.exit(app.exec_())
