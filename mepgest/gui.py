from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QTabWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGridLayout,
    QListWidget, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal, QObject
from mepgest.models import committees
from mepgest.models import delegates
from mepgest.speech import SpeechType

import json

committee_score_labels = {}


# Delegate Manager to handle score updates
class DelegateManager(QObject):
    score_updated = Signal()  # Signal to notify other parts of the app when score changes
    
    def __init__(self):
        super().__init__()

    def update_score(self):
        self.score_updated.emit()  # Emit the signal to notify other parts of the app


# Function to create General Tab
def create_general_tab(tab_widget):
    general_tab = QWidget()
    general_layout = QVBoxLayout(general_tab)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    inner_widget = QWidget()
    inner_layout = QVBoxLayout(inner_widget)

    all_delegates = []
    for committee in committees.values():
        all_delegates.extend(committee.delegates)
    all_delegates.sort(key=lambda d: d.score())

    for delegate in all_delegates:
        delegate_frame = QWidget()
        delegate_layout = QHBoxLayout(delegate_frame)

        name_label = QLabel(f"{delegate.code} {delegate.surname} {delegate.name}")
        name_label.setFont(QFont("Arial", 14))

        committee_label = QLabel(f"{delegate.committee_name}")
        committee_label.setFont(QFont("Arial", 12))

        score_label = QLabel(f"Score: {delegate.score():.2f}")
        score_label.setFont(QFont("Arial", 12))
        score_label.setStyleSheet("")

        delegate_layout.addWidget(name_label)
        delegate_layout.addSpacing(20)
        delegate_layout.addWidget(committee_label)
        delegate_layout.addSpacing(20)
        delegate_layout.addWidget(score_label)
        delegate_layout.addStretch()

        inner_layout.addWidget(delegate_frame)

    inner_widget.setLayout(inner_layout)
    scroll.setWidget(inner_widget)
    general_layout.addWidget(scroll)
    tab_widget.addTab(general_tab, "General List")


def create_committees_tab(tab_widget, delegate_manager):
    committees_tab = QWidget()
    committees_layout = QHBoxLayout(committees_tab)

    left_column = QVBoxLayout()
    right_column = QVBoxLayout()

    committee_list = list(committees.items())
    split_index = (len(committee_list) + 1) // 2

    for i, (name, committee) in enumerate(committee_list):
        # Committee Header
        header = QLabel(f"Committee: {name}")
        header.setFont(QFont("Arial", 18, QFont.Bold))

        # Scroll Area for delegate list
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(250)

        inner_widget = QWidget()
        committee_layout = QVBoxLayout(inner_widget)  # Vertical layout for delegates

        score_labels = []  # Store for score labels of delegates
        sorted_delegates = sorted(committee.delegates, key=lambda d: d.score(), reverse=False)
        
        for delegate in sorted_delegates:
            delegate_frame = QWidget()
            delegate_layout = QHBoxLayout(delegate_frame)

            name_label = QLabel(f"{delegate.code} {delegate.surname} {delegate.name}")
            name_label.setFont(QFont("Arial", 14))

            score_label = QLabel(f"Score: {delegate.score():.2f}")
            score_label.setFont(QFont("Arial", 12))

            delegate_layout.addWidget(name_label)
            delegate_layout.addSpacing(15)
            delegate_layout.addWidget(score_label)
            delegate_layout.addStretch()

            committee_layout.addWidget(delegate_frame)  # Add delegate frame to the list

        # Save the score labels for further usage
        committee_score_labels[name] = [score_label for score_label in sorted_delegates]

        scroll.setWidget(inner_widget)

        # Container for the entire committee section (header + delegates)
        committee_container = QWidget()
        committee_container_layout = QVBoxLayout(committee_container)
        committee_container_layout.addWidget(header)
        committee_container_layout.addWidget(scroll)

        # Apply border ONLY around the committee content (header + delegate list)
        committee_container.setStyleSheet("""
            border: 2px solid #5E81AC;  /* Highlighted border color */
            border-radius: 8px;         /* Rounded corners for the border */
            padding: 10px;              /* Space between border and content */
            margin-bottom: 20px;        /* Space between committees */
        """)

        # Add the committee container to the appropriate column
        if i < split_index:
            left_column.addWidget(committee_container)
        else:
            right_column.addWidget(committee_container)

    # Layout setup for the tab
    committees_layout.addLayout(left_column)
    committees_layout.addSpacing(30)
    committees_layout.addLayout(right_column)

    # Add the committees tab to the tab widget
    tab_widget.addTab(committees_tab, "Committees")



def update_committees(tab_widget, delegate_manager):
    # Trova l'indice del tab "Committees"
    for i in range(tab_widget.count()):
        if tab_widget.tabText(i) == "Committees":
            tab_widget.removeTab(i)
            break

    # Ricrea il tab con i dati aggiornati e ordinati
    create_committees_tab(tab_widget, delegate_manager)


# Function to create Speeches Tab
def create_speeches_tab(tab_widget, delegate_manager, window):
    speeches_tab = QWidget()
    speeches_layout = QVBoxLayout(speeches_tab)

    # Delegate code input
    search_label = QLabel("Enter Delegate Code:")
    search_label.setFont(QFont("Arial", 12))
    speeches_layout.addWidget(search_label)

    code_input = QLineEdit()
    code_input.setPlaceholderText("e.g., 101")
    speeches_layout.addWidget(code_input)

    # Live name display
    name_display_label = QLabel("")
    name_display_label.setFont(QFont("Arial", 10, italic=True))
    name_display_label.setStyleSheet("")
    speeches_layout.addWidget(name_display_label)

    # Speech type dropdown
    speech_type_dropdown = QComboBox()
    speech_type_dropdown.addItems([speech.value for speech in SpeechType])
    speech_type_dropdown.setEditable(False)
    speeches_layout.addWidget(speech_type_dropdown)

    # Add button
    add_button = QPushButton("➕ Add Speech")
    speeches_layout.addWidget(add_button)

    # History of added speeches
    history_label = QLabel("Speech History:")
    history_label.setFont(QFont("Arial", 12))
    speeches_layout.addWidget(history_label)

    speech_history = QListWidget()
    speeches_layout.addWidget(speech_history)

    # Display delegate score
    score_label = QLabel("Delegate Score: 0")
    score_label.setFont(QFont("Arial", 12))
    speeches_layout.addWidget(score_label)

    # Function to add speech
    def add_speech():
        code = code_input.text().strip().upper()
        speech_text = speech_type_dropdown.currentText()
        delegate = delegates.get(code)

        if delegate is None:
            QMessageBox.warning(window, "Delegate Not Found", f"No delegate found with code: {code}")
            return

        speech_type = SpeechType(speech_text)
        delegate.speak(speech_type)

        # Add the speech to history
        speech_history.addItem(f"{delegate.name} {delegate.surname}: {speech_type.value}")

        # Update delegate score
        delegate_score = delegate.score()
        score_label.setText(f"Delegate Score: {delegate_score}")

        # Emit the signal to notify about the score update
        delegate_manager.update_score()

        QMessageBox.information(window, "Speech Added", f"{speech_type.value} added to {delegate.code} {delegate.name} {delegate.surname}.")

    # Live update of delegate name
    def update_delegate_name():
        code = code_input.text().strip().upper()
        delegate = delegates.get(code)
        if delegate:
            name_display_label.setText(f"{delegate.code} {delegate.name} {delegate.surname}")
            # Update delegate score when delegate is found
            delegate_score = delegate.score()
            score_label.setText(f"Delegate Score: {delegate_score}")
        else:
            name_display_label.setText("")
            score_label.setText("Delegate Score: 0")

    code_input.textChanged.connect(update_delegate_name)
    add_button.clicked.connect(add_speech)

    speeches_layout.addStretch()
    tab_widget.addTab(speeches_tab, "Speeches")

    # Connect delegate manager to speeches score update
    delegate_manager.score_updated.connect(lambda: update_speeches(tab_widget))


# Function to update general list scores
def update_general_list(tab_widget):
    # Clear and recreate the general tab to update scores
    tab_widget.clear()
    create_general_tab(tab_widget)



# Function to update speeches scores
def update_speeches(tab_widget):
    # Recreate the speeches tab content
    pass

def load_stylesheet_from_json(filename):
    with open(filename, 'r') as file:
        styles = json.load(file)

    # Convert JSON style rules to a valid stylesheet format string
    stylesheet = ""
    for widget, properties in styles.items():
        widget_style = f"{widget} {{\n"
        for prop, value in properties.items():
            widget_style += f"    {prop}: {value};\n"
        widget_style += "}\n"
        stylesheet += widget_style
    return stylesheet


def launch_gui():
    app = QApplication([])

    # Global Stylesheet for Consistency
    stylesheet = load_stylesheet_from_json("themes/app_theme.json")
    app.setStyleSheet(stylesheet) 


    window = QMainWindow()
    window.setWindowTitle("🎓 MEPGest — Delegate Dashboard")
    window.resize(1000, 700)

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    # Title Section
    title = QLabel("Welcome to MEPGest!")
    title.setFont(QFont("Arial", 28, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("color: #E5E9F0;")  # Light Icy White for Title Text
    layout.addWidget(title)

    # Tabs Section
    tab_widget = QTabWidget()
    layout.addWidget(tab_widget)

    # Initialize Delegate Manager
    delegate_manager = DelegateManager()

    # Create Tabs
    create_general_tab(tab_widget)
    create_committees_tab(tab_widget, delegate_manager)
    create_speeches_tab(tab_widget, delegate_manager, window)

    # Set the central widget and show the window
    window.setCentralWidget(central_widget)
    window.show()

    app.exec()

