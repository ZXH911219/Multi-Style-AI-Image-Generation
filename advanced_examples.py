"""
高級使用示例 (Advanced Usage Examples)
========================================

本文件展示如何在不同場景下使用多風格 AI 繪圖生成器。
"""

from multi_style_image_generator import (
    MultiStyleImageGenerator,
    StyleModelsConfig,
    ImageProcessor
)
from pathlib import Path
import json


# ============================================================================
# 示例 1: 單個圖片生成
# ============================================================================

def example_single_image_generation():
    """生成單張圖片"""
    print("\n" + "="*70)
    print("【示例 1】單個圖片生成")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="一個美麗的日出海景",
        style_name="寫實風格",
        num_images=1
    )
    
    # 顯示結果
    print(f"\n生成的圖片保存在: {result['saved_files']}")
    
    generator.cleanup()


# ============================================================================
# 示例 2: 高質量生成
# ============================================================================

def example_high_quality_generation():
    """生成高質量圖片（使用更多推理步驟）"""
    print("\n" + "="*70)
    print("【示例 2】高質量生成")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="一位優雅的古代公主，穿著華麗的衣裳",
        style_name="寫實風格",
        num_images=4,
        num_inference_steps=50,      # 增加推理步驟
        guidance_scale=9.0            # 提高引導強度
    )
    
    print(f"\n高質量生成完成！")
    print(f"推理步數: 50")
    print(f"引導強度: 9.0")
    
    generator.cleanup()


# ============================================================================
# 示例 3: 快速生成
# ============================================================================

def example_fast_generation():
    """快速生成（減少推理步驟以提高速度）"""
    print("\n" + "="*70)
    print("【示例 3】快速生成")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="卡通風格的小貓",
        style_name="二次元動漫",
        num_images=2,                # 生成 2 張而不是 4 張
        num_inference_steps=20       # 較少的推理步驟
    )
    
    print(f"\n快速生成完成！")
    print(f"推理步數: 20（快速）")
    
    generator.cleanup()


# ============================================================================
# 示例 4: 可重現的結果
# ============================================================================

def example_reproducible_generation():
    """使用相同的隨機種子生成可重現的結果"""
    print("\n" + "="*70)
    print("【示例 4】可重現的結果")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    # 第一次生成
    print("\n第一次生成（seed=42）...")
    result1 = generator.generate(
        prompt_text="星空下的樹木",
        style_name="夢幻藝術",
        num_images=1,
        seed=42
    )
    
    # 第二次生成（使用相同的種子）
    print("\n第二次生成（seed=42）...")
    result2 = generator.generate(
        prompt_text="星空下的樹木",
        style_name="夢幻藝術",
        num_images=1,
        seed=42
    )
    
    print("\n✓ 使用相同的 seed 可以生成相同的圖片")
    
    generator.cleanup()


# ============================================================================
# 示例 5: 批量生成多個風格
# ============================================================================

def example_batch_multi_style_generation():
    """批量生成多個風格的圖片"""
    print("\n" + "="*70)
    print("【示例 5】批量生成多個風格")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    # 定義多個提示詞和風格的組合
    generation_configs = [
        {
            "prompt": "一隻可愛的紅色狐狸",
            "style": "二次元動漫",
            "num_images": 2
        },
        {
            "prompt": "古老的城堡廢墟",
            "style": "寫實風格",
            "num_images": 2
        },
        {
            "prompt": "星系和星星",
            "style": "夢幻藝術",
            "num_images": 2
        },
        {
            "prompt": "未來城市夜景",
            "style": "3D渲染",
            "num_images": 2
        }
    ]
    
    results = []
    for config in generation_configs:
        print(f"\n生成: {config['prompt']} ({config['style']})...")
        result = generator.generate(
            prompt_text=config['prompt'],
            style_name=config['style'],
            num_images=config['num_images']
        )
        results.append(result)
    
    print(f"\n✓ 已完成 {len(results)} 個生成任務")
    
    generator.cleanup()


# ============================================================================
# 示例 6: 同一提示詞不同風格
# ============================================================================

def example_same_prompt_different_styles():
    """使用相同的提示詞生成不同風格的圖片"""
    print("\n" + "="*70)
    print("【示例 6】同一提示詞不同風格")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    prompt = "一個在山頂上的冒險家"
    
    # 遍歷所有可用的風格
    print(f"使用提示詞: '{prompt}'")
    print(f"生成所有可用風格的圖片...\n")
    
    results = {}
    for style_name in StyleModelsConfig.STYLE_MODELS.keys():
        print(f"生成 {style_name}...")
        result = generator.generate(
            prompt_text=prompt,
            style_name=style_name,
            num_images=1
        )
        results[style_name] = result
    
    print(f"\n✓ 已完成所有風格的生成")
    print(f"共生成: {len(results)} 張圖片")
    
    generator.cleanup()
    return results


# ============================================================================
# 示例 7: 詳細參數配置
# ============================================================================

def example_detailed_parameter_configuration():
    """展示所有可配置的參數"""
    print("\n" + "="*70)
    print("【示例 7】詳細參數配置")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    # 所有可用的參數
    result = generator.generate(
        # 必須參數
        prompt_text="一個在古老圖書館裡的魔法師",
        style_name="夢幻藝術",
        
        # 生成配置
        num_images=4,
        num_inference_steps=40,       # 推理步數：20-100
        guidance_scale=8.0,           # 引導強度：5-15
        height=512,                   # 圖片高度：256, 512, 768
        width=512,                    # 圖片寬度：256, 512, 768
        seed=12345,                   # 隨機種子（用於可重現性）
        save_output=True              # 是否保存輸出
    )
    
    print("\n【參數說明】")
    print("- num_inference_steps: 越高質量越好但越慢（推薦 30-50）")
    print("- guidance_scale: 越高越遵守提示詞（推薦 5-12）")
    print("- height/width: 支持 256, 512, 768 等（512x512 最常用）")
    print("- seed: 用於生成可重現的結果")
    
    generator.cleanup()


# ============================================================================
# 示例 8: 結果保存和加載
# ============================================================================

def example_save_and_load_results():
    """保存和加載生成結果"""
    print("\n" + "="*70)
    print("【示例 8】結果保存和加載")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    result = generator.generate(
        prompt_text="一個魔法森林",
        style_name="夢幻藝術",
        num_images=4,
        save_output=True
    )
    
    # 提取元數據
    metadata = {
        'prompt_chinese': result['prompt_chinese'],
        'prompt_english': result['prompt_english'],
        'style': result['style'],
        'model_id': result['model_id'],
        'parameters': result['parameters'],
        'image_files': {k: str(v) for k, v in result['saved_files'].items()}
    }
    
    # 保存元數據
    metadata_file = Path(generator.config.output_dir) / "latest_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 元數據已保存: {metadata_file}")
    print(f"\n元數據內容:")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    
    generator.cleanup()


# ============================================================================
# 示例 9: 錯誤處理
# ============================================================================

def example_error_handling():
    """演示錯誤處理機制"""
    print("\n" + "="*70)
    print("【示例 9】錯誤處理")
    print("="*70)
    
    generator = MultiStyleImageGenerator()
    
    # 案例 1: 無效的風格
    print("\n案例 1: 嘗試使用無效的風格...")
    try:
        result = generator.generate(
            prompt_text="測試提示詞",
            style_name="無效風格"
        )
    except ValueError as e:
        print(f"✓ 捕獲錯誤: {e}")
    
    # 案例 2: 空提示詞
    print("\n案例 2: 使用空提示詞...")
    try:
        result = generator.generate(
            prompt_text="",
            style_name="二次元動漫"
        )
    except Exception as e:
        print(f"✓ 捕獲錯誤: {e}")
    
    # 案例 3: 列出所有可用風格
    print("\n案例 3: 列出所有可用風格...")
    generator.list_available_styles()
    
    generator.cleanup()


# ============================================================================
# 示例 10: 性能監控
# ============================================================================

def example_performance_monitoring():
    """監控生成性能"""
    print("\n" + "="*70)
    print("【示例 10】性能監控")
    print("="*70)
    
    import time
    import torch
    
    generator = MultiStyleImageGenerator()
    
    # 測試不同配置的性能
    configs = [
        {"steps": 20, "guidance": 7.5},
        {"steps": 30, "guidance": 7.5},
        {"steps": 50, "guidance": 7.5},
    ]
    
    print("\n性能對比測試:")
    print(f"{'推理步數':<10} {'引導強度':<10} {'生成時間':<10} {'內存使用':<10}")
    print("-" * 40)
    
    for config in configs:
        # 測試前清理記憶體
        torch.cuda.empty_cache()
        
        start_time = time.time()
        initial_memory = torch.cuda.memory_allocated() / 1024**3 if torch.cuda.is_available() else 0
        
        result = generator.generate(
            prompt_text="測試提示詞",
            style_name="二次元動漫",
            num_images=1,
            num_inference_steps=config['steps'],
            guidance_scale=config['guidance']
        )
        
        elapsed_time = time.time() - start_time
        peak_memory = torch.cuda.max_memory_allocated() / 1024**3 if torch.cuda.is_available() else 0
        
        print(f"{config['steps']:<10} {config['guidance']:<10.1f} {elapsed_time:<10.1f}s {peak_memory:<10.2f}GB")
    
    generator.cleanup()


# ============================================================================
# 主函數
# ============================================================================

def run_all_examples():
    """運行所有示例"""
    print("\n" + "#"*70)
    print("# 多風格 AI 繪圖生成器 - 高級使用示例")
    print("#"*70)
    
    examples = [
        ("單個圖片生成", example_single_image_generation),
        ("高質量生成", example_high_quality_generation),
        ("快速生成", example_fast_generation),
        ("可重現的結果", example_reproducible_generation),
        ("批量生成多個風格", example_batch_multi_style_generation),
        ("同一提示詞不同風格", example_same_prompt_different_styles),
        ("詳細參數配置", example_detailed_parameter_configuration),
        ("結果保存和加載", example_save_and_load_results),
        ("錯誤處理", example_error_handling),
        ("性能監控", example_performance_monitoring),
    ]
    
    print("""
    可用的示例:
    """)
    
    for i, (name, _) in enumerate(examples, 1):
        print(f"    {i}. {name}")
    print(f"    0. 退出\n")
    
    while True:
        try:
            choice = int(input("請選擇示例 (0-10): "))
            
            if choice == 0:
                print("退出")
                break
            elif 1 <= choice <= len(examples):
                _, example_func = examples[choice - 1]
                example_func()
            else:
                print("無效的選擇")
        
        except ValueError:
            print("請輸入有效的數字")
        except KeyboardInterrupt:
            print("\n已中斷")
            break
        except Exception as e:
            print(f"執行出錯: {e}")


if __name__ == "__main__":
    try:
        run_all_examples()
    except Exception as e:
        print(f"發生錯誤: {e}")
        import traceback
        traceback.print_exc()
