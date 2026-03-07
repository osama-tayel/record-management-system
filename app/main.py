"""Entry point for the Record Management System application."""

from app.gui.app_window import AppWindow


def main() -> None:
    """Launch the application."""

    app = AppWindow()
    app.run()


if __name__ == "__main__":
    main()
