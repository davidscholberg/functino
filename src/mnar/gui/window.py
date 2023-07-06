from typing import cast

from PyQt6.QtCore import QMargins, QSettings, Qt
from PyQt6.QtGui import QCloseEvent, QColor, QFont, QKeySequence, QPalette, QShortcut
from PyQt6.QtWidgets import QComboBox, QFrame, QHBoxLayout, QLabel, QMainWindow, QStackedLayout, QTextEdit, QSizePolicy, QSplitter, QVBoxLayout, QWidget

from mnar.execute import get_output
from mnar.gui.editor import Editor
from mnar.gui.language import get_lexer_class
from mnar.gui.theme import Theme, get_uniform_palette
from mnar.language import LanguageProfile, get_language_profiles

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
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)

class MainWindow(QMainWindow):
    """Main window for this application."""
    def __init__(self, theme: Theme) -> None:
        super().__init__()
        self.setWindowTitle("Mnar")
        self._theme = theme
        self._languages_combo_box = QComboBox()
        self._editors_layout = QStackedLayout()
        self._output_widget = OutputWidget()
        self._main_splitter = self._make_main_splitter()
        self.setCentralWidget(self._main_splitter)
        self._populate_languages_combobox()
        self._editor_index_map: dict[int, int] = {}
        self.switch_editor()
        self._restore_window_state()
        self._languages_combo_box.currentIndexChanged.connect(self.switch_editor)
        QShortcut(QKeySequence("Ctrl+r"), self).activated.connect(self.on_run)

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Handle window closed event."""
        self._save_window_state()
        return super().closeEvent(a0)

    def on_run(self) -> None:
        """Callback to run code from the editor."""
        current_editor: Editor = cast(Editor, self._editors_layout.currentWidget())
        editor_text = current_editor.text()
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

    def switch_editor(self) -> None:
        """Switches to the editor instance pointed to by the languages combobox."""
        self._output_widget.clear()
        language_index = self._languages_combo_box.currentIndex()
        editor_index = self._editor_index_map.get(language_index)
        if editor_index is None:
            editor_index = len(self._editor_index_map)
            self._editor_index_map[language_index] = editor_index
        if editor_index < self._editors_layout.count():
            self._editors_layout.setCurrentIndex(editor_index)
            return
        self._editors_layout.addWidget(Editor())
        self._editors_layout.setCurrentIndex(editor_index)
        self._set_editor_lexer()
        self._restore_editor_text()

    def _make_main_splitter(self) -> QSplitter:
        """Create and return the main splitter widget for this window."""
        self._languages_combo_box.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        top_row_spacer = QWidget()
        top_row_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_row_layout = QHBoxLayout()
        top_row_layout.setContentsMargins(QMargins())
        top_row_layout.addWidget(self._languages_combo_box)
        top_row_layout.addWidget(top_row_spacer)
        top_row_container = QWidget()
        top_row_container.setLayout(top_row_layout)
        editors_container = QWidget()
        editors_container.setLayout(self._editors_layout)
        splitter_top_layout = QVBoxLayout()
        splitter_top_layout.setContentsMargins(QMargins())
        splitter_top_layout.addWidget(top_row_container)
        splitter_top_layout.addWidget(editors_container)
        splitter_top_container = QWidget()
        splitter_top_container.setLayout(splitter_top_layout)
        splitter_bottom_layout = QVBoxLayout()
        splitter_bottom_layout.setContentsMargins(QMargins())
        splitter_bottom_layout.addWidget(self._output_widget)
        splitter_bottom_container = QWidget()
        splitter_bottom_container.setLayout(splitter_bottom_layout)
        splitter = UniformSplitter(Qt.Orientation.Vertical)
        splitter.addWidget(splitter_top_container)
        splitter.addWidget(splitter_bottom_container)
        return splitter

    def _populate_languages_combobox(self) -> None:
        """Add all language profiles to the languages combobox."""
        for language_profile in get_language_profiles():
            self._languages_combo_box.addItem(language_profile.name, language_profile)

    def _restore_editor_text(self) -> None:
        """Restore any saved editor text for the current language profile."""
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.beginGroup("editor_text")
        current_language_profile: LanguageProfile = self._languages_combo_box.currentData()
        if settings.contains(current_language_profile.name):
            current_editor: Editor = cast(Editor, self._editors_layout.currentWidget())
            current_editor.setText(settings.value(current_language_profile.name))
        settings.endGroup()
        settings.endGroup()

    def _restore_window_state(self) -> None:
        """
        Restores window state from previous session (or sets defaults if no
        previous session).

        Note that not everything saved by _save_window_state is restored here;
        saved code from editors is not restored until the respective editor is
        loaded by the user.
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
        """
        Persist the state of the window (e.g. the geometry, user text contents,
        etc.).
        """
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("splitter_state", self._main_splitter.saveState())
        settings.beginGroup("editor_text")
        for language_index in range(self._languages_combo_box.count()):
            language_profile: LanguageProfile = self._languages_combo_box.itemData(language_index)
            editor: Editor = cast(Editor, self._editors_layout.widget(self._editor_index_map[language_index]))
            settings.setValue(language_profile.name, editor.text())
        settings.endGroup()
        settings.endGroup()

    def _set_editor_lexer(self) -> None:
        """
        Set lexer for the current editor.

        This only needs to be done once per editor widget instance.
        """
        current_language_profile: LanguageProfile = self._languages_combo_box.currentData()
        current_editor: Editor = cast(Editor, self._editors_layout.currentWidget())
        lexer_class = get_lexer_class(current_language_profile.language_id)
        if lexer_class is None:
            return
        lexer = lexer_class()
        lexer.setPaper(self.palette().color(QPalette.ColorRole.Base))
        lexer.setColor(self.palette().color(QPalette.ColorRole.Text))
        lexer.setFont(current_editor.font())
        for style_id, color_hex in self._theme.get_lexer_color_map(current_language_profile.language_id).items():
            lexer.setColor(QColor(color_hex), style_id)
        current_editor.setLexer(lexer)