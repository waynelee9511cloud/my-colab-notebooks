# Web UI 快速開始指南

## 🚀 3 分鐘快速上手

### 方法 1: Google Colab（最簡單）

1. **開啟示範筆記本**
   - 點擊 [Web_UI_Demo.ipynb](examples/Web_UI_Demo.ipynb)
   - 在 Google Colab 中開啟

2. **執行安裝**
   ```python
   # 執行第一個儲存格
   !pip install -q pdfplumber google-generativeai python-docx Pillow gradio python-dotenv
   ```

3. **啟動 Web UI**
   ```python
   # 執行啟動儲存格
   !python web_interface.py
   ```

4. **開啟公開連結**
   - 點擊顯示的 `https://xxxxx.gradio.live` 連結
   - 在新分頁中開始使用

**時間**: 約 2-3 分鐘

---

### 方法 2: 本地環境（Windows）

1. **下載專案**
   - 下載並解壓縮專案檔案

2. **雙擊啟動**
   - 找到 `launch_web_ui.bat` 檔案
   - 雙擊執行
   - 如果提示安裝依賴，選擇「Y」

3. **開啟瀏覽器**
   - 訪問 `http://localhost:7860`

**時間**: 約 3-5 分鐘（首次安裝需要下載套件）

---

### 方法 3: 本地環境（Mac/Linux）

1. **開啟終端機**
   ```bash
   cd clinical-doc-automation
   ```

2. **執行啟動腳本**
   ```bash
   ./launch_web_ui.sh
   ```
   或
   ```bash
   bash launch_web_ui.sh
   ```

3. **開啟瀏覽器**
   - 訪問 `http://localhost:7860`

**時間**: 約 3-5 分鐘

---

## 📝 使用流程（6 步驟）

### 步驟 1: 取得 API Key（只需一次）

1. 訪問 https://makersuite.google.com/app/apikey
2. 登入 Google 帳號
3. 點擊 "Create API Key"
4. 複製 API Key

⏱️ **時間**: 1 分鐘

---

### 步驟 2: 設定 API Key

1. 在 Web UI 中找到「API Key」輸入框
2. 貼上您的 API Key
3. 點擊「設定 API Key」
4. 看到 ✅ 成功訊息

⏱️ **時間**: 10 秒

---

### 步驟 3: 上傳 Protocol PDF

1. 點擊「Protocol PDF」上傳按鈕
2. 選擇您的 PDF 檔案
3. 等待上傳完成（顯示 ✅）

**可選**: 同時上傳公司 Logo

⏱️ **時間**: 10-30 秒（取決於檔案大小）

---

### 步驟 4: 解析 Protocol

1. 點擊「開始解析 Protocol」
2. 等待 AI 分析（進度條會顯示）
3. 查看提取的資訊（JSON 格式）

⏱️ **時間**: 30-60 秒

---

### 步驟 5: 選擇文件類型

勾選您想要生成的文件：

- ☑️ CRF (病例報告表)
- ☑️ DVP (資料驗證計劃)
- ☑️ User Guide (使用者指南)
- ☑️ DMP (資料管理計劃)

⏱️ **時間**: 5 秒

---

### 步驟 6: 生成並下載

1. 點擊「一鍵生成文件」
2. 等待生成完成（進度條顯示）
3. 點擊下載按鈕獲取文件

⏱️ **時間**: 每個文件約 30-60 秒

---

## 📋 完整範例

### 範例 1: 生成單個 CRF

```
1. 設定 API Key ✓
2. 上傳 Protocol.pdf ✓
3. 解析 Protocol（等待 45 秒）✓
4. 勾選「CRF」✓
5. 點擊生成（等待 40 秒）✓
6. 下載 CRF.docx ✓

總時間: 約 2 分鐘
```

### 範例 2: 生成全套文件

```
1. 設定 API Key ✓
2. 上傳 Protocol.pdf 和 Logo.png ✓
3. 解析 Protocol（等待 45 秒）✓
4. 勾選全部文件類型 ✓
5. 點擊生成（等待 3 分鐘）✓
6. 下載所有文件 ✓

總時間: 約 4-5 分鐘
```

### 範例 3: 自訂資訊後生成

```
1. 設定 API Key ✓
2. 上傳 Protocol.pdf ✓
3. 解析 Protocol（等待 45 秒）✓
4. 在 JSON 編輯器中修改資訊 ✓
5. 點擊「更新資訊」✓
6. 勾選文件類型 ✓
7. 點擊生成 ✓
8. 下載文件 ✓

總時間: 約 5-6 分鐘（包含編輯時間）
```

---

## 💡 使用技巧

### 技巧 1: 提高解析準確度

- ✅ 使用高品質 PDF（非掃描版）
- ✅ 確保 PDF 文字可以複製
- ✅ Protocol 結構清晰、標準化
- ✅ 解析後仔細檢查關鍵資訊

### 技巧 2: 加快生成速度

- ✅ 只選擇需要的文件類型
- ✅ 確保網路連線穩定
- ✅ 在 Colab 中使用（雲端運算）
- ✅ 避免同時處理多個大型 Protocol

### 技巧 3: 優化生成結果

- ✅ 上傳公司 Logo 使文件更專業
- ✅ 在 JSON 中補充缺失的資訊
- ✅ 調整訪視時程和終點指標
- ✅ 添加特定的納入/排除標準

### 技巧 4: 批次處理

如需處理多個 Protocol：

1. 完成第一個 Protocol 的處理
2. 下載生成的文件
3. 重新上傳新的 PDF
4. 重複步驟 3-6

不需要關閉或重啟 Web UI！

---

## ⚠️ 注意事項

### ✓ 重要提醒

1. **API Key 安全**
   - 不要分享您的 API Key
   - API Key 僅在會話中使用，不會被儲存

2. **文件審核**
   - 生成的文件需要專業人員審核
   - 確認醫學術語和定義的準確性
   - 檢查是否符合法規要求

3. **檔案大小**
   - Protocol PDF 建議小於 50 MB
   - 過大的檔案可能導致處理緩慢

4. **會話時間**
   - Colab 會話有時間限制（約 12 小時）
   - 長時間無操作會自動斷線
   - 建議定期保存結果

5. **網路連線**
   - 需要穩定的網路連線
   - 解析和生成過程需要調用 API
   - 斷線可能導致操作失敗

---

## 🐛 常見問題快速解決

| 問題 | 解決方法 |
|------|---------|
| 無法開啟 Web UI | 檢查 Python 是否已安裝，執行啟動腳本 |
| API Key 無效 | 重新生成 API Key，確認無多餘空格 |
| PDF 解析失敗 | 確認 PDF 非掃描版，文字可複製 |
| 生成失敗 | 檢查 Protocol 資訊是否完整，查看錯誤訊息 |
| 下載失敗 | 清除瀏覽器快取，重新生成 |
| 進度條卡住 | 耐心等待，AI 處理需要時間 |
| 公開連結過期 | 重新啟動 Web UI，生成新連結 |

詳細的故障排除，請參考 [WEB_UI_README.md](WEB_UI_README.md)

---

## 📚 進階學習

準備好深入了解？查看這些資源：

- **完整文檔**: [WEB_UI_README.md](WEB_UI_README.md)
- **Protocol Parser**: [PROTOCOL_PARSER_SUMMARY.md](PROTOCOL_PARSER_SUMMARY.md)
- **CRF Generator**: [CRF_GENERATOR_SUMMARY.md](CRF_GENERATOR_SUMMARY.md)
- **DVP Generator**: [DVP_MODULE_SUMMARY.md](DVP_MODULE_SUMMARY.md)
- **User Guide Generator**: [USER_GUIDE_GENERATOR_SUMMARY.txt](USER_GUIDE_GENERATOR_SUMMARY.txt)

---

## 🎯 下一步

### 新手路徑

1. ✅ 完成快速開始（本指南）
2. 📖 閱讀完整的 [WEB_UI_README.md](WEB_UI_README.md)
3. 🧪 嘗試使用範例 Protocol
4. 🔧 探索自訂設定

### 進階路徑

1. ✅ 熟悉 Web UI 基本操作
2. 💻 了解各個模組的功能
3. 🛠️ 自訂文件模板
4. 🔗 整合到現有工作流程

---

## 🆘 需要幫助？

### 查閱文檔

- 完整文檔: [WEB_UI_README.md](WEB_UI_README.md)
- 常見問題: 文檔中的「常見問題」章節
- 故障排除: 文檔中的「故障排除」章節

### 技術支援

如果文檔無法解決您的問題，請：

1. 檢查錯誤訊息的詳細內容
2. 查看日誌輸出
3. 聯繫開發團隊

---

## ✨ 總結

### 使用 Web UI 只需 3 步驟：

1. **啟動**: 開啟 Web UI（Colab 或本地）
2. **上傳**: 上傳 Protocol PDF 並解析
3. **生成**: 選擇文件類型並一鍵生成

### 總時間：

- **首次使用**: 約 5-10 分鐘（包含安裝）
- **後續使用**: 約 2-5 分鐘（每個 Protocol）

### 開始使用：

- **Colab**: 開啟 [Web_UI_Demo.ipynb](examples/Web_UI_Demo.ipynb)
- **本地**: 執行 `launch_web_ui.bat` (Windows) 或 `./launch_web_ui.sh` (Mac/Linux)

---

**準備好了嗎？立即開始使用臨床試驗文件自動化系統！** 🚀

---

**版本**: 1.0.0
**更新日期**: 2025-11-18
**作者**: Clinical Data Automation Team
