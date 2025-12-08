"""
單元測試 (Unit Tests)
=====================

用於測試多風格 AI 繪圖生成器的各個功能模塊
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import torch
from PIL import Image

from multi_style_image_generator import (
    SystemConfig,
    StyleModelsConfig,
    TranslationModule,
    ImageProcessor,
    ModelManager,
    MultiStyleImageGenerator
)


# ============================================================================
# 測試 SystemConfig
# ============================================================================

class TestSystemConfig:
    """測試系統配置類"""
    
    def test_config_initialization(self):
        """測試配置初始化"""
        config = SystemConfig()
        
        assert config.device in ["cuda", "cpu"]
        assert config.torch_dtype in [torch.float16, torch.float32]
        assert isinstance(config.project_root, Path)
    
    def test_directories_creation(self):
        """測試目錄創建"""
        config = SystemConfig()
        
        assert config.output_dir.exists()
        assert config.logs_dir.exists()
        assert config.models_cache_dir.exists()


# ============================================================================
# 測試 StyleModelsConfig
# ============================================================================

class TestStyleModelsConfig:
    """測試風格模型配置類"""
    
    def test_style_models_defined(self):
        """測試風格模型已定義"""
        styles = StyleModelsConfig.STYLE_MODELS
        
        assert len(styles) > 0
        assert '二次元動漫' in styles
        assert '寫實風格' in styles
    
    def test_is_valid_style(self):
        """測試風格驗證"""
        assert StyleModelsConfig.is_valid_style('二次元動漫') == True
        assert StyleModelsConfig.is_valid_style('無效風格') == False
    
    def test_get_model_id(self):
        """測試獲取模型 ID"""
        model_id = StyleModelsConfig.get_model_id('二次元動漫')
        
        assert isinstance(model_id, str)
        assert len(model_id) > 0
    
    def test_invalid_style_raises_error(self):
        """測試無效風格拋出異常"""
        with pytest.raises(ValueError):
            StyleModelsConfig.get_model_id('無效風格')


# ============================================================================
# 測試 TranslationModule
# ============================================================================

class TestTranslationModule:
    """測試翻譯模塊"""
    
    def test_translation_module_initialization(self):
        """測試翻譯模塊初始化"""
        translator = TranslationModule()
        
        assert translator.translator is not None
        assert isinstance(translator.translation_cache, dict)
    
    @patch('deep_translator.GoogleTranslator.translate')
    def test_translate_prompt(self, mock_translate):
        """測試提示詞翻譯"""
        mock_translate.return_value = "A blue-haired girl reading in a library"
        
        translator = TranslationModule()
        result = translator.translate_prompt("一個在圖書館看書的藍髮少女")
        
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_translation_caching(self):
        """測試翻譯緩存"""
        translator = TranslationModule()
        
        # 手動添加到緩存
        test_text = "測試"
        cached_translation = "Test"
        translator.translation_cache[test_text] = cached_translation
        
        # 使用緩存
        result = translator.translate_prompt(test_text, use_cache=True)
        
        assert result == cached_translation


# ============================================================================
# 測試 ImageProcessor
# ============================================================================

class TestImageProcessor:
    """測試圖片處理模塊"""
    
    def create_test_image(self, width=256, height=256):
        """創建測試圖片"""
        return Image.new('RGB', (width, height), color='red')
    
    def test_create_image_grid(self):
        """測試圖片網格創建"""
        images = [self.create_test_image() for _ in range(4)]
        
        grid = ImageProcessor.create_image_grid(images, rows=2, cols=2)
        
        assert isinstance(grid, Image.Image)
        assert grid.size == (512, 512)
    
    def test_image_grid_incorrect_dimensions(self):
        """測試不正確的網格尺寸拋出異常"""
        images = [self.create_test_image() for _ in range(3)]
        
        with pytest.raises(ValueError):
            ImageProcessor.create_image_grid(images, rows=2, cols=2)
    
    def test_save_images(self, tmp_path):
        """測試圖片保存"""
        images = [self.create_test_image() for _ in range(4)]
        
        saved_files = ImageProcessor.save_images(
            images,
            tmp_path,
            prefix="test",
            save_grid=True
        )
        
        assert len(saved_files) > 0
        assert 'image_1' in saved_files
        assert 'grid' in saved_files


# ============================================================================
# 測試 ModelManager
# ============================================================================

class TestModelManager:
    """測試模型管理器"""
    
    def test_model_manager_initialization(self):
        """測試模型管理器初始化"""
        config = SystemConfig()
        manager = ModelManager(config)
        
        assert manager.config is not None
        assert manager.current_pipeline is None
        assert manager.current_model_id is None
    
    @patch('diffusers.StableDiffusionPipeline.from_pretrained')
    def test_model_loading(self, mock_from_pretrained):
        """測試模型加載"""
        mock_pipeline = MagicMock()
        mock_from_pretrained.return_value = mock_pipeline
        
        config = SystemConfig()
        manager = ModelManager(config)
        
        model_id = 'test-model/id'
        # 這會調用 mocked 版本
        # result = manager.load_model(model_id)
        # assert result is not None


# ============================================================================
# 測試 MultiStyleImageGenerator
# ============================================================================

class TestMultiStyleImageGenerator:
    """測試主生成器類"""
    
    def test_generator_initialization(self):
        """測試生成器初始化"""
        generator = MultiStyleImageGenerator()
        
        assert generator.config is not None
        assert generator.model_manager is not None
        assert generator.translation_module is not None
        assert generator.engine is not None
        assert generator.logger is not None


# ============================================================================
# 集成測試
# ============================================================================

class TestIntegration:
    """集成測試"""
    
    def test_style_models_consistency(self):
        """測試風格模型一致性"""
        styles = StyleModelsConfig.STYLE_MODELS
        descriptions = StyleModelsConfig.STYLE_DESCRIPTIONS
        
        # 所有風格都應該有描述
        for style in styles:
            assert style in descriptions


# ============================================================================
# 測試運行
# ============================================================================

def run_tests():
    """運行所有測試"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
