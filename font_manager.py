#font_manager.py
import base64
import sys
import os
from pathlib import Path

class FontManager:
    _loaded_fonts = {}
    
    @classmethod
    def _get_base_path(cls):
        if getattr(sys, 'frozen', False):
            return Path(sys.executable).parent
        return Path(__file__).parent
    
    @classmethod
    def init(cls):
        fonts_dir = cls._get_base_path() / "fonts"
        print(f"looking for fonts in: {fonts_dir}")
        print(f"folder exists: {fonts_dir.exists()}")
        if not fonts_dir.exists():
            print(f"no fonts folder, whatever")
            return
        
        for font_file in list(fonts_dir.glob("*.ttf")) + list(fonts_dir.glob("*.otf")):
            name = font_file.stem.replace('_', ' ').replace('-', ' ')
            cls._loaded_fonts[name] = font_file
        
        print(f"loaded {len(cls._loaded_fonts)} fonts")
    
    @classmethod
    def load_more(cls, directory):
        count = 0
        for font_file in list(Path(directory).glob("*.ttf")) + list(Path(directory).glob("*.otf")):
            name = font_file.stem.replace('_', ' ').replace('-', ' ')
            if name not in cls._loaded_fonts:
                cls._loaded_fonts[name] = font_file
                count += 1
        return count
    
    @classmethod
    def gimme_css(cls, fonts_in_use):
        css = []
        for name in fonts_in_use:
            if name in cls._loaded_fonts:
                with open(cls._loaded_fonts[name], 'rb') as f:
                    data = base64.b64encode(f.read()).decode()
                css.append(f"@font-face{{font-family:'{name}';src:url(data:font/truetype;base64,{data})}}")
        return '\n'.join(css)
    
    @classmethod
    def all_fonts(cls):
        return sorted(cls._loaded_fonts.keys())

FontManager.init()
