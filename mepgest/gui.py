from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QTabWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGridLayout,
    QListWidget, QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtWidgets import QMenu, QToolBar, QFileDialog
from PySide6.QtGui import QAction

from mepgest.models import committees, schools, delegates
from mepgest.loaders import load_delegates
from mepgest.speech import SpeechType

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import json
import qdarktheme

committee_score_labels = {}


# Delegate Manager to handle score updates
class DelegateManager(QObject):
    score_updated = Signal()  # Signal to notify other parts of the app when score changes
    delegates_updated = Signal()  # Signal to notify when the delegates list is updated

    def __init__(self):
        super().__init__()
        self.delegates = []  # List to hold the loaded Delegate instances

    def set_delegates(self, delegates):
        """Sets the delegates in the manager and emits the update signal."""
        self.delegates = delegates
        self.delegates_updated.emit()  # Notify other parts of the app that delegates are updated

    def get_delegates(self):
        """Returns the list of Delegate instances."""
        return self.delegates

    def update_score(self):
        """This method emits the signal to notify other parts of the app when the score is updated."""
        self.score_updated.emit()



class GeneralTab(QWidget):
    def __init__(self, tab_widget, delegate_manager):
        super().__init__()
        self.tab_widget = tab_widget
        self.delegate_manager = delegate_manager
        self.general_layout = QVBoxLayout(self)
        self.delegate_widgets = []
        self.init_ui()
        self.connect_delegate_manager()

    def init_ui(self):
        # === HEADER (OUTSIDE SCROLL AREA) ===
        header_frame = QWidget()
        header_layout = QHBoxLayout(header_frame)

        code_header = QLabel("Code")
        code_header.setFont(QFont("Arial", 12, QFont.Bold))
        code_header.setFixedWidth(80)

        name_header = QLabel("Name")
        name_header.setFont(QFont("Arial", 12, QFont.Bold))
        name_header.setFixedWidth(180)

        speech_header = QLabel("Speeches")
        speech_header.setFont(QFont("Arial", 12, QFont.Bold))
        speech_header.setFixedWidth(100)

        score_header = QLabel("Score")
        score_header.setFont(QFont("Arial", 12, QFont.Bold))
        score_header.setFixedWidth(100)

        header_layout.addWidget(code_header)
        header_layout.addWidget(name_header)
        header_layout.addWidget(speech_header)
        header_layout.addWidget(score_header)
        header_layout.addStretch()

        self.general_layout.addWidget(header_frame)

        # === SCROLL AREA FOR DELEGATES ===
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        inner_widget = QWidget()
        inner_layout = QVBoxLayout(inner_widget)

        # Get all delegates sorted by score
        all_delegates = []
        for committee in committees.values():
            all_delegates.extend(committee.delegates)
        all_delegates.sort(key=lambda d: d.score(), reverse=False)

        self.delegate_widgets.clear()
        for delegate in all_delegates:
            delegate_frame = QWidget()
            delegate_layout = QHBoxLayout(delegate_frame)

            code_label = QLabel(f"{delegate.code}")
            code_label.setFont(QFont("Arial", 12))
            code_label.setFixedWidth(80)

            name_label = QLabel(f"{delegate.surname} {delegate.name}")
            name_label.setFont(QFont("Arial", 12))
            name_label.setFixedWidth(180)

            speech_count = QLabel(f"{delegate.speech_count()}")
            speech_count.setFont(QFont("Arial", 12))
            speech_count.setFixedWidth(100)

            score_label = QLabel(f"{delegate.score():.2f}")
            score_label.setFont(QFont("Arial", 12))
            score_label.setFixedWidth(100)

            delegate_layout.addWidget(code_label)
            delegate_layout.addWidget(name_label)
            delegate_layout.addWidget(speech_count)
            delegate_layout.addWidget(score_label)
            delegate_layout.addStretch()

            inner_layout.addWidget(delegate_frame)

        inner_widget.setLayout(inner_layout)
        self.scroll.setWidget(inner_widget)
        self.general_layout.addWidget(self.scroll)

    def refresh_tab(self):
        """Refresh the delegates' list in the general tab."""
        # Clear the general layout
        while self.general_layout.count():
            item = self.general_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        self.init_ui()  # Reinitialize the UI to refresh the delegate list


    def connect_delegate_manager(self):
        """Connect the delegate manager signals to refresh the tab."""
        self.delegate_manager.score_updated.connect(self.refresh_tab)
        self.delegate_manager.delegates_updated.connect(self.refresh_tab)


class CommitteesTab(QWidget):
    def __init__(self, tab_widget, delegate_manager):
        super().__init__()
        self.tab_widget = tab_widget
        self.delegate_manager = delegate_manager
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.main_widget = QWidget()
        self.scroll_area.setWidget(self.main_widget)

        self.main_layout = QHBoxLayout(self.main_widget)
        self.left_column = QVBoxLayout()
        self.right_column = QVBoxLayout()

        # Add static layout structure only once
        self.main_layout.addLayout(self.left_column)
        self.main_layout.addSpacing(30)
        self.main_layout.addLayout(self.right_column)

        self.init_ui()
        self.connect_delegate_manager()

    def widget(self):
        return self.scroll_area

    def init_ui(self):
        self.committee_list = list(committees.items())  # <--- refresh every time!
        self.split_index = (len(self.committee_list) + 1) // 2
        self.clear_columns()

        for i, (name, committee) in enumerate(self.committee_list):
            header_label = QLabel(f"Committee: {name}")
            header_label.setFont(QFont("Arial", 18, QFont.Bold))

            title_container = QWidget()
            title_layout = QVBoxLayout(title_container)
            title_layout.setContentsMargins(0, 0, 0, 0)
            title_layout.addWidget(header_label)
            title_container.setStyleSheet("""
                border: 2px solid #5E81AC;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            """)

            scroll_inner = QScrollArea()
            scroll_inner.setWidgetResizable(True)
            scroll_inner.setFixedHeight(300)

            inner_widget = QWidget()
            inner_layout = QVBoxLayout(inner_widget)

            header_row = QWidget()
            header_layout = QHBoxLayout(header_row)

            code_header = QLabel("Code")
            code_header.setFont(QFont("Arial", 12, QFont.Bold))
            code_header.setFixedWidth(80)

            name_header = QLabel("Name")
            name_header.setFont(QFont("Arial", 12, QFont.Bold))
            name_header.setFixedWidth(180)

            score_header = QLabel("Score")
            score_header.setFont(QFont("Arial", 12, QFont.Bold))
            score_header.setFixedWidth(100)

            header_layout.addWidget(code_header)
            header_layout.addWidget(name_header)
            header_layout.addWidget(score_header)
            header_layout.addStretch()

            inner_layout.addWidget(header_row)

            sorted_delegates = sorted(committee.delegates, key=lambda d: d.score())

            for delegate in sorted_delegates:
                delegate_frame = QWidget()
                delegate_layout = QHBoxLayout(delegate_frame)

                code_label = QLabel(f"{delegate.code}")
                code_label.setFont(QFont("Arial", 12))
                code_label.setFixedWidth(80)

                name_label = QLabel(f"{delegate.surname} {delegate.name}")
                name_label.setFont(QFont("Arial", 12))
                name_label.setFixedWidth(180)

                score_label = QLabel(f"{delegate.score():.2f}")
                score_label.setFont(QFont("Arial", 12))
                score_label.setFixedWidth(100)

                delegate_layout.addWidget(code_label)
                delegate_layout.addWidget(name_label)
                delegate_layout.addWidget(score_label)
                delegate_layout.addStretch()

                inner_layout.addWidget(delegate_frame)

            scroll_inner.setWidget(inner_widget)

            committee_container = QWidget()
            committee_layout = QVBoxLayout(committee_container)
            committee_layout.setContentsMargins(0, 0, 0, 0)
            committee_layout.addWidget(title_container)
            committee_layout.addWidget(scroll_inner)

            if i < self.split_index:
                self.left_column.addWidget(committee_container)
            else:
                self.right_column.addWidget(committee_container)

    def refresh_tab(self):
        self.init_ui()

    def connect_delegate_manager(self):
        self.delegate_manager.score_updated.connect(self.refresh_tab)
        self.delegate_manager.delegates_updated.connect(self.refresh_tab)

    def clear_columns(self):
        """Clears widgets from left and right columns."""
        for layout in [self.left_column, self.right_column]:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()




class SpeechesTab(QWidget):
    def __init__(self, tab_widget, delegate_manager, window):
        super().__init__()
        self.delegate_manager = delegate_manager
        self.window = window
        
        self.speeches = []
        self.selected_index = None

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout(self)

        self.setup_ui()
        self.connect_signals()

        self.update_warning_visibility()
        tab_widget.addTab(self, "Speeches")

    def setup_ui(self):
        # --- Warning if no delegates ---
        self.warning_label = QLabel("⚠️ No delegates loaded. Please load a delegate file.")
        self.warning_label.setFont(QFont("Arial", 11))
        self.warning_label.setStyleSheet("color: red")
        self.warning_label.setWordWrap(True)
        self.left_layout.addWidget(self.warning_label)
     
        # --- Search Input ---
        search_label = QLabel("Enter Delegate Code:")
        search_label.setFont(QFont("Arial", 12))
        self.left_layout.addWidget(search_label)
     
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("e.g., 101")
        self.left_layout.addWidget(self.code_input)
     
        # --- Name Display ---
        self.name_display_label = QLabel("")
        self.name_display_label.setFont(QFont("Arial", 10, italic=True))
        self.left_layout.addWidget(self.name_display_label)
     
        # --- Speech Type ---
        self.speech_type_dropdown = QComboBox()
        self.speech_type_dropdown.addItems([speech.value for speech in SpeechType])
        self.left_layout.addWidget(self.speech_type_dropdown)
     
        # --- Add/Edit Button ---
        self.add_button = QPushButton("➕ Add Speech")
        self.left_layout.addWidget(self.add_button)
     
        # --- Edit/Delete Action Buttons ---
        self.edit_button = QPushButton("✏️ Apply Edit")
        self.edit_button.setVisible(False)
        self.left_layout.addWidget(self.edit_button)
     
        self.delete_button = QPushButton("🗑️ Delete Speech")
        self.delete_button.setVisible(False)
        self.left_layout.addWidget(self.delete_button)
        
        self.cancel_button = QPushButton("❌ Cancel")
        self.cancel_button.setVisible(False)  # Initially hidden
        self.left_layout.addWidget(self.cancel_button)

        # --- Score ---
        self.score_label = QLabel("Delegate Score: 0")
        self.score_label.setFont(QFont("Arial", 12))
        self.left_layout.addWidget(self.score_label)
     
        self.left_layout.addStretch()
     
        # --- History on the right ---
        history_label = QLabel("Speech History:")
        history_label.setFont(QFont("Arial", 12))
        self.right_layout.addWidget(history_label)
     
        self.speech_history = QListWidget()
        self.right_layout.addWidget(self.speech_history)
     
        self.right_layout.addStretch()
     
        # Layouts
        self.main_layout.addLayout(self.left_layout, stretch=1)
        self.main_layout.addLayout(self.right_layout, stretch=2)


    def connect_signals(self):
        self.code_input.textChanged.connect(self.update_delegate_name)
        self.add_button.clicked.connect(self.add_speech)
        self.delegate_manager.delegates_updated.connect(self.update_warning_visibility)
        self.speech_history.itemClicked.connect(self.select_speech_for_edit)
        self.edit_button.clicked.connect(self.apply_edit)
        self.delete_button.clicked.connect(self.delete_speech)
        self.cancel_button.clicked.connect(self.cancel_edit)

    def update_delegate_name(self):
        code = self.code_input.text().strip().upper()
        delegate = delegates.get(code)
        if delegate:
            self.name_display_label.setText(f"{delegate.code} {delegate.name} {delegate.surname}")
            self.score_label.setText(f"Delegate Score: {delegate.score():.2f}")
        else:
            self.name_display_label.setText("")
            self.score_label.setText("Delegate Score: 0")

    def add_speech(self):
        code = self.code_input.text().strip().upper()
        speech_text = self.speech_type_dropdown.currentText()
        delegate = delegates.get(code)

        if delegate is None:
            QMessageBox.warning(self.window, "Delegate Not Found", f"No delegate found with code: {code}")
            return

        speech_type = SpeechType(speech_text)
        delegate.speak(speech_type)

        # Save for future editing
        self.speeches.append((code, speech_type))
        self.speech_history.addItem(f"{delegate.code} {delegate.name} {delegate.surname} ({delegate.school_name}): {speech_type.value}")

        self.score_label.setText(f"Delegate Score: {delegate.score():.2f}")
        self.delegate_manager.update_score()

        QMessageBox.information(self.window, "Speech Added", f"{speech_type.value} added to {delegate.code} {delegate.name} {delegate.surname}.")

        # Reset input
        self.code_input.clear()
        self.speech_type_dropdown.setCurrentIndex(0)

    def select_speech_for_edit(self, item):
        self.selected_index = self.speech_history.row(item)
        code, speech_type = self.speeches[self.selected_index]

        # Set input fields based on selected speech
        self.code_input.setText(code)
        self.speech_type_dropdown.setCurrentText(speech_type.value)

        # Show Edit and Delete buttons, hide Add button
        self.edit_button.setVisible(True)
        self.delete_button.setVisible(True)
        self.cancel_button.setVisible(True)
        self.add_button.setVisible(False)
        
        
    def deselect_speech(self):
        # Clear selection
        self.selected_index = None

        # Clear input fields
        self.code_input.clear()
        self.speech_type_dropdown.setCurrentIndex(0)

        # Hide Edit and Delete buttons, show Add button
        self.edit_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.add_button.setVisible(True)


    def apply_edit(self):
        if self.selected_index is None:
            return

        new_code = self.code_input.text().strip().upper()
        new_speech_text = self.speech_type_dropdown.currentText()
        new_speech_type = SpeechType(new_speech_text)

        old_code, old_speech_type = self.speeches[self.selected_index]
        old_delegate = delegates.get(old_code)
        if old_delegate:
            old_delegate.unspeak(old_speech_type)

        new_delegate = delegates.get(new_code)
        if new_delegate is None:
            QMessageBox.warning(self.window, "Delegate Not Found", f"No delegate found with code: {new_code}")
            return

        new_delegate.speak(new_speech_type)
        self.speeches[self.selected_index] = (new_code, new_speech_type)

        self.speech_history.item(self.selected_index).setText(
            f"{new_delegate.code} {new_delegate.name} {new_delegate.surname} ({new_delegate.school_name}): {new_speech_type.value}"
        )

        self.score_label.setText(f"Delegate Score: {new_delegate.score():.2f}")
        self.delegate_manager.update_score()

        self.edit_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.selected_index = None
        
    def cancel_edit(self):
        # If a speech was selected, revert to the previous state (no changes)
        code, speech_type = self.speeches[self.selected_index]
        self.code_input.setText(code)
        self.speech_type_dropdown.setCurrentText(speech_type.value)
    
        # Hide Edit, Delete, and Cancel buttons, show Add button
        self.edit_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.cancel_button.setVisible(False)
        self.add_button.setVisible(True)
    
        # Reset selected index
        self.selected_index = None


    def delete_speech(self):
        if self.selected_index is None:
            return

        code, speech_type = self.speeches.pop(self.selected_index)
        delegate = delegates.get(code)
        if delegate:
            delegate.unspeak(speech_type)

        self.speech_history.takeItem(self.selected_index)
        self.delegate_manager.update_score()

        self.code_input.clear()
        self.name_display_label.clear()
        self.score_label.setText("Delegate Score: 0")
        self.edit_button.setVisible(False)
        self.delete_button.setVisible(False)
        self.selected_index = None

    def update_warning_visibility(self):
        self.warning_label.setVisible(len(delegates) == 0)


class StatisticsTab(QWidget):
    def __init__(self, delegate_manager):
        super().__init__()
        self.layout = QHBoxLayout(self)

        # Create two figures
        self.school_figure = Figure(figsize=(5, 5))
        self.committee_figure = Figure(figsize=(5, 5))

        self.school_canvas = FigureCanvas(self.school_figure)
        self.committee_canvas = FigureCanvas(self.committee_figure)

        self.layout.addWidget(self.school_canvas)
        self.layout.addWidget(self.committee_canvas)

        # Draw initial plots
        self.update_plots()

        # Connect to signal
        delegate_manager.score_updated.connect(self.update_plots)

    def update_plots(self):
        self.plot_school_speeches()
        self.plot_committee_speeches()

    def plot_school_speeches(self):
        self.school_figure.clear()
        ax = self.school_figure.add_subplot(111)

        school_speech_counts = {school_name: 0 for school_name in schools.keys()}
        for committee in committees.values():
            for delegate in committee.delegates:
                if delegate.school_name in school_speech_counts:
                    school_speech_counts[delegate.school_name] += len(delegate.speeches)

        school_names = list(school_speech_counts.keys())
        counts = list(school_speech_counts.values())

        colors = plt.cm.tab20.colors  # or 'Set3', 'Pastel1', etc.
        bar_colors = [colors[i % len(colors)] for i in range(len(school_names))]

        bars = ax.bar(range(len(school_names)), counts, color=bar_colors)
        
        ax.set_xticks([bar.get_x() + bar.get_width() / 2 for bar in bars])
        ax.set_xticklabels(school_names, rotation=45, ha='right')
        
        ax.set_ylabel("Number of Speeches")
        ax.set_title("Speeches per School")
        self.school_figure.tight_layout()  # <--- This fixes clipping

        self.school_canvas.draw()

    def plot_committee_speeches(self):
        self.committee_figure.clear()
        ax = self.committee_figure.add_subplot(111)

        committee_speech_counts = {}
        for name, committee in committees.items():
            total = sum(len(delegate.speeches) for delegate in committee.delegates)
            committee_speech_counts[name] = total

        committee_names = list(committee_speech_counts.keys())
        counts = list(committee_speech_counts.values())
        
        colors = plt.cm.tab20.colors  # or 'Set3', 'Pastel1', etc.
        bar_colors = [colors[i % len(colors)] for i in range(len(committee_names))]

        bars = ax.bar(range(len(committee_names)), counts, color=bar_colors)
        
        ax.set_xticks([bar.get_x() + bar.get_width() / 2 for bar in bars])
        ax.set_xticklabels(committee_names, rotation=45, ha='right')
               
        ax.set_ylabel("Number of Speeches")
        ax.set_title("Speeches per Committee")
        self.committee_canvas.draw()



class SettingsMenu(QMenu):
    def __init__(self, app, delegate_manager, parent=None):
        super(SettingsMenu, self).__init__(parent)
        self.app = app
        self.delegate_manager = delegate_manager

        load_action = QAction("Load Participants from File", self)
        load_action.triggered.connect(self.load_participants_from_file)
        self.addAction(load_action)

        theme_toggle_action = QAction("Toggle Light/Dark Theme", self)
        theme_toggle_action.triggered.connect(self.toggle_theme)
        self.addAction(theme_toggle_action)

    def load_participants_from_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Participants Excel File", "", "Excel Files (*.xlsx);;All Files (*)"
        )
        if file_path:
            delegates = load_delegates(file_path)
            if delegates:
                self.delegate_manager.set_delegates(delegates)
                QMessageBox.information(self, "Success", "Delegates loaded successfully.")
            else:
                QMessageBox.warning(self, "Error", "Failed to load delegates.")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        current_stylesheet = self.app.styleSheet()
        if qdarktheme.load_stylesheet("light") == current_stylesheet:
            self.app.setStyleSheet(qdarktheme.load_stylesheet())  # Dark theme
        else:
            self.app.setStyleSheet(qdarktheme.load_stylesheet("light"))  # Light theme


def launch_gui():
    # Create the QApplication instance
    app = QApplication([])

    # Apply light theme to Qt application by default
    app.setStyleSheet(qdarktheme.load_stylesheet())

    # Create the main window
    window = QMainWindow()
    window.setWindowTitle("🎓 MEPGest — Delegate Dashboard")
    window.resize(1000, 700)

    # Central widget and layout
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
    general_tab = GeneralTab(tab_widget, delegate_manager)
    tab_widget.addTab(general_tab, "General List")
    committees_tab = CommitteesTab(tab_widget, delegate_manager)
    tab_widget.addTab(committees_tab.widget(), "Committees")
    statistics_tab = StatisticsTab(delegate_manager)
    tab_widget.addTab(statistics_tab, "Statistics")
    speeches_tab = SpeechesTab(tab_widget, delegate_manager, window)
    tab_widget.addTab(speeches_tab, "Speeches")

    # Add menu bar with theme toggle
    menu_bar = window.menuBar()
    settings_menu = SettingsMenu(app, delegate_manager)  # Pass the app instance to the menu
    menu_bar.addMenu(settings_menu)

    # Add a toolbar with the theme toggle action
    toolbar = QToolBar(window)
    window.addToolBar(toolbar)
    
    # Add settings button to toolbar
    settings_button = QAction("⚙️", window)
    settings_button.triggered.connect(lambda: settings_menu.exec())  # Open settings menu
    toolbar.addAction(settings_button)

    # Set the central widget and show the window
    window.setCentralWidget(central_widget)
    window.show()

    app.exec()