# _                                _                         
#| |customize.py                  | |                        
#| | _____   _____  __ _ _ __   __| |_ ____      ___ __  ___ 
#| |/ _ \ \ / / _ \/ _` | '_ \ / _` | '_ \ \ /\ / / '_ \/ __|
#| | (_) \ V /  __/ (_| | | | | (_| | |_) \ V  V /| | | \__ \
#|_|\___/ \_/ \___|\__,_|_| |_|\__,_| .__/ \_/\_/ |_| |_|___/
#                                   | |                      
#                                   |_|     
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QScrollArea, QWidget, QSpinBox, QLineEdit,
    QComboBox, QCheckBox, QColorDialog, QFileDialog, QDoubleSpinBox,
    QMessageBox
)
from PySide6.QtGui import QColor
from layout_config import LayoutConfig
from font_manager import FontManager

class CustomizeDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Customize Appearance")
        self.resize(750, 850)
        
        layout = QVBoxLayout(self)
        tabs = QTabWidget()
        
        reaping_scroll = QScrollArea()
        reaping_scroll.setWidgetResizable(True)
        reaping_widget = QWidget()
        reaping_layout = QVBoxLayout(reaping_widget)
        
        reaping_layout.addWidget(QLabel("<b>Layout & Sizing</b>"))
        self.tribute_size = self.add_spin(reaping_layout, "Tribute Image Size:", LayoutConfig.TRIBUTE_IMAGE_SIZE, 50, 200)
        self.tribute_spacing = self.add_spin(reaping_layout, "Tribute Spacing:", LayoutConfig.TRIBUTE_SPACING, 0, 50)
        self.district_spacing = self.add_spin(reaping_layout, "District Spacing:", LayoutConfig.DISTRICT_SPACING, 0, 100)
        self.edge_padding = self.add_spin(reaping_layout, "Edge Padding:", LayoutConfig.EDGE_PADDING, 0, 50)
        
        current_radius = LayoutConfig.TRIBUTE_IMAGE_BORDER_RADIUS
        radius_opt = "square"
        if current_radius == "25px":
            radius_opt = "rounded"
        elif current_radius == "50px":
            radius_opt = "circle"
        self.tribute_border_radius = self.add_dropdown(reaping_layout, "Image Corner Style:", ["square", "rounded", "circle"], radius_opt)
        
        reaping_layout.addSpacing(10)
        reaping_layout.addWidget(QLabel("<b>Tribute Image Border (Alive)</b>"))
        self.tribute_border_enabled = self.add_check(reaping_layout, "Border Enabled", LayoutConfig.TRIBUTE_IMAGE_BORDER_ENABLED)
        self.tribute_border_width = self.add_spin(reaping_layout, "Border Width:", LayoutConfig.TRIBUTE_IMAGE_BORDER_WIDTH, 1, 10)
        self.tribute_border_color = self.add_color(reaping_layout, "Border Color:", LayoutConfig.TRIBUTE_IMAGE_BORDER_COLOR)
        self.tribute_border_style = self.add_dropdown(reaping_layout, "Border Style:", ["solid", "dashed", "dotted", "double"], LayoutConfig.TRIBUTE_IMAGE_BORDER_STYLE)
        self.tribute_image_shadow_preset = self.add_dropdown(reaping_layout, "Image Shadow:", ["none", "normal"], LayoutConfig.TRIBUTE_IMAGE_SHADOW_PRESET)
        self.tribute_image_shadow_color = self.add_color(reaping_layout, "Shadow Color:", LayoutConfig.TRIBUTE_IMAGE_SHADOW_COLOR)
        
        reaping_layout.addSpacing(10)
        reaping_layout.addWidget(QLabel("<b>Dead Tribute Styling</b>"))
        self.dead_image_effect = self.add_dropdown(reaping_layout, "Image Effect:", ["none", "grayscale"], LayoutConfig.DEAD_TRIBUTE_IMAGE_EFFECT)
        self.dead_opacity = self.add_double(reaping_layout, "Opacity:", LayoutConfig.DEAD_TRIBUTE_OPACITY, 0.1, 1.0, 0.1)
        self.dead_border_enabled = self.add_check(reaping_layout, "Dead Border Enabled", LayoutConfig.DEAD_TRIBUTE_BORDER_ENABLED)
        self.dead_border_width = self.add_spin(reaping_layout, "Dead Border Width:", LayoutConfig.DEAD_TRIBUTE_BORDER_WIDTH, 1, 10)
        self.dead_border_color = self.add_color(reaping_layout, "Dead Border Color:", LayoutConfig.DEAD_TRIBUTE_BORDER_COLOR)
        self.dead_image_shadow_preset = self.add_dropdown(reaping_layout, "Image Shadow:", ["none", "normal"], LayoutConfig.DEAD_TRIBUTE_SHADOW_PRESET)
        self.dead_image_shadow_color = self.add_color(reaping_layout, "Shadow Color:", LayoutConfig.DEAD_TRIBUTE_SHADOW_COLOR)
        self.dead_name_color = self.add_color(reaping_layout, "Dead Name Color:", LayoutConfig.DEAD_TRIBUTE_NAME_COLOR)
        
        reaping_layout.addSpacing(20)
        reaping_layout.addWidget(QLabel("<b>District Label</b>"))
        self.district_font = self.add_text_ctrl(
            reaping_layout, "District Label",
            LayoutConfig.DISTRICT_LABEL_FONT, LayoutConfig.DISTRICT_LABEL_SIZE,
            LayoutConfig.DISTRICT_LABEL_BOLD, LayoutConfig.DISTRICT_LABEL_ITALIC,
            LayoutConfig.DISTRICT_LABEL_COLOR,
            LayoutConfig.DISTRICT_LABEL_SHADOW_PRESET, LayoutConfig.DISTRICT_LABEL_SHADOW_COLOR,
            LayoutConfig.DISTRICT_LABEL_OUTLINE_STYLE, LayoutConfig.DISTRICT_LABEL_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        reaping_layout.addSpacing(20)
        reaping_layout.addWidget(QLabel("<b>Tribute Name</b>"))
        self.tribute_name_font = self.add_text_ctrl(
            reaping_layout, "Tribute Name",
            LayoutConfig.TRIBUTE_NAME_FONT, LayoutConfig.TRIBUTE_NAME_SIZE,
            LayoutConfig.TRIBUTE_NAME_BOLD, LayoutConfig.TRIBUTE_NAME_ITALIC,
            LayoutConfig.TRIBUTE_NAME_COLOR,
            LayoutConfig.TRIBUTE_NAME_SHADOW_PRESET, LayoutConfig.TRIBUTE_NAME_SHADOW_COLOR,
            LayoutConfig.TRIBUTE_NAME_OUTLINE_STYLE, LayoutConfig.TRIBUTE_NAME_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        reaping_layout.addSpacing(20)
        reaping_layout.addWidget(QLabel("<b>Tribute Status</b>"))
        self.tribute_status_font = self.add_text_ctrl(
            reaping_layout, "Tribute Status",
            LayoutConfig.TRIBUTE_STATUS_FONT, LayoutConfig.TRIBUTE_STATUS_SIZE,
            LayoutConfig.TRIBUTE_STATUS_BOLD, LayoutConfig.TRIBUTE_STATUS_ITALIC,
            LayoutConfig.TRIBUTE_STATUS_COLOR,
            LayoutConfig.TRIBUTE_STATUS_SHADOW_PRESET, LayoutConfig.TRIBUTE_STATUS_SHADOW_COLOR,
            LayoutConfig.TRIBUTE_STATUS_OUTLINE_STYLE, LayoutConfig.TRIBUTE_STATUS_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        self.tribute_status_dead = self.add_color(reaping_layout, "Status Dead Color:", LayoutConfig.TRIBUTE_STATUS_DEAD_COLOR)
        
        reaping_layout.addSpacing(20)
        reaping_layout.addWidget(QLabel("<b>Background</b>"))
        self.reaping_bg = self.add_color(reaping_layout, "Background Color:", LayoutConfig.REAPING_BG_COLOR)
        
        reaping_layout.addStretch()
        reaping_scroll.setWidget(reaping_widget)
        tabs.addTab(reaping_scroll, "Reaping")
        
        feed_scroll = QScrollArea()
        feed_scroll.setWidgetResizable(True)
        feed_widget = QWidget()
        feed_layout = QVBoxLayout(feed_widget)
        
        feed_layout.addWidget(QLabel("<b>Layout</b>"))
        self.feed_width = self.add_spin(feed_layout, "Feed Width:", LayoutConfig.FEED_WIDTH, 400, 1000)
        self.portrait_height = self.add_spin(feed_layout, "Portrait Size:", LayoutConfig.FEED_PORTRAIT_HEIGHT, 50, 300)
        self.portrait_spacing = self.add_spin(feed_layout, "Portrait Spacing:", LayoutConfig.FEED_PORTRAIT_SPACING, 0, 30)
        
        current_portrait_radius = LayoutConfig.FEED_PORTRAIT_BORDER_RADIUS
        portrait_radius_opt = "square"
        if current_portrait_radius == "25px":
            portrait_radius_opt = "rounded"
        elif current_portrait_radius == "50px":
            portrait_radius_opt = "circle"
        self.portrait_border_radius = self.add_dropdown(feed_layout, "Portrait Corner Style:", ["square", "rounded", "circle"], portrait_radius_opt)
        
        feed_layout.addSpacing(10)
        feed_layout.addWidget(QLabel("<b>Portrait Border</b>"))
        self.portrait_border_enabled = self.add_check(feed_layout, "Border Enabled", LayoutConfig.FEED_PORTRAIT_BORDER_ENABLED)
        self.portrait_border_width = self.add_spin(feed_layout, "Border Width:", LayoutConfig.FEED_PORTRAIT_BORDER_WIDTH, 1, 10)
        self.portrait_border_color = self.add_color(feed_layout, "Border Color:", LayoutConfig.FEED_PORTRAIT_BORDER_COLOR)
        self.portrait_border_style = self.add_dropdown(feed_layout, "Border Style:", ["solid", "dashed", "dotted", "double"], LayoutConfig.FEED_PORTRAIT_BORDER_STYLE)
        self.portrait_shadow_preset = self.add_dropdown(feed_layout, "Image Shadow:", ["none", "normal"], LayoutConfig.FEED_PORTRAIT_SHADOW_PRESET)
        self.portrait_shadow_color = self.add_color(feed_layout, "Shadow Color:", LayoutConfig.FEED_PORTRAIT_SHADOW_COLOR)
        
        feed_layout.addSpacing(20)
        feed_layout.addWidget(QLabel("<b>Event Text</b>"))
        self.feed_text_font = self.add_text_ctrl(
            feed_layout, "Event Text",
            LayoutConfig.FEED_EVENT_TEXT_FONT, LayoutConfig.FEED_EVENT_TEXT_SIZE,
            LayoutConfig.FEED_EVENT_TEXT_BOLD, LayoutConfig.FEED_EVENT_TEXT_ITALIC,
            LayoutConfig.FEED_TEXT_COLOR,
            LayoutConfig.FEED_EVENT_TEXT_SHADOW_PRESET, LayoutConfig.FEED_EVENT_TEXT_SHADOW_COLOR,
            LayoutConfig.FEED_EVENT_TEXT_OUTLINE_STYLE, LayoutConfig.FEED_EVENT_TEXT_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        feed_layout.addSpacing(20)
        feed_layout.addWidget(QLabel("<b>Proceed Button</b>"))
        self.proceed_text = self.add_line(feed_layout, "Button Text:", LayoutConfig.PROCEED_BUTTON_TEXT)
        self.proceed_font = self.add_text_ctrl(
            feed_layout, "Proceed Button",
            LayoutConfig.PROCEED_BUTTON_FONT, LayoutConfig.PROCEED_BUTTON_FONT_SIZE,
            LayoutConfig.PROCEED_BUTTON_BOLD, LayoutConfig.PROCEED_BUTTON_ITALIC,
            LayoutConfig.PROCEED_BUTTON_COLOR,
            LayoutConfig.PROCEED_BUTTON_SHADOW_PRESET, LayoutConfig.PROCEED_BUTTON_SHADOW_COLOR,
            LayoutConfig.PROCEED_BUTTON_OUTLINE_STYLE, LayoutConfig.PROCEED_BUTTON_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        self.proceed_hover = self.add_color(feed_layout, "Hover Color:", LayoutConfig.PROCEED_BUTTON_HOVER_COLOR)
        self.proceed_margin = self.add_spin(feed_layout, "Margin Top:", LayoutConfig.PROCEED_BUTTON_MARGIN_TOP, 0, 100)
        
        feed_layout.addSpacing(20)
        feed_layout.addWidget(QLabel("<b>Background</b>"))
        self.feed_bg = self.add_color(feed_layout, "Feed Background:", LayoutConfig.FEED_BG_COLOR)
        
        feed_layout.addStretch()
        feed_scroll.setWidget(feed_widget)
        tabs.addTab(feed_scroll, "Event Feed")
        
        title_scroll = QScrollArea()
        title_scroll.setWidgetResizable(True)
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        
        title_layout.addWidget(QLabel("<b>Season Title Settings</b>"))
        self.season_title_show = self.add_check(title_layout, "Show Season Title", LayoutConfig.SEASON_TITLE_SHOW)
        self.season_title_text = self.add_line(title_layout, "Season Title Text:", LayoutConfig.SEASON_TITLE_TEXT)
        self.season_title_box_bg = self.add_color(title_layout, "Title Box Background:", LayoutConfig.SEASON_TITLE_BOX_BG_COLOR)
        self.season_title_bg_opacity = self.add_dropdown(title_layout, "Title Box Background:", ["Solid", "Clear"], LayoutConfig.SEASON_TITLE_BOX_BG_OPACITY)
        
        title_layout.addSpacing(10)
        self.season_title_font = self.add_text_ctrl(
            title_layout, "Season Title",
            LayoutConfig.SEASON_TITLE_FONT, LayoutConfig.SEASON_TITLE_SIZE,
            LayoutConfig.SEASON_TITLE_BOLD, LayoutConfig.SEASON_TITLE_ITALIC,
            LayoutConfig.SEASON_TITLE_COLOR,
            LayoutConfig.SEASON_TITLE_SHADOW_PRESET, LayoutConfig.SEASON_TITLE_SHADOW_COLOR,
            LayoutConfig.SEASON_TITLE_OUTLINE_STYLE, LayoutConfig.SEASON_TITLE_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        title_layout.addSpacing(20)
        title_layout.addWidget(QLabel("<b>Phase Title Settings</b>"))
        self.feed_title_bg_opacity = self.add_dropdown(title_layout, "Title Box Background:", ["Solid", "Clear"], LayoutConfig.FEED_TITLE_BOX_BG_OPACITY)
        self.feed_title_font = self.add_text_ctrl(
            title_layout, "Phase Title",
            LayoutConfig.FEED_TITLE_FONT, LayoutConfig.FEED_TITLE_SIZE,
            LayoutConfig.FEED_TITLE_BOLD, LayoutConfig.FEED_TITLE_ITALIC,
            LayoutConfig.FEED_TITLE_COLOR,
            LayoutConfig.FEED_TITLE_SHADOW_PRESET, LayoutConfig.FEED_TITLE_SHADOW_COLOR,
            LayoutConfig.FEED_TITLE_OUTLINE_STYLE, LayoutConfig.FEED_TITLE_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        self.feed_title_bg = self.add_color(title_layout, "Title Box Background:", LayoutConfig.FEED_TITLE_BOX_BG_COLOR)
        
        title_layout.addSpacing(20)
        title_layout.addWidget(QLabel("<b>Customize Phase Names</b>"))
        title_layout.addWidget(QLabel("Leave blank to use defaults (Day 1, Night 1, etc.)"))
        title_layout.addSpacing(10)

        self.reaping_phase_name = self.add_line(title_layout, "Reaping:", LayoutConfig.REAPING_TITLE_TEXT)
        self.day_phase_name = self.add_line(title_layout, "Day Phase (use {X} for number):", LayoutConfig.DAY_PHASE_NAME or "Day {X}")
        self.night_phase_name = self.add_line(title_layout, "Night Phase (use {X} for number):", LayoutConfig.NIGHT_PHASE_NAME or "Night {X}")
        self.winner_phase_name = self.add_line(title_layout, "Winner Screen:", LayoutConfig.WIN_SCREEN_NAME or "Winner")

        title_layout.addStretch()
        title_scroll.setWidget(title_widget)
        tabs.addTab(title_scroll, "Title")
        
        district_scroll = QScrollArea()
        district_scroll.setWidgetResizable(True)
        district_widget = QWidget()
        district_layout = QVBoxLayout(district_widget)
        
        district_layout.addWidget(QLabel("Assign custom names to districts (leave blank for default):"))
        district_layout.addSpacing(10)
        
        self.district_name_inputs = {}
        for i in range(1, 25):
            row = QHBoxLayout()
            row.addWidget(QLabel(f"District {i}:"))
            name_edit = QLineEdit()
            name_edit.setPlaceholderText("District {}".format(i))
            name_edit.setMaxLength(30)
            if i in LayoutConfig.DISTRICT_NAMES:
                name_edit.setText(LayoutConfig.DISTRICT_NAMES[i])
            self.district_name_inputs[i] = name_edit
            row.addWidget(name_edit)
            row.addStretch()
            district_layout.addLayout(row)
        
        district_layout.addStretch()
        district_scroll.setWidget(district_widget)
        tabs.addTab(district_scroll, "District Names")
        
        placements_scroll = QScrollArea()
        placements_scroll.setWidgetResizable(True)
        placements_widget = QWidget()
        placements_layout = QVBoxLayout(placements_widget)
        
        placements_layout.addWidget(QLabel("<b>Layout & Sizing</b>"))
        self.placements_image_size = self.add_spin(placements_layout, "Image Size:", LayoutConfig.PLACEMENTS_TRIBUTE_IMAGE_SIZE, 50, 200)
        self.placements_spacing = self.add_spin(placements_layout, "Tribute Spacing:", LayoutConfig.PLACEMENTS_TRIBUTE_SPACING, 0, 50)
        self.placements_row_spacing = self.add_spin(placements_layout, "Row Spacing:", LayoutConfig.PLACEMENTS_ROW_SPACING, 0, 50)
        self.placements_edge_padding = self.add_spin(placements_layout, "Edge Padding:", LayoutConfig.PLACEMENTS_EDGE_PADDING, 0, 50)
        
        current_placements_radius = LayoutConfig.PLACEMENTS_IMAGE_BORDER_RADIUS
        placements_radius_opt = "square"
        if current_placements_radius == "25px":
            placements_radius_opt = "rounded"
        elif current_placements_radius == "50px":
            placements_radius_opt = "circle"
        self.placements_border_radius = self.add_dropdown(placements_layout, "Image Corner Style:", ["square", "rounded", "circle"], placements_radius_opt)
        
        placements_layout.addSpacing(10)
        placements_layout.addWidget(QLabel("<b>Image Border</b>"))
        self.placements_border_enabled = self.add_check(placements_layout, "Border Enabled", LayoutConfig.PLACEMENTS_IMAGE_BORDER_ENABLED)
        self.placements_border_width = self.add_spin(placements_layout, "Border Width:", LayoutConfig.PLACEMENTS_IMAGE_BORDER_WIDTH, 1, 10)
        self.placements_border_color = self.add_color(placements_layout, "Border Color:", LayoutConfig.PLACEMENTS_IMAGE_BORDER_COLOR)
        self.placements_border_style = self.add_dropdown(placements_layout, "Border Style:", ["solid", "dashed", "dotted", "double"], LayoutConfig.PLACEMENTS_IMAGE_BORDER_STYLE)
        
        placements_layout.addSpacing(20)
        placements_layout.addWidget(QLabel("<b>Tribute Name</b>"))
        self.placements_name_font = self.add_text_ctrl(
            placements_layout, "Name",
            LayoutConfig.PLACEMENTS_NAME_FONT, LayoutConfig.PLACEMENTS_NAME_SIZE,
            LayoutConfig.PLACEMENTS_NAME_BOLD, LayoutConfig.PLACEMENTS_NAME_ITALIC,
            LayoutConfig.PLACEMENTS_NAME_COLOR,
            LayoutConfig.PLACEMENTS_NAME_SHADOW_PRESET, LayoutConfig.PLACEMENTS_NAME_SHADOW_COLOR,
            LayoutConfig.PLACEMENTS_NAME_OUTLINE_STYLE, LayoutConfig.PLACEMENTS_NAME_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        placements_layout.addSpacing(20)
        placements_layout.addWidget(QLabel("<b>Placement Rank</b>"))
        self.placements_rank_font = self.add_text_ctrl(
            placements_layout, "Rank",
            LayoutConfig.PLACEMENTS_RANK_FONT, LayoutConfig.PLACEMENTS_RANK_SIZE,
            LayoutConfig.PLACEMENTS_RANK_BOLD, LayoutConfig.PLACEMENTS_RANK_ITALIC,
            LayoutConfig.PLACEMENTS_RANK_COLOR,
            LayoutConfig.PLACEMENTS_RANK_SHADOW_PRESET, LayoutConfig.PLACEMENTS_RANK_SHADOW_COLOR,
            LayoutConfig.PLACEMENTS_RANK_OUTLINE_STYLE, LayoutConfig.PLACEMENTS_RANK_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        placements_layout.addSpacing(20)
        placements_layout.addWidget(QLabel("<b>District Text</b>"))
        self.placements_district_font = self.add_text_ctrl(
            placements_layout, "District",
            LayoutConfig.PLACEMENTS_DISTRICT_FONT, LayoutConfig.PLACEMENTS_DISTRICT_SIZE,
            LayoutConfig.PLACEMENTS_DISTRICT_BOLD, LayoutConfig.PLACEMENTS_DISTRICT_ITALIC,
            LayoutConfig.PLACEMENTS_DISTRICT_COLOR,
            LayoutConfig.PLACEMENTS_DISTRICT_SHADOW_PRESET, LayoutConfig.PLACEMENTS_DISTRICT_SHADOW_COLOR,
            LayoutConfig.PLACEMENTS_DISTRICT_OUTLINE_STYLE, LayoutConfig.PLACEMENTS_DISTRICT_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        placements_layout.addSpacing(20)
        placements_layout.addWidget(QLabel("<b>Kills Text</b>"))
        self.placements_kills_font = self.add_text_ctrl(
            placements_layout, "Kills",
            LayoutConfig.PLACEMENTS_KILLS_FONT, LayoutConfig.PLACEMENTS_KILLS_SIZE,
            LayoutConfig.PLACEMENTS_KILLS_BOLD, LayoutConfig.PLACEMENTS_KILLS_ITALIC,
            LayoutConfig.PLACEMENTS_KILLS_COLOR,
            LayoutConfig.PLACEMENTS_KILLS_SHADOW_PRESET, LayoutConfig.PLACEMENTS_KILLS_SHADOW_COLOR,
            LayoutConfig.PLACEMENTS_KILLS_OUTLINE_STYLE, LayoutConfig.PLACEMENTS_KILLS_OUTLINE_COLOR or LayoutConfig.TEXT_OUTLINE_COLOR
        )
        
        placements_layout.addSpacing(20)
        placements_layout.addWidget(QLabel("<b>Background</b>"))
        self.placements_bg = self.add_color(placements_layout, "Background Color:", LayoutConfig.PLACEMENTS_BG_COLOR)
        
        placements_layout.addStretch()
        placements_scroll.setWidget(placements_widget)
        tabs.addTab(placements_scroll, "Placements")
        
        bg_scroll = QScrollArea()
        bg_scroll.setWidgetResizable(True)
        bg_widget = QWidget()
        bg_layout = QVBoxLayout(bg_widget)
        
        bg_layout.addWidget(QLabel("Set background images for each phase:"))
        bg_layout.addSpacing(10)
        
        self.bg_image_inputs = {}
        bg_phases = [
            ("Reaping/Preview", "REAPING_BG_IMAGE"),
            ("Bloodbath", "BLOODBATH_BG_IMAGE"),
            ("Day", "DAY_BG_IMAGE"),
            ("Night", "NIGHT_BG_IMAGE"),
            ("Winner", "WINNER_BG_IMAGE"),
            ("Placements", "PLACEMENTS_BG_IMAGE")
        ]
        
        for label, config_key in bg_phases:
            row = QHBoxLayout()
            row.addWidget(QLabel("{}:".format(label)))
            
            path_edit = QLineEdit()
            path_edit.setPlaceholderText("Image path...")
            current_val = getattr(LayoutConfig, config_key, "")
            if current_val:
                path_edit.setText(current_val)
            
            browse_btn = QPushButton("Browse")
            browse_btn.setAutoDefault(False)
            browse_btn.setDefault(False)
            
            def make_browse(edit):
                def browse():
                    filepath, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
                    if filepath:
                        edit.setText(filepath)
                return browse
            
            browse_btn.clicked.connect(make_browse(path_edit))
            
            self.bg_image_inputs[config_key] = path_edit
            row.addWidget(path_edit, 3)
            row.addWidget(browse_btn)
            bg_layout.addLayout(row)
        
        bg_layout.addWidget(QLabel("\nBackground Offsets:"))
        self.reaping_bg_x = self.add_line(bg_layout, "Reaping X Offset:", LayoutConfig.REAPING_BG_X_OFFSET)
        self.reaping_bg_y = self.add_line(bg_layout, "Reaping Y Offset:", LayoutConfig.REAPING_BG_Y_OFFSET)
        self.feed_bg_x = self.add_line(bg_layout, "Feed X Offset:", LayoutConfig.FEED_BG_X_OFFSET)
        self.feed_bg_y = self.add_line(bg_layout, "Feed Y Offset:", LayoutConfig.FEED_BG_Y_OFFSET)
        
        bg_layout.addStretch()
        bg_scroll.setWidget(bg_widget)
        tabs.addTab(bg_scroll, "Backgrounds")
        
        layout.addWidget(tabs)
        
        btn_layout = QHBoxLayout()

        save_to_file_btn = QPushButton("Save to File")
        save_to_file_btn.setAutoDefault(False)
        save_to_file_btn.clicked.connect(self.save_to_file)

        load_from_file_btn = QPushButton("Load from File")
        load_from_file_btn.setAutoDefault(False)
        load_from_file_btn.clicked.connect(self.load_from_file)

        btn_layout.addWidget(save_to_file_btn)
        btn_layout.addWidget(load_from_file_btn)
        btn_layout.addStretch()

        save_btn = QPushButton("Apply")
        save_btn.clicked.connect(self.save_no_close)
        save_btn.setAutoDefault(False)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.reject)
        close_btn.setDefault(True)

        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
    
    def save_to_file(self):
        self.apply_settings()
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Settings", "simulator_settings.json", "JSON Files (*.json)"
        )
        if filepath:
            LayoutConfig.save_to_file(filepath)
            QMessageBox.information(self, "Saved", "Settings saved to:\n{}".format(filepath))

    def load_from_file(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Load Settings", "", "JSON Files (*.json)"
        )
        if filepath:
            success = LayoutConfig.load_from_file(filepath)
            if success:
                self.close()
                new_dialog = CustomizeDialog(self.parent())
                new_dialog.exec()
                QMessageBox.information(self, "Loaded", f"Settings loaded from:\n{filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to load settings file!")
    
    def save_no_close(self):
        self.apply_settings()
        
        main_window = self.parent()
        if hasattr(main_window, 'districts') and main_window.districts:
            html = main_window.gen_reaping_html(main_window.districts, show_proceed=False)
            main_window.reaping_view.setHtml(html)
        
        QMessageBox.information(self, "Saved", "Settings have been applied!")
    
    def add_spin(self, layout, label, default, min_val, max_val):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        spin = QSpinBox()
        spin.setRange(min_val, max_val)
        spin.setValue(default)
        spin.setKeyboardTracking(False)
        spin.setFocusPolicy(Qt.StrongFocus)
        row.addWidget(spin)
        row.addStretch()
        layout.addLayout(row)
        return spin
    
    def add_double(self, layout, label, default, min_val, max_val, step):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        spin = QDoubleSpinBox()
        spin.setRange(min_val, max_val)
        spin.setSingleStep(step)
        spin.setValue(default)
        spin.setKeyboardTracking(False)
        spin.setFocusPolicy(Qt.StrongFocus)
        row.addWidget(spin)
        row.addStretch()
        layout.addLayout(row)
        return spin
    
    def add_line(self, layout, label, default):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        edit = QLineEdit(str(default))
        row.addWidget(edit)
        row.addStretch()
        layout.addLayout(row)
        return edit
    
    def add_check(self, layout, label, default):
        row = QHBoxLayout()
        check = QCheckBox(label)
        check.setChecked(default)
        row.addWidget(check)
        row.addStretch()
        layout.addLayout(row)
        return check
    
    def add_dropdown(self, layout, label, options, default):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        combo = QComboBox()
        combo.addItems(options)
        combo.setCurrentText(str(default))
        row.addWidget(combo)
        row.addStretch()
        layout.addLayout(row)
        return combo
    
    def add_color(self, layout, label, default):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        
        btn = QPushButton()
        btn.setFixedSize(60, 25)
        btn.setStyleSheet("background-color: {};".format(default))
        btn.current_color = default
        btn.setAutoDefault(False)
        btn.setDefault(False)
        
        def pick_color():
            color = QColorDialog.getColor(QColor(btn.current_color), self)
            if color.isValid():
                btn.current_color = color.name()
                btn.setStyleSheet("background-color: {};".format(color.name()))
        
        btn.clicked.connect(pick_color)
        row.addWidget(btn)
        row.addStretch()
        layout.addLayout(row)
        return btn
    
    def add_text_ctrl(self, layout, name, font_name, size, bold, italic, color, 
                               shadow_preset, shadow_color, outline_style, outline_color):
        group = QWidget()
        group_layout = QVBoxLayout(group)
        group_layout.setContentsMargins(10, 5, 10, 10)
        
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Font:"))
        font_combo = QComboBox()
        font_combo.addItems(["Arial", "Verdana", "Georgia", "Times New Roman"] + FontManager.all_fonts())
        font_combo.setEditable(True)
        font_combo.setCurrentText(font_name)
        row1.addWidget(font_combo)
        row1.addStretch()
        group_layout.addLayout(row1)
        
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Size:"))
        size_spin = QSpinBox()
        size_spin.setRange(6, 72)
        size_spin.setValue(size)
        size_spin.setKeyboardTracking(False)
        size_spin.setFocusPolicy(Qt.StrongFocus)
        row2.addWidget(size_spin)
        
        bold_check = QCheckBox("Bold")
        bold_check.setChecked(bold)
        row2.addWidget(bold_check)
        
        italic_check = QCheckBox("Italic")
        italic_check.setChecked(italic)
        row2.addWidget(italic_check)
        row2.addStretch()
        group_layout.addLayout(row2)
        
        color_row = QHBoxLayout()
        color_row.addWidget(QLabel("Color:"))
        color_btn = QPushButton()
        color_btn.setFixedSize(60, 25)
        color_btn.setStyleSheet(f"background-color: {color};")
        color_btn.current_color = color
        color_btn.setAutoDefault(False)
        color_btn.setDefault(False)
        
        def pick_color():
            col = QColorDialog.getColor(QColor(color_btn.current_color), self)
            if col.isValid():
                color_btn.current_color = col.name()
                color_btn.setStyleSheet(f"background-color: {col.name()};")
        
        color_btn.clicked.connect(pick_color)
        color_row.addWidget(color_btn)
        color_row.addStretch()
        group_layout.addLayout(color_row)
        
        shadow_row = QHBoxLayout()
        shadow_row.addWidget(QLabel("Shadow:"))
        shadow_combo = QComboBox()
        shadow_combo.addItems(["none", "normal", "strong", "custom"])
        shadow_combo.setCurrentText(shadow_preset)
        shadow_combo.setToolTip("none=off | normal=3-layer glow | strong=6-layer glow | custom=raw CSS")
        shadow_row.addWidget(shadow_combo)
        
        shadow_color_btn = QPushButton()
        shadow_color_btn.setFixedSize(60, 25)
        shadow_color_btn.setStyleSheet(f"background-color: {shadow_color};")
        shadow_color_btn.current_color = shadow_color
        shadow_color_btn.setAutoDefault(False)
        shadow_color_btn.setDefault(False)
        shadow_color_btn.setToolTip("Color of the shadow/glow")
        
        def pick_shadow_color():
            col = QColorDialog.getColor(QColor(shadow_color_btn.current_color), self)
            if col.isValid():
                shadow_color_btn.current_color = col.name()
                shadow_color_btn.setStyleSheet(f"background-color: {col.name()};")
        
        shadow_color_btn.clicked.connect(pick_shadow_color)
        shadow_row.addWidget(shadow_color_btn)
        shadow_row.addStretch()
        group_layout.addLayout(shadow_row)
        
        outline_row = QHBoxLayout()
        outline_row.addWidget(QLabel("Outline:"))
        outline_combo = QComboBox()
        outline_combo.addItems(["none", "outline"])
        outline_combo.setToolTip("none=off | outline=4-way shadow border")
        if outline_style and outline_style != "none":
            outline_combo.setCurrentText("outline")
        else:
            outline_combo.setCurrentText("none")
        outline_row.addWidget(outline_combo)

        outline_color_btn = QPushButton()
        outline_color_btn.setFixedSize(60, 25)
        outline_color_btn.setStyleSheet("background-color: {};".format(outline_color))
        outline_color_btn.current_color = outline_color
        outline_color_btn.setAutoDefault(False)
        outline_color_btn.setDefault(False)
        outline_color_btn.setToolTip("Color of the outline")

        def pick_outline_color():
            col = QColorDialog.getColor(QColor(outline_color_btn.current_color), self)
            if col.isValid():
                outline_color_btn.current_color = col.name()
                outline_color_btn.setStyleSheet("background-color: {};".format(col.name()))

        outline_color_btn.clicked.connect(pick_outline_color)
        outline_row.addWidget(outline_color_btn)
        outline_row.addStretch()
        group_layout.addLayout(outline_row)

        layout.addWidget(group)
        
        return {
            "font": font_combo,
            "size": size_spin,
            "bold": bold_check,
            "italic": italic_check,
            "color": color_btn,
            "shadow_preset": shadow_combo,
            "shadow_color": shadow_color_btn,
            "outline": outline_combo,
            "outline_color": outline_color_btn
        }
    
    def apply_settings(self):
        LayoutConfig.TRIBUTE_IMAGE_SIZE = self.tribute_size.value()
        LayoutConfig.TRIBUTE_SPACING = self.tribute_spacing.value()
        LayoutConfig.DISTRICT_SPACING = self.district_spacing.value()
        LayoutConfig.EDGE_PADDING = self.edge_padding.value()
        
        radius_map = {"square": "0px", "rounded": "25px", "circle": "50px"}
        LayoutConfig.TRIBUTE_IMAGE_BORDER_RADIUS = radius_map[self.tribute_border_radius.currentText()]
        
        LayoutConfig.TRIBUTE_IMAGE_BORDER_ENABLED = self.tribute_border_enabled.isChecked()
        LayoutConfig.TRIBUTE_IMAGE_BORDER_WIDTH = self.tribute_border_width.value()
        LayoutConfig.TRIBUTE_IMAGE_BORDER_COLOR = self.tribute_border_color.current_color
        LayoutConfig.TRIBUTE_IMAGE_BORDER_STYLE = self.tribute_border_style.currentText()
        LayoutConfig.TRIBUTE_IMAGE_SHADOW_PRESET = self.tribute_image_shadow_preset.currentText()
        LayoutConfig.TRIBUTE_IMAGE_SHADOW_COLOR = self.tribute_image_shadow_color.current_color
        
        LayoutConfig.DEAD_TRIBUTE_IMAGE_EFFECT = self.dead_image_effect.currentText()
        LayoutConfig.DEAD_TRIBUTE_OPACITY = self.dead_opacity.value()
        LayoutConfig.DEAD_TRIBUTE_BORDER_ENABLED = self.dead_border_enabled.isChecked()
        LayoutConfig.DEAD_TRIBUTE_BORDER_WIDTH = self.dead_border_width.value()
        LayoutConfig.DEAD_TRIBUTE_BORDER_COLOR = self.dead_border_color.current_color
        LayoutConfig.DEAD_TRIBUTE_SHADOW_PRESET = self.dead_image_shadow_preset.currentText()
        LayoutConfig.DEAD_TRIBUTE_SHADOW_COLOR = self.dead_image_shadow_color.current_color
        LayoutConfig.DEAD_TRIBUTE_NAME_COLOR = self.dead_name_color.current_color
        
        LayoutConfig.DISTRICT_LABEL_FONT = self.district_font["font"].currentText()
        LayoutConfig.DISTRICT_LABEL_SIZE = self.district_font["size"].value()
        LayoutConfig.DISTRICT_LABEL_BOLD = self.district_font["bold"].isChecked()
        LayoutConfig.DISTRICT_LABEL_ITALIC = self.district_font["italic"].isChecked()
        LayoutConfig.DISTRICT_LABEL_COLOR = self.district_font["color"].current_color
        LayoutConfig.DISTRICT_LABEL_SHADOW_PRESET = self.district_font["shadow_preset"].currentText()
        LayoutConfig.DISTRICT_LABEL_SHADOW_COLOR = self.district_font["shadow_color"].current_color
        LayoutConfig.DISTRICT_LABEL_OUTLINE_STYLE = self.district_font["outline"].currentText()
        LayoutConfig.DISTRICT_LABEL_OUTLINE_COLOR = self.district_font["outline_color"].current_color
        
        LayoutConfig.TRIBUTE_NAME_FONT = self.tribute_name_font["font"].currentText()
        LayoutConfig.TRIBUTE_NAME_SIZE = self.tribute_name_font["size"].value()
        LayoutConfig.TRIBUTE_NAME_BOLD = self.tribute_name_font["bold"].isChecked()
        LayoutConfig.TRIBUTE_NAME_ITALIC = self.tribute_name_font["italic"].isChecked()
        LayoutConfig.TRIBUTE_NAME_COLOR = self.tribute_name_font["color"].current_color
        LayoutConfig.TRIBUTE_NAME_SHADOW_PRESET = self.tribute_name_font["shadow_preset"].currentText()
        LayoutConfig.TRIBUTE_NAME_SHADOW_COLOR = self.tribute_name_font["shadow_color"].current_color
        LayoutConfig.TRIBUTE_NAME_OUTLINE_STYLE = self.tribute_name_font["outline"].currentText()
        LayoutConfig.TRIBUTE_NAME_OUTLINE_COLOR = self.tribute_name_font["outline_color"].current_color
        
        LayoutConfig.TRIBUTE_STATUS_FONT = self.tribute_status_font["font"].currentText()
        LayoutConfig.TRIBUTE_STATUS_SIZE = self.tribute_status_font["size"].value()
        LayoutConfig.TRIBUTE_STATUS_BOLD = self.tribute_status_font["bold"].isChecked()
        LayoutConfig.TRIBUTE_STATUS_ITALIC = self.tribute_status_font["italic"].isChecked()
        LayoutConfig.TRIBUTE_STATUS_COLOR = self.tribute_status_font["color"].current_color
        LayoutConfig.TRIBUTE_STATUS_SHADOW_PRESET = self.tribute_status_font["shadow_preset"].currentText()
        LayoutConfig.TRIBUTE_STATUS_SHADOW_COLOR = self.tribute_status_font["shadow_color"].current_color
        LayoutConfig.TRIBUTE_STATUS_OUTLINE_STYLE = self.tribute_status_font["outline"].currentText()
        LayoutConfig.TRIBUTE_STATUS_OUTLINE_COLOR = self.tribute_status_font["outline_color"].current_color
        LayoutConfig.TRIBUTE_STATUS_DEAD_COLOR = self.tribute_status_dead.current_color
        
        LayoutConfig.REAPING_BG_COLOR = self.reaping_bg.current_color
        
        LayoutConfig.FEED_WIDTH = self.feed_width.value()
        LayoutConfig.FEED_PORTRAIT_HEIGHT = self.portrait_height.value()
        LayoutConfig.FEED_PORTRAIT_SPACING = self.portrait_spacing.value()
        
        radius_map = {"square": "0px", "rounded": "25px", "circle": "50px"}
        LayoutConfig.FEED_PORTRAIT_BORDER_RADIUS = radius_map[self.portrait_border_radius.currentText()]
        
        LayoutConfig.FEED_PORTRAIT_BORDER_ENABLED = self.portrait_border_enabled.isChecked()
        LayoutConfig.FEED_PORTRAIT_BORDER_WIDTH = self.portrait_border_width.value()
        LayoutConfig.FEED_PORTRAIT_BORDER_COLOR = self.portrait_border_color.current_color
        LayoutConfig.FEED_PORTRAIT_BORDER_STYLE = self.portrait_border_style.currentText()
        LayoutConfig.FEED_PORTRAIT_SHADOW_PRESET = self.portrait_shadow_preset.currentText()
        LayoutConfig.FEED_PORTRAIT_SHADOW_COLOR = self.portrait_shadow_color.current_color
        
        LayoutConfig.FEED_TITLE_FONT = self.feed_title_font["font"].currentText()
        LayoutConfig.FEED_TITLE_SIZE = self.feed_title_font["size"].value()
        LayoutConfig.FEED_TITLE_BOLD = self.feed_title_font["bold"].isChecked()
        LayoutConfig.FEED_TITLE_ITALIC = self.feed_title_font["italic"].isChecked()
        LayoutConfig.FEED_TITLE_COLOR = self.feed_title_font["color"].current_color
        LayoutConfig.FEED_TITLE_SHADOW_PRESET = self.feed_title_font["shadow_preset"].currentText()
        LayoutConfig.FEED_TITLE_SHADOW_COLOR = self.feed_title_font["shadow_color"].current_color
        LayoutConfig.FEED_TITLE_OUTLINE_STYLE = self.feed_title_font["outline"].currentText()
        LayoutConfig.FEED_TITLE_OUTLINE_COLOR = self.feed_title_font["outline_color"].current_color
        LayoutConfig.FEED_TITLE_BOX_BG_COLOR = self.feed_title_bg.current_color
        LayoutConfig.FEED_TITLE_BOX_BG_OPACITY = self.feed_title_bg_opacity.currentText()
        
        LayoutConfig.FEED_EVENT_TEXT_FONT = self.feed_text_font["font"].currentText()
        LayoutConfig.FEED_EVENT_TEXT_SIZE = self.feed_text_font["size"].value()
        LayoutConfig.FEED_EVENT_TEXT_BOLD = self.feed_text_font["bold"].isChecked()
        LayoutConfig.FEED_EVENT_TEXT_ITALIC = self.feed_text_font["italic"].isChecked()
        LayoutConfig.FEED_TEXT_COLOR = self.feed_text_font["color"].current_color
        LayoutConfig.FEED_EVENT_TEXT_SHADOW_PRESET = self.feed_text_font["shadow_preset"].currentText()
        LayoutConfig.FEED_EVENT_TEXT_SHADOW_COLOR = self.feed_text_font["shadow_color"].current_color
        LayoutConfig.FEED_EVENT_TEXT_OUTLINE_STYLE = self.feed_text_font["outline"].currentText()
        LayoutConfig.FEED_EVENT_TEXT_OUTLINE_COLOR = self.feed_text_font["outline_color"].current_color
        
        LayoutConfig.PROCEED_BUTTON_TEXT = self.proceed_text.text()
        LayoutConfig.PROCEED_BUTTON_FONT = self.proceed_font["font"].currentText()
        LayoutConfig.PROCEED_BUTTON_FONT_SIZE = self.proceed_font["size"].value()
        LayoutConfig.PROCEED_BUTTON_BOLD = self.proceed_font["bold"].isChecked()
        LayoutConfig.PROCEED_BUTTON_ITALIC = self.proceed_font["italic"].isChecked()
        LayoutConfig.PROCEED_BUTTON_COLOR = self.proceed_font["color"].current_color
        LayoutConfig.PROCEED_BUTTON_SHADOW_PRESET = self.proceed_font["shadow_preset"].currentText()
        LayoutConfig.PROCEED_BUTTON_SHADOW_COLOR = self.proceed_font["shadow_color"].current_color
        LayoutConfig.PROCEED_BUTTON_OUTLINE_STYLE = self.proceed_font["outline"].currentText()
        LayoutConfig.PROCEED_BUTTON_OUTLINE_COLOR = self.proceed_font["outline_color"].current_color
        LayoutConfig.PROCEED_BUTTON_HOVER_COLOR = self.proceed_hover.current_color
        LayoutConfig.PROCEED_BUTTON_MARGIN_TOP = self.proceed_margin.value()
        
        LayoutConfig.FEED_BG_COLOR = self.feed_bg.current_color
        
        LayoutConfig.SEASON_TITLE_SHOW = self.season_title_show.isChecked()
        LayoutConfig.SEASON_TITLE_TEXT = self.season_title_text.text()
        LayoutConfig.SEASON_TITLE_BOX_BG_COLOR = self.season_title_box_bg.current_color
        LayoutConfig.SEASON_TITLE_BOX_BG_OPACITY = self.season_title_bg_opacity.currentText()
        LayoutConfig.SEASON_TITLE_FONT = self.season_title_font["font"].currentText()
        LayoutConfig.SEASON_TITLE_SIZE = self.season_title_font["size"].value()
        LayoutConfig.SEASON_TITLE_BOLD = self.season_title_font["bold"].isChecked()
        LayoutConfig.SEASON_TITLE_ITALIC = self.season_title_font["italic"].isChecked()
        LayoutConfig.SEASON_TITLE_COLOR = self.season_title_font["color"].current_color
        LayoutConfig.SEASON_TITLE_SHADOW_PRESET = self.season_title_font["shadow_preset"].currentText()
        LayoutConfig.SEASON_TITLE_SHADOW_COLOR = self.season_title_font["shadow_color"].current_color
        LayoutConfig.SEASON_TITLE_OUTLINE_STYLE = self.season_title_font["outline"].currentText()
        LayoutConfig.SEASON_TITLE_OUTLINE_COLOR = self.season_title_font["outline_color"].current_color
        
        LayoutConfig.REAPING_TITLE_TEXT = self.reaping_phase_name.text()
        LayoutConfig.DAY_PHASE_NAME = self.day_phase_name.text()
        LayoutConfig.NIGHT_PHASE_NAME = self.night_phase_name.text()
        LayoutConfig.WIN_SCREEN_NAME = self.winner_phase_name.text()
        
        LayoutConfig.DISTRICT_NAMES = {}
        for district_num, name_edit in self.district_name_inputs.items():
            name = name_edit.text().strip()
            if name:
                LayoutConfig.DISTRICT_NAMES[district_num] = name
        
        for config_key, path_edit in self.bg_image_inputs.items():
            setattr(LayoutConfig, config_key, path_edit.text().strip())
        
        LayoutConfig.REAPING_BG_X_OFFSET = self.reaping_bg_x.text()
        LayoutConfig.REAPING_BG_Y_OFFSET = self.reaping_bg_y.text()
        LayoutConfig.FEED_BG_X_OFFSET = self.feed_bg_x.text()
        LayoutConfig.FEED_BG_Y_OFFSET = self.feed_bg_y.text()
        
        LayoutConfig.PLACEMENTS_TRIBUTE_IMAGE_SIZE = self.placements_image_size.value()
        LayoutConfig.PLACEMENTS_TRIBUTE_SPACING = self.placements_spacing.value()
        LayoutConfig.PLACEMENTS_ROW_SPACING = self.placements_row_spacing.value()
        LayoutConfig.PLACEMENTS_EDGE_PADDING = self.placements_edge_padding.value()
        
        radius_map = {"square": "0px", "rounded": "25px", "circle": "50px"}
        LayoutConfig.PLACEMENTS_IMAGE_BORDER_RADIUS = radius_map[self.placements_border_radius.currentText()]
        
        LayoutConfig.PLACEMENTS_IMAGE_BORDER_ENABLED = self.placements_border_enabled.isChecked()
        LayoutConfig.PLACEMENTS_IMAGE_BORDER_WIDTH = self.placements_border_width.value()
        LayoutConfig.PLACEMENTS_IMAGE_BORDER_COLOR = self.placements_border_color.current_color
        LayoutConfig.PLACEMENTS_IMAGE_BORDER_STYLE = self.placements_border_style.currentText()
        
        LayoutConfig.PLACEMENTS_NAME_FONT = self.placements_name_font["font"].currentText()
        LayoutConfig.PLACEMENTS_NAME_SIZE = self.placements_name_font["size"].value()
        LayoutConfig.PLACEMENTS_NAME_BOLD = self.placements_name_font["bold"].isChecked()
        LayoutConfig.PLACEMENTS_NAME_ITALIC = self.placements_name_font["italic"].isChecked()
        LayoutConfig.PLACEMENTS_NAME_COLOR = self.placements_name_font["color"].current_color
        LayoutConfig.PLACEMENTS_NAME_SHADOW_PRESET = self.placements_name_font["shadow_preset"].currentText()
        LayoutConfig.PLACEMENTS_NAME_SHADOW_COLOR = self.placements_name_font["shadow_color"].current_color
        LayoutConfig.PLACEMENTS_NAME_OUTLINE_STYLE = self.placements_name_font["outline"].currentText()
        LayoutConfig.PLACEMENTS_NAME_OUTLINE_COLOR = self.placements_name_font["outline_color"].current_color
        
        LayoutConfig.PLACEMENTS_RANK_FONT = self.placements_rank_font["font"].currentText()
        LayoutConfig.PLACEMENTS_RANK_SIZE = self.placements_rank_font["size"].value()
        LayoutConfig.PLACEMENTS_RANK_BOLD = self.placements_rank_font["bold"].isChecked()
        LayoutConfig.PLACEMENTS_RANK_ITALIC = self.placements_rank_font["italic"].isChecked()
        LayoutConfig.PLACEMENTS_RANK_COLOR = self.placements_rank_font["color"].current_color
        LayoutConfig.PLACEMENTS_RANK_SHADOW_PRESET = self.placements_rank_font["shadow_preset"].currentText()
        LayoutConfig.PLACEMENTS_RANK_SHADOW_COLOR = self.placements_rank_font["shadow_color"].current_color
        LayoutConfig.PLACEMENTS_RANK_OUTLINE_STYLE = self.placements_rank_font["outline"].currentText()
        LayoutConfig.PLACEMENTS_RANK_OUTLINE_COLOR = self.placements_rank_font["outline_color"].current_color
        
        LayoutConfig.PLACEMENTS_DISTRICT_FONT = self.placements_district_font["font"].currentText()
        LayoutConfig.PLACEMENTS_DISTRICT_SIZE = self.placements_district_font["size"].value()
        LayoutConfig.PLACEMENTS_DISTRICT_BOLD = self.placements_district_font["bold"].isChecked()
        LayoutConfig.PLACEMENTS_DISTRICT_ITALIC = self.placements_district_font["italic"].isChecked()
        LayoutConfig.PLACEMENTS_DISTRICT_COLOR = self.placements_district_font["color"].current_color
        LayoutConfig.PLACEMENTS_DISTRICT_SHADOW_PRESET = self.placements_district_font["shadow_preset"].currentText()
        LayoutConfig.PLACEMENTS_DISTRICT_SHADOW_COLOR = self.placements_district_font["shadow_color"].current_color
        LayoutConfig.PLACEMENTS_DISTRICT_OUTLINE_STYLE = self.placements_district_font["outline"].currentText()
        LayoutConfig.PLACEMENTS_DISTRICT_OUTLINE_COLOR = self.placements_district_font["outline_color"].current_color
        
        LayoutConfig.PLACEMENTS_KILLS_FONT = self.placements_kills_font["font"].currentText()
        LayoutConfig.PLACEMENTS_KILLS_SIZE = self.placements_kills_font["size"].value()
        LayoutConfig.PLACEMENTS_KILLS_BOLD = self.placements_kills_font["bold"].isChecked()
        LayoutConfig.PLACEMENTS_KILLS_ITALIC = self.placements_kills_font["italic"].isChecked()
        LayoutConfig.PLACEMENTS_KILLS_COLOR = self.placements_kills_font["color"].current_color
        LayoutConfig.PLACEMENTS_KILLS_SHADOW_PRESET = self.placements_kills_font["shadow_preset"].currentText()
        LayoutConfig.PLACEMENTS_KILLS_SHADOW_COLOR = self.placements_kills_font["shadow_color"].current_color
        LayoutConfig.PLACEMENTS_KILLS_OUTLINE_STYLE = self.placements_kills_font["outline"].currentText()
        LayoutConfig.PLACEMENTS_KILLS_OUTLINE_COLOR = self.placements_kills_font["outline_color"].current_color
        
        LayoutConfig.PLACEMENTS_BG_COLOR = self.placements_bg.current_color
