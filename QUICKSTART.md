# 快速啟動指南 (Quick Start Guide)

## 📦 專案文件清單

```
HW4/
├── multi_style_image_generator.py      ⭐ 主程序（1000+ 行完整代碼）
├── advanced_examples.py                 📚 10 個高級使用示例
├── test_image_generator.py             🧪 單元測試
├── requirements.txt                    📋 依賴包列表
├── config.json                         ⚙️  配置文件
├── README.md                           📖 完整文檔（含 FAQ）
├── QUICKSTART.md                       🚀 本文件
├── generated_images/                   📁 生成的圖片輸出目錄
├── logs/                               📁 日誌記錄目錄
└── models_cache/                       📁 模型緩存目錄
```

---

## ⚡ 5 分鐘快速開始

### 第 1 步：安裝依賴

```bash
# 安裝必要的包
pip install -r requirements.txt
```

### 第 2 步：運行程序

```bash
# 運行主程序
python multi_style_image_generator.py

# 或直接在 Python 中使用
python -c "
from multi_style_image_generator import MultiStyleImageGenerator
generator = MultiStyleImageGenerator()
result = generator.generate('一個藍髮少女', '二次元動漫', num_images=1)
generator.cleanup()
print('完成！')
"
```

### 第 3 步：查看結果

生成的圖片保存在：
```
generated_images/[時間戳]/
├── 二次元動漫_images_01.png
├── 二次元動漫_images_02.png
├── 二次元動漫_images_03.png
├── 二次元動漫_images_04.png
└── 二次元動漫_images_grid.png
```

---

## 🎯 常用命令

### 查看可用風格
```bash
python -c "
from multi_style_image_generator import MultiStyleImageGenerator
gen = MultiStyleImageGenerator()
gen.list_available_styles()
gen.cleanup()
"
```

### 生成二次元動漫圖片
```bash
python -c "
from multi_style_image_generator import MultiStyleImageGenerator
gen = MultiStyleImageGenerator()
gen.generate('一個可愛的貓咪', '二次元動漫')
gen.cleanup()
"
```

### 生成寫實風格圖片
```bash
python -c "
from multi_style_image_generator import MultiStyleImageGenerator
gen = MultiStyleImageGenerator()
gen.generate('一個美麗的風景', '寫實風格')
gen.cleanup()
"
```

### 生成高質量圖片
```bash
python -c "
from multi_style_image_generator import MultiStyleImageGenerator
gen = MultiStyleImageGenerator()
gen.generate('藝術作品', '夢幻藝術', 
    num_inference_steps=50, 
    guidance_scale=9.0)
gen.cleanup()
"
```

---

## 💻 代碼片段

### 基本用法
```python
from multi_style_image_generator import MultiStyleImageGenerator

# 初始化
generator = MultiStyleImageGenerator()

# 生成圖片
result = generator.generate(
    prompt_text="一個在圖書館看書的藍髮少女",
    style_name="二次元動漫"
)

# 查看結果
result['grid'].show()

# 清理
generator.cleanup()
```

### 高級用法
```python
# 批量生成
prompts = [
    ("一隻貓", "二次元動漫"),
    ("森林", "油畫風格"),
    ("城市", "3D渲染")
]

for prompt, style in prompts:
    result = generator.generate(prompt, style, num_images=2)
    print(f"✓ 已生成: {prompt} ({style})")
```

### 自定義參數
```python
result = generator.generate(
    prompt_text="提示詞",
    style_name="風格",
    num_images=4,
    num_inference_steps=50,     # 品質
    guidance_scale=8.0,         # 遵守程度
    height=512,                 # 高度
    width=512,                  # 寬度
    seed=12345,                 # 可重現性
    save_output=True            # 保存
)
```

---

## 🔧 疑難排除

### 問題：CUDA out of memory

**解決方案：**
```python
# 生成更少的圖片
result = generator.generate(prompt, style, num_images=1)

# 或減少推理步驟
result = generator.generate(prompt, style, 
    num_inference_steps=20)
```

### 問題：第一次運行很慢

**原因：** 首次下載模型（5-50GB）

**解決方案：** 等待完成，後續運行會快得多

### 問題：翻譯失敗

**解決方案：** 直接使用英文提示詞
```python
result = generator.generate(
    "a blue-haired girl reading in library",
    "二次元動漫"
)
```

### 問題：GPU 不可用

**檢查：**
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

**解決：** 安裝 CUDA 相關驅動程序

---

## 📊 性能指標

| 配置 | 時間 | 記憶體 | 質量 |
|------|------|--------|------|
| 快速 (20步, 1張) | 10s | 3GB | ⭐⭐ |
| 標準 (30步, 4張) | 45s | 6GB | ⭐⭐⭐ |
| 高質 (50步, 4張) | 75s | 7GB | ⭐⭐⭐⭐ |
| 超高 (100步, 4張) | 150s | 8GB | ⭐⭐⭐⭐⭐ |

---

## 🎨 風格對比

### 寫實風格
```python
generator.generate("一個女人", "寫實風格")
# 結果：高度寫實的攝影風格
```

### 二次元動漫
```python
generator.generate("一個女孩", "二次元動漫")
# 結果：日本動漫風格的可愛人物
```

### 夢幻藝術
```python
generator.generate("森林", "夢幻藝術")
# 結果：超現實的藝術作品
```

### 3D 渲染
```python
generator.generate("城市", "3D渲染")
# 結果：逼真的 3D CGI 效果
```

### 油畫風格
```python
generator.generate("鄉村", "油畫風格")
# 結果：宮崎駿風格的油畫
```

---

## 📚 進階資源

- 📖 完整文檔: [README.md](README.md)
- 💡 高級示例: [advanced_examples.py](advanced_examples.py)
- 🧪 單元測試: [test_image_generator.py](test_image_generator.py)
- ⚙️  配置文件: [config.json](config.json)

---

## 🚀 下一步

### 嘗試這些任務：

1. ✅ 運行基本示例
   ```bash
   python multi_style_image_generator.py
   # 選擇選項 1
   ```

2. ✅ 運行高級示例
   ```bash
   python advanced_examples.py
   # 選擇感興趣的示例
   ```

3. ✅ 自定義提示詞
   ```bash
   python multi_style_image_generator.py
   # 選擇選項 7（自定義生成）
   ```

4. ✅ 查看日誌
   ```bash
   # 打開 logs/ 目錄查看生成記錄
   ```

---

## 💡 提示和技巧

### 提示 1: 編寫更好的提示詞

```python
# ❌ 不好的提示詞
"女孩"

# ✅ 好的提示詞
"一個年輕的女孩，穿著紅色連衣裙，
 在花園裡，陽光灑在她身上，
 高質量，逼真，細節豐富"
```

### 提示 2: 調整引導強度

```python
# 低引導 (5.0) - 更多創意，不太遵守提示
result = generator.generate(prompt, style, guidance_scale=5.0)

# 高引導 (10.0) - 嚴格遵守提示，較少創意
result = generator.generate(prompt, style, guidance_scale=10.0)
```

### 提示 3: 使用種子獲得可重現結果

```python
# 相同的提示和種子 = 相同的圖片
result1 = generator.generate("貓", "二次元動漫", seed=42)
result2 = generator.generate("貓", "二次元動漫", seed=42)
# result1 和 result2 完全相同
```

### 提示 4: 批量生成時清理記憶體

```python
import torch

for i in range(10):
    torch.cuda.empty_cache()  # 清理前清除舊的
    result = generator.generate(f"提示詞 {i}", "風格")
```

---

## 📞 獲取幫助

### 查看日誌
```bash
# 檢查最近的生成記錄
cat logs/generation_log_*.json
```

### 測試系統
```bash
python -c "
from multi_style_image_generator import SystemConfig
config = SystemConfig()
config.print_system_info()
"
```

### 列出風格
```bash
python -c "
from multi_style_image_generator import StyleModelsConfig
StyleModelsConfig.print_available_styles()
"
```

---

## 📝 注意事項

⚠️ **首次運行會下載大量模型文件（10-50GB）**
- 取決於選擇的風格
- 需要穩定的網絡連接
- 請耐心等待

⚠️ **GPU 記憶體要求**
- 最少 6GB（推薦 12GB+）
- 不足時會發生 CUDA OOM 錯誤

⚠️ **生成時間**
- 使用 GPU: 10-150 秒/批
- 使用 CPU: 5-30 分鐘/批（不推薦）

---

## 🎉 開始享受！

你現在已經準備好使用多風格 AI 繪圖生成器了！

```bash
python multi_style_image_generator.py
```

祝你創作愉快！🎨✨

---

**最後更新**: 2025-12-06  
**版本**: 1.0.0
