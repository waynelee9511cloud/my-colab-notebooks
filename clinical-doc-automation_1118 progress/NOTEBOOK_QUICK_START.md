# 臨床試驗文件自動化系統 - 快速開始指南

## 📋 系統概述

這是一個完整整合的 Google Colab Notebook，整合了五個核心模組，提供臨床試驗文件的一鍵生成功能。

### 📦 檔案位置
```
clinical-doc-automation/Clinical_Trial_Document_Automation_System.ipynb
```

---

## 🚀 快速開始（5分鐘上手）

### 步驟 1: 開啟 Notebook

在 Google Colab 中開啟：
1. 訪問 https://colab.research.google.com/
2. 點擊 `File` → `Upload notebook`
3. 上傳 `Clinical_Trial_Document_Automation_System.ipynb`

或者在本地 Jupyter 環境中開啟：
```bash
cd clinical-doc-automation
jupyter notebook Clinical_Trial_Document_Automation_System.ipynb
```

### 步驟 2: 執行安裝（Section 1）

執行前兩個 code cells：
1. 安裝套件
2. 驗證安裝

等待約 1-2 分鐘完成套件安裝。

### 步驟 3: 設定環境（Section 2）

執行 Section 2 的所有 cells：
1. 導入基礎模組
2. 設置專案結構
3. 導入自訂模組

**重要**: 如果在 Colab 中，需要先上傳 `modules` 資料夾！

### 步驟 4: 配置參數（Section 3）

1. **設定 API Key**
   - 輸入您的 Gemini API Key
   - 如何取得: https://makersuite.google.com/app/apikey

2. **上傳檔案**
   - 📄 Protocol PDF（必須）
   - 🖼️ Logo 圖片（選填）
   - 📋 Word 範本（選填）

3. **設定參數**
   - 贊助商名稱
   - 試驗階段
   - 選擇要生成的文件類型

### 步驟 5: 一鍵生成（Section 8）

點擊「🚀 一鍵生成所有文件」按鈕，系統將自動：
1. 解析 Protocol PDF
2. 生成 CRF
3. 生成 DVP
4. 生成 User Guide

⏱️ 預計時間：3-5 分鐘

### 步驟 6: 下載結果（Section 9）

選擇下載方式：
- 📥 個別下載所有檔案
- 📦 下載 ZIP 壓縮檔（推薦）

---

## 📚 功能特點

### ✅ 五大核心模組

1. **Protocol Parser（試驗書解析器）**
   - 自動從 PDF 提取關鍵資訊
   - 使用 Google Gemini AI
   - 支援中英文

2. **CRF Generator（病例報告表生成器）**
   - 自動生成 CRF 表單
   - 支援多種欄位類型
   - 專業 Word 格式

3. **DVP Generator（資料驗證計畫生成器）**
   - 自動生成驗證規則
   - 包含範圍、一致性、Protocol 偏差檢查
   - 輸出詳細 DVP 文件

4. **User Guide Generator（使用者手冊生成器）**
   - 自動生成 CRF 填寫說明
   - 包含欄位說明和範例
   - 支援螢幕截圖

5. **Word Formatter（文件格式化工具）**
   - 統一文件格式
   - 添加頁首、頁尾、Logo
   - 專業臨床試驗文件

### 🎯 生成文件

執行後將獲得：
1. **Protocol_Info.json** - Protocol 結構化資訊
2. **Protocol_CRF.docx** - 病例報告表
3. **Protocol_DVP.docx** - 資料驗證計畫
4. **Protocol_DVP_rules.json** - 驗證規則 JSON
5. **Protocol_User_Guide.docx** - 使用者手冊

---

## 🔧 使用模式

### 模式一：一鍵生成（推薦新手）

適合：快速生成所有文件

步驟：
1. 設定 API Key
2. 上傳 Protocol PDF
3. 點擊「一鍵生成」
4. 下載結果

優點：
- ✅ 簡單快速
- ✅ 自動化流程
- ✅ 適合標準 Protocol

### 模式二：逐步執行（推薦進階用戶）

適合：需要檢查中間結果或自訂設定

步驟：
1. Section 4: 解析 Protocol（檢查提取資訊）
2. Section 5: 生成 CRF（可自訂欄位）
3. Section 6: 生成 DVP（可添加自訂規則）
4. Section 7: 生成 User Guide（可修改說明）
5. Section 9: 下載結果

優點：
- ✅ 更多控制權
- ✅ 可檢查中間結果
- ✅ 可自訂內容

---

## 💡 使用技巧

### API Key 管理

**方法 1: 直接輸入（測試用）**
```python
api_key_input.value = "YOUR_API_KEY"
```

**方法 2: Colab Secrets（推薦）**
```python
from google.colab import userdata
api_key = userdata.get('GEMINI_API_KEY')
```

### 檔案上傳

**Colab 環境：**
- 使用介面按鈕上傳
- 檔案會儲存在 session 中

**本地環境：**
- 手動設定檔案路徑
- 修改 `uploaded_files` 字典

### 參數優化

**快速模式：**
- 使用 `gemini-1.5-flash`
- 速度快、免費額度高

**高品質模式：**
- 使用 `gemini-1.5-pro`
- 更準確但較慢

---

## ❓ 常見問題

### Q1: Colab 中 modules 資料夾找不到？

**A:** 在 Colab 中需要手動上傳 modules 資料夾：
1. 點擊左側檔案圖示
2. 上傳整個 `modules` 資料夾
3. 重新執行 Section 2

### Q2: API Key 錯誤？

**A:** 確認：
- API Key 正確複製（無多餘空格）
- API Key 已啟用
- 網路連線正常

### Q3: Protocol 解析失敗？

**A:** 檢查：
- PDF 是否可正常開啟
- PDF 文字是否可選取（非掃描版）
- PDF 大小是否合理（建議 < 50MB）

### Q4: 生成時間太長？

**A:** 可能原因：
- Protocol 太大（試試限制頁數）
- 網路速度慢
- API 配額限制

解決方法：
- 使用 `gemini-1.5-flash`
- 限制 `max_pages=50`
- 分批生成文件

### Q5: 下載失敗？

**A:** 在 Colab 中：
- 檢查瀏覽器彈出視窗設定
- 使用 ZIP 下載（較穩定）
- 或從左側檔案面板手動下載

---

## 🎓 進階功能

### 自訂驗證規則

在 Section 6 中添加：

```python
# 添加自訂 DVP 規則
dvp_gen.add_custom_rule(
    description="血壓收案標準檢查",
    query_text="請驗證收縮壓 ≥140 或舒張壓 ≥90",
    severity=Severity.CRITICAL,
    validation_type=ValidationType.PROTOCOL_DEVIATION,
    form_name="生命徵象"
)
```

### 自訂 CRF 欄位

在 Section 5 中添加：

```python
# 添加自訂 CRF 欄位
custom_fields = [
    CRFField(
        "custom_field",
        "自訂欄位",
        "自訂表單",
        "text",
        required=True
    )
]
```

### 批次處理

處理多個 Protocol：

```python
protocols = ['protocol1.pdf', 'protocol2.pdf', 'protocol3.pdf']

for protocol_pdf in protocols:
    uploaded_files['protocol_pdf'] = protocol_pdf
    generate_all_documents()
```

---

## 📊 效能指標

### 處理時間（參考）

| 步驟 | 時間 | 說明 |
|------|------|------|
| Protocol 解析 | 30-60秒 | 取決於 PDF 大小 |
| CRF 生成 | 1-2分鐘 | 取決於表單數量 |
| DVP 生成 | 1-2分鐘 | 取決於欄位數量 |
| User Guide 生成 | 1-2分鐘 | 取決於表單數量 |
| **總計** | **3-5分鐘** | 完整流程 |

### 資源需求

- **記憶體**: 約 500MB
- **儲存空間**: 約 50MB（含輸出）
- **網路**: 需要穩定連線（API 呼叫）

### API 配額

免費額度（Gemini）：
- Flash: 15 RPM, 1M TPM
- Pro: 2 RPM, 32K TPM

---

## 🔒 資料安全

### 隱私保護

- ✅ 所有處理在您的 session 中進行
- ✅ PDF 僅傳送給 Google Gemini API
- ✅ 不會儲存在第三方伺服器
- ✅ Session 結束後自動清除

### 建議做法

1. 使用去識別化的 Protocol
2. 不要在 Notebook 中儲存 API Key
3. 定期清理輸出資料夾
4. 下載後刪除 Colab 檔案

---

## 📞 支援資源

### 文件

- `README.md` - 專案總覽
- `modules/README.md` - 模組說明
- 各模組的 QUICKSTART 文件

### 範例

- `examples/` 資料夾中有各模組的使用範例
- 可參考學習進階用法

---

## 🚀 更新日誌

### v1.0.0 (2025-11-18)

**新功能：**
- ✅ 整合 5 個核心模組
- ✅ 一鍵生成功能
- ✅ 互動式 UI（ipywidgets）
- ✅ 檔案上傳介面
- ✅ 進度顯示
- ✅ ZIP 下載功能

**核心模組：**
- Protocol Parser v1.0
- CRF Generator v1.0
- DVP Generator v1.0
- User Guide Generator v1.0
- Word Formatter v1.0

---

## 🎉 開始使用

準備好了嗎？立即開啟 Notebook 開始使用！

```bash
# 本地環境
jupyter notebook Clinical_Trial_Document_Automation_System.ipynb

# 或上傳到 Google Colab
# https://colab.research.google.com/
```

---

**祝您使用順利！如有任何問題，請參考常見問題或聯絡開發團隊。**
