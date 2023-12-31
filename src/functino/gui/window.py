from typing import cast

from PyQt6.QtCore import QMargins, QSettings, Qt
from PyQt6.QtGui import (
    QCloseEvent,
    QColor,
    QFont,
    QKeySequence,
    QPalette,
    QShortcut,
)
from PyQt6.QtSvgWidgets import QSvgWidget
from PyQt6.QtWidgets import (
    QPushButton,
    QComboBox,
    QFontDialog,
    QFrame,
    QHBoxLayout,
    QMainWindow,
    QStackedLayout,
    QTextEdit,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from functino.execute import get_output
from functino.gui.editor import Editor
from functino.gui.exception import pop_up_error_message
from functino.gui.icon import IconSet
from functino.gui.language import get_lexer_class
from functino.gui.theme import Theme, get_uniform_palette
from functino.language import LanguageProfile, get_language_profiles


class UniformSplitter(QSplitter):
    """
    QSplitter with uniform styling.
    """

    def __init__(self, orientation: Qt.Orientation) -> None:
        super().__init__(orientation)
        self.setPalette(get_uniform_palette(self.palette()))
        self.setAutoFillBackground(True)


class OutputWidget(QTextEdit):
    """
    Widget for displaying the results of executing the code in the editor.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setReadOnly(True)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)


class MainWindow(QMainWindow):
    """
    Main window for this application.
    """

    def __init__(self, theme: Theme, icon_set: IconSet) -> None:
        super().__init__()
        self.setWindowTitle("Functino")
        self._theme = theme
        self._icon_set = icon_set
        self._languages_combo_box = QComboBox()
        self._languages_combo_box.setToolTip("Select Language Profile")
        self._run_button = SvgButton(self._icon_set.play_icon_data)
        self._run_button.setToolTip("Run (Ctrl+r)")
        self._settings_button = SvgButton(self._icon_set.settings_icon_data)
        self._editors_layout = QStackedLayout()
        self._output_widget = OutputWidget()
        self._main_splitter = self._make_main_splitter()
        self.setCentralWidget(self._main_splitter)
        self._populate_languages_combobox()
        self._restore_window_state()
        self._editor_index_map: dict[int, int] = {}
        self.switch_editor()
        self._languages_combo_box.currentIndexChanged.connect(self.switch_editor)
        self._run_button.clicked.connect(self.on_run)
        QShortcut(QKeySequence("Ctrl+r"), self).activated.connect(self.on_run)
        self._settings_button.clicked.connect(self.on_settings_click)

    def closeEvent(self, a0: QCloseEvent) -> None:
        """
        Handle window closed event.
        """
        self._save_window_state()
        return super().closeEvent(a0)

    def on_run(self) -> None:
        """
        Callback to run code from the editor.
        """
        current_editor: Editor = cast(Editor, self._editors_layout.currentWidget())
        editor_text = current_editor.text()
        current_language_profile = self._languages_combo_box.currentData()
        if current_language_profile is None:
            pop_up_error_message("no language profile loaded")
            return
        try:
            stdout, stderr = get_output(current_language_profile, editor_text)
        except Exception as e:
            pop_up_error_message(e)
            return
        self._output_widget.setText("")
        if not stderr and not stdout:
            text_color_hex = QColor(Qt.GlobalColor.darkGray).name(
                QColor.NameFormat.HexArgb
            )
            html = f'<span style="color:{text_color_hex}"><em>no output</em></span>'
            self._output_widget.setHtml(html)
        if stderr:
            original_text_color = self._output_widget.palette().color(
                QPalette.ColorRole.Text
            )
            self._output_widget.setTextColor(Qt.GlobalColor.red)
            self._output_widget.append(stderr)
            self._output_widget.setTextColor(original_text_color)
        if stdout:
            self._output_widget.append(stdout)
        scrollbar = self._output_widget.verticalScrollBar()
        scrollbar.setValue(scrollbar.minimum())

    def on_settings_click(self) -> None:
        """
        Handles settings button click.
        """
        new_font, _ = QFontDialog.getFont(self._output_widget.font())
        for i in range(self._editors_layout.count()):
            editor: Editor = cast(Editor, self._editors_layout.widget(i))
            editor.setFont(new_font)
            lexer = editor.lexer()
            if lexer is not None:
                lexer.setFont(new_font)
        self._output_widget.setFont(new_font)

    def switch_editor(self) -> None:
        """
        Switches to the editor instance pointed to by the languages combobox.
        """
        self._output_widget.clear()
        language_index = self._languages_combo_box.currentIndex()
        editor_index = self._editor_index_map.get(language_index)
        if editor_index is None:
            editor_index = len(self._editor_index_map)
            self._editor_index_map[language_index] = editor_index
        if editor_index < self._editors_layout.count():
            self._editors_layout.setCurrentIndex(editor_index)
            return
        editor = Editor()
        editor.setFont(self._output_widget.font())
        self._editors_layout.addWidget(editor)
        self._editors_layout.setCurrentIndex(editor_index)
        self._set_editor_lexer()
        self._restore_editor_text()

    def _make_main_splitter(self) -> QSplitter:
        """
        Create and return the main splitter widget for this window.
        """
        self._languages_combo_box.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )
        top_row_spacer = QWidget()
        top_row_spacer.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        top_row_layout = QHBoxLayout()
        top_row_layout.setContentsMargins(QMargins())
        top_row_layout.addWidget(self._languages_combo_box)
        top_row_layout.addWidget(self._run_button)
        top_row_layout.addWidget(self._settings_button)
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
        """
        Add all language profiles to the languages combobox.
        """
        try:
            for language_profile in get_language_profiles():
                self._languages_combo_box.addItem(
                    language_profile.name, language_profile
                )
        except Exception as e:
            pop_up_error_message(e)

    def _restore_editor_text(self) -> None:
        """
        Restore any saved editor text for the current language profile.
        """
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.beginGroup("editor_text")
        current_language_profile: LanguageProfile = (
            self._languages_combo_box.currentData()
        )
        if current_language_profile is not None and settings.contains(
            current_language_profile.name
        ):
            current_editor: Editor = cast(Editor, self._editors_layout.currentWidget())
            current_editor.setText(settings.value(current_language_profile.name))
        settings.endGroup()
        settings.endGroup()

    def _restore_window_state(self) -> None:
        """
        Restores window state from previous session (or sets defaults if no previous
        session).

        Note that not everything saved by _save_window_state is restored here; saved
        code from editors is not restored until the respective editor is loaded.
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
            self._main_splitter.setStretchFactor(0, 20)
            self._main_splitter.setStretchFactor(1, 1)
        if settings.contains("language_selection"):
            previous_language_profile_name = settings.value("language_selection")
            for language_index in range(self._languages_combo_box.count()):
                language_profile: LanguageProfile = self._languages_combo_box.itemData(
                    language_index
                )
                if previous_language_profile_name == language_profile.name:
                    self._languages_combo_box.setCurrentIndex(language_index)
                    break
        if settings.contains("font"):
            saved_font = QFont()
            saved_font.fromString(settings.value("font"))
            self._output_widget.setFont(saved_font)
        else:
            self._output_widget.setFont(QFont("Consolas", 11))
        settings.endGroup()

    def _save_window_state(self) -> None:
        """
        Persist the state of the window (e.g. the geometry, user text contents, etc.).
        """
        settings = QSettings()
        settings.beginGroup("main_window")
        settings.setValue("window_geometry", self.saveGeometry())
        settings.setValue("splitter_state", self._main_splitter.saveState())
        current_language_profile: LanguageProfile = (
            self._languages_combo_box.currentData()
        )
        if current_language_profile is not None:
            settings.setValue("language_selection", current_language_profile.name)
        settings.setValue("font", self._output_widget.font().toString())
        settings.beginGroup("editor_text")
        for language_index in range(self._languages_combo_box.count()):
            if language_index not in self._editor_index_map:
                continue
            language_profile: LanguageProfile = self._languages_combo_box.itemData(
                language_index
            )
            editor: Editor = cast(
                Editor,
                self._editors_layout.widget(self._editor_index_map[language_index]),
            )
            settings.setValue(language_profile.name, editor.text())
        settings.endGroup()
        settings.endGroup()

    def _set_editor_lexer(self) -> None:
        """
        Set lexer for the current editor.

        This only needs to be done once per editor widget instance.

        Note that currently the background colors of the themes are ignored; only the
        foreground colors are used. The background colors come from the window palette.
        """
        current_language_profile: LanguageProfile = (
            self._languages_combo_box.currentData()
        )
        if current_language_profile is None:
            return
        try:
            lexer_color_map = self._theme.get_lexer_color_map(
                current_language_profile.language_id
            )
        except Exception as e:
            pop_up_error_message(e)
            return
        lexer_class = get_lexer_class(current_language_profile.language_id)
        if lexer_class is None:
            return
        lexer = lexer_class()
        lexer.setPaper(self.palette().color(QPalette.ColorRole.Base))
        lexer.setColor(self.palette().color(QPalette.ColorRole.Text))
        lexer.setFont(self._output_widget.font())
        for style_id, color_hex in lexer_color_map.items():
            lexer.setColor(QColor(color_hex), style_id)
        current_editor: Editor = cast(Editor, self._editors_layout.currentWidget())
        current_editor.setLexer(lexer)


class SvgButton(QPushButton):
    """
    Button that displays an SVG image.

    This class mostly exists to encapsulate the extra complexity required to load an SVG
    from memory instead of a file.
    """

    def __init__(self, svg_data: bytes) -> None:
        super().__init__()
        svg_widget = QSvgWidget()
        renderer = svg_widget.renderer()
        renderer.load(svg_data)  # type: ignore (idk why pylance doesn't like this)
        renderer.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(svg_widget)
        self.setLayout(layout)
