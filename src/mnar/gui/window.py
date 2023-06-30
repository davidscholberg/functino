from PyQt6.QtCore import QMargins, QSettings, Qt
from PyQt6.QtGui import QCloseEvent, QColor, QKeySequence, QPalette, QShortcut
from PyQt6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QMainWindow, QTextEdit, QSizePolicy, QSplitter, QVBoxLayout, QWidget

from mnar.execute import get_output
from mnar.gui.editor import Editor
from mnar.gui.theme import get_uniform_palette
from mnar.language import get_language_profiles

class UniformSplitter(QSplitter):
    """QSplitter with uniform styling."""
    def __init__(self, orientation: Qt.Orientation) -> None:
        super().__init__(orientation)
        self.setPalette(get_uniform_palette(self.palette()))
        self.setAutoFillBackground(True)

class OutputWidget(QTextEdit):
    """Widget for displaying the results of executing the code in the editor."""
    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)
        self.setFrameStyle(QFrame.Shape.NoFrame)

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
        self._output_widget.setText("")
        if not stderr and not stdout:
            text_color_hex = QColor(Qt.GlobalColor.darkGray).name(QColor.NameFormat.HexArgb)
            html = f"<span style=\"color:{text_color_hex}\"><em>no output</em></span>"
            self._output_widget.setHtml(html)
            return
        if stderr:
            original_text_color = self._output_widget.palette().color(QPalette.ColorRole.Text)
            self._output_widget.setTextColor(Qt.GlobalColor.red)
            self._output_widget.append(stderr)
            self._output_widget.setTextColor(original_text_color)
        if stdout:
            self._output_widget.append(stdout)

    def _make_main_splitter(self) -> QSplitter:
        """Create and return the main splitter widget for this window."""
        for language_profile in get_language_profiles():
            self._languages_combo_box.addItem(language_profile.name, language_profile)
        self._languages_combo_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        top_row_spacer = QWidget()
        top_row_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_row_layout = QHBoxLayout()
        top_row_layout.setContentsMargins(QMargins())
        top_row_layout.addWidget(self._languages_combo_box)
        top_row_layout.addWidget(top_row_spacer)
        top_row_container = QWidget()
        top_row_container.setLayout(top_row_layout)
        editor_layout = QVBoxLayout()
        editor_layout.setContentsMargins(QMargins())
        editor_layout.addWidget(top_row_container)
        editor_layout.addWidget(self._editor)
        editor_container = QWidget()
        editor_container.setLayout(editor_layout)
        output_layout = QVBoxLayout()
        output_layout.setContentsMargins(QMargins())
        output_layout.addWidget(self._output_widget)
        output_container = QWidget()
        output_container.setLayout(output_layout)
        splitter = UniformSplitter(Qt.Orientation.Vertical)
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