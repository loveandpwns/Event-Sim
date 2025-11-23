from PySide6.QtCore import QTimer, QUrl
from PySide6.QtWidgets import QFileDialog, QMessageBox, QApplication
from PySide6.QtGui import QGuiApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from pathlib import Path
import os
import re

class ScreenshotCapture:
    def __init__(self, main_window):
        self.main = main_window
        self.temp_view = None
        self.fpath = None
        self.remaining = []
        self.folder = ""
        self.idx = 0
    
    def capture_current(self):
        if not self.main.sim:
            self.main.confirm_all()
        if not self.main.sim or not hasattr(self.main, 'center_stack'):
            if hasattr(self.main, 'districts') and self.main.districts:
                self.main.reaping_view.page().toHtml(lambda html: self.got_html(html, self.main.reaping_view))
            else:
                QMessageBox.warning(self.main, "Screenshot", "No content to screenshot!")
            return
        
        current_view = self.main.reaping_view if self.main.center_stack.currentIndex() == 0 else self.main.feed_view
        current_view.page().toHtml(lambda html: self.got_html(html, current_view))
    
    def got_html(self, html, source_view):
        match = re.search(r'<div class="phase-title">([^<]+)</div>', html)
        if match:
            phase_name = match.group(1).strip().replace(" ", "_").replace("/", "-")
        else:
            phase_name = "Preview"
        
        print(f"\nSCREENSHOT: {phase_name}")
        
        filepath, _ = QFileDialog.getSaveFileName(
            self.main, "Save Screenshot",
            f"{phase_name}.png",
            "PNG Images (*.png);;JPEG Images (*.jpg)"
        )
        
        if not filepath:
            return
        
        self.fpath = filepath
        
        if source_view == self.main.feed_view:
            height = getattr(self.main, 'last_feed_height', 2000)
        else:
            height = getattr(self.main, 'last_reaping_height', 2000)
        
        print("using height:", height)
        
        from layout_config import LayoutConfig
        width = LayoutConfig.FEED_WIDTH if source_view == self.main.feed_view else LayoutConfig.REAPING_MAX_WIDTH
        
        html = re.sub(r'<script src="qrc:///qtwebchannel/qwebchannel\.js"></script>', '', html)
        html = re.sub(r'<script>.*?new QWebChannel.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'onclick="callBridge\(.*?\)"', '', html)
        
        self.temp_view = QWebEngineView()
        self.temp_view.setFixedSize(width, height)
        self.temp_view.move(-50000, -50000) #offscreen
        
        self.temp_view.page().settings().setAttribute(
            self.temp_view.page().settings().WebAttribute.ShowScrollBars, False
        )
        
        print(f"temp view created {width}x{height}")
        
        self.temp_view.loadFinished.connect(self.on_load)
        
        base_url = QUrl.fromLocalFile(str(Path.cwd()) + "/")
        self.temp_view.setHtml(html, base_url)
    
    def on_load(self, success):
        if not success:
            print("load failed")
            if self.temp_view:
                self.temp_view.deleteLater()
            self.temp_view = None
            QMessageBox.warning(self.main, "Screenshot", "Failed to load page!")
            return
        
        self.temp_view.show()
        
        print("loaded, grabbing...")
        QTimer.singleShot(500, self.grab) #wait for render
    
    def grab(self):
        pixmap = self.temp_view.grab()
        print(f"grabbed {pixmap.width()}x{pixmap.height()}")
        
        success = pixmap.save(self.fpath)
        
        if success:
            print("saved", pixmap.width(), pixmap.height())
            QMessageBox.information(self.main, "Screenshot", f"Saved:\n{self.fpath}")
            
            self.temp_view.deleteLater()
            self.temp_view = None
        else:
            self.temp_view.deleteLater()
            self.temp_view = None
            QMessageBox.warning(self.main, "Screenshot", "Save failed!")
    
    def capture_all(self):
        if not self.main.sim:
            self.main.confirm_all()
        folder = QFileDialog.getExistingDirectory(self.main, "Select Folder for Screenshots")
        if not folder:
            return
        
        on_preview = not self.main.sim or not hasattr(self.main, 'center_stack')
        
        if on_preview:
            if not hasattr(self.main, 'districts') or not self.main.districts:
                QMessageBox.warning(self.main, "Screenshot All", "Generate tributes first!")
                return
            
            preview_filepath = os.path.join(folder, "000_Preview.png")
            self.main.reaping_view.page().toHtml(lambda html: self.cap_preview(html, folder))
            return
        
        self.continue_all(folder, start_index=0)
    
    def cap_preview(self, html, folder):
        preview_filepath = os.path.join(folder, "000_Preview.png")
        self.fpath = preview_filepath
        
        from layout_config import LayoutConfig
        width = LayoutConfig.REAPING_MAX_WIDTH
        height = getattr(self.main, 'last_reaping_height', 2000)
        
        html = re.sub(r'<script src="qrc:///qtwebchannel/qwebchannel\.js"></script>', '', html)
        html = re.sub(r'<script>.*?new QWebChannel.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'onclick="callBridge\(.*?\)"', '', html)
        
        self.temp_view = QWebEngineView()
        self.temp_view.setFixedSize(width, height)
        self.temp_view.move(-50000, -50000)
        self.temp_view.page().settings().setAttribute(
            self.temp_view.page().settings().WebAttribute.ShowScrollBars, False
        )
        
        self.pending_folder = folder
        self.temp_view.loadFinished.connect(self.preview_done)
        
        from pathlib import Path
        from PySide6.QtCore import QUrl
        base_url = QUrl.fromLocalFile(str(Path.cwd()) + "/")
        self.temp_view.setHtml(html, base_url)
    
    def preview_done(self, success):
        if not success:
            print("preview failed")
            self.continue_all(self.pending_folder, start_index=0)
            return
        
        self.temp_view.show()
        QTimer.singleShot(500, self.save_preview) #wait for render
    
    def save_preview(self):
        pixmap = self.temp_view.grab()
        pixmap.save(self.fpath)
        print("saved preview")
        
        self.temp_view.deleteLater()
        self.temp_view = None
        
        self.main.start_simulation()
        self.continue_all(self.pending_folder, start_index=0)
    
    def continue_all(self, folder, start_index):
        if self.main.sim._s.phase.kind.name == "REAPING":
            self.main.sim.step()
        
        while self.main.sim.can_step():
            self.main.sim.step()
        
        for ui_t in self.main.roster:
            eng_t = next((t for t in self.main.sim._s.tributes.values()
                          if t.display_name == ui_t.name), None)
            if eng_t:
                ui_t.alive = eng_t.alive
        
        timeline = self.main.sim.timeline()
        self.remaining = []
        
        for idx in range(start_index, len(timeline)):
            phase_result = timeline[idx]
            phase_name = phase_result.title.replace(" ", "_").replace("/", "-")
            filepath = os.path.join(folder, f"{idx:03d}_{phase_name}.png")
            self.remaining.append((idx, filepath, phase_result))
        
        self.folder = folder
        self.idx = 0
        self.next_batch()
    
    def next_batch(self):
        if self.idx >= len(self.remaining):
            if hasattr(self.main, 'center_stack'):
                last_idx = len(self.remaining) - 1
                last_phase_idx = self.remaining[last_idx][0]
                self.main.on_nav_select(last_phase_idx)
            
            QMessageBox.information(
                self.main, "Screenshot All", 
                f"Saved {len(self.remaining) + 1} screenshots to:\n{self.folder}"
            )
            return
        
        idx, filepath, phase_result = self.remaining[self.idx]
        
        self.main.on_nav_select(idx)
        
        QTimer.singleShot(1500, lambda: self.batch_shot(filepath)) #wait longer for full render
    
    def batch_shot(self, filepath):
        current_view = self.main.reaping_view if self.main.center_stack.currentIndex() == 0 else self.main.feed_view
        
        current_view.page().toHtml(lambda html: self.batch_html(html, current_view, filepath))
    
    def batch_html(self, html, source_view, filepath):
        self.fpath = filepath
        
        if source_view == self.main.feed_view:
            height = getattr(self.main, 'last_feed_height', 2000)
        else:
            height = getattr(self.main, 'last_reaping_height', 2000)
        
        print(f"batch {self.idx + 1}/{len(self.remaining)} h={height}")
        
        from layout_config import LayoutConfig
        width = LayoutConfig.FEED_WIDTH if source_view == self.main.feed_view else LayoutConfig.REAPING_MAX_WIDTH
        
        html = re.sub(r'<script src="qrc:///qtwebchannel/qwebchannel\.js"></script>', '', html)
        html = re.sub(r'<script>.*?new QWebChannel.*?</script>', '', html, flags=re.DOTALL)
        html = re.sub(r'onclick="callBridge\(.*?\)"', '', html)
        
        self.temp_view = QWebEngineView()
        self.temp_view.setFixedSize(width, height)
        self.temp_view.move(-50000, -50000)
        self.temp_view.page().settings().setAttribute(
            self.temp_view.page().settings().WebAttribute.ShowScrollBars, False
        )
        
        self.temp_view.loadFinished.connect(self.batch_load)
        
        base_url = QUrl.fromLocalFile(str(Path.cwd()) + "/")
        self.temp_view.setHtml(html, base_url)
    
    def batch_load(self, success):
        if not success:
            print("batch load failed, skip")
            self.idx += 1
            QTimer.singleShot(100, self.next_batch)
            return
        
        self.temp_view.show()
        QTimer.singleShot(500, self.batch_grab) #wait for render
    
    def batch_grab(self):
        pixmap = self.temp_view.grab()
        
        self.temp_view.deleteLater()
        self.temp_view = None
        
        success = pixmap.save(self.fpath)
        
        if success:
            print(f"saved batch {self.idx + 1}/{len(self.remaining)}")
        
        QApplication.processEvents()
        
        self.idx += 1
        QTimer.singleShot(100, self.next_batch)
