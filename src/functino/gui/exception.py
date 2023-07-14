from PyQt6.QtWidgets import QMessageBox


def pop_up_error_message(e: Exception | str) -> None:
    """Show an error message pop up with the given error shown."""
    message_box = QMessageBox()
    message_box.setText(f"Oops! An error has occurred. Details below:\n\n{e}")
    message_box.exec()
