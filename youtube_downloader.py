from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QTabWidget,
    QTabBar,
    QLineEdit,
    QSizePolicy,
    QMessageBox,
    QComboBox,
    QProgressBar,
    QDesktopWidget,
    QStyledItemDelegate,
    QToolButton,
    QMenu,
    QAction
)
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QPainter, QLinearGradient, QPen
from PyQt5.QtCore import (Qt, QThread, QStandardPaths, pyqtSignal, QMutex, QWaitCondition, QRect, QPropertyAnimation, QSequentialAnimationGroup, 
                         QEasingCurve, QPoint, QTimer, QSize)
import yt_dlp
from yt_dlp import YoutubeDL
import os
from PIL import Image
from time import sleep
import platform
import re
import sys

# For files in the SAME folder as the .exe:
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

resource_path("images/close b.png").replace("\\", "/")

class SplashScreen(QWidget):
    fade_out_sig = pyqtSignal()
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        icon_path = resource_path("images/Untitled-2.png").replace("\\", "/")
        self.setWindowIcon(self.create_high_res_icon(icon_path))
        self.setup_ui()
        self.setup_animations()
        self.center_on_screen()

    def create_high_res_icon(self, path):
        """Create an icon with multiple resolutions."""
        icon = QIcon()
        sizes = [16, 32, 48, 64, 96, 128, 256]
        for size in sizes:
            pixmap = QPixmap(path).scaled(
                QSize(size, size),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            icon.addPixmap(pixmap)
        return icon

    def center_on_screen(self):
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.4)
        height = int(screen.height() * 0.4)
        self.resize(min(width, 1000), min(height, 600))
        frame_geo = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(center_point)
        self.move(frame_geo.topLeft())

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(40, 40, 40))
        gradient.setColorAt(1, QColor(10, 10, 10))
        painter.fillRect(self.rect(), gradient)


        # Draw a white border around the screen
        border_pen = QPen(QColor(222, 222, 222))  # White color
        border_pen.setWidth(2)  # 2px border width
        painter.setPen(border_pen)
        painter.drawRect(self.rect())  # Draw a rectangle around the widget

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 0, 40, 50)
        main_layout.setSpacing(10)

        # Logo container with safe margins
        self.logo_container = QWidget()
        self.logo_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        logo_layout = QHBoxLayout(self.logo_container)
        logo_layout.setContentsMargins(40, 5, 40, 25)
        
        self.logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path("images/proffessional logo.png").replace("\\", "/"))
        logo_pixmap = logo_pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(logo_pixmap)
        logo_layout.addWidget(self.logo_label, 0, Qt.AlignCenter)
        main_layout.addWidget(self.logo_container)

        # Text label
        self.thank_label = QLabel("Thank You For Choosing Our Smart Applications")
        self.thank_label.setAlignment(Qt.AlignCenter)
        self.thank_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 26px;
                font-weight: 300;
                letter-spacing: 2px;
            }
        """)
        main_layout.addWidget(self.thank_label)

       # Button and arrow container
        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        btn_layout.setSpacing(15)  # Adjust spacing between button and arrow


        # Simple modern button
        self.start_btn = QPushButton("Start Downloading")
        self.start_btn.setCursor(Qt.PointingHandCursor)
        self.start_btn.setFixedSize(220, 50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #161616;
                color: #f0f0f0;
                font-size: 20px;
                margin: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #161616;
                color : #ffffff;
                font-weight: 600;
            }
            QPushButton:pressed {
                background-color: #161616;
            }
        """)
        self.start_btn.clicked.connect(self.fade_out)

        # Arrow label
        self.arrow_label = QLabel()
        arrow_pixmap = QPixmap(resource_path("images/icons8-right-arrow-100.png").replace("\\", "/"))  # Update path
        arrow_pixmap = arrow_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.arrow_label.setPixmap(arrow_pixmap)

        # Add the button and arrow to the layout
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.arrow_label)

        # Add a spacer to push the arrow to the right
         # Add a spacer to the right of the arrow to provide space for the animation
        btn_layout.addSpacing(20)  # Add 20px spacing for the arrow animation
        # btn_layout.addStretch()

        # Add the button container to the main layout
        main_layout.addWidget(btn_container, 0, Qt.AlignCenter)

    def setup_animations(self):
        # Logo animation (unchanged)
        self.float_anim = QSequentialAnimationGroup()
        anim_right = QPropertyAnimation(self.logo_container, b"pos")
        anim_right.setDuration(1500)
        anim_right.setEasingCurve(QEasingCurve.InOutQuad)
        anim_right.setStartValue(QPoint(0, 0))
        anim_right.setEndValue(QPoint(30, 40))
        anim_center = QPropertyAnimation(self.logo_container, b"pos")
        anim_center.setDuration(1500)
        anim_center.setEasingCurve(QEasingCurve.InOutQuad)
        anim_center.setStartValue(QPoint(30, 40))
        anim_center.setEndValue(QPoint(0, 0))
        self.float_anim.addAnimation(anim_right)
        self.float_anim.addAnimation(anim_center)
        self.float_anim.setLoopCount(-1)
        self.float_anim.start()

        # Arrow hover animation (updated)
        self.arrow_anim = QPropertyAnimation(self.arrow_label, b"pos")
        self.arrow_anim.setDuration(200)
        self.arrow_anim.setEasingCurve(QEasingCurve.OutQuad)

        # Use a QTimer to delay setting the initial position
        QTimer.singleShot(0, self.initialize_arrow_animation)


    def initialize_arrow_animation(self):
        # Store the initial position of the arrow_label after the layout is applied
        self.arrow_initial_pos = self.arrow_label.pos()

        # Set the start and end values relative to the initial position
        self.arrow_anim.setStartValue(self.arrow_initial_pos)
        self.arrow_anim.setEndValue(self.arrow_initial_pos + QPoint(10, 0))  # Move 10 pixels to the right

        # Connect hover events (updated)
        def start_arrow_animation():
            self.arrow_anim.setDirection(QPropertyAnimation.Forward)
            self.arrow_anim.start()

        def reverse_arrow_animation():
            self.arrow_anim.setDirection(QPropertyAnimation.Backward)
            self.arrow_anim.start()

        self.start_btn.enterEvent = lambda e: start_arrow_animation()
        self.start_btn.leaveEvent = lambda e: reverse_arrow_animation()


    def fade_out(self):
        print('fading away')
        self.float_anim.stop()
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(1000)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        # Change the finished connection to ensure proper order
        self.fade_anim.finished.connect(self._on_fade_finished)  # New method
        self.fade_anim.start()

    def _on_fade_finished(self):
        print("Fade finished, emitting signal")
        # Close and delete the splash before emitting the signal
        self.close()
        self.deleteLater()
        QApplication.processEvents()  # Ensure GUI updates
        self.fade_out_sig.emit()  # Emit signal after closing




class CustomMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid gray;
                color: black;
                border-radius: 0px;  /* Force no rounded corners */
            }
            QMenu::item {
                background-color: transparent;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #ff5c5c;
                color: white;
            }
        """)
class CustomLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

    def contextMenuEvent(self, event):
        # Create a custom menu
        menu = CustomMenu(self)

        # Add actions with proper functionality
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)
        cut_action = QAction("Cut", self)

        # Connect actions to the respective QLineEdit methods
        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        cut_action.triggered.connect(self.cut)

        menu.addAction(copy_action)
        menu.addAction(paste_action)
        menu.addAction(cut_action)

        # Show the menu at the cursor position
        menu.exec_(event.globalPos())



class ClearableLineEdit(CustomLineEdit):
    def __init__(self, parent=None):
        super(ClearableLineEdit, self).__init__(parent)
        
        # Create the clear button
        self.clear_button = QToolButton(self)
        # Set your custom icon (replace the path with your actual icon file)
        self.clear_button.setIcon(QIcon(resource_path("images/close b.png").replace("\\", "/")))

        self.clear_button.setToolTip("Clear text")
        # Change cursor to a pointing hand when hovering over the button
        self.clear_button.setCursor(Qt.PointingHandCursor)
        # Remove button borders and background so it blends with the QLineEdit
        self.clear_button.setStyleSheet("QToolButton { border: none; padding: 0px; background: transparent; }")
        self.clear_button.hide()  # Hide the button initially
        
        # Connect the button's clicked signal to the clear() slot
        self.clear_button.clicked.connect(self.clear)
        
        # Update button visibility whenever the text changes
        self.textChanged.connect(self.update_clear_button_visibility)
        
        # Adjust right padding of the QLineEdit so text doesn't overlap with the button.
        frameWidth = self.style().pixelMetric(self.style().PM_DefaultFrameWidth)
        buttonSize = self.clear_button.sizeHint()
        self.setStyleSheet("QLineEdit { padding-right: %dpx; }" % (buttonSize.width() + frameWidth + 2))
        
        # ✅ Fix: Ensure text stops before reaching the clear button
        self.setTextMargins(0, 0, buttonSize.width() + frameWidth + 5, 0)
    
    def resizeEvent(self, event):
        """Reposition the clear button when the QLineEdit is resized."""
        buttonSize = self.clear_button.sizeHint()
        frameWidth = self.style().pixelMetric(self.style().PM_DefaultFrameWidth)
        self.clear_button.move(self.rect().right() - frameWidth - buttonSize.width(),
                               (self.rect().bottom() - buttonSize.height() + 1) // 2)
        super(ClearableLineEdit, self).resizeEvent(event)
    
    def update_clear_button_visibility(self, text):
        """Show the clear button only when there is text."""
        self.clear_button.setVisible(bool(text))

class HiddenItemDelegate(QStyledItemDelegate):
    """ Hides the first item (index 0) from the dropdown menu. """
    def paint(self, painter, option, index):
        if index.row() == 0:
            return  # Do not paint (hide it)
        super().paint(painter, option, index)

    def sizeHint(self, option, index):
        if index.row() == 0:
            return QSize(0, 0)  # Hide the item by setting its size to 0
        return super().sizeHint(option, index)
# Default Downloads folder
def get_folder_in_downloads(folder_name):
    # Get the standard path for the Downloads folder
    downloads_folder = QStandardPaths.writableLocation(QStandardPaths.DownloadLocation)

    # Define the Music folder path inside Downloads
    download_folder = f"{downloads_folder}/{folder_name}"

    # Check if the folder exists; if not, create it
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    return download_folder


def is_valid_youtube_video(url):
    # Regular expressions for YouTube video & Shorts (not playlists)
    video_pattern = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    shorts_pattern = (
        r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})"
    )

    # Reject URLs containing 'list=' (indicating a playlist)
    if "list=" in url:
        return False

    # Check if it's a valid YouTube video or Shorts URL
    if re.match(video_pattern, url) or re.match(shorts_pattern, url):
        return True

    return False

def is_live_video(url):
    with yt_dlp.YoutubeDL() as ydl:
        info_dict = ydl.extract_info(url, download=False)
    # The 'is_live' key is typically present for live videos.
    return info_dict.get("is_live", False)

# Set recommended environment variables before importing PyQt
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

# Determine the correct path to ffmpeg.exe
if getattr(sys, "frozen", False):  # Check if running as a PyInstaller bundle
    ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
else:  # Running as a Python script
    ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg.exe")





# Set ffmpeg binary environment variable for yt-dlp or other libraries
os.environ["FFMPEG_BINARY"] = ffmpeg_path


def get_user_agent():
    os_name = platform.system()
    os_version = platform.version()
    architecture = platform.architecture()[0]

    if os_name == "Windows":
        user_agent = f"Mozilla/5.0 (Windows NT {os_version}; {architecture}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    elif os_name == "Linux":
        user_agent = f"Mozilla/5.0 (X11; Linux {architecture}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    elif os_name == "Darwin":  # macOS
        user_agent = f"Mozilla/5.0 (Macintosh; Intel Mac OS X {os_version}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    else:
        user_agent = "Mozilla/5.0 (compatible; yt-dlp/2025.01.13; +https://github.com/yt-dlp/yt-dlp)"

    return user_agent


def show_message(
    message_type="",
    title="",
    message="",
    file_existence_status="",
    video_title="",
    parent="",
    file_type="video",
):
    if not file_existence_status:
        msg = QMessageBox(parent)
        msg.setWindowTitle(title)
        msg.setText(message)

        # Remove the default title bar
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        # Set message box style based on the type
        if message_type == "warning":
            border_color = "#F44336"
            msg.setIcon(QMessageBox.Warning)
        elif message_type == "information":
            border_color = "#4CAF50"
            msg.setIcon(QMessageBox.Information)

        # Apply modern styling with enhanced border
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: #fff;
                border: 3px solid {border_color};  /* Blue border to make it more visible */
                border-radius: 8px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333;
            }}
            QLabel {{
                color: #444;
            }}
            QPushButton {{
                background: #ff5c5c;
                color: black;
                border: none;
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: black;
                color: white;
            }}
            QPushButton:pressed {{
                background-color: #bf360c;
            }}
        """)

        # Set the message box position relative to the main window
        if parent:
            # Get the geometry of the main window
            main_geometry = parent.geometry()
            x = (
                main_geometry.x()
                + main_geometry.width() // 2
                - msg.sizeHint().width() // 2
            )
            y = (
                main_geometry.y()
                + main_geometry.height() // 2
                - msg.sizeHint().height() // 2
            )
            msg.move(x, y)

        msg.exec_()

        return None
    else:
        # Show a QMessageBox to ask the user
        msg = QMessageBox(parent)
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("File Exists")
        if file_type == "video":
            msg.setText(f"The file '{video_title}.mp4' already exists.")
        else:
            msg.setText(f"The file '{video_title}.mp3' already exists.")
        msg.setInformativeText(
            "Do you want to Replace it or download it with a different name?"
        )

        # Remove the default title bar
        msg.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)

        # Apply styling for the QMessageBox with a more visible border
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #fff;
                border: 3px solid #FF9800;  
                border-radius: 3px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 14px;
                color: #333;
                margin: 0px;  /* Remove any padding/margin around the message box */
            }
            QLabel {
                color: #444;
            }
            QPushButton {
                background: #ff5c5c;
                color: black;
                border: none;
                border-radius: 10px;
                padding: 8px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background: black;
                color: white;
            }
            QPushButton:pressed {
                background-color: #bf360c;
            }
        """)

        # Add custom buttons for user interaction
        overwrite_button = msg.addButton("Replace", QMessageBox.YesRole)
        rename_button = msg.addButton("Download and Rename", QMessageBox.NoRole)
        cancel_button = msg.addButton("Cancel", QMessageBox.RejectRole)

        # Function to center the QMessageBox
        # Centering the QMessageBox
        # Centering on the screen
        screen_geometry = QDesktopWidget().availableGeometry().center()
        msg_rect = msg.sizeHint()
        x = screen_geometry.x() - (msg_rect.width() // 2)
        y = screen_geometry.y() - (msg_rect.height() // 2)

        # Ensure the QMessageBox is centered after layout
        msg.exec_()  # Show the QMessageBox

        # Return the clicked button's response
        if msg.clickedButton() == overwrite_button:
            return "replace"
        elif msg.clickedButton() == rename_button:
            return "rename"
        elif msg.clickedButton() == cancel_button:
            return "cancel"


# Modified Worker Class
class Worker(QThread):
    finished = pyqtSignal(str, str)  # (title, image_path)
    error = pyqtSignal(str)
    valid_url = pyqtSignal()
    resolutions_fetched = pyqtSignal(list)  # New signal for resolutions
    live_url= pyqtSignal()

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.available_resolutions = None  # Store resolutions here

    def run(self):
        try:
            if not is_valid_youtube_video(self.url):
                pattern = r"^(https://www\.youtube\.com/watch\?v=[^&]+)"

                match = re.search(pattern, self.url)
                # get first video url when its play list 
                if match:
                    self.url = match.group(1)
                    global video_url_variable, convert_video_url_variable
                    video_url_variable = self.url
                    convert_video_url_variable = self.url
                else:
                    self.valid_url.emit()

            if is_live_video(self.url):
                self.live_url.emit()
                return
            os.chdir(get_folder_in_downloads("Video"))
            
            # Fetch main data
            title, image_path = self.fetch_url_data(self.url)
            
            # Fetch resolutions in the same thread
            self.available_resolutions = self.fetch_available_resolutions(self.url)
            
            # Emit signals
            self.finished.emit(title, image_path)
            if self.available_resolutions and str(self.url).startswith("https://www.youtube.com/watch"):
                self.resolutions_fetched.emit(self.available_resolutions)
                
        except Exception as e:
            self.error.emit(str(e))

    def fetch_url_data(self, video_url):
        """
        Downloads the thumbnail of a YouTube video using yt-dlp, converts it to .jpg format,
        and returns the video title and the name of the downloaded image.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            tuple: A tuple containing the video title and the thumbnail file name.
        """
        ydl_opts = {
            "ffmpeg_location": ffmpeg_path,
            "quiet": True,
            "skip_download": True,  # Do not download the video
            "writethumbnail": True,  # Download the thumbnail
            "outtmpl": "%(title)s_thumbnail.%(ext)s",  # Output template for the thumbnail
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info and download thumbnail
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get("title", "Unknown Title")

            # Find the actual downloaded thumbnail file
            for file in os.listdir("."):
                if file.endswith("_thumbnail.webp"):
                    thumbnail_file_name_webp = file
                    break
            else:
                raise FileNotFoundError("Thumbnail file in .webp format was not found.")

            # Convert .webp to .jpg using Pillow
            thumbnail_file_name_jpg = (
                f"{os.path.splitext(thumbnail_file_name_webp)[0]}.jpg"
            )
            with Image.open(thumbnail_file_name_webp) as img:
                img.convert("RGB").save(thumbnail_file_name_jpg, "JPEG")
            os.remove(thumbnail_file_name_webp)  # Clean up the .webp file

        return video_title, thumbnail_file_name_jpg
    

    def fetch_available_resolutions(self, url):
        """Same logic as your original fetch_available_resolutions moved here"""
        if str(url).startswith("https://www.youtube.com/watch"):
            with yt_dlp.YoutubeDL() as ydl:
                info_dict = ydl.extract_info(url, download=False)
                formats = info_dict.get("formats", [])

            available_resolutions = [
                f["height"]
                for f in formats
                if "height" in f and f["height"] is not None
            ]
            available_resolutions = sorted(set(available_resolutions), reverse=True)

            video_duration = info_dict.get("duration", 0)
            if video_duration > 6000:
                available_resolutions = [
                    res for res in available_resolutions if res <= 720
                ]

            return [
                str(res) + 'P'
                for res in available_resolutions
                if res >= 144 and res != 180
            ]
        return None







class DownloadVideoWorker(QThread):
    progress_update = pyqtSignal(int, str)  # (percentage, message)
    finished = pyqtSignal()
    error = pyqtSignal(str)
    success = pyqtSignal(str)
    file_conflict = pyqtSignal(str, str)
    cancelled = pyqtSignal()  # Signal emitted when cancellation occurs

    def __init__(self, main_window, url, res_idx, path, resolution_text):
        super().__init__()
        self.main_window = main_window
        self.url = url
        self.res_idx = res_idx
        self.path = path
        self.resolution_text = resolution_text
        self.user_choice = None
        self.total_phases = 3
        self.current_phase = 0
        self.last_download_phase = None
        self.post_processing_started = False
        self.current_phase_max_percent = 0.0

        # For storing progress values and messages.
        self.last_progress = 0
        self.last_message = ""
        self.pre_pause_message = ""
        self.output_file_prefix = None  # used for cleanup if cancelled

        # Flags.
        self.processing_phase = False
        self._cancelled = False

        # Pause/Resume controls.
        self.pause_mutex = QMutex()
        self.pause_condition = QWaitCondition()
        self.paused = False

    def run(self):
        try:
            # Reset state.
            self.current_phase = 0
            self.last_download_phase = None
            self.current_phase_max_percent = 0.0
            self.post_processing_started = False
            self.processing_phase = False
            self.progress_update.emit(0, "Preparing download...")
            print(f"index: {self.res_idx}, resolution: {self.resolution_text}")

            def download_yt_video():
                # Extract video info.
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info_dict = ydl.extract_info(self.url, download=False)
                    formats = info_dict.get('formats', [])
                    video_title = str(info_dict.get('title', 'video'))

                # Resolution handling.
                available_resolutions = [
                    f['height'] for f in formats if 'height' in f and f['height'] is not None
                ]
                available_resolutions = sorted(set(available_resolutions), reverse=True)
                available_resolutions = [res for res in available_resolutions if res >= 144 and res != 180]
                if info_dict.get('duration', 0) > 6000:
                    available_resolutions = [res for res in available_resolutions if res <= 720]
                chosen_resolution = available_resolutions[self.res_idx]
                print(f"Index: {self.res_idx}, Resolution: {chosen_resolution}")

                # File handling.
                os.chdir(self.path)
                # Replace illegal filename characters.
                video_title = ''.join([c if c not in '<>:"/\\|?*' else '#' for c in video_title])
                output_file = video_title.split('.mp4')[0] if '.mp4' in video_title else video_title
                self.output_file_prefix = output_file  # store prefix for later cleanup

                if self._cancelled:
                    raise Exception("Download cancelled by user.")

                if any(f.startswith(video_title) for f in os.listdir()):
                    # --- New Behavior: Wait if paused before showing file conflict ---
                    while self.paused:
                        if self._cancelled:
                            raise Exception("Download cancelled by user.")
                        sleep(0.1)
                    self.file_conflict.emit(video_title, "video")
                    while self.user_choice is None:
                        if self._cancelled:
                            raise Exception("Download cancelled by user.")
                        sleep(0.1)
                    if self.user_choice == "replace":
                        output_file = f"{output_file}"
                        print(f"Overwriting file with name: {output_file}")
                    elif self.user_choice == "rename":
                        print("User chose to rename the file.")
                        all_files = os.listdir()
                        matching_files = [f for f in all_files if f.startswith(output_file) and f.endswith(".mp4")]
                        max_counter = 0
                        for file in matching_files:
                            if file == f"{output_file}.mp4":
                                continue
                            try:
                                counter = int(file[len(output_file) + 2 : file.rfind(')')])
                                max_counter = max(max_counter, counter)
                            except ValueError:
                                pass
                        new_counter = max_counter + 1
                        output_file = f"{output_file} ({new_counter})"
                        print(f"Renamed file to: {output_file}")
                    elif self.user_choice == "cancel":
                        return "C"
                    else:
                        print("No valid option selected.")
                        return

                print(f"Downloading to: {output_file}")

                class MyLogger:
                    def __init__(self, worker):
                        self.worker = worker

                    def debug(self, msg):
                        # Immediately abort if cancelled.
                        if self.worker._cancelled:
                            raise Exception("Download cancelled by user.")
                            
                        # Handle only valid percentage messages.
                        if "Downloading" in msg and "%" in msg:
                            try:
                                match = re.search(r"(\d+\.?\d*)%", msg)
                                if match:
                                    percent = float(match.group(1))
                                    overall = int(
                                        ((self.worker.current_phase - 1) / self.worker.total_phases * 100)
                                        + (percent / self.worker.total_phases)
                                    )
                                    # Update last_progress and last_message
                                    self.worker.last_progress = overall
                                    self.worker.last_message = f"Downloading {self.worker.current_phase}/{self.worker.total_phases - 1}: {percent:.1f}%"
                                    
                                    self.worker.progress_update.emit(
                                        overall,
                                        self.worker.last_message,
                                    )
                            except Exception:
                                pass

                        elif "[Merger]" in msg:
                            self.worker.last_message = "Converting video..."
                            self.worker.progress_update.emit(75, self.worker.last_message)
                        elif "[VideoConvertor]" in msg:
                            self.worker.last_message = "Finalizing video..."
                            self.worker.progress_update.emit(90, self.worker.last_message)

                    def warning(self, msg):
                        pass

                    def error(self, msg):
                        self.worker.progress_update.emit(0, f"Error: {msg}")

                def progress_hook(d):
                    # When the status is "downloading", add pause/resume/cancel logic.
                    if d["status"] == "downloading":
                        # --- Pause/Resume/Cancel Logic (only during downloading) ---
                        self.pause_mutex.lock()
                        if not self.processing_phase:
                            while self.paused:
                                if self._cancelled:
                                    self.pause_mutex.unlock()
                                    raise Exception("Download cancelled by user.")
                                # Emit the paused status so the UI shows it.
                                self.progress_update.emit(self.last_progress, self.pre_pause_message + " (Paused)")
                                self.pause_condition.wait(self.pause_mutex)
                        self.pause_mutex.unlock()

                        # --- Download Progress Calculation ---
                        try:
                            percent = float(d.get("_percent_str", "0%").strip("%").strip())
                        except:
                            percent = 0

                        # Fallback calculation if percentage not available.
                        if percent == 0:
                            downloaded = d.get("downloaded_bytes", 0)
                            total = d.get("total_bytes") or d.get("total_bytes_estimate", 1)
                            if total > 0:
                                percent = min((downloaded / total) * 100, 100)  # Cap at 100%

                        # Phase tracking: update phase if the format changes.
                        if d["info_dict"]["format_id"] != self.last_download_phase:
                            self.current_phase += 1
                            self.last_download_phase = d["info_dict"]["format_id"]
                            self.current_phase_max_percent = 0.0

                        # Update max percent for the current phase.
                        if percent > self.current_phase_max_percent:
                            self.current_phase_max_percent = percent

                    # --- Overall Progress Calculation (runs regardless of status) ---
                    overall = int(
                        ((self.current_phase - 1) / self.total_phases * 100)
                        + (self.current_phase_max_percent / self.total_phases)
                    )
                    overall = max(0, min(100, overall))

                    # Update last_progress and last_message.
                    self.last_progress = overall
                    msg = f"Downloading {self.current_phase}/{self.total_phases - 1}: {self.current_phase_max_percent:.1f}%"
                    self.last_message = msg

                    self.progress_update.emit(overall, msg)

                ydl_opts = {
                    'ffmpeg_location': ffmpeg_path,
                    'format': (f"bestaudio+bestvideo[height={chosen_resolution}]"
                               if str(self.url).startswith("https://www.youtube.com/watch")
                               else f"bestvideo+bestaudio/best"),
                    'postprocessors': [{
                        'key': 'FFmpegVideoConvertor',
                        'preferedformat': 'mp4',
                    }],
                    'postprocessor_args': [
                        '-preset', 'ultrafast',
                        '-fs', '4294967295'
                    ],
                    'outtmpl': f'{output_file}.%(ext)s',
                    'progress_hooks': [progress_hook],
                    'logger': MyLogger(self),
                    'verbose': True,
                    'buffer-size': 1024 * 1024 * 100,
                    'User-Agent': get_user_agent(),
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])

                if not self._cancelled:
                    self.progress_update.emit(100, "Download complete!")
                    sleep(1)

            ret = download_yt_video()
            if ret == "C":
                self.error.emit("Download cancelled by user.")
            elif self._cancelled:
                self.cleanup_download()
                self.cancelled.emit()
            else:
                self.success.emit(self.resolution_text)
            self.finished.emit()

        except Exception as e:
            if self._cancelled:
                self.cleanup_download()
                self.cancelled.emit()
            else:
                self.cleanup_download()
                self.error.emit(f"Download failed: {str(e)}")
                print(str(e))

    def set_user_choice(self, choice):
        self.user_choice = choice

    def pause(self):
        # Only allow pause if not in processing phase.
        if self.processing_phase:
            return
        self.pause_mutex.lock()
        self.paused = True
        self.pause_mutex.unlock()
        self.pre_pause_message = self.last_message
        self.progress_update.emit(self.last_progress, self.pre_pause_message + " (Paused)")

    def resume(self):
        # Only allow resume if not in processing phase.
        if self.processing_phase:
            return
        self.pause_mutex.lock()
        self.paused = False
        self.pause_condition.wakeAll()
        self.pause_mutex.unlock()
        self.progress_update.emit(self.last_progress, self.pre_pause_message)

    def cancel(self):
        self.pause_mutex.lock()
        # Allow cancellation at any phase by setting the flag.
        self._cancelled = True
        self.paused = False  # ensure we exit any paused state.
        self.pause_condition.wakeAll()
        self.pause_mutex.unlock()
        self.progress_update.emit(self.last_progress, self.last_message + " (Cancelled)")

    def cleanup_download(self):
        if self.output_file_prefix:
            for f in os.listdir():
                # Remove only unfinished files while keeping completed ones.
                if f.startswith(self.output_file_prefix) and (
                    f.endswith(".part") or f.endswith(".ytdl") or f.endswith(".f*") or f.endswith(".webm") or f.endswith('.mp4.part')
                ):
                    try:
                        os.remove(f)
                        print(f"Removed unfinished file: {f}")
                    except Exception as e:
                        print(f"Failed to remove file {f}: {e}")







class DownloadAudioWorker(QThread):
    progress_update = pyqtSignal(int, str)  # (percentage, message)
    finished = pyqtSignal()
    success = pyqtSignal()
    error = pyqtSignal(str)
    file_conflict = pyqtSignal(str, str)
    cancelled = pyqtSignal()  # Emitted when cancellation occurs

    def __init__(self, main_window, url, path):
        super().__init__()
        self.main_window = main_window
        self.url = url
        self.path = path
        self.user_choice = None
        self.total_phases = 3
        self.current_phase = 0
        self.last_download_phase = None
        self.post_processing_started = False
        self.current_phase_max_percent = 0.0

        # For storing the last progress value and message.
        self.last_progress = 0
        self.last_message = ""
        self.pre_pause_message = ""
        self.output_file_prefix = None  # Used for cleanup if cancelled

        # Flag to indicate we are in the ffmpeg processing phase.
        self.processing_phase = False
        self._cancelled = False

        # Pause/Resume controls.
        self.pause_mutex = QMutex()
        self.pause_condition = QWaitCondition()
        self.paused = False

    def run(self):
        try:
            # Reset progress state at start.
            self.current_phase = 0
            self.last_download_phase = None
            self.current_phase_max_percent = 0.0
            self.post_processing_started = False
            self.processing_phase = False
            self.progress_update.emit(0, "Preparing download...")

            def download_yt_Audio():
                # Extract audio info (without downloading).
                if self._cancelled:
                    raise Exception("Download cancelled by user.")
                with YoutubeDL() as ydl:
                    info_dict = ydl.extract_info(self.url, download=False)
                    formats = info_dict.get("formats", [])
                    audio_title = str(info_dict.get("title", "audio"))

                # File handling: sanitize title and set output file name.
                os.chdir(self.path)
                audio_title = "".join([c if c not in '<>:"/\\|?*' else "#" for c in audio_title])
                output_file = audio_title.split(".mp3")[0] if ".mp3" in audio_title else audio_title
                self.output_file_prefix = output_file
                if self._cancelled:
                    raise Exception("Download cancelled by user.")
                if any(f for f in os.listdir() if output_file in f):
                    self.file_conflict.emit(audio_title, "audio")
                    while self.user_choice is None:
                        sleep(0.1)
                    if self.user_choice == "replace":
                        base_name = audio_title.split(".mp3")[0] if audio_title.endswith(".mp3") else audio_title
                        output_file = f"{base_name}"
                    elif self.user_choice == "rename":
                        all_files = os.listdir()
                        base_name = audio_title.split(".mp3")[0] if audio_title.endswith(".mp3") else audio_title
                        print(f"base_name :{base_name}")
                        matching_files = [f for f in all_files if f.startswith(audio_title) and f.endswith(".mp3")]
                        max_counter = 0
                        for file in matching_files:
                            if file == f"{base_name}.mp3":
                                continue  # Skip the original name.
                            try:
                                counter = int(file[len(base_name) + 2 : file.rfind(")")])
                                max_counter = max(max_counter, counter)
                            except ValueError:
                                pass
                        new_counter = max_counter + 1
                        output_file = f"{base_name} ({new_counter})"
                    elif self.user_choice == "cancel":
                        return "C"
                    else:
                        print("No valid option selected.")
                        return

                print(f"Downloading to: {output_file}")

                class MyLogger:
                    def __init__(self, worker):
                        self.worker = worker

                    def debug(self, msg):
                        if "Downloading" in msg and "%" in msg:
                            if self.worker._cancelled:
                                raise Exception("Download cancelled by user.")
                            try:
                                match = re.search(r'(\d+\.?\d*)%', msg)
                                if match:
                                    percent = float(match.group(1))
                                    overall = int(
                                        ((self.worker.current_phase - 1) / self.worker.total_phases * 100) +
                                        (percent / self.worker.total_phases)
                                    )
                                    self.worker.last_progress = overall
                                    m = f"Downloading {self.worker.current_phase}/{self.worker.total_phases-1}: {percent:.1f}%"
                                    self.worker.last_message = m
                                    self.worker.progress_update.emit(overall, m)
                            except Exception as e:
                                pass
                        elif "[ExtractAudio]" in msg:
                            if self.worker._cancelled:
                                raise Exception("Download cancelled by user.")
                            self.worker.processing_phase = True
                            self.worker.last_message = "Extracting Audio...."
                            self.worker.progress_update.emit(90, "Extracting Audio.... Please Wait!")
                        elif "[Merger]" in msg:
                            if self.worker._cancelled:
                                raise Exception("Download cancelled by user.")
                            self.worker.processing_phase = True
                            self.worker.last_message = "Merging audio... Please wait."
                            self.worker.progress_update.emit(75, "Merging audio... Please wait.")
                        elif "[AudioConvertor]" in msg:
                            if self.worker._cancelled:
                                raise Exception("Download cancelled by user.")
                            self.worker.processing_phase = True
                            self.worker.last_message = "Finalizing audio..."
                            self.worker.progress_update.emit(95, "Finalizing audio...Please wait it might take a time!")

                    def warning(self, msg):
                        pass

                    def error(self, msg):
                        self.worker.progress_update.emit(0, f"Error: {msg}")

                def progress_hook(d):
                    # Check for cancellation.
                    if self._cancelled:
                        raise Exception("Download cancelled by user.")

                    # Allow pausing only in the download phase.
                    self.pause_mutex.lock()
                    if not self.processing_phase:
                        while self.paused:
                            if self._cancelled:
                                self.pause_mutex.unlock()
                                raise Exception("Download cancelled by user.")
                            self.pause_condition.wait(self.pause_mutex)
                    self.pause_mutex.unlock()

                    if d['status'] == 'downloading':
                        if self._cancelled:
                                raise Exception("Download cancelled by user.")
                        try:
                            percent = float(d.get('_percent_str', '0%').strip('%').strip())
                        except:
                            percent = 0
                        if percent == 0:
                            downloaded = d.get('downloaded_bytes', 0)
                            total = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
                            if total > 0:
                                percent = min((downloaded / total) * 100, 100)
                        if d['info_dict']['format_id'] != self.last_download_phase:
                            self.current_phase += 1
                            self.last_download_phase = d['info_dict']['format_id']
                            self.current_phase_max_percent = 0.0
                        if percent > self.current_phase_max_percent:
                            self.current_phase_max_percent = percent
                    overall = int(
                        ((self.current_phase - 1) / self.total_phases * 100) +
                        (self.current_phase_max_percent / self.total_phases)
                    )
                    overall = max(0, min(100, overall))
                    self.last_progress = overall
                    m = f"Downloading: {self.current_phase_max_percent:.1f}%"
                    self.last_message = m
                    self.progress_update.emit(overall, m)

                ydl_opts = {
                    "ffmpeg_location": ffmpeg_path,
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                        }
                    ],
                    "postprocessor_args": [
                        "-preset", "ultrafast",
                        "-fs", "4294967295",
                    ],
                    "outtmpl": f"{output_file}",
                    "progress_hooks": [progress_hook],
                    "logger": MyLogger(self),
                    "verbose": True,
                    "buffer-size": 1024 * 1024 * 100,
                    "User-Agent": get_user_agent(),
                }

                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([self.url])

                if not self._cancelled:
                    self.progress_update.emit(100, "Download complete!")
                    sleep(1)

            ret = download_yt_Audio()
            if ret == "C":
                self.error.emit("Download cancelled by user.")
            elif self._cancelled:
                self.cleanup_download()
                self.cancelled.emit()
            else:
                self.success.emit()
            self.finished.emit()

        except Exception as e:
            if self._cancelled:
                self.cleanup_download()
                self.cancelled.emit()
            else:
                self.error.emit(f"Download failed: {str(e)}")

    def set_user_choice(self, choice):
        self.user_choice = choice

    # Pause/resume only affect the download phase.
    def pause(self):
        if self.processing_phase:
            return
        self.pause_mutex.lock()
        self.paused = True
        self.pause_mutex.unlock()
        self.pre_pause_message = self.last_message
        self.progress_update.emit(self.last_progress, self.pre_pause_message + " (Paused)")

    def resume(self):
        if self.processing_phase:
            return
        self.pause_mutex.lock()
        self.paused = False
        self.pause_condition.wakeAll()
        self.pause_mutex.unlock()
        self.progress_update.emit(self.last_progress, self.pre_pause_message)

    # Cancel the download at any time.
    def cancel(self):
        self.pause_mutex.lock()
        # Allow cancellation at any phase by setting the flag
        self._cancelled = True
        self.paused = False  # ensure we exit any paused state
        self.pause_condition.wakeAll()
        self.pause_mutex.unlock()
        self.progress_update.emit(self.last_progress, self.last_message + " (Cancelled)")

    # Clean up any partially downloaded file(s) based on output_file_prefix.
    def cleanup_download(self):
        if self.output_file_prefix:
            for f in os.listdir():
                if f.startswith(self.output_file_prefix) and f.endswith(".part"):
                    try:
                        os.remove(f)
                        print(f"Removed unfinished file: {f}")
                    except Exception as e:
                        print(f"Failed to remove file {f}: {e}")



class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Video Downloader")

        # Set frameless and rounded edges
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

        # Set the window icon (for taskbar)
        self.setWindowIcon(QIcon(resource_path("images/Untitled-2.ico")))

        # Window size configuration
        self.set_proper_size()
        self.center_window()
        self.oldPos = None

        # Initialize UI before showing
        self.initUI()
        

        self.splash = SplashScreen(None)  # Changed from None to self
        QApplication.instance().setQuitOnLastWindowClosed(False)  # Add this line
        self.splash.fade_out_sig.connect(self._handle_splash_fade)
        self.splash.show()

    def _handle_splash_fade(self):
        QApplication.instance().setQuitOnLastWindowClosed(True)  # Restore default behavior
        self.show()  # Show the main window
        self.activateWindow()  # Steal focus
        self.raise_()  # Bring to front

    def mousePressEvent(self, event):
        # Map the combo box's rectangle to global coordinates
        combo_rect = self.resolution_combo.rect()
        global_top_left = self.resolution_combo.mapToGlobal(combo_rect.topLeft())
        global_bottom_right = self.resolution_combo.mapToGlobal(combo_rect.bottomRight())
        combo_global_rect = QRect(global_top_left, global_bottom_right)
        
        # If the click is within the combo box's area, do not initiate dragging.
        if combo_global_rect.contains(event.globalPos()):
            super().mousePressEvent(event)
            return
        
        # Otherwise, store the position for dragging.
        self.oldPos = event.globalPos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            # Calculate the distance moved.
            delta = event.globalPos() - self.oldPos
            # Move the window by that amount.
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Reset the dragging variable.
        self.oldPos = None
        super().mouseReleaseEvent(event)

    def center_window(self):
        # Center window on screen
        frame_geo = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geo.moveCenter(center_point)
        self.move(frame_geo.topLeft())

    def set_proper_size(self):
        # Set base size but allow resizing
        screen = QDesktopWidget().screenGeometry()
        
        # Use 80% of screen width/height or 900x600 whichever is smaller
        width = min(int(screen.width() * 0.8), 900)
        height = min(int(screen.height() * 0.8), 600)
        
        self.resize(width, height)
        
        # Set size constraints (optional)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(1200, 800)

    def handle_worker_message(self, msg_type, title, message):
        # Use self as parent since we're in main thread
        show_message(
            message_type=msg_type,
            title=title,
            message=message,
            parent=self,  # This is the key part
        )

    def handle_file_conflict(self, video_title, file_type):
        # Show dialog using main window as parent
        choice = show_message(
            file_existence_status=True,
            video_title=video_title,
            file_type=file_type,
            parent=self,
        )
        # Send choice back to worker
        self.download_worker.set_user_choice(choice)

    def initUI(self):
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        window_geometry = self.geometry()

        # Calculate the position to center the window
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        # Move the window to the calculated position
        self.move(x, y)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Custom Title Bar
        title_bar = QHBoxLayout()
        title_bar.setContentsMargins(2, 2, 2, 2)
        # Minimize Button
        minimize_button = QPushButton()
        minimize_button.setFixedSize(30, 30)
        minimize_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: 5px;
                padding: 5px;
                icon : url({resource_path("images/mini b.png").replace("\\", "/")})
            }}
            QPushButton:hover {{
                background-color: #989898; /* Light blue background */
                icon : url({resource_path("images/mini w.png").replace("\\", "/")});
            }}
        """)
        minimize_button.clicked.connect(self.showMinimized)

        # Close Button
        close_button = QPushButton()
        close_button.setFixedSize(30, 30)
        close_button.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border-radius: 5px;
                padding: 5px;
                icon : url({resource_path("images/close b.png").replace("\\", "/")})
            }}
            QPushButton:hover {{
                background-color: #f23f43; /* Light blue background */
                icon : url({resource_path("images/close w.png").replace("\\", "/")});

            }}
        """)
        close_button.clicked.connect(self.close)

        # Add widgets to title bar
        title_bar.addStretch(1)
        title_bar.addWidget(minimize_button)
        title_bar.addWidget(close_button)

        # Main Content
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Create center widget with layout for logo and title
        center_widget = QWidget()
        center_layout = QHBoxLayout()
        center_widget.setLayout(center_layout)

        # Logo
        logo = QLabel()
        logo.setPixmap(
            QPixmap(resource_path("images/Untitled-2.png")).scaled(
                60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        logo.setStyleSheet("margin: 0px; padding: 0px;")
        logo.setAlignment(Qt.AlignCenter)

        # Title Label
        content_title = QLabel("Youtube Downloader")
        content_title.setFont(QFont("Arial", 25, QFont.Bold))
        content_title.setStyleSheet("""
            QLabel {
                color: black; 
                background: transparent; 
                margin: 0px; 
                padding: 0px;
                border: none; 
            }
        """)
        content_title.setAlignment(Qt.AlignCenter)

        # Add Logo and Title to Horizontal Layout
        center_layout.addWidget(logo)
        center_layout.addWidget(content_title)
        center_layout.setAlignment(Qt.AlignCenter)

        # Tab Widget
        tab_widget = QTabWidget(self)
        # tab_widget.setTabBarAutoHide(True)  # Hide the default tab bar
        tab_widget.tabBar().hide()

        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none; /* Remove the border around the pane */
                border-radius: 12;
            }
        """)
        # Custom Tab Bar
        custom_tab_bar = QTabBar()
        custom_tab_bar.setDrawBase(False)
        custom_tab_bar.setExpanding(False)

        # Style the custom tab bar
        custom_tab_bar.setStyleSheet("""
            QTabBar::tab {
                background: rgba(255, 255, 255, 0.2);  /* Black background for the tabs */
                border: 2px solid #ccc;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                color: black;  /* White text color */
                min-width: 130px;
                text-align: center;
                margin: 0px 8px;
            }
            QTabBar::tab:selected {
                background: black;  /* Semi-transparent background when selected */
                border: 2px solid #f23f43;  /* Red border on selected tab */
                color: white;  /* White text color on selected */
            }
            QTabBar::tab:hover {
                background: rgba(169, 169, 169, 0.5);  /* Grey background on hover */
                color: black;  /* Black text color on hover */
            }
        """)

        # Connect the custom tab bar
        custom_tab_bar.currentChanged.connect(tab_widget.setCurrentIndex)
        tab_widget.currentChanged.connect(custom_tab_bar.setCurrentIndex)

        # First Tab: Download
        download_tab = QWidget()
        download_layout = QVBoxLayout(download_tab)

        # Add horizontal layout for image and text (initially hidden)
        result_layout = QHBoxLayout()

        # Image placeholder
        result_image = QLabel()
        result_image.setFixedSize(150, 90)  # Adjust size as needed
        result_image.setStyleSheet("background-color: transparent;")
        result_image.setAlignment(Qt.AlignCenter)

        # Text placeholder
        result_text = QLabel()
        result_text.setFont(QFont("Arial", 12, QFont.Bold))
        result_text.setStyleSheet("color: black; background-color: transparent;")
        result_text.setAlignment(Qt.AlignCenter)

        # Add image and text to the result layout
        result_layout.addSpacing(60)  # Add spacing on the left
        result_layout.addWidget(result_image)
        result_layout.addWidget(result_text)
        result_layout.addStretch()  # Add spacing on the right
        result_layout.setContentsMargins(20, 20, 20, 20)

        # Widget to manage the result layout (initially hidden)
        result_layout_widget = QWidget()
        result_layout_widget.setLayout(result_layout)
        result_layout_widget.setVisible(False)  # Hide the widget initially

        # Add title label
        title_label = QLabel("Enter URL & Download Location")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        title_label.setStyleSheet(
            "color: black;background-color: transparent;"
        )  # Add bottom padding for spacing
        download_layout.addWidget(title_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Add horizontal layout for input field and search button
        url_input_layout = QHBoxLayout()

        # URL input field
        url_input = ClearableLineEdit(self)
        url_input.setPlaceholderText("Enter video URL...")
        url_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #5b9bd5;
            }
        """)
        
        url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        url_input_layout.addSpacing(60)
        url_input_layout.addWidget(url_input)

        # Search Button
        search_button = QPushButton("Search")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        search_button.setFixedWidth(100)  # Set a fixed width for the button
        
        url_input_layout.addWidget(search_button)
        url_input_layout.addSpacing(60)

        # Add the horizontal layout to the vertical layout
        download_layout.addLayout(url_input_layout)
        # Add result layout or stretch based on condition
        download_layout.addWidget(result_layout_widget)  # Initially hidden

        download_layout.addStretch()  # Add stretch to replace result_layout when hidden

        # Add horizontal layout for Download Location input field and Browse button
        location_input_layout = QHBoxLayout()

        # Download Location input field
        location_input = CustomLineEdit(self)
        location_input.setPlaceholderText("Enter Download Location...")
        location_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #5b9bd5;
            }
        """)
        location_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        location_input_layout.addSpacing(60)
        location_input_layout.addWidget(location_input)

        # Browse Button
        browse_button = QPushButton("Browse")
        browse_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
        """)
        browse_button.setFixedWidth(100)  # Set a fixed width for the button
        location_input_layout.addWidget(browse_button)
        location_input_layout.addSpacing(60)

        # Add the horizontal layout to the vertical layout
        download_layout.addLayout(location_input_layout)

        # Create horizontal layout for Download button and Resolution dropdown list
        download_resolution_layout = QHBoxLayout()

        # Download Button
        download_button = QPushButton("Download MP4")
        download_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        # Download Button
        pause_download_button = QPushButton("Pause")
        pause_download_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        pause_download_button.setFixedWidth(75)
        pause_download_button.setVisible(False)
        
        # Download Button
        Resume_download_button = QPushButton("Resume")
        Resume_download_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        Resume_download_button.setFixedWidth(90)
        Resume_download_button.setVisible(False)

        # Download Button
        download_cancel_button = QPushButton("Cancel")
        download_cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        download_cancel_button.setFixedWidth(85)
        download_cancel_button.setVisible(False)
        
        # Resolution Dropdown
        self.resolution_combo = QComboBox()
        arrow_icon_path = resource_path("images/down arrow.png")

        self.resolution_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #ff5c5c;
                color: black;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                font-weight: bold;
                width: 48px;
            }}
            QComboBox QAbstractItemView {{
                background-color: #ff5c5c;
                color: black;
                border-radius: 5px;
            }}
            QComboBox::drop-down {{
                border: none;
                subcontrol-origin: padding;
                subcontrol-position: center right;
                width: 20px;
                margin: 0px;
            }}
            QComboBox::down-arrow {{
                image: url({arrow_icon_path.replace("\\", "/")});  /* Dynamic path */
                width: 12px;
                height: 12px;
            }}
        """)
        self.resolution_combo.setVisible(False)

        # Add Download Button and Resolution Dropdown to the layout
        download_resolution_layout.addStretch()
        download_resolution_layout.addWidget(download_button)
        download_resolution_layout.addWidget(self.resolution_combo)
        download_resolution_layout.addWidget(pause_download_button)
        download_resolution_layout.addWidget(Resume_download_button)
        download_resolution_layout.addWidget(download_cancel_button)
        download_resolution_layout.addStretch()

        # Create a container widget to hold the layout
        download_resolution_widget = QWidget()
        download_resolution_widget.setLayout(download_resolution_layout)

        # Initially hide the download section (this is key)
        download_resolution_widget.setVisible(False)

        # Add this widget to the main download layout after the location input layout
        download_layout.addWidget(download_resolution_widget)

        # Create and add the progress bar to the layout
        progress_bar = QProgressBar()
        progress_bar.setAlignment(Qt.AlignCenter)
        progress_bar.setValue(0)
        progress_bar.setStyleSheet("font-size: 14px; color: black;")
        progress_bar.setVisible(False)  # Initially hidden
        progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ff5c5c;  
                background-color: black;  /* Light background */
                text-align: center;
                font-size: 14px;
                font-weight: bold;
                color: white;  /* Text color */
            }
            
            QProgressBar::chunk {
                border: 2px solid #ff5c5c;
                background-color: #ff5c5c;  /* Blue progress chunk */
                border-radius: 12px;  /* Rounded chunk corners */
            }
        """)
        download_layout.addWidget(progress_bar)  # Add it to the layout

        # # Function to update the download section (called after search)
        # def update_download_section():
        #     # Ensure that the Download and Resolution sections are added only once
        #     if not download_resolution_widget.isVisible():
        #         download_resolution_widget.setVisible(
        #             True
        #         )  # Make it visible once the search is successful

        #     # Update the resolution dropdown with current data
        #     update_resolution_dropdown()

        def handle_download():
            global video_url_variable

            # Validation checks
            if not video_url_variable:
                show_message("warning", "Invalid URL", "URL is empty.", parent=self)
                return
            if not video_url_variable.startswith("https://www.youtube.com/"):
                show_message(
                    "warning",
                    "Invalid URL",
                    "URL is invalid. Please enter a valid YouTube link.",
                    parent=self,
                )
                return

            path = location_input.text().strip()
            if not path:
                show_message("warning", "Invalid Path", "Location is empty.", parent=self)
                return

            try:
                os.chdir(path)
            except Exception as e:
                show_message(
                    "warning", "Invalid Path", f"Location Not Found!", parent=self
                )
                return

            # Initialize worker
            if self.resolution_combo.currentText() == 'Quality':
                show_message(
                    "warning", "Invalid Quality", f"Please Choose A Quality", parent=self
                )
                return
            self.download_worker = DownloadVideoWorker(
                main_window=self,
                url=video_url_variable,
                res_idx=self.resolution_combo.currentIndex() -1,
                path=path,
                resolution_text=self.resolution_combo.currentText(),
            )
            # Configure UI
            download_button.setEnabled(False)
            download_button.setText("Downloading...")
            progress_bar.setValue(0)
            progress_bar.setVisible(True)
            self.resolution_combo.setVisible(False)
            pause_download_button.setVisible(True)
            pause_download_button.setEnabled(True)
            download_cancel_button.setVisible(True)
            download_cancel_button.setEnabled(True)

            # Connect signals
            self.download_worker.progress_update.connect(update_progress)
            self.download_worker.success.connect(handle_success)
            self.download_worker.error.connect(handle_error)
            self.download_worker.file_conflict.connect(resolve_conflict)
            self.download_worker.finished.connect(cleanup_download)
            self.download_worker.cancelled.connect(handle_cancelled)

            # Start download
            self.download_worker.start()

        def pause_download():
            if self.download_worker:
                self.download_worker.pause()
                download_button.setText("Paused...")
                pause_download_button.setVisible(False)
                pause_download_button.setEnabled(False)
                Resume_download_button.setVisible(True)
                Resume_download_button.setEnabled(True)

        def resume_download():
            if self.download_worker:
                self.download_worker.resume()
                download_button.setText("Downloading...")
                Resume_download_button.setVisible(False)
                Resume_download_button.setEnabled(False)
                pause_download_button.setVisible(True)
                pause_download_button.setEnabled(True)

        def cancel_download():
            if self.download_worker:
                download_cancel_button.setEnabled(False)
                download_cancel_button.setText('Canceling..')
                download_cancel_button.setFixedWidth(120)
                # Schedule the rest of the cancellation after 3000 milliseconds (3 seconds)
                QTimer.singleShot(3000, continue_cancel_download)

        def continue_cancel_download():
            # Continue with the download cancellation
            self.download_worker.cancel()
            pause_download_button.setEnabled(False)
            Resume_download_button.setEnabled(False)
            show_message("information", "Canceled", "Download Canceled!", parent=self)
            


        def update_progress(value, text):
            progress_bar.setValue(value)
            progress_bar.setFormat(text)
            QApplication.processEvents()  # Force UI update

            if ("Converting" in text or "Finalizing" in text or "Download complete" in text):
                pause_download_button.setVisible(False)
                Resume_download_button.setVisible(False)
                download_button.setText("Processing...")
                download_cancel_button.setVisible(False)
            else:
                download_button.setText("Downloading...")

        def handle_success(resolution):
            global video_url_variable

            if "youtube.com/watch" in video_url_variable:
                show_message(
                    "information",
                    "Success",
                    f"Downloaded at {resolution} resolution successfully!",
                    parent=self,
                )

            else:
                show_message(
                    "information", "Success", f"Downloaded successfully!", parent=self
                )

        def handle_error(error):
            progress_bar.setValue(0)
            show_message("warning", "Error", error, parent=self)

        def resolve_conflict(title, file_type):
            choice = show_message(
                file_existence_status=True,
                video_title=title,
                file_type=file_type,
                parent=self,
            )
            self.download_worker.set_user_choice(choice)

        def cleanup_download():
            download_cancel_button.setEnabled(False)
            download_cancel_button.setVisible(False)
            download_cancel_button.setFixedWidth(85)
            download_cancel_button.setText('Cancel')
            pause_download_button.setEnabled(False)
            pause_download_button.setVisible(False)
            Resume_download_button.setEnabled(False)
            Resume_download_button.setVisible(False)
            download_button.setEnabled(True)
            download_button.setText("Download MP4")
            progress_bar.setVisible(False)
            url_input.clear()
            self.resolution_combo.clear()
            result_image.clear()
            result_text.clear()
            self.resolution_combo.setVisible(False)
            download_resolution_widget.setVisible(False)
            global video_url_variable
            video_url_variable = ""

        def handle_cancelled():
            print("Download cancelled by user.")
            download_cancel_button.setEnabled(False)
            download_cancel_button.setVisible(False)
            download_cancel_button.setText('Cancel')
            pause_download_button.setEnabled(False)
            pause_download_button.setVisible(False)
            Resume_download_button.setEnabled(False)
            Resume_download_button.setVisible(False)
            download_button.setEnabled(True)
            download_button.setText("Download MP4")
            progress_bar.setVisible(False)
            url_input.clear()
            self.resolution_combo.clear()
            result_image.clear()
            result_text.clear()
            self.resolution_combo.setVisible(False)
            download_resolution_widget.setVisible(False)
            global video_url_variable
            video_url_variable = ""

        # Set margins and spacing for better positioning
        download_layout.setSpacing(15)  # Add spacing between widgets
        download_layout.setContentsMargins(20, 20, 20, 20)  # Add uniform margins
        download_layout.addStretch()

        # Function to validate URL and display results
        def handle_search():
            global video_url_variable  # Declare as global to access the URL in other functions
            video_url_variable = url_input.text().strip()
            # Disable with visual feedback

            # Check if the URL is empty
            if not video_url_variable:
                show_message(
                    message_type="warning",
                    title="Invalid URL",
                    message="URL is empty.",
                    parent=self,
                )
                # QMessageBox.warning(None, "Invalid URL", "URL is empty.")
                return

            # Check if the URL is a valid YouTube link
            if not video_url_variable.startswith("https://www.youtube.com/"):
                show_message(
                    message_type="warning",
                    title="Invalid URL",
                    message="URL is invalid. Please enter a valid YouTube link.",
                    parent=self,
                )
                # QMessageBox.warning(None, "Invalid URL", "URL is invalid. Please enter a valid YouTube link.")
                return

            search_button.setEnabled(False)
            search_button.setFixedWidth(120)
            search_button.setText("Searching...")

            # Re-enable when finished (success or error)
            def enable_button():
                search_button.setEnabled(True)
                search_button.setFixedWidth(100)
                search_button.setText("Search")

            # Create worker thread
            self.worker = Worker(video_url_variable)
            self.worker.finished.connect(enable_button)
            self.worker.error.connect(enable_button)
            self.worker.valid_url.connect(handle_video_search_playlist)
            self.worker.live_url.connect(handle_video_search_live)
            # Add this new connection
            self.worker.resolutions_fetched.connect(handle_resolutions)

            self.worker.finished.connect(handle_search_result)  # New method
            self.worker.error.connect(
                lambda err: show_message("warning", "Error", err, parent=self)
            )
            self.worker.start()  # Start the thread

        def handle_video_search_playlist():
            show_message(
                "warning",
                "Invalid URL",
                "Sorry This Version of application can only download video or short not a playlist.\n\nWe Promise it will be in the next versions.",
                parent=self,
            )
        def handle_video_search_live():
            show_message(
                "warning",
                "Invalid URL",
                "Sorry This app is for downloading and converting only normal videos not a live one.",
                parent=self,
            )
            search_button.setEnabled(True)
            search_button.setFixedWidth(100)
            search_button.setText("Search")
            url_input.clear()
            global video_url_variable
            video_url_variable = ""
        # New handler for resolutions
        def handle_resolutions(available_resolutions):
            if available_resolutions:
                print("its youtube video not short")
                self.resolution_combo.clear()
                self.resolution_combo.setVisible(True)
                self.resolution_combo.addItem("Quality")
                self.resolution_combo.model().item(0).setEnabled(False)
                self.resolution_combo.addItems(available_resolutions)
                # Hide index 0 from the dropdown
                self.resolution_combo.setItemDelegate(HiddenItemDelegate(self.resolution_combo))
                self.resolution_combo.setCurrentIndex(0)

            else:
                print("its youtube short not video")
                self.resolution_combo.setVisible(False)


        # Modified update_download_section (remove resolution update call)
        def update_download_section():
            if not download_resolution_widget.isVisible():
                download_resolution_widget.setVisible(True)
        # Update the text and image in the result layout
        def handle_search_result(title, image_path):
            if title and image_path:
                result_text.setText(title)
                result_image.setPixmap(
                    QPixmap(image_path).scaled(
                        150, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                )
                os.remove(image_path)

                # Show the result layout widget
                result_layout_widget.setVisible(True)

                # Remove any existing stretch above the result_layout_widget
                for i in range(download_layout.count())[:-2]:
                    item = download_layout.itemAt(i)
                    if item.spacerItem():  # If it's a spacer
                        download_layout.removeItem(item)

                # Update the download section after the search
                update_download_section()  # Make the download button and resolution dropdown visible
            else:
                QMessageBox.warning(
                    None,
                    "Invalid Data",
                    "This URL doesnt have image to show try another url!",
                )
                return

        location_input.setText(get_folder_in_downloads("Video"))

        # Connect the Browse button to open a file dialog and update the text field
        def browse_folder():
            from PyQt5.QtWidgets import QFileDialog

            folder_path = QFileDialog.getExistingDirectory(
                None, "Select Video Folder", get_folder_in_downloads("Video")
            )
            if folder_path:
                location_input.setText(folder_path)

        # Connect the Search button to handle_search
        search_button.clicked.connect(handle_search)
        download_button.clicked.connect(handle_download)

        browse_button.clicked.connect(browse_folder)
        pause_download_button.clicked.connect(pause_download)
        Resume_download_button.clicked.connect(resume_download)
        download_cancel_button.clicked.connect(cancel_download)





        # Second Tab: Convert to MP3
        convert_tab = QWidget()
        convert_layout = QVBoxLayout(convert_tab)

        # Add horizontal layout for image and text (initially hidden)
        convert_result_layout = QHBoxLayout()

        # Image placeholder
        convert_result_image = QLabel()
        convert_result_image.setFixedSize(150, 90)  # Adjust size as needed
        convert_result_image.setStyleSheet("background-color: transparent;")
        convert_result_image.setAlignment(Qt.AlignCenter)

        # Text placeholder
        convert_result_text = QLabel()
        convert_result_text.setFont(QFont("Arial", 12, QFont.Bold))
        convert_result_text.setStyleSheet(
            "color: black; background-color: transparent;"
        )
        convert_result_text.setAlignment(Qt.AlignCenter)

        # Add image and text to the result layout
        convert_result_layout.addSpacing(60)  # Add spacing on the left
        convert_result_layout.addWidget(convert_result_image)
        convert_result_layout.addWidget(convert_result_text)
        convert_result_layout.addStretch()  # Add spacing on the right
        convert_result_layout.setContentsMargins(20, 20, 20, 20)

        # Widget to manage the result layout (initially hidden)
        convert_result_layout_widget = QWidget()
        convert_result_layout_widget.setLayout(convert_result_layout)
        convert_result_layout_widget.setVisible(False)  # Hide the widget initially

        # Add title label
        convert_title_label = QLabel("Enter URL & MP3 Save Location")
        convert_title_label.setFont(QFont("Arial", 12, QFont.Bold))
        convert_title_label.setStyleSheet(
            "color: black;background-color: transparent;"
        )  # Add bottom padding for spacing
        convert_layout.addWidget(
            convert_title_label, alignment=Qt.AlignTop | Qt.AlignLeft
        )

        # Add horizontal layout for input field and search button
        convert_url_input_layout = QHBoxLayout()

        # URL input field setup
        convert_url_input = ClearableLineEdit(self)
        convert_url_input.setPlaceholderText("Enter video URL to be converted...")
        convert_url_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #5b9bd5;
            }
            /* Prevent stylesheet from overriding the clear button icon */
            QLineEdit QToolButton {
                border: none;
                background: transparent;
            }
        """)

        

        
        convert_url_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        convert_url_input_layout.addSpacing(60)
        convert_url_input_layout.addWidget(convert_url_input)


        # Search Button
        convert_search_button = QPushButton("Search")
        convert_search_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
                                            
        """)
        convert_search_button.setFixedWidth(100)
        convert_url_input_layout.addWidget(convert_search_button)
        convert_url_input_layout.addSpacing(60)

        # Add the horizontal layout to the vertical layout
        convert_layout.addLayout(convert_url_input_layout)
        # Add result layout or stretch based on condition
        convert_layout.addWidget(convert_result_layout_widget)  # Initially hidden

        convert_layout.addStretch()  # Add stretch to replace result_layout when hidde

        # Add horizontal layout for MP3 Save Location input field and Browse button
        convert_location_input_layout = QHBoxLayout()

        # MP3 Save Location input field
        convert_location_input = CustomLineEdit(self)
        convert_location_input.setPlaceholderText("Enter MP3 Save Location...")
        convert_location_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid gray;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #5b9bd5;
            }
        """)
        convert_location_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        convert_location_input_layout.addSpacing(60)
        convert_location_input_layout.addWidget(convert_location_input)

        # Browse Button
        convert_browse_button = QPushButton("Browse")
        convert_browse_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
        """)
        convert_browse_button.setFixedWidth(100)  # Set a fixed width for the button
        convert_location_input_layout.addWidget(convert_browse_button)
        convert_location_input_layout.addSpacing(60)

        # Add the horizontal layout to the vertical layout
        convert_layout.addLayout(convert_location_input_layout)

        # Create horizontal layout for Convert button and Audio Quality dropdown list
        convert_quality_layout = QHBoxLayout()

        # Convert Button
        convert_button = QPushButton("Download MP3")
        convert_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        convert_button.setFixedWidth(150)

         # Download Button
        pause_convert_button = QPushButton("Pause")
        pause_convert_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        pause_convert_button.setFixedWidth(75)
        pause_convert_button.setVisible(False)
        
        # Download Button
        Resume_convert_button = QPushButton("Resume")
        Resume_convert_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        Resume_convert_button.setFixedWidth(90)
        Resume_convert_button.setVisible(False)

        # Download Button
        convert_cancel_button = QPushButton("Cancel")
        convert_cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5c5c; 
                color: black; 
                border-radius: 5px; 
                padding: 5px 15px; 
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: black;
                color: white;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        convert_cancel_button.setFixedWidth(85)
        convert_cancel_button.setVisible(False)

        # Add Convert Button and Audio Quality Dropdown to the layout
        convert_quality_layout.addStretch()
        convert_quality_layout.addWidget(convert_button)
        convert_quality_layout.addWidget(pause_convert_button)
        convert_quality_layout.addWidget(Resume_convert_button)
        convert_quality_layout.addWidget(convert_cancel_button)
        convert_quality_layout.addStretch()

        # Create a container widget to hold the layout
        convert_quality_widget = QWidget()
        convert_quality_widget.setLayout(convert_quality_layout)

        # Initially hide the convert section (this is key)
        convert_quality_widget.setVisible(False)

        # Add this widget to the main convert layout after the location input layout
        convert_layout.addWidget(convert_quality_widget)

        # Create and add the progress bar to the layout
        convert_progress_bar = QProgressBar()
        convert_progress_bar.setAlignment(Qt.AlignCenter)
        convert_progress_bar.setValue(0)
        convert_progress_bar.setStyleSheet("font-size: 14px; color: black;")
        convert_progress_bar.setVisible(False)  # Initially hidden
        convert_progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ff5c5c;  
                background-color: black;  /* Light background */
                text-align: center;
                font-size: 14px;
                font-weight: bold;
                color: white;  /* Text color */
            }
            
            QProgressBar::chunk {
                border: 2px solid #ff5c5c;
                background-color: #ff5c5c;  /* Blue progress chunk */
                border-radius: 12px;  /* Rounded chunk corners */
            }
        """)
        convert_layout.addWidget(convert_progress_bar)  # Add it to the layout

        def update_convert_section():
            print("Updating convert section...")  # Debug statement
            # Ensure that the Convert section is added only once
            if not convert_quality_widget.isVisible():
                print("Making convert section visible.")  # Debug statement
                convert_quality_widget.setVisible(
                    True
                )  # Make it visible once the search is successful

            # Update the available audio bitrates dropdown with current data
            # update_audio_quality_dropdown()

        # Function to handle the download action (this is just a placeholder for now)
        def handle_convert():
            global convert_video_url_variable

            print("Handling convert action...")  # Debug statement

            # Check if the URL is empty
            if not convert_url_input.text().strip():
                print("URL input is empty.")  # Debug statement
                show_message(
                    message_type="warning",
                    title="Invalid URL",
                    message="URL is empty.",
                    parent=self,
                )
                return

            # Get the URL from the input field
            convert_video_url_variable = convert_url_input.text().strip()

            # Check if the URL is a valid YouTube link
            if not convert_video_url_variable.startswith("https://www.youtube.com/"):
                print("Invalid YouTube URL.")  # Debug statement
                show_message(
                    message_type="warning",
                    title="Invalid URL",
                    message="URL is invalid. Please enter a valid YouTube link.",
                    parent=self,
                )
                return

            # selected_bitrate = audio_quality_combo.currentIndex()  # Audio bitrate selection
            # print(f"Selected bitrate index: {selected_bitrate}")  # Debug statement

            path = convert_location_input.text().strip()

            if not path:
                print("Path input is empty.")  # Debug statement
                show_message(
                    message_type="warning",
                    title="Invalid Path",
                    message="Path is empty.",
                    parent=self,
                )
                return

            try:
                os.chdir(path)
                print(f"Changed working directory to: {path}")  # Debug statement

            except:
                show_message(
                    message_type="warning",
                    title="Invalid Path",
                    message="Path is Invalid.",
                    parent=self,
                )
                return

            self.download_audio_worker = DownloadAudioWorker(
                main_window=self,
                url=convert_video_url_variable,
                path=path,
            )

            # Configure UI
            convert_button.setEnabled(False)
            convert_button.setText("Downloading...")
            convert_progress_bar.setValue(0)
            convert_progress_bar.setVisible(True)
            pause_convert_button.setVisible(True)
            pause_convert_button.setEnabled(True)
            convert_cancel_button.setVisible(True)
            convert_cancel_button.setEnabled(True)

            # Connect signals
            self.download_audio_worker.progress_update.connect(update_audio_progress)
            self.download_audio_worker.error.connect(handle_audio_error)
            self.download_audio_worker.file_conflict.connect(resolve_audio_conflict)
            self.download_audio_worker.success.connect(handle_audio_success)
            self.download_audio_worker.finished.connect(cleanup_audio_download)
            self.download_audio_worker.cancelled.connect(handle_convert_cancelled)

            # Start download
            self.download_audio_worker.start()

        def pause_audio_download():
            if self.download_audio_worker:
                self.download_audio_worker.pause()
                download_button.setText("Paused...")
                pause_convert_button.setVisible(False)
                pause_convert_button.setEnabled(False)
                Resume_convert_button.setVisible(True)
                Resume_convert_button.setEnabled(True)

        def resume_audio_download():
            if self.download_audio_worker:
                self.download_audio_worker.resume()
                download_button.setText("Downloading...")
                Resume_convert_button.setVisible(False)
                Resume_convert_button.setEnabled(False)
                pause_convert_button.setVisible(True)
                pause_convert_button.setEnabled(True)

        def cancel_convert():
            if self.download_audio_worker:
                convert_cancel_button.setEnabled(False)
                convert_cancel_button.setText('Canceling..')
                convert_cancel_button.setFixedWidth(120)
                # Schedule the rest of the cancellation after 3000 milliseconds (3 seconds)
                QTimer.singleShot(1000, continue_cancel_convert)

        def continue_cancel_convert():
            # Continue with the download cancellation
            self.download_audio_worker.cancel()
            pause_convert_button.setEnabled(False)
            Resume_convert_button.setEnabled(False)
            show_message("information", "Canceled", "Download Canceled!", parent=self)

        def update_audio_progress(value, text):
            convert_progress_bar.setValue(value)
            convert_progress_bar.setFormat(text)
            

            if ("Extracting" in text or "Merging" in text or "Finalizing" in text or "Download complete" in text):
                pause_convert_button.setVisible(False)
                Resume_convert_button.setVisible(False)
                convert_button.setText("Processing...")
                convert_cancel_button.setVisible(False)
            else:
                convert_button.setText("Downloading...")

            QApplication.processEvents()  # Force UI update
        

        def handle_audio_success():
            show_message(
                "information", "Success", "Downloaded successfully!", parent=self
            )

        def handle_audio_error(error):
            convert_progress_bar.setValue(0)
            show_message("warning", "Error", error, parent=self)

        def resolve_audio_conflict(title, file_type):
            choice = show_message(
                file_existence_status=True,
                video_title=title,
                file_type=file_type,
                parent=self,
            )
            self.download_audio_worker.set_user_choice(choice)

        def cleanup_audio_download():
            convert_cancel_button.setEnabled(False)
            convert_cancel_button.setVisible(False)
            convert_cancel_button.setFixedWidth(85)
            convert_cancel_button.setText('Cancel')
            pause_convert_button.setEnabled(False)
            pause_convert_button.setVisible(False)
            Resume_convert_button.setEnabled(False)
            Resume_convert_button.setVisible(False)
            convert_button.setEnabled(True)
            convert_button.setText("Download MP3")
            convert_progress_bar.setVisible(False)
            convert_url_input.clear()
            convert_result_image.clear()
            convert_result_text.clear()
            convert_quality_widget.setVisible(False)
            global convert_video_url_variable
            convert_video_url_variable = ""

        def handle_convert_cancelled():
            convert_cancel_button.setEnabled(False)
            convert_cancel_button.setVisible(False)
            convert_cancel_button.setText('Cancel')
            pause_convert_button.setEnabled(False)
            pause_convert_button.setVisible(False)
            Resume_convert_button.setEnabled(False)
            Resume_convert_button.setVisible(False)
            convert_button.setEnabled(True)
            convert_button.setText("Download MP3")
            convert_progress_bar.setVisible(False)
            convert_url_input.clear()
            convert_result_image.clear()
            convert_result_text.clear()
            convert_quality_widget.setVisible(False)
            global convert_video_url_variable
            convert_video_url_variable = ""

        

        # Function to validate URL and display results
        def handle_convert_search():
            global convert_video_url_variable  # Declare as global to access the URL in other functions
            convert_video_url_variable = convert_url_input.text().strip()

            # Check if the URL is empty
            if not convert_video_url_variable:
                show_message(
                    message_type="warning",
                    title="Invalid URL",
                    message="URL is empty.",
                    parent=self,
                )
                # QMessageBox.warning(None, "Invalid URL", "URL is empty.")
                return

            # Check if the URL is a valid YouTube link
            if not convert_video_url_variable.startswith("https://www.youtube.com/"):
                show_message(
                    message_type="warning",
                    title="Invalid URL",
                    message="URL is invalid. Please enter a valid YouTube link.",
                    parent=self,
                )
                # QMessageBox.warning(None, "Invalid URL", "URL is invalid. Please enter a valid YouTube link.")
                return

            convert_search_button.setEnabled(False)
            convert_search_button.setFixedWidth(120)
            convert_search_button.setText("Searching...")

            # Re-enable when finished (success or error)
            def enable_convert_button():
                convert_search_button.setEnabled(True)
                convert_search_button.setFixedWidth(100)
                convert_search_button.setText("Search")

            # Create worker thread
            self.worker = Worker(convert_video_url_variable)
            self.worker.finished.connect(enable_convert_button)
            self.worker.error.connect(enable_convert_button)
            self.worker.valid_url.connect(handle_audio_search_playlist)
            self.worker.live_url.connect(handle_audio_search_live)

            self.worker.finished.connect(handle_convert_search_result)  # New method
            self.worker.error.connect(
                lambda err: show_message("warning", "Error", err, parent=self)
            )
            self.worker.start()  # Start the thread

        def handle_audio_search_playlist():
            show_message(
                "warning",
                "Invalid URL",
                "Sorry This Version of application can only convert video or short to audio not a playlist.\n\nWe Promise it will be in the next versions.",
                parent=self,
            )
        def handle_audio_search_live():
            show_message(
                "warning",
                "Invalid URL",
                "Sorry This app is for downloading and converting only normal videos not a live one.",
                parent=self,
            )
            convert_search_button.setEnabled(True)
            convert_search_button.setFixedWidth(100)
            convert_search_button.setText("Search")
            convert_url_input.clear()
            global convert_video_url_variable
            convert_video_url_variable = ""

        # Update the text and image in the result layout
        def handle_convert_search_result(title, image_path):
            if title and image_path:
                convert_result_text.setText(title)
                convert_result_image.setPixmap(
                    QPixmap(image_path).scaled(
                        150, 90, Qt.KeepAspectRatio, Qt.SmoothTransformation
                    )
                )
                os.remove(image_path)

                # Show the result layout widget
                convert_result_layout_widget.setVisible(True)

                # Remove any existing stretch above the result_layout_widget
                for i in range(convert_layout.count())[:-2]:
                    item = convert_layout.itemAt(i)
                    if item.spacerItem():  # If it's a spacer
                        convert_layout.removeItem(item)

                # Update the download section after the search
                update_convert_section()  # Make the download button and resolution dropdown visible
            else:
                QMessageBox.warning(
                    None,
                    "Invalid Data",
                    "This URL doesnt have image to show try another url!",
                )
                return

        # Set the initial text in the convert_location_input field
        convert_location_input.setText(get_folder_in_downloads("Music"))

        # Browse Button functionality
        def convert_browse_folder():
            from PyQt5.QtWidgets import QFileDialog

            # Use the default music folder as the starting directory for the file dialog
            folder_path = QFileDialog.getExistingDirectory(
                None, "Select Download Folder", get_folder_in_downloads("Music")
            )

            if folder_path:
                convert_location_input.setText(folder_path)

        # Connect the Search button to handle_search
        convert_search_button.clicked.connect(handle_convert_search)
        convert_button.clicked.connect(handle_convert)

        convert_browse_button.clicked.connect(convert_browse_folder)
        Resume_convert_button.clicked.connect(resume_audio_download)
        pause_convert_button.clicked.connect(pause_audio_download)
        convert_cancel_button.clicked.connect(cancel_convert)

        # Set margins and spacing for better positioning
        convert_layout.setSpacing(15)  # Add spacing between widgets
        convert_layout.setContentsMargins(20, 20, 20, 20)  # Add uniform margins
        convert_layout.addStretch()

        # Add tabs
        tab_widget.addTab(download_tab, "Download")
        # Add tabs
        tab_widget.addTab(convert_tab, "Convert To MP3")
        custom_tab_bar.addTab("Download MP4")
        custom_tab_bar.addTab("Convert To MP3")

        # Center the custom tab bar
        tab_bar_layout = QHBoxLayout()
        tab_bar_layout.addStretch()
        tab_bar_layout.addWidget(custom_tab_bar)
        tab_bar_layout.addStretch()

        # Add widgets to content layout
        content_layout.addWidget(center_widget)
        content_layout.addSpacing(80)
        content_layout.addLayout(tab_bar_layout)
        content_layout.addWidget(tab_widget)

        # Add title bar and content layout to main layout
        main_layout.addLayout(title_bar)
        main_layout.addLayout(content_layout)

        # Set gradient background for the entire central widget
        central_widget.setStyleSheet("""
            QWidget {
                background: #fffef0;
                border-radius: 12px;
            }
        """)

    # Remove all override events except what's needed
    # def changeEvent(self, event):
    #     # Handle normal minimization/restoration
    #     if event.type() == QEvent.WindowStateChange:
    #         if self.isMinimized():
    #             print("Minimized to taskbar")  # Optional debug
    #     super().changeEvent(event)




if __name__ == "__main__":
    # Set high DPI scaling before creating the application
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    # Apply the stylesheet to the application
    app.setStyleSheet("""
        QWidget {
            border-radius: 10px;  /* Global border radius */
        }
        QMenu {
            border-radius: 0px !important;  /* Override for QMenu */
        }
    """)
    app.setStyleSheet("""
    QMenu {
        background-color: white;  /* Background color of the menu */
        border: 1px solid gray;  /* Border around the menu */
        color: black;  /* Text color */
        border-radius: 0px !important;  /* Remove rounded corners */
    }
    QMenu::item {
        background-color: transparent;  /* Background color of menu items */
        padding: 5px 20px;  /* Padding for menu items */
    }
    QMenu::item:selected {
        background-color: #ff5c5c;  /* Background color when hovered */
        color: white;  /* Text color when hovered */
    }
""")
    
        
    window = AppWindow()
    sys.exit(app.exec_())
