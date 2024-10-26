import sys
import json
import os
import shutil
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLineEdit, QLabel, QFileDialog, 
                             QTextEdit, QScrollArea, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

class JSONUpdater(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('JSON Updater')
        self.setGeometry(100, 100, 800, 900)

        layout = QVBoxLayout()

        # Image uploader
        self.image_label = QLabel('Drag and drop image here')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet('border: 2px dashed #aaa')
        self.image_label.setMinimumHeight(100)
        layout.addWidget(self.image_label)

        # Food JSON updater
        layout.addWidget(QLabel('Food JSON Updater'))
        self.food_name_jp = QLineEdit(placeholderText='Food Name (JP)')
        self.food_name_en = QLineEdit(placeholderText='Food Name (EN)')
        self.food_price = QLineEdit(placeholderText='Price')
        self.food_currency = QLineEdit(placeholderText='Currency')
        layout.addWidget(self.food_name_jp)
        layout.addWidget(self.food_name_en)
        layout.addWidget(self.food_price)
        layout.addWidget(self.food_currency)
        self.add_food_btn = QPushButton('Add Food')
        self.add_food_btn.clicked.connect(self.add_food)
        layout.addWidget(self.add_food_btn)

        # Shop JSON updater
        layout.addWidget(QLabel('Shop JSON Updater'))
        self.shop_rank = QLineEdit(placeholderText='Rank')
        self.shop_name = QLineEdit(placeholderText='Store Name')
        self.shop_place = QLineEdit(placeholderText='Place')
        self.shop_country_jp = QLineEdit(placeholderText='Country (JP)')
        self.shop_country_en = QLineEdit(placeholderText='Country (EN)')
        self.shop_description_jp = QTextEdit(placeholderText='Description (JP)')
        self.shop_description_en = QTextEdit(placeholderText='Description (EN)')
        self.shop_map_jp = QLineEdit(placeholderText='Map URL (JP)')
        self.shop_map_en = QLineEdit(placeholderText='Map URL (EN)')
        
        # Food selection for shop
        self.food_selector = QComboBox()
        self.update_food_selector()
        self.selected_foods = []
        
        layout.addWidget(self.shop_rank)
        layout.addWidget(self.shop_name)
        layout.addWidget(self.shop_place)
        layout.addWidget(self.shop_country_jp)
        layout.addWidget(self.shop_country_en)
        layout.addWidget(self.shop_description_jp)
        layout.addWidget(self.shop_description_en)
        layout.addWidget(self.shop_map_jp)
        layout.addWidget(self.shop_map_en)
        layout.addWidget(QLabel('Select Foods:'))
        layout.addWidget(self.food_selector)
        
        add_food_to_shop_btn = QPushButton('Add Selected Food to Shop')
        add_food_to_shop_btn.clicked.connect(self.add_food_to_shop)
        layout.addWidget(add_food_to_shop_btn)
        
        self.selected_foods_label = QLabel('Selected Foods: ')
        layout.addWidget(self.selected_foods_label)
        
        self.update_shop_btn = QPushButton('Update Shop')
        self.update_shop_btn.clicked.connect(self.update_shop)
        layout.addWidget(self.update_shop_btn)

        scroll = QScrollArea()
        scroll.setWidget(QWidget())
        scroll.widget().setLayout(layout)
        scroll.setWidgetResizable(True)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                self.handle_image(f)

    def handle_image(self, file_path):
        next_id = self.get_next_id()
        new_filename = f'bc{next_id}.jpg'
        destination = os.path.join('src', 'images', 'public', 'beancurd_images', new_filename)
        shutil.copy(file_path, destination)
        self.image_label.setText(f'Image uploaded: {new_filename}')

    def get_next_id(self):
        with open('src/jsons/shop.json', 'r') as f:
            shops = json.load(f)
        max_id = max(int(shop['ID']) for shop in shops)
        return str(max_id + 1).zfill(2)

    def update_food_selector(self):
        with open('src/jsons/food.json', 'r') as f:
            foods = json.load(f)
        self.food_selector.clear()
        for food in foods:
            self.food_selector.addItem(f"{food['food_name_jp']} ({food['ID']})")

    def add_food_to_shop(self):
        selected_food = self.food_selector.currentText()
        food_id = selected_food.split('(')[-1].strip(')')
        if food_id not in self.selected_foods:
            self.selected_foods.append(food_id)
            self.selected_foods_label.setText(f"Selected Foods: {', '.join(self.selected_foods)}")

    def add_food(self):
        with open('src/jsons/food.json', 'r+') as f:
            foods = json.load(f)
            new_food = {
                'ID': str(len(foods) + 1).zfill(2),
                'food_name_jp': self.food_name_jp.text(),
                'food_name_en': self.food_name_en.text(),
                'price': self.food_price.text(),
                'currency': self.food_currency.text()
            }
            foods.append(new_food)
            f.seek(0)
            json.dump(foods, f, indent=4)
            f.truncate()
        self.food_name_jp.clear()
        self.food_name_en.clear()
        self.food_price.clear()
        self.food_currency.clear()
        self.update_food_selector()
        QMessageBox.information(self, "Success", "Food added successfully!")

    def update_shop(self):
        with open('src/jsons/shop.json', 'r+') as f:
            shops = json.load(f)
            new_rank = int(self.shop_rank.text())
            new_shop = {
                'ID': self.get_next_id(),
                'rank': new_rank,
                'store_name': self.shop_name.text(),
                'place': self.shop_place.text(),
                'picture': [f"/MyPage/public/images/beancurd_images/bc{self.get_next_id()}.jpg"],
                'foods_id': self.selected_foods,
                'country_jp': self.shop_country_jp.text(),
                'country_en': self.shop_country_en.text(),
                'descriptions_jp': [{'line': line} for line in self.shop_description_jp.toPlainText().split('\n') if line],
                'descriptions_en': [{'line': line} for line in self.shop_description_en.toPlainText().split('\n') if line],
                'map_jp': self.shop_map_jp.text(),
                'map_en': self.shop_map_en.text()
            }

            # Update ranks
            for shop in shops:
                if new_rank != -1 and shop['rank'] >= new_rank:
                    shop['rank'] += 1
            
            # Insert new shop
            shops.append(new_shop)
            shops.sort(key=lambda x: x['rank'])

            f.seek(0)
            json.dump(shops, f, indent=4)
            f.truncate()

        self.shop_rank.clear()
        self.shop_name.clear()
        self.shop_place.clear()
        self.shop_country_jp.clear()
        self.shop_country_en.clear()
        self.shop_description_jp.clear()
        self.shop_description_en.clear()
        self.shop_map_jp.clear()
        self.shop_map_en.clear()
        self.selected_foods = []
        self.selected_foods_label.setText("Selected Foods: ")
        QMessageBox.information(self, "Success", "Shop updated successfully!")

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure you want to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONUpdater()
    ex.show()
    sys.exit(app.exec_())