# coding: utf-8
"""
多風格 AI 繪圖生成器 (Multi-Style AI Image Generator)
========================================================

使用 Hugging Face Diffusers 和 Stable Diffusion 創建支持多種藝術風格的 AI 繪圖生成器。

功能特色:
    - 支持中文提示詞自動翻譯成英文
    - 支持多種預訓練模型風格選擇（寫實、動漫、夢幻、3D、油畫）
    - 支持批次生成與網格顯示
    - GPU 加速和記憶體優化（float16 精度）
    - 完整的錯誤處理和日誌記錄

版本: 1.0
作者: AI Assistant
日期: 2025-12-06
"""

import torch
import numpy as np
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageDraw
from deep_translator import GoogleTranslator
from typing import List, Tuple, Optional, Dict
import os
import sys
from pathlib import Path
from datetime import datetime
import json


# ============================================================================
# 第 1 部分：系統配置和初始化
# ============================================================================

class SystemConfig:
    """系統配置類別"""
    
    def __init__(self):
        """初始化系統配置"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        self.project_root = Path(__file__).parent
        self.output_dir = self.project_root / "generated_images"
        self.logs_dir = self.project_root / "logs"
        self.models_cache_dir = self.project_root / "models_cache"
        
        # 創建必要的目錄
        self._create_directories()
    
    def _create_directories(self):
        """創建專案所需的目錄"""
        for directory in [self.output_dir, self.logs_dir, self.models_cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def print_system_info(self):
        """打印系統信息"""
        print("\n" + "="*70)
        print("【系統信息】")
        print("="*70)
        print(f"PyTorch 版本: {torch.__version__}")
        print(f"使用設備: {self.device.upper()}")
        print(f"數據類型: {self.torch_dtype}")
        
        if torch.cuda.is_available():
            print(f"GPU 設備: {torch.cuda.get_device_name(0)}")
            print(f"GPU 總記憶體: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
            print(f"可用記憶體: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        else:
            print("[WARNING] 未檢測到 CUDA GPU，將使用 CPU（速度較慢）")
        
        print(f"專案根目錄: {self.project_root}")
        print(f"輸出目錄: {self.output_dir}")
        print("="*70 + "\n")


# ============================================================================
# 第 2 部分：風格模型配置
# ============================================================================

class StyleModelsConfig:
    """風格模型配置類別"""
    
    # 定義所有可用的風格和對應的模型 ID
    STYLE_MODELS: Dict[str, str] = {
        '寫實風格': 'runwayml/stable-diffusion-v1-5',
        '二次元動漫': 'hakurei/waifu-diffusion',
        '夢幻藝術': 'dreamlike-art/dreamlike-diffusion-1.0',
        '3D渲染': 'runwayml/stable-diffusion-v1-5',
        '油畫風格': 'runwayml/stable-diffusion-v1-5'
    }
    
    # 風格描述信息
    STYLE_DESCRIPTIONS: Dict[str, str] = {
        '寫實風格': '高質量的寫實攝影風格，適合生成逼真的人物和場景',
        '二次元動漫': '日本動漫風格，適合生成可愛的動畫人物',
        '夢幻藝術': '神幻夢幻風格，適合生成超現實和藝術作品',
        '3D渲染': '3D CGI 風格，適合生成逼真的三維渲染效果',
        '油畫風格': '宮崎駿風格的油畫藝術風格'
    }
    
    @classmethod
    def print_available_styles(cls):
        """打印所有可用的風格"""
        print("\n" + "="*70)
        print("【可用的風格列表】")
        print("="*70)
        for idx, (style_name, model_id) in enumerate(cls.STYLE_MODELS.items(), 1):
            description = cls.STYLE_DESCRIPTIONS.get(style_name, "")
            print(f"\n{idx}. 【{style_name}】")
            print(f"   模型 ID: {model_id}")
            print(f"   描述: {description}")
        print("\n" + "="*70 + "\n")
    
    @classmethod
    def is_valid_style(cls, style_name: str) -> bool:
        """檢查風格是否有效"""
        return style_name in cls.STYLE_MODELS
    
    @classmethod
    def get_model_id(cls, style_name: str) -> str:
        """獲取風格對應的模型 ID"""
        if not cls.is_valid_style(style_name):
            raise ValueError(
                f"不支持的風格: '{style_name}'\n"
                f"支持的風格有: {', '.join(cls.STYLE_MODELS.keys())}"
            )
        return cls.STYLE_MODELS[style_name]


# ============================================================================
# 第 3 部分：翻譯模塊
# ============================================================================

class TranslationModule:
    """翻譯模塊 - 將中文提示詞翻譯為英文"""
    
    def __init__(self):
        """初始化翻譯器"""
        self.translator = GoogleTranslator(source_language='zh-CN', target_language='en')
        self.translation_cache: Dict[str, str] = {}
    
    def translate_prompt(self, text: str, use_cache: bool = True) -> str:
        """
        將中文提示詞翻譯成英文
        
        參數:
            text (str): 中文提示詞
            use_cache (bool): 是否使用緩存翻譯結果
        
        返回:
            str: 翻譯後的英文提示詞
        
        異常:
            Exception: 翻譯失敗時拋出異常
        """
        # 檢查是否已在緩存中
        if use_cache and text in self.translation_cache:
            print(f"[OK] 使用緩存翻譯結果")
            return self.translation_cache[text]
        
        try:
            # 執行翻譯
            translated_text = self.translator.translate(text)
            
            # 存儲到緩存
            if use_cache:
                self.translation_cache[text] = translated_text
            
            return translated_text
        
        except Exception as e:
            print(f"[WARNING] 翻譯出錯: {e}")
            print(f"將使用原文作為提示詞")
            return text
    
    def print_translation_result(self, chinese: str, english: str):
        """打印翻譯結果"""
        print(f"\n【翻譯結果】")
        print(f"原文 (中文): {chinese}")
        print(f"譯文 (英文): {english}")


# ============================================================================
# 第 4 部分：圖片處理模塊
# ============================================================================

class ImageProcessor:
    """圖片處理模塊"""
    
    @staticmethod
    def create_image_grid(imgs: List[Image.Image], rows: int, cols: int) -> Image.Image:
        """
        將多張圖片組合成網格顯示
        
        參數:
            imgs (List[Image.Image]): PIL Image 物件列表
            rows (int): 網格行數
            cols (int): 網格列數
        
        返回:
            Image.Image: 組合後的網格圖片
        
        異常:
            ValueError: 當圖片數量不符合網格尺寸時拋出異常
        """
        if len(imgs) != rows * cols:
            raise ValueError(
                f"圖片數量 ({len(imgs)}) 不符合網格尺寸 ({rows}x{cols}={rows*cols})"
            )
        
        # 獲取第一張圖片的尺寸
        w, h = imgs[0].size
        
        # 計算網格的總尺寸
        grid_width = cols * w
        grid_height = rows * h
        grid = Image.new('RGB', size=(grid_width, grid_height))
        
        # 將每張圖片貼到對應的位置
        for i, img in enumerate(imgs):
            x = (i % cols) * w
            y = (i // cols) * h
            grid.paste(img, box=(x, y))
        
        return grid
    
    @staticmethod
    def add_grid_labels(grid: Image.Image, rows: int, cols: int) -> Image.Image:
        """
        在網格圖片上添加標籤
        
        參數:
            grid (Image.Image): 網格圖片
            rows (int): 行數
            cols (int): 列數
        
        返回:
            Image.Image: 帶有標籤的網格圖片
        """
        # 創建可繪圖物件
        draw = ImageDraw.Draw(grid)
        
        # 圖片尺寸
        w = grid.width // cols
        h = grid.height // rows
        
        # 添加標籤
        for i in range(rows * cols):
            x = (i % cols) * w
            y = (i // cols) * h
            label = f"#{i + 1}"
            
            # 在圖片左上角添加標籤
            draw.text(
                (x + 10, y + 10),
                label,
                fill=(255, 255, 255),
                font=None
            )
        
        return grid
    
    @staticmethod
    def save_images(
        images: List[Image.Image],
        output_dir: Path,
        prefix: str = "generated",
        save_grid: bool = True,
        grid_rows: int = 2,
        grid_cols: int = 2
    ) -> Dict[str, Path]:
        """
        保存生成的圖片
        
        參數:
            images (List[Image.Image]): 圖片列表
            output_dir (Path): 輸出目錄
            prefix (str): 文件名前綴
            save_grid (bool): 是否保存網格圖片
            grid_rows (int): 網格行數
            grid_cols (int): 網格列數
        
        返回:
            Dict[str, Path]: 保存的文件路徑字典
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        saved_files = {}
        
        # 創建時間戳目錄
        time_dir = output_dir / timestamp
        time_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存單張圖片
        for idx, img in enumerate(images, 1):
            filename = f"{prefix}_{idx:02d}.png"
            filepath = time_dir / filename
            img.save(filepath)
            saved_files[f"image_{idx}"] = filepath
            print(f"[OK] 已保存: {filepath}")
        
        # 保存網格圖片
        if save_grid and len(images) == grid_rows * grid_cols:
            try:
                grid = ImageProcessor.create_image_grid(images, grid_rows, grid_cols)
                grid_filename = f"{prefix}_grid.png"
                grid_filepath = time_dir / grid_filename
                grid.save(grid_filepath)
                saved_files["grid"] = grid_filepath
                print(f"[OK] 已保存網格圖片: {grid_filepath}")
            except Exception as e:
                print(f"[WARNING] 保存網格圖片失敗: {e}")
        
        return saved_files


# ============================================================================
# 第 5 部分：模型管理模塊
# ============================================================================

class ModelManager:
    """模型管理類別 - 負責模型的載入和卸載"""
    
    def __init__(self, config: SystemConfig):
        """
        初始化模型管理器
        
        參數:
            config (SystemConfig): 系統配置
        """
        self.config = config
        self.current_pipeline = None
        self.current_model_id = None
    
    def load_model(self, model_id: str) -> StableDiffusionPipeline:
        """
        載入 Stable Diffusion 模型
        
        參數:
            model_id (str): Hugging Face 模型 ID
        
        返回:
            StableDiffusionPipeline: 載入的模型管道
        
        異常:
            Exception: 模型載入失敗時拋出異常
        """
        # 如果已經載入相同的模型，直接返回
        if self.current_model_id == model_id and self.current_pipeline is not None:
            print(f"[OK] 模型已載入（使用緩存）")
            return self.current_pipeline
        
        # 卸載舊模型
        if self.current_pipeline is not None:
            self.unload_model()
        
        print(f"正在載入模型: {model_id}")
        
        try:
            # 載入模型
            pipeline = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=self.config.torch_dtype,
                safety_checker=None,
                cache_dir=str(self.config.models_cache_dir)
            )
            
            # 設置為評估模式
            pipeline = pipeline.to(self.config.device)
            pipeline.enable_attention_slicing()
            
            # 保存當前模型信息
            self.current_pipeline = pipeline
            self.current_model_id = model_id
            
            print(f"[OK] 模型載入成功")
            print(f"[OK] 模型已移至 {self.config.device.upper()}")
            
            return pipeline
        
        except Exception as e:
            print(f"[ERROR] 模型載入失敗: {e}")
            raise
    
    def unload_model(self):
        """卸載當前模型並釋放 GPU 記憶體"""
        if self.current_pipeline is not None:
            del self.current_pipeline
            self.current_pipeline = None
            self.current_model_id = None
            
            # 清除 GPU 記憶體
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            print("[OK] 模型已卸載，記憶體已釋放")


# ============================================================================
# 第 6 部分：圖片生成引擎
# ============================================================================

class ImageGenerationEngine:
    """圖片生成引擎 - 負責 AI 圖片生成的核心邏輯"""
    
    def __init__(
        self,
        config: SystemConfig,
        model_manager: ModelManager,
        translation_module: TranslationModule
    ):
        """
        初始化圖片生成引擎
        
        參數:
            config (SystemConfig): 系統配置
            model_manager (ModelManager): 模型管理器
            translation_module (TranslationModule): 翻譯模塊
        """
        self.config = config
        self.model_manager = model_manager
        self.translation_module = translation_module
        self.image_processor = ImageProcessor()
    
    def generate_images(
        self,
        prompt_text: str,
        style_name: str,
        num_images: int = 4,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        height: int = 512,
        width: int = 512,
        seed: Optional[int] = None,
        save_output: bool = True
    ) -> Dict:
        """
        根據中文提示詞和風格生成 AI 圖片
        
        參數:
            prompt_text (str): 中文提示詞
            style_name (str): 風格名稱
            num_images (int): 生成的圖片數量（默認 4 張）
            num_inference_steps (int): 推理步數（默認 30）
            guidance_scale (float): 提示詞引導強度（默認 7.5）
            height (int): 生成圖片高度（默認 512）
            width (int): 生成圖片寬度（默認 512）
            seed (int, optional): 隨機種子（用於可重現性）
            save_output (bool): 是否保存輸出圖片
        
        返回:
            Dict: 包含生成圖片和元數據的字典
        
        異常:
            ValueError: 當風格無效時拋出異常
            Exception: 其他生成失敗時拋出異常
        """
        
        # 檢查風格有效性
        if not StyleModelsConfig.is_valid_style(style_name):
            raise ValueError(
                f"不支持的風格: '{style_name}'\n"
                f"支持的風格有: {', '.join(StyleModelsConfig.STYLE_MODELS.keys())}"
            )
        
        print(f"\n{'='*70}")
        print(f"【開始生成圖片】")
        print(f"{'='*70}")
        
        # 步驟 1: 翻譯提示詞
        print(f"\n[步驟 1/5] 翻譯提示詞...")
        english_prompt = self.translation_module.translate_prompt(prompt_text)
        self.translation_module.print_translation_result(prompt_text, english_prompt)
        
        # 步驟 2: 獲取模型 ID
        print(f"\n[步驟 2/5] 準備模型...")
        model_id = StyleModelsConfig.get_model_id(style_name)
        print(f"風格: {style_name}")
        print(f"模型 ID: {model_id}")
        print(f"提示詞: {english_prompt}")
        print(f"生成數量: {num_images} 張")
        print(f"推理步數: {num_inference_steps}")
        print(f"引導強度: {guidance_scale}")
        print(f"圖片尺寸: {width}x{height}")
        
        # 步驟 3: 載入模型
        print(f"\n[步驟 3/5] 載入模型...")
        try:
            pipeline = self.model_manager.load_model(model_id)
        except Exception as e:
            print(f"[ERROR] 模型載入失敗: {e}")
            raise
        
        # 步驟 4: 生成圖片
        print(f"\n[步驟 4/5] 生成圖片...")
        try:
            # 設置隨機種子以便重現
            if seed is not None:
                generator = torch.Generator(device=self.config.device)
                generator.manual_seed(seed)
            else:
                generator = None
            
            # 執行推理
            result = pipeline(
                prompt=english_prompt,
                num_images_per_prompt=num_images,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                height=height,
                width=width,
                generator=generator
            )
            
            images = result.images
            print(f"[OK] 已成功生成 {len(images)} 張圖片")
        
        except Exception as e:
            print(f"[ERROR] 圖片生成失敗: {e}")
            raise
        
        # 步驟 5: 組合和保存
        print(f"\n[步驟 5/5] 組合和保存圖片...")
        
        # 組合成網格
        if num_images == 4:
            grid = self.image_processor.create_image_grid(images, rows=2, cols=2)
        elif num_images == 2:
            grid = self.image_processor.create_image_grid(images, rows=1, cols=2)
        else:
            grid = self.image_processor.create_image_grid(images, rows=1, cols=num_images)
        
        print(f"[OK] 網格已組合完成")
        
        # 保存圖片
        saved_files = {}
        if save_output:
            saved_files = self.image_processor.save_images(
                images,
                self.config.output_dir,
                prefix=f"{style_name}_images",
                save_grid=True,
                grid_rows=2 if num_images == 4 else 1,
                grid_cols=2 if num_images == 4 else num_images
            )
        
        # 清除 GPU 記憶體
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        print(f"{'='*70}\n")
        
        # 返回結果
        return {
            'images': images,
            'grid': grid,
            'prompt_chinese': prompt_text,
            'prompt_english': english_prompt,
            'style': style_name,
            'model_id': model_id,
            'saved_files': saved_files,
            'parameters': {
                'num_images': num_images,
                'num_inference_steps': num_inference_steps,
                'guidance_scale': guidance_scale,
                'height': height,
                'width': width,
                'seed': seed
            }
        }


# ============================================================================
# 第 7 部分：日誌記錄模塊
# ============================================================================

class Logger:
    """日誌記錄模塊"""
    
    def __init__(self, log_dir: Path):
        """
        初始化日誌記錄器
        
        參數:
            log_dir (Path): 日誌輸出目錄
        """
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / f"generation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.generations = []
    
    def log_generation(self, result: Dict):
        """
        記錄一次圖片生成
        
        參數:
            result (Dict): 生成結果字典
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'prompt_chinese': result['prompt_chinese'],
            'prompt_english': result['prompt_english'],
            'style': result['style'],
            'model_id': result['model_id'],
            'parameters': result['parameters'],
            'saved_files': {k: str(v) for k, v in result['saved_files'].items()}
        }
        
        self.generations.append(log_entry)
        self._save_log()
    
    def _save_log(self):
        """保存日誌到 JSON 文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(self.generations, f, ensure_ascii=False, indent=2)
    
    def print_generation_log(self, result: Dict):
        """打印生成日誌"""
        print("\n" + "="*70)
        print("【生成日誌】")
        print("="*70)
        print(f"中文提示詞: {result['prompt_chinese']}")
        print(f"英文提示詞: {result['prompt_english']}")
        print(f"選擇風格: {result['style']}")
        print(f"使用模型: {result['model_id']}")
        print(f"生成時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if result['saved_files']:
            print(f"\n已保存的文件:")
            for key, filepath in result['saved_files'].items():
                print(f"  - {key}: {filepath}")
        
        print("="*70 + "\n")


# ============================================================================
# 第 8 部分：主應用程序類別
# ============================================================================

class MultiStyleImageGenerator:
    """多風格 AI 繪圖生成器 - 主應用程序類別"""
    
    def __init__(self):
        """初始化生成器"""
        self.config = SystemConfig()
        self.model_manager = ModelManager(self.config)
        self.translation_module = TranslationModule()
        self.engine = ImageGenerationEngine(
            self.config,
            self.model_manager,
            self.translation_module
        )
        self.logger = Logger(self.config.logs_dir)
        self.config.print_system_info()
    
    def generate(
        self,
        prompt_text: str,
        style_name: str,
        num_images: int = 4,
        **kwargs
    ) -> Dict:
        """
        生成圖片的主接口
        
        參數:
            prompt_text (str): 中文提示詞
            style_name (str): 風格名稱
            num_images (int): 生成圖片數量
            **kwargs: 其他生成參數
        
        返回:
            Dict: 生成結果
        """
        result = self.engine.generate_images(
            prompt_text=prompt_text,
            style_name=style_name,
            num_images=num_images,
            **kwargs
        )
        
        self.logger.log_generation(result)
        self.logger.print_generation_log(result)
        
        return result
    
    def list_available_styles(self):
        """列出所有可用的風格"""
        StyleModelsConfig.print_available_styles()
    
    def cleanup(self):
        """清理資源"""
        self.model_manager.unload_model()


# ============================================================================
# 第 9 部分：使用範例和主程序
# ============================================================================

def example_1_basic_usage():
    """
    【範例 1】基本使用 - 二次元動漫風格
    """
    print("\n" + "#"*70)
    print("# 範例 1: 基本使用 - 二次元動漫風格")
    print("#"*70)
    
    # 初始化生成器
    generator = MultiStyleImageGenerator()
    
    # 列出可用風格
    generator.list_available_styles()
    
    # 生成圖片
    result = generator.generate(
        prompt_text="一個在圖書館看書的藍髮少女",
        style_name="二次元動漫",
        num_images=4
    )
    
    # 清理資源
    generator.cleanup()
    
    return result


def example_2_realistic_style():
    """
    【範例 2】寫實風格
    """
    print("\n" + "#"*70)
    print("# 範例 2: 寫實風格")
    print("#"*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="一個穿著古裝的美女，站在宮殿裡",
        style_name="寫實風格",
        num_images=4,
        num_inference_steps=40,
        guidance_scale=8.0
    )
    
    generator.cleanup()
    return result


def example_3_fantasy_art():
    """
    【範例 3】夢幻藝術風格
    """
    print("\n" + "#"*70)
    print("# 範例 3: 夢幻藝術風格")
    print("#"*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="夢幻的森林中一隻發光的鹿",
        style_name="夢幻藝術",
        num_images=4
    )
    
    generator.cleanup()
    return result


def example_4_3d_rendering():
    """
    【範例 4】3D 渲染風格
    """
    print("\n" + "#"*70)
    print("# 範例 4: 3D 渲染風格")
    print("#"*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="一個美麗的賽博朋克城市夜景",
        style_name="3D渲染",
        num_images=4
    )
    
    generator.cleanup()
    return result


def example_5_oil_painting():
    """
    【範例 5】油畫風格
    """
    print("\n" + "#"*70)
    print("# 範例 5: 油畫風格（宮崎駿風格）")
    print("#"*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="日本鄉村的小房子，被田野和樹木包圍",
        style_name="油畫風格",
        num_images=4
    )
    
    generator.cleanup()
    return result


def example_6_batch_generation():
    """
    【範例 6】批量生成多個風格
    """
    print("\n" + "#"*70)
    print("# 範例 6: 批量生成多個風格")
    print("#"*70)
    
    generator = MultiStyleImageGenerator()
    
    prompts_and_styles = [
        ("一隻可愛的貓咪", "二次元動漫"),
        ("森林中的小屋", "油畫風格"),
        ("未來城市", "3D渲染")
    ]
    
    results = []
    for prompt, style in prompts_and_styles:
        print(f"\n生成: {prompt} ({style})")
        result = generator.generate(
            prompt_text=prompt,
            style_name=style,
            num_images=2
        )
        results.append(result)
    
    generator.cleanup()
    return results


# ============================================================================
# 第 10 部分：主程序入口
# ============================================================================

def main():
    """
    主程序入口
    
    可以選擇運行不同的範例或自定義提示詞
    """
    print("\n" + "="*70)
    print("多風格 AI 繪圖生成器")
    print("Multi-Style AI Image Generator")
    print("="*70)
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                            功能菜單                                        ║
║                                                                            ║
║  1. 範例 1: 二次元動漫風格 (推薦首次嘗試)                                  ║
║  2. 範例 2: 寫實風格                                                      ║
║  3. 範例 3: 夢幻藝術風格                                                  ║
║  4. 範例 4: 3D 渲染風格                                                   ║
║  5. 範例 5: 油畫風格                                                      ║
║  6. 範例 6: 批量生成                                                      ║
║  7. 自定義生成 (輸入自己的提示詞和風格)                                   ║
║  8. 列出所有可用風格                                                      ║
║  0. 退出                                                                  ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
    """)
    
    while True:
        choice = input("\n請選擇功能 (0-8): ").strip()
        
        if choice == "0":
            print("感謝使用多風格 AI 繪圖生成器！")
            break
        
        elif choice == "1":
            example_1_basic_usage()
        
        elif choice == "2":
            example_2_realistic_style()
        
        elif choice == "3":
            example_3_fantasy_art()
        
        elif choice == "4":
            example_4_3d_rendering()
        
        elif choice == "5":
            example_5_oil_painting()
        
        elif choice == "6":
            example_6_batch_generation()
        
        elif choice == "7":
            print("\n【自定義生成】")
            prompt = input("請輸入中文提示詞: ").strip()
            if not prompt:
                print("提示詞不能為空！")
                continue
            
            generator = MultiStyleImageGenerator()
            generator.list_available_styles()
            
            style = input("請選擇風格名稱: ").strip()
            
            try:
                num_images = int(input("請輸入生成圖片數量 (1-4, 默認 4): ").strip() or "4")
            except ValueError:
                num_images = 4
            
            try:
                result = generator.generate(
                    prompt_text=prompt,
                    style_name=style,
                    num_images=num_images
                )
            except Exception as e:
                print(f"生成失敗: {e}")
            finally:
                generator.cleanup()
        
        elif choice == "8":
            generator = MultiStyleImageGenerator()
            generator.list_available_styles()
            generator.cleanup()
        
        else:
            print("無效的選擇，請重試！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已被用戶中斷")
    except Exception as e:
        print(f"發生未預期的錯誤: {e}")
        import traceback
        traceback.print_exc()
