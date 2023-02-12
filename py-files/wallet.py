

import os
import settings
import subprocess
import traceback

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QPushButton, QLabel, QLineEdit, 
                             QWidget, QGridLayout, QMessageBox,
                             QRadioButton)

class Wallet(QWidget):
    def __init__(self):
        super().__init__()

        # Creating local variables
        self.vkey_name = ""
        self.address = ""
        self.pkh = ""

        # Starting text and Cardano picture
        self.label_0_0 = QLabel("Manage wallet address and its keys.")
        picture_0_2 = QLabel("")
        picture_0_2.setPixmap(QPixmap("./images/cardano.png"))
        picture_0_2.setFixedSize(80,80)
        picture_0_2.setScaledContents(True)

        # Widgets for verification key section 
        self.label_1_0 = QLabel("Input verification key name:")
        self.input_2_0 = QLineEdit()
        self.button_2_1 = QPushButton("Set")

        # Widgets for signing key section 
        self.label_3_0 = QLabel("Signing key name:")
        self.input_4_0 = QLineEdit()
        self.button_5_0 = QPushButton("Generate both keys")

        # Widget actions for signing and verifaction key section
        self.button_2_1.clicked.connect(self.set_verification_key)
        self.button_5_0.clicked.connect(self.generate_skey_and_vkey)

        # Widgets for payment address section 
        self.label_7_0 = QLabel("Input payment address name:")
        self.input_8_0 = QLineEdit()
        self.button_8_1 = QPushButton("Set")
        self.button_8_2 = QPushButton("Generate")
        self.label_9_0 = QLabel("Payment address:")
        self.radioButton_9_1 = QRadioButton("Mainnet")
        self.radioButton_9_2 = QRadioButton("Testnet")
        self.input_10_0 = QLineEdit()
        self.button_10_1 = QPushButton("Show")

        # Widget actions for payment address section  
        self.button_8_1.clicked.connect(self.set_address) 
        self.button_8_2.clicked.connect(self.generate_address) 
        self.button_10_1.clicked.connect(self.show_address) 

        # Widgets for payment address key hash section 
        self.label_12_0 = QLabel("Payment public key hash name:")
        self.input_13_0 = QLineEdit()
        self.button_13_1 = QPushButton("Set")
        self.button_13_2 = QPushButton("Generate")
        self.label_14_0 = QLabel("Key hash:")
        self.input_15_0 = QLineEdit()
        self.button_15_1 = QPushButton("Show")

        # Widget actions for payment public key hash section 
        self.button_13_1.clicked.connect(self.set_pkh) 
        self.button_13_2.clicked.connect(self.generate_pkh) 
        self.button_15_1.clicked.connect(self.show_pkh) 

        # Set label fonts 
        labels = [self.label_0_0, 
                  self.label_1_0, self.label_3_0, 
                  self.label_7_0, self.label_9_0,
                  self.label_12_0, self.label_14_0]
        for label in labels:
            font = label.font()
            font.setPointSize(12)
            label.setFont(font)

        # Set lineEdit sizes 
        inputs = [self.input_2_0, self.input_4_0, 
                  self.input_8_0, self.input_10_0,
                  self.input_13_0, self.input_15_0]
        for input in inputs:
            input.setFixedSize(500,30)

        # Set button sizes 
        buttons = [self.button_2_1,  
                   self.button_8_1, self.button_8_2, 
                   self.button_10_1, self.button_13_1, 
                   self.button_13_2, self.button_15_1] 
        for button in buttons:
            button.setFixedSize(80,30)  

        self.button_5_0.setFixedSize(160,30)  

        # Space between the sections
        self.emptyLabel = QLabel()

        # Layouts 
        layout = QGridLayout()
        layout.addWidget(self.label_0_0, 0, 0) 
        layout.addWidget(picture_0_2, 0, 2) 
        # Adding widgets for verification key section 
        layout.addWidget(self.label_1_0, 1, 0) 
        layout.addWidget(self.input_2_0, 2, 0) 
        layout.addWidget(self.button_2_1, 2, 1) 
        layout.addWidget(self.emptyLabel, 3, 0)
        # Adding widgets for signing key section 
        layout.addWidget(self.label_3_0, 3, 0)
        layout.addWidget(self.input_4_0, 4, 0)
        layout.addWidget(self.button_5_0, 5, 0)
        layout.addWidget(self.emptyLabel, 6, 0)
        # Adding widgets for payment address section 
        layout.addWidget(self.label_7_0, 7, 0)
        layout.addWidget(self.input_8_0, 8, 0)
        layout.addWidget(self.button_8_1, 8, 1)
        layout.addWidget(self.button_8_2, 8, 2)
        layout.addWidget(self.label_9_0, 9, 0)
        layout.addWidget(self.radioButton_9_1, 9, 1)
        layout.addWidget(self.radioButton_9_2, 9, 2)
        layout.addWidget(self.input_10_0, 10, 0)
        layout.addWidget(self.button_10_1, 10, 1) 
        layout.addWidget(self.emptyLabel, 11, 0)
        # Adding widgets for payment public key hash section 
        layout.addWidget(self.label_12_0, 12, 0)
        layout.addWidget(self.input_13_0, 13, 0)
        layout.addWidget(self.button_13_1, 13, 1)
        layout.addWidget(self.button_13_2, 13, 2)
        layout.addWidget(self.label_14_0, 14, 0)
        layout.addWidget(self.input_15_0, 15, 0)
        layout.addWidget(self.button_15_1, 15, 1)
        layout.addWidget(self.emptyLabel, 16, 0)

        self.setLayout(layout)

    def set_verification_key(self):
        vkey_name = self.input_2_0.text()
        vkey_path = settings.folder_path + "/" + vkey_name
        vkey_exists = os.path.isfile(vkey_path)
        
        skey_name = vkey_name.split(".")[0] + ".skey"
        skey_path = settings.folder_path + "/" + skey_name
        skey_exists = os.path.isfile(skey_path) 

        if vkey_exists:
            self.vkey_name = vkey_name
            if skey_exists:
                self.input_4_0.setText(skey_name)
        else:
            msg = "Verification key does not exists.\n" + \
                  "Please specify a valid file name."                        
            QMessageBox.warning(self, "Notification:", msg,
                                QMessageBox.Close)

    def generate_skey_and_vkey(self):
        file_number_counter = 1
        while(True):
            if len(str(file_number_counter)) == 1:
                self.vkey_name = "0" + str(file_number_counter) + ".vkey"
                skey_name = "0" + str(file_number_counter) + ".skey"
            else:
                self.vkey_name = str(file_number_counter) + ".vkey"
                skey_name = str(file_number_counter) + ".skey"
            
            vkey_file_path = settings.folder_path + "/" + self.vkey_name
            vkey_file_exists = os.path.isfile(vkey_file_path)

            skey_file_path = settings.folder_path + "/" + skey_name
            skey_file_exists = os.path.isfile(skey_file_path)

            if (not vkey_file_exists) and (not skey_file_exists):
                command = "cardano-cli address key-gen " + \
                          "--verification-key-file " + self.vkey_name + " " + \
                          "--signing-key-file " + skey_name 

                if settings.debug_mode:
                    print(command)
                else:
                    try:
                        subprocess.Popen(command.split(), cwd=settings.folder_path)
                        self.input_2_0.setText(self.vkey_name)
                        self.input_4_0.setText(skey_name)
                    except Exception:
                        output = traceback.format_exc()
                        log_error_msg(output)
                        
                        msg = "Verification and signing key could not be generated.\n" + \
                              "Check if cardano node is running and is synced.\n" + \
                              "Look at the error.log file for error output." 
                        QMessageBox.warning(self, "Notification:", msg,
                                            QMessageBox.Close)
                break
            
            file_number_counter += 1

    def set_address(self): 
        address_name = self.input_8_0.text()
        address_path = settings.folder_path + "/" + address_name
        address_exists = os.path.isfile(address_path)
        
        if address_exists:
            with open(address_path, "r") as file:
                self.address = file.read()
        else:
            msg = "Address does not exists.\n" + \
                  "Please specify a valid file name."                       
            QMessageBox.warning(self, "Notification:", msg,
                                QMessageBox.Close)

    def generate_address(self):
        is_mainnet = self.radioButton_9_1.isChecked()
        is_testnet = self.radioButton_9_2.isChecked()

        if (not is_mainnet) and (not is_testnet):
            msg = "Select option mainnet or testnet."    
            QMessageBox.warning(self, "Notification:", msg,
                                QMessageBox.Close)
        else:
            if self.vkey_name == "":
                msg = "Please set or generate first a verification key."     
                QMessageBox.warning(self, "Notification:", msg,
                                    QMessageBox.Close)
            else:
                file_number_counter = 1
                while(True):
                    if len(str(file_number_counter)) == 1:
                        address_name = "0" + str(file_number_counter) + ".addr"
                    else:
                        address_name = str(file_number_counter) + ".addr"
                    
                    address_file_path = settings.folder_path + "/" + address_name
                    address_file_exists = os.path.isfile(address_file_path)

                    if not address_file_exists:
                        def handle_command(command):
                            if settings.debug_mode:
                                print(command)
                            else:
                                try:
                                    subprocess.Popen(command.split(), cwd=settings.folder_path)
                                    self.input_8_0.seText(address_name) 
                                    with open(address_file_path, "r") as file:
                                        self.address = file.read() 
                                except Exception:
                                    output = traceback.format_exc()
                                    log_error_msg(output)
                                    
                                    msg = "Address could not be generated.\n" + \
                                          "Check if cardano node is running and is synced.\n" + \
                                          "Look at the error.log file for error output."                    
                                    QMessageBox.warning(self, "Notification:", msg,
                                                        QMessageBox.Close)

                        if is_testnet:
                            net_part = "--testnet-magic 1097911063 "
                        elif is_mainnet:
                            net_part = "--mainnet "

                        command = "cardano-cli address build " + \
                                  "--payment-verification-key-file " + self.vkey_name + " " + \
                                  net_part + \
                                  "--out-file " + address_name
                        handle_command(command)
                        break

                    file_number_counter += 1 

    def show_address(self): 
        self.input_10_0.setText(self.address)

    def set_pkh(self): 
        pkh_name = self.input_13_0.text()
        pkh_path = settings.folder_path + "/" + pkh_name
        pkh_exists = os.path.isfile(pkh_path)
        
        if pkh_exists:
            with open(pkh_path, "r") as file:
                self.pkh = file.read()
        else:
            msg = "Public key hash does not exists.\n" + \
                  "Please specify a valid file name."                        
            QMessageBox.warning(self, "Notification:", msg,
                                QMessageBox.Close)

    def generate_pkh(self):
        if self.vkey_name == "":
            msg = "Please set or generate first a verification key."     
            QMessageBox.warning(self, "Notification:", msg,
                                QMessageBox.Close)
        else:
            file_number_counter = 1
            while(True):
                if len(str(file_number_counter)) == 1:
                    pkh_name = "0" + str(file_number_counter) + ".pkh"
                else:
                    pkh_name = str(file_number_counter) + ".pkh"
                
                pkh_file_path = settings.folder_path + "/" + pkh_name
                pkh_file_exists = os.path.isfile(pkh_file_path)

                if not pkh_file_exists:
                    command = "cardano-cli address key-hash " + \
                              "--payment-verification-key-file " + self.vkey_name + " " + \
                              "--out-file " + pkh_name
                    if settings.debug_mode:
                        print(command)
                    else:
                        try:
                            subprocess.Popen(command.split(), cwd=settings.folder_path)
                            self.input_13_0.setText(pkh_name)
                            with open(pkh_file_path, "r") as file:
                                self.pkh = file.read()
                        except Exception:
                            output = traceback.format_exc()
                            log_error_msg(output)
                            
                            msg = "Public key hash could not be generated.\n" + \
                                  "Check if cardano node is running and is synced.\n" + \
                                  "Look at the error.log file for error output."                     
                            QMessageBox.warning(self, "Notification:", msg,
                                                QMessageBox.Close)
                    break

                file_number_counter += 1

    def show_pkh(self): 
        self.input_15_0.setText(self.pkh)

def log_error_msg(output):
    with open("./error.log", "w") as file:
        file.write(output)

