from PyQt6.QtCore import QMargins, QSettings, Qt
from PyQt6.QtGui import QCloseEvent, QKeySequence, QShortcut
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit, QSizePolicy, QSplitter, QVBoxLayout, QWidget

from mnar.execute import get_output
from mnar.gui.editor import Editor
from mnar.language import get_language_profiles

class OutputWidget(QPlainTextEdit):
    """Widget for displaying the results of executing the code in the editor."""
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)

class MainWindow(QMainWindow):
    """Main window for this application."""
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        self._languages_combo_box = QComboBox()
        self._editor = Editor()
        self._output_widget = OutputWidget()
        self._main_splitter = self._make_main_splitter()
        self.setCentralWidget(self._main_splitter)
        self._restore_window_state()
        QShortcut(QKeySequence("Ctrl+r"), self).activated.connect(self.on_run)

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Handle window closed event."""
        self._save_window_state()
        return super().closeEvent(a0)

    def on_run(self) -> None:
        """Callback to run code from the editor."""
        editor_text = self._editor.text()
        current_language_profile = self._languages_combo_box.currentData()
        stdout, stderr = get_output(current_language_profile, editor_text)
        output_str = f"stderr:\n{stderr}\nstdout:\n{stdout}"
        self._output_widget.setPlainText(output_str)

    def _make_main_splitter(self) -> QSplitter:
        """Create and return the main splitter widget for this window."""
        editor_container = QWidget()
        editor_layout = QVBoxLayout()
        editor_layout.setContentsMargins(QMargins())
        for language_profile in get_language_profiles():
            self._languages_combo_box.addItem(language_profile.name, language_profile)
        self._languages_combo_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        top_row_spacer = QWidget()
        top_row_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_row_container = QWidget()
        top_row_layout = QHBoxLayout()
        top_row_layout.setContentsMargins(QMargins())
        top_row_layout.addWidget(self._languages_combo_box)
        top_row_layout.addWidget(top_row_spacer)
        top_row_container.setLayout(top_row_layout)
        editor_layout.addWidget(top_row_container)
        editor_layout.addWidget(self._editor)
        editor_container.setLayout(editor_layout)
        output_container = QWidget()
        output_layout = QVBoxLayout()
        output_layout.setContentsMargins(QMargins())
        output_layout.addWidget(QLabel("Output:"))
        output_layout.addWidget(self._output_widget)
        output_container.setLayout(output_layout)
        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(editor_container)
        splitter.addWidget(output_container)
        return splitter

    def _restore_window_state(self) -> None:
        """
        Restores window state from previous session (or sets defaults if no
        previous session).
        """
        settings = QSettings()
        settings.beginGroup("main_window")
        if settings.contains("window_geometry"):
            self.restoreGeometry(settings.value("window_geometry"))
        else:
            self.resize(800, 600)
        if settings.contains("splitter_state"):
            self._main_splitter.restoreState(settings.value("splitter_state"))
        else:
            self._main_splitter.setStretchFactor(0, 2)
            self._main_splitter.setStretchFactor(1, 1)
        settings.endGroup()

    def _save_window_state(self) -> None:
        """Persist the state of the window (i.e. the geometry)."""
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("splitter_state", self._main_splitter.saveState())
        settings.endGroup()