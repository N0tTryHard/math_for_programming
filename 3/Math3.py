import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFrame


def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            if 'А' <= char <= 'Я':
                shift_base = ord('А')
                result += chr((ord(char) - shift_base + shift) % 32 + shift_base)
            elif 'а' <= char <= 'я':
                shift_base = ord('а')
                result += chr((ord(char) - shift_base + shift) % 32 + shift_base)
            else:
                result += char
        else:
            result += char
    return result


class CaesarCipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Шифр Цезаря')

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
        self.input_text_encrypt = QLineEdit(encrypt_frame)
        encrypt_layout.addWidget(self.input_text_encrypt)

        # Поле для ввода сдвига для зашифровки
        shift_label_encrypt = QLabel("Сдвиг", encrypt_frame)
        encrypt_layout.addWidget(shift_label_encrypt)
        self.shift_encrypt = QLineEdit(encrypt_frame)
        encrypt_layout.addWidget(self.shift_encrypt)

        # Зашифрованное сообщение
        encrypted_label = QLabel("Зашифрованное сообщение", encrypt_frame)
        encrypt_layout.addWidget(encrypted_label)
        self.encrypted_text = QLineEdit(encrypt_frame)
        encrypt_layout.addWidget(self.encrypted_text)

        # Кнопка зашифровать
        encrypt_button = QPushButton("Зашифровать", encrypt_frame)
        encrypt_button.clicked.connect(self.encrypt)
        encrypt_layout.addWidget(encrypt_button)

        # Ввод сообщения для расшифровки
        input_label_decrypt = QLabel("Ввод сообщения для расшифровки", decrypt_frame)
        decrypt_layout.addWidget(input_label_decrypt)
        self.input_text_decrypt = QLineEdit(decrypt_frame)
        decrypt_layout.addWidget(self.input_text_decrypt)

        # Поле для ввода сдвига для расшифровки
        shift_label_decrypt = QLabel("Сдвиг", decrypt_frame)
        decrypt_layout.addWidget(shift_label_decrypt)
        self.shift_decrypt = QLineEdit(decrypt_frame)
        decrypt_layout.addWidget(self.shift_decrypt)

        # Расшифрованное сообщение
        decrypted_label = QLabel("Расшифрованное сообщение", decrypt_frame)
        decrypt_layout.addWidget(decrypted_label)
        self.decrypted_text = QLineEdit(decrypt_frame)
        decrypt_layout.addWidget(self.decrypted_text)

        # Кнопка расшифровать
        decrypt_button = QPushButton("Расшифровать", decrypt_frame)
        decrypt_button.clicked.connect(self.decrypt)
        decrypt_layout.addWidget(decrypt_button)

    def encrypt(self):
        text = self.input_text_encrypt.text()
        shift = int(self.shift_encrypt.text())
        encrypted_text = caesar_cipher(text, shift)
        self.encrypted_text.setText(encrypted_text)

    def decrypt(self):
        text = self.input_text_decrypt.text()
        shift = int(self.shift_decrypt.text())
        decrypted_text = caesar_cipher(text, -shift)
        self.decrypted_text.setText(decrypted_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CaesarCipherApp()
    ex.show()
    sys.exit(app.exec_())
