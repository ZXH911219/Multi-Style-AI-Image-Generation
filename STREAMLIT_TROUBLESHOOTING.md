# 🚀 Streamlit 應用 - 快速修復指南

## 📋 問題診斷

**症狀**: 輸入提示詞後沒有圖片生成

**原因**: 需要安裝完整的依賴包 (torch, diffusers 等)

---

## ✅ 快速修復方案

### 步驟 1: 安裝所有依賴

打開 PowerShell，執行：

```powershell
cd c:\Users\user\Desktop\HW4
pip install -r requirements.txt
```

**預期時間**: 10-15 分鐘  
**網絡要求**: 穩定的互聯網連接 (500MB+ 下載)

### 步驟 2: 驗證安裝

檢查所有必要的包是否已安裝：

```powershell
python -c "import torch; import diffusers; import transformers; print('✓ All packages installed')"
```

### 步驟 3: 重新啟動 Streamlit

停止當前的應用 (按 Ctrl+C)，然後重新啟動：

```powershell
cd c:\Users\user\Desktop\HW4
streamlit run streamlit_app.py
```

### 步驟 4: 測試生成

1. 打開瀏覽器訪問 `http://localhost:8502`
2. 輸入提示詞 (例如："美麗的森林")
3. 選擇風格
4. 點擊 "🎨 生成圖片"

---

## 🔍 詳細故障排除

### 問題 1: ImportError - 找不到 torch

**症狀**: `ModuleNotFoundError: No module named 'torch'`

**解決方案**:
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 問題 2: CUDA/GPU 錯誤

**症狀**: `CUDA out of memory` 或 `No CUDA device found`

**解決方案**:
1. 在 Streamlit 應用中選擇 **"CPU"** 模式
2. 或減少生成數量和推理步數

### 問題 3: 下載模型超時

**症狀**: 應用卡在下載模型

**解決方案**:
- 確保有穩定的網絡連接
- 檢查 Hugging Face API 是否可訪問
- 可能需要設置代理

### 問題 4: 應用無法啟動

**症狀**: `streamlit: command not found`

**解決方案**:
```powershell
pip install streamlit --upgrade
```

---

## 📦 requirements.txt 內容

應確保包含以下包：

```
torch>=2.0.0
diffusers>=0.21.0
transformers>=4.30.0
pillow>=9.5.0
numpy>=1.24.0
deep-translator>=1.11.4
accelerate>=0.20.0
safetensors>=0.3.0
streamlit>=1.28.0
```

---

## 🎯 完整安裝步驟 (推薦)

### 方案 A: 使用 Pip (簡單快速)

```powershell
# 進入項目目錄
cd c:\Users\user\Desktop\HW4

# 安裝所有依賴
pip install -r requirements.txt

# 啟動應用
streamlit run streamlit_app.py
```

### 方案 B: 使用 Conda (完整隔離)

```powershell
# 創建新環境
conda create -n ai_gen python=3.10

# 啟用環境
conda activate ai_gen

# 進入項目目錄
cd c:\Users\user\Desktop\HW4

# 安裝依賴
pip install -r requirements.txt

# 啟動應用
streamlit run streamlit_app.py
```

---

## ✨ 應用功能確認

### 成功的標誌

✅ 應用在瀏覽器中打開  
✅ 可以輸入提示詞  
✅ 可以選擇風格  
✅ 可以調整參數  
✅ 點擊生成後出現進度條  
✅ 生成完成後顯示圖片  

### 預期的生成時間

| 情況 | 時間 |
|------|------|
| 首次運行 (下載模型) | 10-30 分鐘 |
| 後續運行 (GPU, 30 步) | 30-60 秒 |
| 後續運行 (CPU, 30 步) | 3-5 分鐘 |

---

## 🎓 使用示例

### 示例 1: 寫實風景

```
提示詞: 美麗的山水風景，陽光照射，清晨時分
風格: Realistic
數量: 1
步數: 30
強度: 7.5
設備: cuda (或 cpu)
```

### 示例 2: 動漫角色

```
提示詞: 魔法少女，穿著紅色和服，閃閃發光
風格: Anime 2D
數量: 4
步數: 30
強度: 7.5
設備: cuda (或 cpu)
```

---

## 📞 進一步幫助

### 如果還是無法生成

1. **查看應用側欄**
   - 側欄有安裝指南
   - 常見問題解答
   - 系統信息

2. **查看項目文檔**
   - STREAMLIT_GUIDE.md - 完整指南
   - README.md - API 文檔
   - SETUP_GUIDE.md - 環境設置

3. **檢查日誌**
   - 終端會顯示詳細錯誤信息
   - 查看 logs/ 目錄中的生成日誌

### 聯繫支持

如果問題持續存在：
1. 檢查網絡連接
2. 確認 Python 版本 >= 3.8
3. 嘗試重新安裝依賴
4. 查看錯誤信息中的具體問題

---

## 🔄 快速重啟流程

如果需要重新開始：

```powershell
# 1. 停止當前應用 (按 Ctrl+C)

# 2. 清除緩存
python -c "import streamlit; print(streamlit.caching.clear_cache())"

# 3. 重新啟動
streamlit run streamlit_app.py --logger.level=debug
```

---

## ✅ 確認清單

在聯繫支持前，請確認：

- [ ] Python 版本 >= 3.8
- [ ] 已執行 `pip install -r requirements.txt`
- [ ] 已驗證包安裝: `python -c "import torch; print('OK')"`
- [ ] 網絡連接穩定
- [ ] Streamlit 版本 >= 1.28.0
- [ ] 磁盤空間充足 (100GB+)
- [ ] 沒有其他程序占用 GPU

---

**版本**: 1.0.0  
**更新**: 2025-12-07  
**狀態**: 故障排除指南

祝您使用愉快！如有問題，請參考本指南。🎨✨
