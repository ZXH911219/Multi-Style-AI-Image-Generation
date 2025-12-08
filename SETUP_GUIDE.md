# 完整後續步驟指南

## 📋 目錄
1. 環境驗證
2. 依賴安裝
3. 項目驗證
4. 運行程序
5. 常見問題

---

## ✅ 步驟 1: 環境驗證

### Python 環境信息
- **Python 版本**: 3.10.19 (Conda 環境)
- **執行路徑**: `c:\Users\user\anaconda3\envs\aiot_streamlit\python.exe`
- **工作目錄**: `c:\Users\user\Desktop\HW4`

### 已安裝的主要套件
✓ Pillow 11.1.0 (圖片處理)
✓ NumPy 2.1.3 (數值計算)
✓ JSON (內建)
✓ PathLib (內建)
✓ DateTime (內建)

---

## 🔧 步驟 2: 依賴安裝

### 方式 A: 完整安裝 (推薦)

在終端執行:
```powershell
cd c:\Users\user\Desktop\HW4
pip install -r requirements.txt
```

**預期時間**: 10-15 分鐘  
**所需套件**:
- torch>=2.0.0 (深度學習框架)
- diffusers>=0.21.0 (擴散模型)
- transformers>=4.30.0 (模型庫)
- deep-translator>=1.11.4 (翻譯)

### 方式 B: 最小安裝 (僅演示)

如果只想演示，可以跳過完整安裝，直接使用現有環境。

---

## 🧪 步驟 3: 項目驗證

### 驗證項目文件完整性

執行以下 PowerShell 命令檢查所有文件:

```powershell
# 進入項目目錄
cd c:\Users\user\Desktop\HW4

# 列出所有Python文件
Get-ChildItem -Filter "*.py" -Recurse | ForEach-Object { Write-Host $_.FullName }

# 列出所有文檔
Get-ChildItem -Filter "*.md" -Recurse | ForEach-Object { Write-Host $_.FullName }

# 列出配置文件
Get-ChildItem -Filter "*.json" -Recurse | ForEach-Object { Write-Host $_.FullName }

# 列出配置文件
Get-ChildItem -Filter "*.txt" -Recurse | ForEach-Object { Write-Host $_.FullName }
```

### 預期的項目文件結構

```
c:\Users\user\Desktop\HW4\
├── 【Python 程序】
│   ├── multi_style_image_generator.py      (1200+ 行)
│   ├── advanced_examples.py                (500+ 行)
│   ├── test_image_generator.py            (200+ 行)
│   └── quickstart_demo.py                 (新增演示)
│
├── 【Jupyter Notebook】
│   └── multi_style_image_generator.ipynb   (15 個單元)
│
├── 【文檔】
│   ├── README.md                          (完整文檔)
│   ├── QUICKSTART.md                      (快速指南)
│   ├── PROJECT_OVERVIEW.md                (項目總結)
│   ├── PROJECT_COMPLETION.md              (完成報告)
│   ├── FILELIST.md                        (文件列表)
│   └── SETUP_GUIDE.md                     (本文件)
│
├── 【配置文件】
│   ├── requirements.txt                   (依賴清單)
│   ├── environment.yml                    (Conda 環境)
│   └── config.json                        (項目配置)
│
└── 【自動生成目錄】(首次運行時創建)
    ├── generated_images/                  (生成的圖片)
    ├── logs/                              (日誌記錄)
    ├── models_cache/                      (模型緩存)
    └── demo_output/                       (演示輸出)
```

---

## 🚀 步驟 4: 運行程序

### 選項 A: 運行完整程序 (需要安裝所有依賴)

```powershell
cd c:\Users\user\Desktop\HW4
python multi_style_image_generator.py
```

**流程**:
1. 顯示交互式菜單
2. 選擇風格 (1-6)
3. 輸入中文提示詞
4. 等待生成 (首次運行會下載模型 10-30 分鐘)
5. 查看生成的圖片

### 選項 B: 運行快速演示 (無需額外依賴)

```powershell
cd c:\Users\user\Desktop\HW4
python quickstart_demo.py
```

**功能**:
- 展示系統概覽
- 模擬完整工作流程
- 演示 5 種風格
- 保存演示日誌

### 選項 C: 運行高級示例 (需要完整依賴)

```powershell
cd c:\Users\user\Desktop\HW4
python advanced_examples.py
```

**包含 10 個示例**:
1. 單個圖片生成
2. 高質量生成
3. 快速生成
4. 可重現結果
5. 批量多風格
6. 同提示詞不同風格
7. 詳細參數配置
8. 結果保存加載
9. 錯誤處理
10. 性能監控

### 選項 D: 運行單元測試

```powershell
cd c:\Users\user\Desktop\HW4
python -m pytest test_image_generator.py -v
```

---

## 📖 步驟 5: 查看文檔

### 重要文檔順序

1. **QUICKSTART.md** (5 分鐘) - 快速開始
   - 立即運行的命令
   - 常見問題
   - 性能指標

2. **README.md** (30 分鐘) - 完整文檔
   - 系統要求
   - 安裝指南
   - API 文檔
   - 常見問題 (8 個)

3. **PROJECT_OVERVIEW.md** (15 分鐘) - 架構說明
   - 項目結構
   - 功能實現
   - 代碼品質
   - 性能優化

4. **advanced_examples.py** (參考) - 代碼示例
   - 10 個實用示例
   - 各種使用場景

### 快速查看命令

```powershell
# 查看快速開始
cat QUICKSTART.md

# 查看完整文檔
cat README.md

# 查看項目結構
cat PROJECT_OVERVIEW.md | Select-String "結構", "功能" -Context 5
```

---

## ⚙️ 步驟 6: 配置系統

### 修改配置 (config.json)

```json
{
  "device": "cuda",              // 使用 GPU
  "dtype": "float16",            // 精度優化
  "inference_steps": 30,         // 推理步數
  "guidance_scale": 7.5,         // 引導強度
  "image_size": [512, 512]       // 圖片尺寸
}
```

### 環境變量設置

```powershell
# 使用 CPU 模式 (GPU 不可用時)
$env:CUDA_VISIBLE_DEVICES = "-1"

# 增加 Python 輸出緩衝
$env:PYTHONUNBUFFERED = "1"

# 設置工作目錄
cd c:\Users\user\Desktop\HW4
```

---

## 🔍 步驟 7: 驗證安裝

### 驗證 Python 導入

創建 `test_imports.py`:
```python
import sys
print("Python:", sys.version)

try:
    from pathlib import Path
    print("✓ pathlib - OK")
except: print("✗ pathlib - FAILED")

try:
    from PIL import Image
    print("✓ Pillow - OK")
except: print("✗ Pillow - FAILED")

try:
    import numpy
    print("✓ NumPy - OK")
except: print("✗ NumPy - FAILED")

try:
    from multi_style_image_generator import MultiStyleImageGenerator
    print("✓ Main module - OK")
except Exception as e:
    print(f"✗ Main module - FAILED: {e}")
```

執行:
```powershell
python test_imports.py
```

---

## 📊 步驟 8: 首次運行檢查清單

- [ ] Python 版本 >= 3.8
- [ ] Pillow 已安裝 (圖片處理)
- [ ] NumPy 已安裝 (數值計算)
- [ ] 項目文件完整 (所有 .py 和 .md 文件)
- [ ] 配置文件有效 (config.json)
- [ ] 可以導入主模塊
- [ ] 有足夠的磁盤空間 (50GB+ 用於模型)
- [ ] 網絡連接正常 (下載模型)

---

## 💾 步驟 9: 輸出文件管理

### 生成的文件位置

```
generated_images/
├── YYYYMMDD_HHMMSS/          (按時間戳組織)
│   ├── style_images_01.png   (原始圖片)
│   ├── style_images_02.png
│   ├── style_images_03.png
│   ├── style_images_04.png
│   └── style_images_grid.png (2x2 網格)
└── ...

logs/
├── generation_log_YYYYMMDD_HHMMSS.json  (生成日誌)
└── ...

models_cache/
├── models--runwayml--stable-diffusion-v1-5/
├── models--hakurei--waifu-diffusion/
└── ... (其他模型)
```

### 清理緩存

```powershell
# 刪除生成的圖片
Remove-Item -Recurse generated_images -Force

# 刪除日誌
Remove-Item -Recurse logs -Force

# 保留模型緩存 (下次運行會快得多)
# Remove-Item -Recurse models_cache -Force
```

---

## 🎯 步驟 10: 常見問題和解決方案

### Q1: 導入錯誤 "No module named 'torch'"

**解決**:
```powershell
pip install torch torchvision
```

### Q2: GPU 不可用 (使用 CPU)

**檢查**:
```powershell
python -c "import torch; print(torch.cuda.is_available())"
```

**如果為 False，使用 CPU 模式**:
```python
# 在 multi_style_image_generator.py 中修改
config = SystemConfig()
config.device = "cpu"  # 改為 CPU
```

### Q3: 記憶體不足 (CUDA out of memory)

**解決**:
- 減少生成數量: `num_images=1` 而不是 4
- 減少推理步驟: `num_inference_steps=20` 而不是 30
- 使用更小的模型

### Q4: 首次運行很慢

**原因**: 下載模型 (5-50GB)

**解決**: 耐心等待 (10-30 分鐘)，後續運行會快得多

### Q5: 翻譯失敗

**解決**: 
- 檢查網絡連接
- 直接使用英文提示詞
- 查看 README.md 的【故障排除】

---

## 📅 完整時間表

| 步驟 | 時間 |
|------|------|
| 1. 環境檢查 | 1 分鐘 |
| 2. 安裝依賴 | 10-15 分鐘 |
| 3. 項目驗證 | 2 分鐘 |
| 4. 首次運行 + 模型下載 | 10-30 分鐘 |
| 5. 生成圖片 | 30-150 秒 |
| **總計** | **30-60 分鐘** |

後續運行會快得多 (只需 30-150 秒)

---

## ✨ 快速命令參考

```powershell
# 進入項目目錄
cd c:\Users\user\Desktop\HW4

# 查看可用文件
ls *.py
ls *.md
ls *.txt

# 安裝依賴
pip install -r requirements.txt

# 運行主程序
python multi_style_image_generator.py

# 運行演示
python quickstart_demo.py

# 查看生成的圖片
explorer generated_images

# 查看日誌
cat logs\generation_log_*.json
```

---

## 🎓 推薦學習路徑

**初級用戶** (1 小時):
1. 閱讀 QUICKSTART.md
2. 運行快速演示: `python quickstart_demo.py`
3. 查看生成的日誌

**中級用戶** (3 小時):
1. 閱讀 README.md
2. 運行主程序: `python multi_style_image_generator.py`
3. 嘗試不同風格和提示詞

**高級用戶** (5+ 小時):
1. 研究源代碼: `multi_style_image_generator.py`
2. 運行高級示例: `python advanced_examples.py`
3. 自定義參數和風格

---

## 🎉 完成確認

執行完所有步驟後，您將擁有：

✅ 完整的 AI 圖片生成系統  
✅ 5 種預設藝術風格  
✅ 中文提示詞支持  
✅ GPU 優化和加速  
✅ 完整的文檔和示例  
✅ 自動日誌記錄  
✅ 性能監控工具  

---

## 📞 支持資源

- **文檔**: `README.md` (完整)
- **快速指南**: `QUICKSTART.md`
- **代碼示例**: `advanced_examples.py`
- **項目總結**: `PROJECT_OVERVIEW.md`
- **疑難排除**: `README.md` 的【常見問題】

---

**準備好開始了嗎？**

執行:
```powershell
python quickstart_demo.py
```

或:
```powershell
python multi_style_image_generator.py
```

祝使用愉快！🎨✨

---

**最後更新**: 2025-12-06  
**版本**: 1.0.0
