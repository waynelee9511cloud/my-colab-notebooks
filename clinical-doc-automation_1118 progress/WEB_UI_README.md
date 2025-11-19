# 臨床試驗文件自動化系統 - Web UI 使用指南

## 📖 目錄

1. [簡介](#簡介)
2. [功能特點](#功能特點)
3. [系統需求](#系統需求)
4. [安裝指南](#安裝指南)
5. [快速開始](#快速開始)
6. [詳細使用說明](#詳細使用說明)
7. [在 Google Colab 中使用](#在-google-colab-中使用)
8. [本地環境使用](#本地環境使用)
9. [故障排除](#故障排除)
10. [常見問題](#常見問題)
11. [進階設定](#進階設定)

---

## 簡介

臨床試驗文件自動化系統 Web UI 是一個基於 Gradio 的網頁應用程式，提供友善的圖形化介面，讓使用者可以輕鬆地：

- 上傳 Protocol PDF 並自動提取關鍵資訊
- 生成多種臨床試驗文件（CRF、DVP、User Guide、DMP）
- 自訂和編輯提取的資訊
- 一鍵下載生成的文件

無需編寫任何程式碼，即可完成複雜的文件生成任務！

---

## 功能特點

### ✅ 核心功能

- **PDF 解析**: 使用 AI 自動提取 Protocol 中的關鍵資訊
- **多文件生成**: 支援 CRF、DVP、User Guide、DMP 四種文件類型
- **資訊編輯**: 提供 JSON 編輯器，可自訂提取的資訊
- **進度顯示**: 即時顯示處理進度
- **檔案管理**: 支援上傳 PDF 和 Logo，下載生成的文件

### ✅ 使用者體驗

- **友善介面**: 直觀的步驟式操作流程
- **中英文支援**: 介面和文檔支援中英文
- **即時反饋**: 每個操作都有明確的狀態提示
- **錯誤處理**: 詳細的錯誤訊息和解決建議

### ✅ 技術特點

- **雲端部署**: 在 Google Colab 中可以一鍵啟動
- **本地運行**: 也支援在本地環境中運行
- **公開分享**: 在 Colab 中自動創建公開連結
- **安全性**: API Key 僅在會話中使用，不會被儲存

---

## 系統需求

### 必要條件

- **Python 版本**: 3.8 或以上
- **網路連線**: 需要連線到 Google Gemini API
- **瀏覽器**: Chrome、Firefox、Safari 或 Edge（最新版本）

### 推薦配置

- **記憶體**: 至少 2 GB RAM
- **儲存空間**: 至少 500 MB 可用空間
- **處理器**: 雙核心或以上

---

## 安裝指南

### 方法 1: 在 Google Colab 中使用（推薦）

Google Colab 提供免費的雲端運算資源，適合快速體驗和測試。

1. 開啟 [Web_UI_Demo.ipynb](examples/Web_UI_Demo.ipynb)
2. 按照筆記本中的指示操作
3. 無需本地安裝任何軟體

### 方法 2: 本地安裝

#### 步驟 1: 克隆或下載專案

```bash
# 使用 git 克隆（如果專案在 GitHub 上）
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO/clinical-doc-automation

# 或直接下載 ZIP 檔案並解壓縮
```

#### 步驟 2: 創建虛擬環境（推薦）

```bash
# 創建虛擬環境
python -m venv venv

# 啟動虛擬環境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

#### 步驟 3: 安裝依賴套件

```bash
pip install -r requirements.txt
```

---

## 快速開始

### 在 Google Colab 中

1. 開啟 [Web_UI_Demo.ipynb](examples/Web_UI_Demo.ipynb)
2. 執行所有代碼儲存格
3. 點擊顯示的公開連結開啟 Web UI
4. 按照介面指示操作

### 在本地環境中

1. 開啟終端機並切換到專案目錄

```bash
cd clinical-doc-automation
```

2. 啟動 Web UI

```bash
python web_interface.py
```

3. 在瀏覽器中開啟顯示的網址（通常是 `http://localhost:7860`）

---

## 詳細使用說明

### 步驟 1: 設定 Gemini API Key

#### 1.1 取得 API Key

1. 訪問 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 使用 Google 帳號登入
3. 點擊 **"Create API Key"** 或 **"Get API Key"**
4. 複製生成的 API Key

#### 1.2 在 Web UI 中設定

1. 在「步驟 1: 設定 Gemini API Key」區域找到輸入框
2. 貼上您的 API Key
3. 點擊 **"設定 API Key"** 按鈕
4. 看到「✅ API Key已設定成功！」訊息表示設定完成

**注意**: API Key 僅在當前會話中使用，關閉瀏覽器後會自動清除。

---

### 步驟 2: 上傳檔案

#### 2.1 上傳 Protocol PDF（必填）

1. 在「Protocol PDF (必填)」區域點擊上傳按鈕
2. 選擇您的 Protocol PDF 檔案
3. 等待上傳完成
4. 看到「✅ PDF已上傳成功！」訊息

**支援的格式**: PDF
**檔案大小限制**: 建議小於 50 MB
**內容要求**: PDF 必須包含可提取的文字（不支援純圖片掃描版）

#### 2.2 上傳公司 Logo（選填）

1. 在「公司 Logo (選填)」區域點擊上傳按鈕
2. 選擇您的 Logo 圖片檔案
3. 等待上傳完成

**支援的格式**: PNG、JPG、JPEG
**建議尺寸**: 300x100 像素或類似比例
**用途**: Logo 會出現在生成的文件頁首

---

### 步驟 3: 解析 Protocol

1. 確認已完成步驟 1 和 2.1
2. 點擊 **"開始解析 Protocol"** 按鈕
3. 等待 AI 分析（通常需要 30-60 秒）
4. 解析完成後，提取的資訊會顯示在下方的 JSON 編輯器中

**解析內容包括**:
- 試驗標題和編號
- 贊助商資訊
- 試驗階段和設計
- 目標族群和樣本數
- 訪視時程
- 主要和次要終點指標
- 納入和排除標準
- 所需的 CRF 領域

---

### 步驟 4: 編輯 Protocol 資訊（可選）

解析完成後，您可以在 JSON 編輯器中查看和修改提取的資訊。

#### 4.1 查看資訊

- 提取的資訊以 JSON 格式顯示
- 可以展開或摺疊各個欄位
- 支援語法高亮

#### 4.2 編輯資訊

1. 直接在編輯器中修改 JSON 內容
2. 確保 JSON 格式正確（使用引號、逗號等）
3. 點擊 **"更新資訊"** 按鈕保存修改
4. 看到「✅ Protocol資訊已更新！」訊息表示更新成功

**編輯範例**:

```json
{
  "study_title": "修改後的試驗標題",
  "protocol_number": "PROTO-2025-001",
  "sponsor": "公司名稱",
  "phase": "Phase II",
  ...
}
```

---

### 步驟 5: 選擇文件類型

在「步驟 5: 選擇要生成的文件類型」區域，勾選您想要生成的文件：

#### 文件類型說明

1. **CRF (病例報告表)**
   - 用於收集臨床試驗資料的表單
   - 包含所有訪視的資料收集欄位
   - 基於 Protocol 的訪視時程和終點指標生成

2. **DVP (資料驗證計劃)**
   - 定義資料驗證規則和流程
   - 包含資料完整性檢查和邏輯驗證
   - 確保收集的資料品質

3. **User Guide (使用者指南)**
   - EDC 系統使用手冊
   - 提供詳細的操作步驟和截圖
   - 幫助使用者正確填寫 CRF

4. **DMP (資料管理計劃)**
   - 描述資料管理策略和流程
   - 包含資料收集、清理、鎖定等流程
   - 符合 GCP 規範

**提示**: 您可以同時選擇多個文件類型，系統會依序生成。

---

### 步驟 6: 生成文件

1. 確認已選擇至少一種文件類型
2. 點擊 **"一鍵生成文件"** 按鈕
3. 觀察進度條顯示生成進度
4. 等待所有文件生成完成

**生成時間**:
- 單個文件: 約 30-60 秒
- 多個文件: 時間會累加

---

### 步驟 7: 下載文件

生成完成後：

1. 在「下載生成的文件」區域會顯示所有生成的文件
2. 點擊各個檔案的下載按鈕
3. 檔案會下載到您的本地電腦

**檔案格式**: Microsoft Word (.docx)
**檔案命名**: `{Protocol編號}_{文件類型}.docx`

---

## 在 Google Colab 中使用

### 優點

- ✅ 無需安裝任何軟體
- ✅ 免費的雲端運算資源
- ✅ 自動創建公開分享連結
- ✅ 可以在任何裝置上訪問

### 啟動步驟

1. 開啟 [Web_UI_Demo.ipynb](examples/Web_UI_Demo.ipynb)
2. 按順序執行以下儲存格：
   - 安裝依賴套件
   - 準備專案檔案（上傳或克隆）
   - 驗證專案結構
   - 啟動 Web UI
3. 點擊顯示的公開連結（類似 `https://xxxxx.gradio.live`）
4. 在新分頁中開始使用

### 注意事項

- Colab 會話有時間限制（通常 12 小時）
- 長時間無操作會自動斷線
- 斷線後需要重新執行所有儲存格
- 建議定期儲存筆記本

---

## 本地環境使用

### 啟動服務

```bash
# 方法 1: 直接執行
python web_interface.py

# 方法 2: 自訂端口
python web_interface.py --port 8080
```

### 訪問介面

啟動後，在瀏覽器中開啟顯示的網址：

- 本地訪問: `http://localhost:7860`
- 區域網路訪問: `http://YOUR_IP:7860`

### 創建公開連結

如果需要分享給其他人，可以在代碼中設定 `share=True`：

```python
from web_interface import ClinicalDocWebUI

web_ui = ClinicalDocWebUI()
web_ui.launch(share=True, server_port=7860)
```

這會創建一個臨時的公開連結（有效期 72 小時）。

---

## 故障排除

### 問題 1: 模組導入錯誤

**錯誤訊息**:
```
ModuleNotFoundError: No module named 'gradio'
```

**解決方法**:
```bash
pip install gradio
# 或安裝所有依賴
pip install -r requirements.txt
```

---

### 問題 2: API Key 無效

**錯誤訊息**:
```
❌ API Key 驗證失敗
```

**解決方法**:
1. 確認 API Key 是否正確（無多餘空格）
2. 檢查 API Key 是否已啟用
3. 訪問 [Google AI Studio](https://makersuite.google.com/app/apikey) 重新生成
4. 確認您的 Google 帳號有權限使用 Gemini API

---

### 問題 3: PDF 解析失敗

**錯誤訊息**:
```
❌ 解析失敗: Unable to extract text from PDF
```

**可能原因和解決方法**:

1. **PDF 是掃描版或圖片**
   - 解決: 使用 OCR 工具先轉換為文字 PDF
   - 推薦工具: Adobe Acrobat、Online OCR

2. **PDF 被加密**
   - 解決: 先解除 PDF 加密保護

3. **PDF 檔案損壞**
   - 解決: 嘗試重新下載或生成 PDF

4. **PDF 太大**
   - 解決: 壓縮 PDF 或分段處理

---

### 問題 4: 文件生成失敗

**錯誤訊息**:
```
❌ 生成失敗: [具體錯誤訊息]
```

**解決方法**:

1. **檢查 Protocol 資訊是否完整**
   - 確認 JSON 中的關鍵欄位不為空
   - 特別是 `study_title`, `protocol_number` 等

2. **檢查輸出目錄權限**
   ```bash
   # 確認 output 目錄存在且可寫入
   mkdir -p output
   chmod 755 output
   ```

3. **檢查記憶體**
   - 生成大型文件可能需要較多記憶體
   - 嘗試關閉其他程式

4. **查看詳細錯誤**
   - 錯誤訊息會顯示詳細的堆疊追蹤
   - 根據錯誤訊息進行相應處理

---

### 問題 5: Web UI 無法訪問

**現象**: 無法開啟 Web UI 網址

**解決方法**:

1. **確認服務已啟動**
   ```bash
   # 檢查是否有錯誤訊息
   python web_interface.py
   ```

2. **檢查端口是否被占用**
   ```bash
   # Linux/Mac
   lsof -i :7860

   # Windows
   netstat -ano | findstr :7860
   ```

3. **嘗試不同的端口**
   ```python
   web_ui.launch(server_port=8080)
   ```

4. **檢查防火牆設定**
   - 確認防火牆沒有阻擋該端口

5. **清除瀏覽器快取**
   - 按 Ctrl+Shift+Delete 清除快取
   - 或使用無痕模式

---

### 問題 6: 公開連結過期

**現象**: Gradio 公開連結顯示「Link Expired」

**解決方法**:

1. **重新啟動 Web UI**
   - 公開連結有 72 小時有效期
   - 重新執行代碼會生成新連結

2. **在 Colab 中重新執行儲存格**
   ```python
   # 重新執行啟動 Web UI 的儲存格
   web_ui.launch(share=True)
   ```

---

## 常見問題

### Q1: 需要付費嗎？

**A**:
- **Gemini API**: 目前提供免費額度，足夠一般使用
- **Gradio**: 完全免費和開源
- **Google Colab**: 提供免費的基礎版本
- **本專案**: 完全免費

### Q2: 生成的文件可以直接使用嗎？

**A**: 生成的文件提供了良好的基礎架構和內容，但仍需要專業人員進行以下檢查：

- 醫學術語和定義的準確性
- Protocol 特定的細節
- 法規要求的完整性
- 格式和排版的調整

建議將生成的文件作為初稿，經過審核和修改後再使用。

### Q3: 支援哪些語言的 Protocol？

**A**:
- 目前主要支援英文 Protocol
- 中文 Protocol 也可以處理，但準確度可能略低
- 其他語言需要測試

### Q4: 可以自訂文件模板嗎？

**A**:
- 目前使用預設的專業模板
- 進階使用者可以修改 `modules/` 中的生成器代碼
- 未來版本會提供更靈活的模板自訂功能

### Q5: 資料安全嗎？

**A**:
- 上傳的 PDF 僅在會話中使用
- API Key 不會被儲存
- 生成的文件儲存在本地或 Colab 臨時目錄
- 建議不要上傳包含敏感個資的文件

### Q6: 可以批次處理多個 Protocol 嗎？

**A**:
- 當前版本一次處理一個 Protocol
- 您可以重複使用同一個 Web UI 實例處理多個文件
- 批次處理功能計劃在未來版本中加入

### Q7: 生成文件需要多久？

**A**:
- PDF 解析: 30-60 秒
- 單個文件生成: 30-60 秒
- 多個文件: 時間累加
- 總時間取決於 Protocol 複雜度和網路速度

### Q8: 為什麼解析結果不完整？

**A**: 可能的原因：

1. **Protocol 結構不標準**
   - 解決: 手動編輯 JSON 補充資訊

2. **PDF 品質問題**
   - 解決: 使用更清晰的 PDF

3. **AI 模型限制**
   - 解決: 嘗試使用更高級的模型（如 `gemini-1.5-pro`）

4. **關鍵資訊位置特殊**
   - 解決: 在 JSON 編輯器中手動添加

---

## 進階設定

### 使用不同的 AI 模型

預設使用 `gemini-1.5-flash`（快速、免費），您可以修改為其他模型：

```python
from web_interface import ClinicalDocWebUI

web_ui = ClinicalDocWebUI()

# 修改模型（需要在生成器中設定）
# gemini-1.5-flash: 快速、免費
# gemini-1.5-pro: 更準確、可能需要付費
```

### 自訂輸出目錄

```python
import os

# 設定自訂輸出目錄
output_dir = "/path/to/your/output"
os.makedirs(output_dir, exist_ok=True)

# 在生成器中使用
```

### 設定日誌級別

```python
import logging

# 設定為 DEBUG 以查看詳細資訊
logging.basicConfig(level=logging.DEBUG)

# 或設定為 WARNING 只顯示警告和錯誤
logging.basicConfig(level=logging.WARNING)
```

### 整合到現有系統

如果您想將 Web UI 整合到現有的系統中：

```python
from web_interface import ClinicalDocWebUI

# 創建實例
web_ui = ClinicalDocWebUI()

# 自訂設定
web_ui.api_key = "your_api_key"
web_ui.pdf_path = "path/to/protocol.pdf"

# 程式化調用
status, json_result = web_ui.parse_protocol()
status, files = web_ui.generate_documents(["CRF", "DVP"])
```

---

## 更新和維護

### 檢查更新

```bash
# 如果專案在 GitHub 上
git pull origin main
```

### 更新依賴套件

```bash
pip install --upgrade -r requirements.txt
```

### 回報問題

如果您遇到任何問題或有功能建議，請：

1. 查看本文檔的故障排除章節
2. 檢查是否有相關的文檔
3. 聯繫開發團隊

---

## 授權和聲明

### 授權

本專案僅供教育和研究目的使用。

### 免責聲明

- 生成的文件需經過專業人員審核後才能用於正式用途
- 使用者需自行確保符合相關法規要求
- 開發團隊不對使用本系統產生的任何後果負責

### 隱私政策

- 本系統不會儲存您的 API Key
- 上傳的檔案僅在會話中使用
- 生成的文件儲存在本地或您指定的位置
- 建議不要上傳包含敏感個資的文件

---

## 聯絡資訊

**開發團隊**: Clinical Data Automation Team
**版本**: 1.0.0
**最後更新**: 2025-11-18

---

## 附錄

### A. 鍵盤快捷鍵

- `Ctrl + Enter`: 在文字輸入框中提交
- `Ctrl + A`: 選擇全部（在編輯器中）
- `Ctrl + Z`: 撤銷（在編輯器中）
- `Ctrl + S`: 保存（部分瀏覽器支援）

### B. 支援的 Protocol 結構

系統最佳支援以下結構的 Protocol：

- ICH E6 GCP 指南格式
- 包含清晰的章節標題
- 有明確的訪視時程表
- 詳細列出納入/排除標準
- 明確定義主要和次要終點

### C. 文件模板結構

生成的文件遵循以下行業標準：

- **CRF**: CDISC CDASH 標準
- **DVP**: GCDMP 指南
- **User Guide**: 使用者友善的步驟式說明
- **DMP**: ICH E6 和 FDA 指南

### D. 範例檔案

專案包含以下範例檔案：

- `examples/Web_UI_Demo.ipynb`: Web UI 示範筆記本
- `examples/Protocol_Parser_Demo.ipynb`: Protocol 解析示範

---

**感謝使用臨床試驗文件自動化系統！**

如果本系統對您有幫助，歡迎分享給您的同事和朋友。

祝您工作順利！🎉
