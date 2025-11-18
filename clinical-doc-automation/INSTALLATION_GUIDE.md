# 安裝指南 - 臨床試驗文件自動化系統

> 完整的安裝、配置和驗證指南

---

## 📋 目錄

1. [系統需求](#系統需求)
2. [安裝步驟](#安裝步驟)
3. [配置設定](#配置設定)
4. [驗證安裝](#驗證安裝)
5. [常見問題](#常見問題)
6. [故障排除](#故障排除)

---

## 💻 系統需求

### 最低需求

| 項目 | 需求 |
|------|------|
| **作業系統** | Windows 10+, macOS 10.15+, Linux (Ubuntu 18.04+) |
| **Python** | 3.8 或更高版本 |
| **RAM** | 2 GB |
| **硬碟空間** | 500 MB |
| **網路** | 穩定的網際網路連線（用於 API 調用）|

### 建議配置

| 項目 | 建議 |
|------|------|
| **作業系統** | Windows 11, macOS 13+, Ubuntu 22.04+ |
| **Python** | 3.10 或 3.11 |
| **RAM** | 4 GB 或更多 |
| **硬碟空間** | 1 GB 或更多 |
| **網路** | 高速網路（提升 AI 調用速度）|

### 軟體依賴

- Python 3.8+
- pip (Python 套件管理器)
- Microsoft Word 或 LibreOffice Writer（用於查看生成的文件）
- 網頁瀏覽器（Chrome、Firefox、Edge、Safari）

---

## 🚀 安裝步驟

### 方法 1: 在 Google Colab 使用（最簡單，推薦）⭐

**優點**: 無需安裝，雲端運行，免費 GPU

**步驟**:

1. **開啟 Google Colab**
   ```
   訪問: https://colab.research.google.com/
   ```

2. **上傳 Notebook**
   - 點擊「檔案」→「上傳筆記本」
   - 選擇 `Clinical_Trial_Document_Automation_System.ipynb`

3. **上傳模組資料夾**
   - 在左側檔案面板中
   - 點擊「上傳」圖示
   - 上傳整個 `modules/` 資料夾

4. **執行 Section 1-2**
   - 自動安裝所有依賴
   - 無需手動配置

5. **完成！**
   - 參閱 `NOTEBOOK_QUICK_START.md` 開始使用

**時間**: 約 5 分鐘

---

### 方法 2: Windows 安裝

#### 步驟 1: 檢查 Python

打開「命令提示字元」（CMD）:

```cmd
python --version
```

如果顯示 Python 3.8+，跳到步驟 3。否則，繼續步驟 2。

#### 步驟 2: 安裝 Python

1. 訪問 https://www.python.org/downloads/
2. 下載最新的 Python 3.11
3. 執行安裝程式
   - ✅ **重要**: 勾選「Add Python to PATH」
4. 完成安裝
5. 重啟命令提示字元
6. 再次檢查：`python --version`

#### 步驟 3: 下載專案

方法 A（如果有 Git）:
```cmd
git clone <repository-url>
cd clinical-doc-automation
```

方法 B（沒有 Git）:
1. 下載專案 ZIP 檔
2. 解壓縮到任意位置
3. 在命令提示字元中進入該資料夾

#### 步驟 4: 建立虛擬環境（建議）

```cmd
python -m venv venv
venv\Scripts\activate
```

看到 `(venv)` 前綴表示成功。

#### 步驟 5: 安裝依賴

```cmd
pip install -r requirements.txt
```

等待安裝完成（約 2-5 分鐘）。

#### 步驟 6: 驗證安裝

```cmd
python test_installation.py
```

看到「✓ 所有檢查通過」表示成功。

#### 步驟 7: 啟動 Web UI

```cmd
launch_web_ui.bat
```

或手動執行：
```cmd
python web_interface.py
```

瀏覽器會自動開啟 http://localhost:7860

**完成！** 🎉

---

### 方法 3: macOS/Linux 安裝

#### 步驟 1: 檢查 Python

打開「終端機」:

```bash
python3 --version
```

如果顯示 Python 3.8+，跳到步驟 3。

#### 步驟 2: 安裝 Python（如果需要）

**macOS**:
```bash
# 使用 Homebrew
brew install python@3.11
```

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

**CentOS/RHEL**:
```bash
sudo yum install python3.11
```

#### 步驟 3: 下載專案

```bash
# 如果有 Git
git clone <repository-url>
cd clinical-doc-automation

# 或下載 ZIP 後解壓縮
unzip clinical-doc-automation.zip
cd clinical-doc-automation
```

#### 步驟 4: 建立虛擬環境

```bash
python3 -m venv venv
source venv/bin/activate
```

看到 `(venv)` 前綴表示成功。

#### 步驟 5: 安裝依賴

```bash
pip install -r requirements.txt
```

#### 步驟 6: 驗證安裝

```bash
python test_installation.py
```

#### 步驟 7: 啟動 Web UI

```bash
chmod +x launch_web_ui.sh  # 給予執行權限
./launch_web_ui.sh
```

或手動執行：
```bash
python web_interface.py
```

**完成！** 🎉

---

## ⚙️ 配置設定

### 1. 取得 Gemini API Key

**重要**: 系統需要 Google Gemini API Key 才能運行。

**步驟**:

1. 訪問 https://makersuite.google.com/app/apikey
2. 使用 Google 帳號登入
3. 點擊「Create API key」（建立 API 金鑰）
4. 點擊「Create API key in new project」
5. 複製生成的 API Key（格式類似：AIzaSy...）

**費用**: 完全免費
- Gemini 1.5 Flash: 每天 1,500 次免費請求
- Gemini 1.5 Pro: 每天 50 次免費請求
- 一般使用下免費額度綽綽有餘

### 2. 設定 API Key

**方法 A: Web UI（推薦）**
- 啟動 Web UI
- 在第一個輸入框中貼上 API Key
- 點擊「設定 API Key」

**方法 B: 環境變數**

Windows (CMD):
```cmd
setx GEMINI_API_KEY "your-api-key-here"
```

Windows (PowerShell):
```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

macOS/Linux:
```bash
# 暫時設定（本次 session）
export GEMINI_API_KEY="your-api-key-here"

# 永久設定（加入 ~/.bashrc 或 ~/.zshrc）
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**方法 C: 在代碼中設定**
```python
from automation_workflow import ClinicalDocAutomation

automation = ClinicalDocAutomation(
    protocol_pdf="protocol.pdf",
    api_key="your-api-key-here"  # 直接傳入
)
```

### 3. 可選配置

**設定輸出目錄**:
```python
# 預設: output/
automation = ClinicalDocAutomation(
    protocol_pdf="protocol.pdf",
    api_key="your-key",
    output_dir="my_custom_output"  # 自訂
)
```

**選擇 AI 模型**:
```python
from modules.protocol_parser import ProtocolParser

# Flash 模型（快速、免費額度高）
parser = ProtocolParser(api_key="your-key", model="gemini-1.5-flash")

# Pro 模型（準確度更高）
parser = ProtocolParser(api_key="your-key", model="gemini-1.5-pro")
```

---

## ✅ 驗證安裝

### 自動驗證（推薦）

執行測試腳本：

```bash
python test_installation.py
```

**檢查項目**:
1. ✓ Python 版本（3.8+）
2. ✓ 依賴套件已安裝
3. ✓ API Key 設定正確
4. ✓ 模組可正常導入
5. ✓ 檔案結構完整
6. ✓ 目錄權限正確
7. ✓ 功能測試通過

**預期輸出**:
```
臨床試驗文件自動化系統 - 安裝驗證
======================================

1. Python 版本檢查... ✓ 通過
2. 依賴套件檢查... ✓ 通過
3. API Key 檢查... ✓ 通過
4. 模組導入檢查... ✓ 通過
5. 檔案結構檢查... ✓ 通過
6. 目錄權限檢查... ✓ 通過
7. 功能測試... ✓ 通過

======================================
✅ 所有檢查通過！系統已準備就緒。
```

### 手動驗證

**測試 1: 檢查 Python 套件**
```bash
python -c "import docx; import pdfplumber; import google.generativeai as genai; print('✓ 所有套件正常')"
```

**測試 2: 檢查模組**
```bash
python -c "from modules.protocol_parser import ProtocolParser; from modules.crf_generator import CRFGenerator; print('✓ 模組導入成功')"
```

**測試 3: 檢查 Web UI**
```bash
python -c "import gradio; print('✓ Gradio 已安裝')"
```

**測試 4: 運行快速範例**
```bash
python examples/quick_test.py
```

---

## ❓ 常見問題

### Q1: `pip install` 失敗

**錯誤**: `Could not find a version that satisfies the requirement`

**解決方法**:
```bash
# 更新 pip
python -m pip install --upgrade pip

# 重試安裝
pip install -r requirements.txt
```

---

### Q2: 找不到 Python 或 pip

**Windows**:
- 重新安裝 Python，確保勾選「Add Python to PATH」
- 重啟命令提示字元

**macOS/Linux**:
```bash
# 使用 python3 和 pip3
python3 --version
pip3 install -r requirements.txt
```

---

### Q3: 導入模組錯誤

**錯誤**: `ModuleNotFoundError: No module named 'modules'`

**解決方法**:
```bash
# 確保在正確的目錄中
cd /path/to/clinical-doc-automation

# 確認目錄結構
ls modules/  # 應該看到 *.py 檔案

# 重新執行
python web_interface.py
```

---

### Q4: Gemini API 錯誤

**錯誤**: `Invalid API key`

**解決方法**:
1. 檢查 API Key 是否正確（沒有多餘空格）
2. 確認 API Key 已啟用
3. 訪問 https://makersuite.google.com/app/apikey 檢查狀態
4. 嘗試建立新的 API Key

**錯誤**: `Quota exceeded`

**解決方法**:
1. 等待配額重置（每天重置）
2. 或使用新的 Google 帳號建立新 API Key
3. 或升級到付費方案（不推薦，免費額度通常足夠）

---

### Q5: Web UI 無法啟動

**錯誤**: `Address already in use`

**解決方法**:
```bash
# 使用不同的埠號
python web_interface.py --port 7861

# 或找到並關閉佔用 7860 埠的程式
# Windows:
netstat -ano | findstr :7860

# macOS/Linux:
lsof -i :7860
```

---

### Q6: 權限錯誤

**Windows**:
- 以系統管理員身分執行命令提示字元

**macOS/Linux**:
```bash
# 給予執行權限
chmod +x launch_web_ui.sh
chmod +x *.sh

# 或使用 sudo（不建議）
sudo python web_interface.py
```

---

### Q7: 虛擬環境問題

**忘記啟用虛擬環境**:

Windows:
```cmd
venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

**刪除並重新建立虛擬環境**:
```bash
# 刪除舊的
rm -rf venv  # Linux/Mac
rd /s venv   # Windows

# 重新建立
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 重新安裝
pip install -r requirements.txt
```

---

## 🔧 故障排除

### 診斷工具

**1. 執行完整診斷**:
```bash
python test_installation.py --verbose
```

**2. 檢查日誌**:
```bash
# 查看最新日誌
cat automation.log

# Windows:
type automation.log
```

**3. 測試單一模組**:
```bash
# 測試 Protocol Parser
python modules/test_protocol_parser.py

# 測試 CRF Generator
python modules/test_crf_generator.py

# 測試 DVP Generator
python modules/test_dvp_generator.py
```

### 完整重置

如果一切都失敗，完整重新安裝：

```bash
# 1. 刪除虛擬環境
rm -rf venv/  # Linux/Mac
rd /s venv    # Windows

# 2. 清理快取
rm -rf __pycache__/
rm -rf modules/__pycache__/
rm -rf examples/__pycache__/

# 3. 重新建立虛擬環境
python -m venv venv

# 4. 啟用虛擬環境
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 5. 更新 pip
pip install --upgrade pip

# 6. 重新安裝依賴
pip install -r requirements.txt

# 7. 驗證
python test_installation.py
```

---

## 📞 獲得幫助

如果以上都無法解決問題：

1. **查看文檔**
   - `README.md` - 主要文檔
   - `FAQ.md` - 常見問題
   - 各模組的 `README_*.md`

2. **檢查範例**
   - `examples/` 資料夾中的範例代碼
   - 確保按照範例的方式使用

3. **查看日誌**
   - `automation.log` - 詳細日誌
   - 錯誤訊息通常包含解決方案

4. **系統資訊**
   準備以下資訊：
   - 作業系統和版本
   - Python 版本
   - 錯誤訊息完整內容
   - 執行的命令
   - `test_installation.py` 的輸出

---

## 🎉 安裝成功！

如果 `test_installation.py` 顯示所有檢查通過，恭喜您！系統已準備就緒。

**下一步**:

### 🌐 使用 Web UI（最簡單）
```bash
python web_interface.py
# 開啟瀏覽器訪問 http://localhost:7860
```
📖 參閱：`WEB_UI_QUICKSTART.md`

### ☁️ 使用 Google Colab
開啟 `Clinical_Trial_Document_Automation_System.ipynb`
📖 參閱：`NOTEBOOK_QUICK_START.md`

### 💻 使用命令列
```bash
python automation_workflow.py --protocol your_protocol.pdf
```
📖 參閱：`QUICKSTART_AUTOMATION.md`

### 🐍 使用 Python API
```python
from automation_workflow import ClinicalDocAutomation
automation = ClinicalDocAutomation("protocol.pdf", "api-key")
report = automation.run_all()
```
📖 參閱：`AUTOMATION_WORKFLOW_README.md`

---

**祝您使用順利！** 🚀
