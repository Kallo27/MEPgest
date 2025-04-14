#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File: gui.py
# Created: 14-04-2025
# Author: Lorenzo Calandra Buonaura <lorenzocb01@gmail.com>
# Institution: APS Model European Parliament Italia
#
# Description: 
#


from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QTabWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QGridLayout
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from mepgest.models import committees
from PySide6.QtWidgets import QLineEdit, QPushButton, QComboBox, QMessageBox
from mepgest.models import delegates
from mepgest.speech import SpeechType


def launch_gui():
    app = QApplication([])

    window = QMainWindow()
    window.setWindowTitle("🎓 MEPGest — Delegate Dashboard")
    window.resize(1000, 700)

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)

    # Title
    title = QLabel("Welcome to MEPGest!")
    title.setFont(QFont("Arial", 28, QFont.Bold))
    title.setAlignment(Qt.AlignCenter)
    layout.addWidget(title)

    # Tabs
    tab_widget = QTabWidget()
    layout.addWidget(tab_widget)

    # === General List Tab ===
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
        score_label.setStyleSheet("color: gray;")

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

    # === Committees Tab (grid of scrollable committees) ===
    committees_tab = QWidget()
    committees_layout = QHBoxLayout(committees_tab)

    left_column = QVBoxLayout()
    right_column = QVBoxLayout()

    committee_list = list(committees.items())
    split_index = (len(committee_list) + 1) // 2

    for i, (name, committee) in enumerate(committee_list):
        # Header
        header = QLabel(f"Committee: {name}")
        header.setFont(QFont("Arial", 18, QFont.Bold))

        # Scroll area for this committee
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(250)

        inner_widget = QWidget()
        grid_layout = QGridLayout(inner_widget)

        for index, delegate in enumerate(committee.delegates):
            delegate_frame = QWidget()
            delegate_layout = QHBoxLayout(delegate_frame)

            name_label = QLabel(f"{delegate.code} {delegate.surname} {delegate.name}")
            name_label.setFont(QFont("Arial", 14))
            score_label = QLabel(f"Score: {delegate.score():.2f}")
            score_label.setFont(QFont("Arial", 12))
            score_label.setStyleSheet("color: gray;")

            delegate_layout.addWidget(name_label)
            delegate_layout.addSpacing(15)
            delegate_layout.addWidget(score_label)
            delegate_layout.addStretch()

            row = index // 2
            col = index % 2
            grid_layout.addWidget(delegate_frame, row, col)

        scroll.setWidget(inner_widget)

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.addWidget(header)
        container_layout.addWidget(scroll)

        if i < split_index:
            left_column.addWidget(container)
        else:
            right_column.addWidget(container)

    committees_layout.addLayout(left_column)
    committees_layout.addSpacing(30)
    committees_layout.addLayout(right_column)

    tab_widget.addTab(committees_tab, "Committees")

    # === Speeches Tab ===
    speeches_tab = QWidget()
    speeches_layout = QVBoxLayout(speeches_tab)

    search_label = QLabel("Enter Delegate Code:")
    search_label.setFont(QFont("Arial", 12))
    speeches_layout.addWidget(search_label)

    code_input = QLineEdit()
    code_input.setPlaceholderText("e.g., 101")
    speeches_layout.addWidget(code_input)

    speech_type_dropdown = QComboBox()
    speech_type_dropdown.addItems([speech.value for speech in SpeechType])
    speeches_layout.addWidget(speech_type_dropdown)

    add_button = QPushButton("➕ Add Speech")
    speeches_layout.addWidget(add_button)

    def add_speech():
        code = code_input.text().strip().upper()
        speech_text = speech_type_dropdown.currentText()
        delegate = delegates.get(code)

        if delegate is None:
            QMessageBox.warning(window, "Delegate Not Found", f"No delegate found with code: {code}")
            return

        speech_type = SpeechType(speech_text)
        delegate.speak(speech_type)
        QMessageBox.information(window, "Speech Added", f"{speech_type.value} added to {delegate.name} {delegate.surname}.")

    add_button.clicked.connect(add_speech)

    speeches_layout.addStretch()
    tab_widget.addTab(speeches_tab, "Speeches")


    window.setCentralWidget(central_widget)
    window.show()
    app.exec()
