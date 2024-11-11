import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt

# Custom QLabel class with click signal
class ClickableLabel(QLabel):
    clicked = pyqtSignal()  # Signal to emit when label is clicked

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()  # Emit signal when label is clicked

class ImageWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Responsive Image Viewer")

        # Load the image using QPixmap
        self.pixmap = QPixmap("/home/biswarup/Desktop/TEST/jarvis/jarvis/JARVIC_MICROPHONE.png")

        # Set initial window size to half the size of the image
        window_width = self.pixmap.width() // 2
        window_height = self.pixmap.height() // 2
        self.setGeometry(100, 100, window_width, window_height)

        # Create a clickable label to display the image
        self.label = ClickableLabel(self)
        self.label.setPixmap(self.pixmap)

        # Connect the label's clicked signal to a slot
        self.label.clicked.connect(self.on_image_click)

    # Slot to handle image click
    def on_image_click(self):
        print("Image clicked!")

    # Override the resize event to make the image responsive and centered
    def resizeEvent(self, event):
        # Scale the pixmap to fit the label size, maintaining aspect ratio
        scaled_pixmap = self.pixmap.scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Set the scaled pixmap to the label
        self.label.setPixmap(scaled_pixmap)
        
        # Calculate the position to center the label
        label_x = (self.width() - scaled_pixmap.width()) // 2
        label_y = (self.height() - scaled_pixmap.height()) // 2

        # Move the label to the centered position
        self.label.setGeometry(label_x, label_y, scaled_pixmap.width(), scaled_pixmap.height())

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageWindow()
    window.show()
    sys.exit(app.exec_())
