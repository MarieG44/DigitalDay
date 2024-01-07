# PROTOTYPE 1

import sys
import threading
import time
import pygetwindow as gw
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import matplotlib.pyplot as plt

app_data = {}
current_window = None
start_time = None
tracking = False
tracking_thread = None

def track_app_time():
    global current_window, start_time, tracking, app_data
    while tracking:
        new_window = gw.getActiveWindow()
        if new_window != current_window:
            if current_window is not None:
                end_time = time.time()
                elapsed_time = end_time - start_time
                app_name = current_window.title

                if app_name in app_data:
                    app_data[app_name] += elapsed_time / 60  # Convert to minutes
                else:
                    app_data[app_name] = elapsed_time / 60

            current_window = new_window
            start_time = time.time()

        time.sleep(1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Usage Tracker")
        self.setGeometry(100, 100, 280, 80)

        layout = QVBoxLayout()
        self.start_button = QPushButton("Start Tracking", self)
        self.start_button.clicked.connect(self.start_tracking)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton("Stop Tracking and Show Histogram", self)
        self.stop_button.clicked.connect(self.stop_tracking)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_tracking(self):
        global tracking, tracking_thread
        tracking = True
        tracking_thread = threading.Thread(target=track_app_time)
        tracking_thread.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_tracking(self):
        global tracking
        tracking = False
        if tracking_thread is not None:
            tracking_thread.join()
        self.display_histogram()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def display_histogram(self):
        global app_data  # Declare app_data as global
        if app_data:
        # Generate the bar plot
            plt.bar(app_data.keys(), app_data.values())

        # Labeling
            plt.xlabel('Applications')
            plt.ylabel('Time in minutes')
            plt.title('Application Usage Time')

        # Rotate the x-axis labels vertically and align to center
            plt.xticks(rotation=90, ha='center')

        # Layout adjustment to prevent clipping of labels
            plt.tight_layout()

        # Display the plot
            plt.show()
        app_data = {}  # Reset app_data for the next tracking session


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())







#CONCERNS:
#implement data storage within GUI
#app seems to start a new tracking cycle when user presses stop --> have to reload program for each new cycle
#
#




