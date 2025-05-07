import random
import re
from aqt import mw, gui_hooks
from aqt.qt import (
    QAction,
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QLabel,
    QColorDialog,
    QColor,
    QWidget,
)

# Default configuration
CONFIG_DEFAULTS = {
    "interval": 20,
    "style": "goofy",
    "target": "card",
    "debug": False,
    "goofy_background": "#ADD8E6",  # Light blue
    "goofy_font_color": "#0000FF",  # Blue
    "goofy_font": "Arial",         # Default font
}

def load_config():
    """Merge stored config with defaults to ensure all fields are present."""
    stored = mw.col.conf.get("von_restorff", {})
    cfg = CONFIG_DEFAULTS.copy()
    cfg.update(stored)
    return cfg

def save_config(cfg):
    mw.col.conf["von_restorff"] = cfg
    mw.col.flush()

# State variables
review_counter = 0
last_effect_nid = None
last_effect_cid = None

def apply_von_restorff_effect(card):
    global review_counter, last_effect_nid, last_effect_cid
    cfg = load_config()
    
    if not card:
        return

    review_counter += 1
    if cfg["debug"]:
        print(f"Review #{review_counter}, card={card.id}, note={card.nid}")

    # Reset at end of interval
    if review_counter % cfg["interval"] == 0:
        last_effect_nid = None
        last_effect_cid = None
        if cfg["debug"]:
            print("Interval ended, resetting")

    # Select a new card/note at start of interval
    if review_counter % cfg["interval"] == 1:
        if cfg["target"] == "note":
            last_effect_nid = card.nid
        else:
            last_effect_cid = card.id
        if cfg["debug"]:
            sel = last_effect_nid if cfg["target"] == "note" else last_effect_cid
            print(f"Selected {cfg['target']} ID {sel} for effect")

    # Determine if we apply the effect now
    apply_effect = (
        (cfg["target"] == "note" and card.nid == last_effect_nid) or
        (cfg["target"] == "card" and card.id == last_effect_cid)
    )

    if apply_effect:
        if cfg["style"] == "goofy":
            js = f"""
                document.body.style.color = '{cfg['goofy_font_color']}';
                document.body.style.backgroundColor = '{cfg['goofy_background']}';
                document.body.style.fontFamily = '{cfg['goofy_font']}';
            """
        else:  # inverted
            js = """
                document.body.style.color = 'white';
                document.body.style.backgroundColor = '#333';
            """
        mw.reviewer.web.eval(js)
        if cfg["debug"]:
            print(f"Applied {cfg['style']} style")
    else:
        # Clear any previous styles
        js = """
            document.body.style.color = '';
            document.body.style.backgroundColor = '';
            document.body.style.fontFamily = '';
        """
        mw.reviewer.web.eval(js)
        if cfg["debug"]:
            print("Cleared styles")

# Settings dialog
class VonRestorffSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Von Restorff Settings")
        self.cfg = load_config()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Interval
        il = QHBoxLayout()
        il.addWidget(QLabel("Interval (cards):"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 1000)
        self.interval_spin.setValue(self.cfg["interval"])
        il.addWidget(self.interval_spin)
        layout.addLayout(il)

        # Style
        sl = QHBoxLayout()
        sl.addWidget(QLabel("Style:"))
        self.style_combo = QComboBox()
        self.style_combo.addItems(["goofy", "inverted"])
        self.style_combo.setCurrentText(self.cfg["style"])
        self.style_combo.currentTextChanged.connect(self._toggle_goofy_fields)
        sl.addWidget(self.style_combo)
        layout.addLayout(sl)

        # Goofy customization (wrapped in a QWidget for show/hide)
        self.goofy_widget = QWidget()
        goofy_layout = QVBoxLayout()

        # Background color
        bg_layout = QHBoxLayout()
        bg_layout.addWidget(QLabel("Goofy Background:"))
        self.bg_button = QPushButton("Pick Color")
        self.bg_button.clicked.connect(self._pick_background)
        bg_layout.addWidget(self.bg_button)
        self.bg_preview = QLabel()
        self.bg_preview.setFixedSize(20, 20)
        self.bg_preview.setStyleSheet(f"background-color: {self.cfg['goofy_background']};")
        bg_layout.addWidget(self.bg_preview)
        goofy_layout.addLayout(bg_layout)

        # Font color
        fc_layout = QHBoxLayout()
        fc_layout.addWidget(QLabel("Goofy Font Color:"))
        self.fc_button = QPushButton("Pick Color")
        self.fc_button.clicked.connect(self._pick_font_color)
        fc_layout.addWidget(self.fc_button)
        self.fc_preview = QLabel()
        self.fc_preview.setFixedSize(20, 20)
        self.fc_preview.setStyleSheet(f"background-color: {self.cfg['goofy_font_color']};")
        fc_layout.addWidget(self.fc_preview)
        goofy_layout.addLayout(fc_layout)

        # Goofy font
        fl = QHBoxLayout()
        fl.addWidget(QLabel("Goofy Font:"))
        self.font_combo = QComboBox()
        self.font_combo.addItems([
            "Arial", "Times New Roman", "Verdana", "Helvetica",
            "Georgia", "Courier New", "Comic Sans MS",
        ])
        self.font_combo.setCurrentText(self.cfg["goofy_font"])
        fl.addWidget(self.font_combo)
        goofy_layout.addLayout(fl)

        self.goofy_widget.setLayout(goofy_layout)
        layout.addWidget(self.goofy_widget)

        # Target
        tl = QHBoxLayout()
        tl.addWidget(QLabel("Target:"))
        self.target_combo = QComboBox()
        self.target_combo.addItems(["card", "note"])
        self.target_combo.setCurrentText(self.cfg["target"])
        tl.addWidget(self.target_combo)
        layout.addLayout(tl)

        # Debug
        self.debug_check = QCheckBox("Enable debug logs")
        self.debug_check.setChecked(self.cfg["debug"])
        layout.addWidget(self.debug_check)

        # Buttons
        btns = QHBoxLayout()
        save = QPushButton("Save")
        save.clicked.connect(self._save)
        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btns.addWidget(save)
        btns.addWidget(cancel)
        layout.addLayout(btns)

        # Initialize visibility based on current style
        self._toggle_goofy_fields(self.style_combo.currentText())

    def _toggle_goofy_fields(self, style):
        """Show/hide goofy customization fields based on selected style."""
        self.goofy_widget.setVisible(style == "goofy")

    def _pick_background(self):
        color = QColorDialog.getColor(QColor(self.cfg["goofy_background"]), self)
        if color.isValid():
            self.cfg["goofy_background"] = color.name()
            self.bg_preview.setStyleSheet(f"background-color: {color.name()};")

    def _pick_font_color(self):
        color = QColorDialog.getColor(QColor(self.cfg["goofy_font_color"]), self)
        if color.isValid():
            self.cfg["goofy_font_color"] = color.name()
            self.fc_preview.setStyleSheet(f"background-color: {color.name()};")

    def _save(self):
        hex_re = re.compile(r"^#[0-9A-Fa-f]{6}$")
        bg = self.cfg["goofy_background"]
        fc = self.cfg["goofy_font_color"]
        if not hex_re.match(bg):
            bg = CONFIG_DEFAULTS["goofy_background"]
        if not hex_re.match(fc):
            fc = CONFIG_DEFAULTS["goofy_font_color"]

        new_cfg = {
            "interval": self.interval_spin.value(),
            "style": self.style_combo.currentText(),
            "target": self.target_combo.currentText(),
            "debug": self.debug_check.isChecked(),
            "goofy_background": bg,
            "goofy_font_color": fc,
            "goofy_font": self.font_combo.currentText(),
        }
        save_config(new_cfg)
        self.accept()

def open_settings():
    dlg = VonRestorffSettingsDialog(mw)
    dlg.exec()

# Add to Tools menu
action = QAction("Von Restorff Settings", mw)
action.triggered.connect(open_settings)
mw.form.menuTools.addAction(action)

# Hook into Anki’s reviewer
gui_hooks.reviewer_did_show_question.append(apply_von_restorff_effect)