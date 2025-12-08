# 快速參考卡片 - 多風格 AI 繪圖生成器

## 🎯 30 秒快速開始

```powershell
cd c:\Users\user\Desktop\HW4
python quickstart_demo.py
```

---

## 📋 核心命令

| 命令 | 功能 | 時間 |
|------|------|------|
| `python quickstart_demo.py` | 交互式演示 (無需 GPU) | 3 秒 |
| `pip install -r requirements.txt` | 安裝所有依賴 | 10-15 分鐘 |
| `python multi_style_image_generator.py` | 運行主程序 (需要 GPU) | 30-150 秒 |
| `python advanced_examples.py` | 10 個代碼示例 | 5-10 分鐘 |
| `python -m pytest test_image_generator.py -v` | 運行單元測試 | 2-5 分鐘 |

---

## 🎨 5 種藝術風格

| # | 風格名稱 | 提示詞示例 | 最佳用途 |
|----|---------|----------|---------|
| 1 | Realistic (寫實) | "美麗的森林風景" | 照片級別寫實圖像 |
| 2 | Anime 2D (二次元) | "魔法少女變身" | 日式動漫風格圖像 |
| 3 | Fantasy Art (幻想) | "龍在雲中飛行" | 奇幻和魔法場景 |
| 4 | 3D Rendering (3D) | "未來城市建築" | 3D 渲染和 CG 效果 |
| 5 | Oil Painting (油畫) | "向日葵田野" | 油畫和藝術風格 |

---

## 📁 重要文件位置

```
Project Root: c:\Users\user\Desktop\HW4\
├── 快速開始          → QUICKSTART.md
├── 完整文檔          → README.md
├── 架構設計          → PROJECT_OVERVIEW.md
├── 設置幫助          → SETUP_GUIDE.md
├── 項目總結          → FINAL_SUMMARY.md
├── 代碼示例          → advanced_examples.py
├── 運行演示          → quickstart_demo.py
└── 核心系統          → multi_style_image_generator.py

生成輸出:
generated_images/     → 生成的 PNG 圖片
logs/                 → JSON 格式日誌
models_cache/         → 已下載的模型 (50GB+)
```

---

## 🔧 常見配置

### 更改推理步數 (速度 vs 質量)

```python
# 快速生成 (15 步，10-20 秒)
generator = MultiStyleImageGenerator(num_inference_steps=15)

# 標準生成 (30 步，30-50 秒)
generator = MultiStyleImageGenerator(num_inference_steps=30)

# 高質量 (50 步，50-100 秒)
generator = MultiStyleImageGenerator(num_inference_steps=50)
```

### 更改生成數量

```python
# 1 張圖片
images = generator.generate_images(num_images=1)

# 2 張圖片
images = generator.generate_images(num_images=2)

# 4 張圖片 (2x2 網格)
images = generator.generate_images(num_images=4)
```

### 使用 CPU 模式

```python
config = SystemConfig()
config.device = "cpu"  # 改為 CPU (慢)
```

---

## 🐛 故障排除速查表

| 問題 | 解決方案 |
|------|---------|
| `No module named 'torch'` | `pip install torch torchvision` |
| GPU 不可用 | 檢查: `python -c "import torch; print(torch.cuda.is_available())"` |
| 記憶體不足 | 減少 `num_images=1`, `num_inference_steps=20` |
| 翻譯失敗 | 檢查網絡連接或直接使用英文 |
| 首次很慢 | 正常 (首次下載模型 10-30 分鐘) |
| 文件未找到 | 確保在 `c:\Users\user\Desktop\HW4` 目錄 |

---

## 📊 性能指標

| 配置 | 速度 | 質量 | 記憶體 |
|------|------|------|--------|
| 快速 (15 步) | 快 | 中等 | 低 |
| **標準 (30 步)** | **中等** | **好** | **中等** |
| 高質量 (50 步) | 慢 | 優秀 | 高 |

### 典型運行時間

```
首次運行:     10-30 分鐘 (包括模型下載)
後續運行:     30-150 秒 (模型已緩存)
圖片生成:     取決於推理步數
  - 15 步:    10-20 秒
  - 30 步:    30-50 秒 (推薦)
  - 50 步:    50-100 秒
```

---

## 💾 系統要求

**最低配置**:
- Python 3.8+
- GPU 512 MB RAM (建議更多)
- 50+ GB 磁盤空間
- 網絡連接 (首次下載)

**推薦配置**:
- Python 3.10+
- NVIDIA GPU 6+ GB VRAM
- 100+ GB 磁盤空間
- 20+ Mbps 網絡

---

## 🚀 5 分鐘快速之旅

### 分鐘 1: 準備
```powershell
cd c:\Users\user\Desktop\HW4
```

### 分鐘 2: 查看演示
```powershell
python quickstart_demo.py
```

### 分鐘 3-4: 閱讀文檔
```powershell
cat QUICKSTART.md
```

### 分鐘 5: 開始使用
```powershell
# 選項 A: 無需安裝
python quickstart_demo.py

# 選項 B: 完整使用 (需要先安裝)
pip install -r requirements.txt
python multi_style_image_generator.py
```

---

## 🎓 代碼片段

### 生成單張圖片

```python
from multi_style_image_generator import MultiStyleImageGenerator

generator = MultiStyleImageGenerator()
images = generator.generate_images(
    prompt="美麗的山水風景",
    style="realistic",
    num_images=1
)
```

### 批量生成不同風格

```python
styles = ["realistic", "anime", "fantasy", "3d", "oil"]
for style in styles:
    images = generator.generate_images(
        prompt="花園中的花朵",
        style=style,
        num_images=1
    )
```

### 設置自定義參數

```python
images = generator.generate_images(
    prompt="城市夜景",
    style="3d",
    num_images=4,
    num_inference_steps=50,
    guidance_scale=7.5,
    negative_prompt="模糊，低質量"
)
```

---

## 📞 幫助資源

| 需要 | 查看 | 時間 |
|------|------|------|
| 快速開始 | QUICKSTART.md | 5 分鐘 |
| 完整指南 | README.md | 30 分鐘 |
| 代碼示例 | advanced_examples.py | 20 分鐘 |
| 架構設計 | PROJECT_OVERVIEW.md | 15 分鐘 |
| 設置幫助 | SETUP_GUIDE.md | 10 分鐘 |
| 項目總結 | FINAL_SUMMARY.md | 10 分鐘 |
| 常見問題 | README.md 第 10 節 | 5 分鐘 |

---

## ✨ 核心特性

- ✓ 5 種藝術風格
- ✓ 中文提示詞支持
- ✓ 批量圖片生成
- ✓ GPU 優化加速
- ✓ 完整日誌系統
- ✓ 10 個代碼示例
- ✓ 20+ 單元測試
- ✓ 生產級別代碼

---

## 🎯 下一步

1. ✓ 運行: `python quickstart_demo.py`
2. ✓ 閱讀: QUICKSTART.md
3. ✓ 安裝: `pip install -r requirements.txt`
4. ✓ 使用: `python multi_style_image_generator.py`
5. ✓ 探索: `advanced_examples.py`

---

**準備好了嗎？** 立即執行:

```powershell
python quickstart_demo.py
```

祝您使用愉快！🎨✨

---

**版本**: 1.0.0  
**最後更新**: 2025-12-06  
**狀態**: 生產就緒
