# 下一步：啟用真實 AI 圖片生成

## 當前進度 ✅

你已經完成了：
- ✅ Streamlit 應用已運行（http://localhost:8501）
- ✅ 演示版本可以顯示佔位圖片
- 🔄 **現在正在安裝依賴函式庫**...

---

## 完整步驟指南

### 第 1 步：等待安裝完成 ⏳ **（CURRENT - 進行中）**

正在後臺安裝：
```
torch, torchvision, diffusers, transformers, deep-translator, pillow
```

**預計時間：** 5-15 分鐘（取決於網路速度和 GPU）

**檢查進度：** 看終端窗口中的進度條

---

### 第 2 步：安裝完成後，重啟 Streamlit 應用 🔄

當看到提示 `Successfully installed` 時：

1. **停止當前應用**
   - 在 Streamlit 終端中按 `Ctrl+C`

2. **啟動真實版本**
   ```powershell
   cd c:\Users\user\Desktop\HW4
   streamlit run streamlit_app_real.py
   ```

3. **打開應用**
   - http://localhost:8501

---

### 第 3 步：首次運行 - 下載 AI 模型 📥

**重要：** 首次使用每個風格時，會自動下載 AI 模型（5-50 GB）

這只需要做 **一次**，然後就會被保存。

**預計時間：**
- 首次下載模型：10-30 分鐘
- 之後生成圖片：20-100 秒（取決於步驟數和硬體）

---

### 第 4 步：開始生成圖片！ 🎨

應用準備好後：

1. **輸入提示詞**
   ```
   例：一座美麗的山，日出，清晨光線
   A beautiful mountain with sunrise and morning light
   ```

2. **選擇藝術風格**（5 種選擇）
   - Realistic（逼真）
   - Anime 2D（動漫）
   - Fantasy Art（奇幻）
   - 3D Rendering（3D 渲染）
   - Oil Painting（油畫）

3. **調整參數**
   - 圖片數量：1-4 張
   - 質量級別（步驟）：10-50
   - 指導強度：1.0-15.0

4. **點擊 "Generate Images"**
   - 等待生成完成
   - 查看結果！

---

## 🔧 故障排除

### 問題 1：安裝卡住或失敗

**解決方法：**
```powershell
# 重新安裝
pip install --upgrade pip
pip install torch torchvision
pip install diffusers transformers deep-translator pillow
```

### 問題 2：GPU 內存不足

**解決方法：**
1. 減少圖片數量
2. 降低步驟數（例如改為 20）
3. 選擇 CPU 模式

### 問題 3：模型下載失敗

**解決方法：**
1. 檢查網路連線
2. 重新啟動應用
3. 刪除模型快取：
   ```powershell
   Remove-Item $env:USERPROFILE\.cache\huggingface -Recurse -Force
   ```

---

## 📊 性能預期

### 使用 GPU（NVIDIA）
- 10 步：3-5 秒
- 20 步：8-12 秒
- 30 步：12-18 秒
- 50 步：20-30 秒

### 使用 CPU
- 10 步：20-40 秒
- 20 步：40-80 秒
- 30 步：60-120 秒
- 不建議超過 30 步

---

## 📁 檔案位置

| 檔案 | 用途 |
|------|------|
| `streamlit_app.py` | 當前演示版本 |
| `streamlit_app_real.py` | ⭐ 真實版本（新） |
| `multi_style_image_generator.py` | AI 生成核心模塊 |
| `requirements.txt` | 依賴列表 |
| `config.json` | 配置設定 |

---

## ✨ 5 種藝術風格詳解

### 1️⃣ Realistic（逼真）
- **模型：** runwayml/stable-diffusion-v1-5
- **最適合：** 風景、肖像、產品
- **例子：** "一隻躺在沙灘上的黃金獵犬，日落"

### 2️⃣ Anime 2D（動漫）
- **模型：** hakurei/waifu-diffusion
- **最適合：** 人物、角色、場景
- **例子：** "一個穿著魔法少女服裝的女孩，戰鬥姿態"

### 3️⃣ Fantasy Art（奇幻）
- **模型：** dreamlike-art/dreamlike-diffusion-1.0
- **最適合：** 魔法、生物、奇幻世界
- **例子：** "一隻神秘的龍在雲層中飛行"

### 4️⃣ 3D Rendering（3D 渲染）
- **模型：** stablediffusionapi/realistic-vision-v30
- **最適合：** 建築、產品、科技
- **例子：** "一個未來主義的城市，霓虹燈，夜晚"

### 5️⃣ Oil Painting（油畫）
- **模型：** nitrosocial/Ghibli-Diffusion
- **最適合：** 風景、藝術、裝飾
- **例子：** "向日葵田，黃昏陽光"

---

## 💡 提示詞編寫技巧

**好的提示詞：**
```
一隻白色的柴犬坐在公園裡，背景是櫻花樹，
陽光灑下，非常詳細和逼真的照片
```

**提高品質的關鍵詞：**
- 詳細的（detailed）
- 高品質（high quality）
- 專業的（professional）
- 傑作（masterpiece）
- 藝術性（artistic）

---

## 🎯 預期體驗

### 第一次運行
```
總時間：30-50 分鐘
- 下載模型：20-40 分鐘
- 首次生成：10-20 分鐘
```

### 之後每次
```
總時間：30-100 秒（取決於設定）
- 準備模型：5 秒
- 生成圖片：25-95 秒
```

---

## ❓ 常見問題

**Q: 為什麼需要下載模型？**
A: AI 模型是龐大的文件集合，需要下載才能在本地運行。

**Q: 模型存儲在哪裡？**
A: 用戶主目錄的 `.cache/huggingface` 資料夾。

**Q: 可以離線使用嗎？**
A: 是的，第一次下載後就可以離線使用。

**Q: 如何加快生成速度？**
A: 使用 GPU、減少步驟數、降低分辨率。

---

## ✅ 檢查清單

使用前檢查：
- [ ] PyTorch 已安裝（`python -c "import torch; print('OK')"` 無錯誤）
- [ ] Diffusers 已安裝
- [ ] GPU 驅動是最新的（如有 GPU）
- [ ] 硬碟有 50GB+ 自由空間
- [ ] 網路連線穩定

---

## 🚀 立即開始

等安裝完成後，只需運行：

```powershell
cd c:\Users\user\Desktop\HW4
streamlit run streamlit_app_real.py
```

然後開始生成驚人的 AI 藝術作品！

祝好運！🎉
