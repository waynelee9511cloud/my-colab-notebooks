# 自動化工作流程檔案索引

## Clinical Document Automation - 檔案總覽

本文檔列出所有與自動化工作流程相關的檔案及其用途。

---

## 📁 核心檔案

### 1. `automation_workflow.py` ⭐

**路徑**: `/clinical-doc-automation/automation_workflow.py`

**類型**: Python 腳本（可執行）

**大小**: ~1000+ 行程式碼

**功能**:
- 端到端自動化工作流程主控制器
- 整合所有文件生成模組
- CLI 命令列介面
- 批次處理功能
- 進度追蹤和日誌記錄
- 錯誤處理和報告生成

**主要類別**:
- `ClinicalDocAutomation` - 主要自動化類別
- `BatchProcessor` - 批次處理器
- `GenerationTask` - 任務管理
- `AutomationReport` - 報告生成

**使用方式**:
```bash
python automation_workflow.py --protocol protocol.pdf
```

---

## 📚 文檔檔案

### 2. `AUTOMATION_WORKFLOW_README.md` ⭐

**路徑**: `/clinical-doc-automation/AUTOMATION_WORKFLOW_README.md`

**類型**: Markdown 文檔

**功能**: 完整的使用說明文檔

**內容**:
- 功能特色介紹
- 詳細安裝指南
- 使用方法（CLI + Python API）
- 配置選項說明
- 錯誤處理指南
- 執行報告說明
- 進階功能
- 常見問題解答
- 完整範例

**適合對象**: 所有使用者

### 3. `QUICKSTART_AUTOMATION.md` ⭐

**路徑**: `/clinical-doc-automation/QUICKSTART_AUTOMATION.md`

**類型**: Markdown 快速開始指南

**功能**: 5 分鐘快速上手

**內容**:
- 3 步驟快速開始
- 常用命令範例
- 基本 Python 使用
- 常見設定
- 問題快速解決
- 使用技巧
- 檢查清單

**適合對象**: 新手使用者

### 4. `WORKFLOW_SUMMARY.md`

**路徑**: `/clinical-doc-automation/WORKFLOW_SUMMARY.md`

**類型**: Markdown 技術文檔

**功能**: 系統架構與工作流程詳解

**內容**:
- 系統架構圖
- 工作流程詳解（5 個階段）
- 核心類別和方法
- 執行流程時序圖
- 錯誤處理機制
- 效能考量
- 擴展性說明
- 最佳實踐

**適合對象**: 開發者、技術人員

### 5. `CLI_REFERENCE.md`

**路徑**: `/clinical-doc-automation/CLI_REFERENCE.md`

**類型**: Markdown 參考手冊

**功能**: 完整的 CLI 命令列參考

**內容**:
- 基本語法
- 快速參考
- 完整參數列表（含詳細說明）
- 使用範例（7 個範例）
- 退出碼說明
- 環境變數設定
- 錯誤處理
- Shell 腳本整合
- 與其他工具整合

**適合對象**: CLI 使用者、腳本開發者

### 6. `AUTOMATION_FILES_INDEX.md`（本檔案）

**路徑**: `/clinical-doc-automation/AUTOMATION_FILES_INDEX.md`

**類型**: Markdown 索引文檔

**功能**: 所有相關檔案的索引和導航

---

## 💡 範例檔案

### 7. `examples/automation_example.py` ⭐

**路徑**: `/clinical-doc-automation/examples/automation_example.py`

**類型**: Python 範例腳本（可執行）

**功能**: 7 個完整的使用範例

**包含範例**:
1. 基本使用 - 生成所有文件
2. 選擇性生成 - 只生成特定文件
3. 自訂輸出目錄
4. 批次處理
5. 錯誤處理
6. 使用執行報告
7. 使用環境變數

**使用方式**:
```bash
python examples/automation_example.py
```

---

## 🔧 工具檔案

### 8. `test_installation.py`

**路徑**: `/clinical-doc-automation/test_installation.py`

**類型**: Python 測試腳本（可執行）

**功能**: 驗證安裝和環境設置

**檢查項目**:
- Python 版本
- 依賴套件
- API Key 設置
- 模組導入
- 檔案結構
- 目錄權限
- 功能測試

**使用方式**:
```bash
python test_installation.py
```

**輸出**:
- 彩色的檢查結果
- 詳細的錯誤訊息
- 解決方案建議
- 總結報告

---

## 📦 依賴的模組

以下模組由自動化工作流程使用（已存在）：

### 9. `modules/protocol_parser.py`

**功能**: Protocol PDF 解析
- 使用 pdfplumber 讀取 PDF
- 使用 Gemini AI 提取結構化資訊
- 輸出 JSON 格式的 Protocol 資訊

### 10. `modules/crf_generator.py`

**功能**: CRF 文件生成
- 基於 Protocol 資訊生成 CRF
- 支援標準 CDISC 領域
- 生成 Word 格式文件

### 11. `modules/dvp_generator.py`

**功能**: DVP 文件生成
- 生成數據驗證規則
- 支援多種驗證類型
- 生成 Word 格式文件

### 12. `modules/user_guide_generator.py`

**功能**: User Guide 文件生成
- 生成 EDC/ePRO 系統使用指南
- 包含完整的操作流程
- 生成截圖需求清單

---

## 📊 檔案結構總覽

```
clinical-doc-automation/
│
├── automation_workflow.py                 ⭐ 主要執行檔
├── test_installation.py                   🔧 安裝測試工具
│
├── AUTOMATION_WORKFLOW_README.md          📚 完整使用說明
├── QUICKSTART_AUTOMATION.md               📚 快速開始指南
├── WORKFLOW_SUMMARY.md                    📚 系統架構文檔
├── CLI_REFERENCE.md                       📚 CLI 參考手冊
├── AUTOMATION_FILES_INDEX.md              📚 本檔案
│
├── examples/
│   └── automation_example.py              💡 7 個使用範例
│
├── modules/
│   ├── protocol_parser.py                 📦 Protocol 解析模組
│   ├── crf_generator.py                   📦 CRF 生成模組
│   ├── dvp_generator.py                   📦 DVP 生成模組
│   └── user_guide_generator.py            📦 User Guide 生成模組
│
└── requirements.txt                        📝 依賴套件清單
```

---

## 🎯 使用指南

### 我應該從哪裡開始？

#### 如果您是新手...
1. 先閱讀 [`QUICKSTART_AUTOMATION.md`](#3-quickstart_automationmd-) - 5 分鐘快速上手
2. 運行 `test_installation.py` 驗證環境
3. 查看 `examples/automation_example.py` 中的範例
4. 執行第一個自動化任務

#### 如果您想深入了解...
1. 閱讀 [`AUTOMATION_WORKFLOW_README.md`](#2-automation_workflow_readmemd-) - 完整文檔
2. 閱讀 [`WORKFLOW_SUMMARY.md`](#4-workflow_summarymd) - 技術架構
3. 查看各個模組的原始碼

#### 如果您主要使用命令列...
1. 閱讀 [`CLI_REFERENCE.md`](#5-cli_referencemd) - CLI 參考手冊
2. 查看常用命令範例
3. 學習如何整合到 Shell 腳本

#### 如果您想整合到現有系統...
1. 閱讀 `automation_workflow.py` 原始碼
2. 查看 Python API 使用範例
3. 參考 [`WORKFLOW_SUMMARY.md`](#4-workflow_summarymd) 中的擴展性章節

---

## 📖 文檔閱讀順序建議

### 快速上手路徑（30 分鐘）

```
1. QUICKSTART_AUTOMATION.md      (5 分鐘)
   └─> 快速開始指南

2. test_installation.py           (5 分鐘)
   └─> 驗證環境設置

3. examples/automation_example.py (10 分鐘)
   └─> 查看範例程式

4. 執行第一個任務                 (10 分鐘)
   └─> python automation_workflow.py --protocol test.pdf
```

### 完整學習路徑（2 小時）

```
1. QUICKSTART_AUTOMATION.md           (10 分鐘)
2. AUTOMATION_WORKFLOW_README.md      (40 分鐘)
3. CLI_REFERENCE.md                   (30 分鐘)
4. examples/automation_example.py     (20 分鐘)
5. 實際操作                           (20 分鐘)
```

### 技術深入路徑（4 小時）

```
1. QUICKSTART_AUTOMATION.md           (10 分鐘)
2. AUTOMATION_WORKFLOW_README.md      (40 分鐘)
3. WORKFLOW_SUMMARY.md                (60 分鐘)
4. automation_workflow.py 原始碼      (90 分鐘)
5. 各模組原始碼                       (40 分鐘)
```

---

## 🔍 快速查找

### 我想知道...

- **如何開始使用？** → [`QUICKSTART_AUTOMATION.md`](#3-quickstart_automationmd-)
- **所有功能列表？** → [`AUTOMATION_WORKFLOW_README.md`](#2-automation_workflow_readmemd-) 的「功能特色」章節
- **命令列參數說明？** → [`CLI_REFERENCE.md`](#5-cli_referencemd)
- **Python API 如何使用？** → [`AUTOMATION_WORKFLOW_README.md`](#2-automation_workflow_readmemd-) 的「Python API 使用」章節
- **如何批次處理？** → [`CLI_REFERENCE.md`](#5-cli_referencemd) 或 `examples/automation_example.py`
- **系統如何運作？** → [`WORKFLOW_SUMMARY.md`](#4-workflow_summarymd)
- **遇到錯誤怎麼辦？** → [`AUTOMATION_WORKFLOW_README.md`](#2-automation_workflow_readmemd-) 的「錯誤處理」章節
- **報告如何閱讀？** → [`AUTOMATION_WORKFLOW_README.md`](#2-automation_workflow_readmemd-) 的「執行報告」章節
- **如何擴展功能？** → [`WORKFLOW_SUMMARY.md`](#4-workflow_summarymd) 的「擴展性」章節

---

## 📈 檔案大小和統計

| 檔案 | 類型 | 行數（估計） | 大小 |
|------|------|-------------|------|
| `automation_workflow.py` | Python | ~1000 | ~40 KB |
| `examples/automation_example.py` | Python | ~400 | ~15 KB |
| `test_installation.py` | Python | ~350 | ~12 KB |
| `AUTOMATION_WORKFLOW_README.md` | Markdown | ~850 | ~45 KB |
| `QUICKSTART_AUTOMATION.md` | Markdown | ~400 | ~20 KB |
| `WORKFLOW_SUMMARY.md` | Markdown | ~700 | ~35 KB |
| `CLI_REFERENCE.md` | Markdown | ~800 | ~35 KB |
| `AUTOMATION_FILES_INDEX.md` | Markdown | ~450 | ~20 KB |
| **總計** | | **~4,950** | **~222 KB** |

---

## ✅ 功能檢查清單

使用以下清單確認您已經掌握所有功能：

### 基本功能
- [ ] 可以執行單個 Protocol 自動化
- [ ] 可以查看生成的文件
- [ ] 可以閱讀執行報告
- [ ] 理解輸出目錄結構

### CLI 使用
- [ ] 知道如何使用 `--protocol` 參數
- [ ] 知道如何使用 `--generate` 選擇文件類型
- [ ] 知道如何使用 `--output-dir` 指定輸出
- [ ] 知道如何使用 `--verbose` 查看詳細日誌

### 批次處理
- [ ] 可以使用 `--batch` 處理多個 Protocol
- [ ] 理解批次處理的輸出結構
- [ ] 可以查看批次處理摘要報告

### Python API
- [ ] 可以在 Python 程式中導入模組
- [ ] 可以創建 `ClinicalDocAutomation` 實例
- [ ] 可以調用 `run_all()` 方法
- [ ] 可以處理 `AutomationReport` 物件

### 進階功能
- [ ] 理解錯誤處理機制
- [ ] 知道如何使用環境變數
- [ ] 可以整合到 Shell 腳本
- [ ] 理解系統架構和擴展性

---

## 🎓 學習資源

### 初學者資源
1. [`QUICKSTART_AUTOMATION.md`](#3-quickstart_automationmd-) - 快速開始
2. `examples/automation_example.py` - 範例 1-3
3. [`CLI_REFERENCE.md`](#5-cli_referencemd) - 基本命令

### 中級資源
1. [`AUTOMATION_WORKFLOW_README.md`](#2-automation_workflow_readmemd-) - 完整文檔
2. `examples/automation_example.py` - 範例 4-7
3. [`CLI_REFERENCE.md`](#5-cli_referencemd) - 進階命令

### 進階資源
1. [`WORKFLOW_SUMMARY.md`](#4-workflow_summarymd) - 技術架構
2. `automation_workflow.py` - 原始碼
3. 各模組原始碼和文檔

---

## 🔗 相關連結

### 內部連結
- [Protocol Parser 文檔](PROTOCOL_PARSER_SUMMARY.md)
- [CRF Generator 文檔](CRF_GENERATOR_SUMMARY.md)
- [DVP Module 文檔](DVP_MODULE_SUMMARY.md)
- [User Guide Generator 文檔](USER_GUIDE_GENERATOR_SUMMARY.txt)

### 外部資源
- [Google AI Studio](https://makersuite.google.com/app/apikey) - 獲取 Gemini API Key
- [Python-docx 文檔](https://python-docx.readthedocs.io/)
- [PDFPlumber 文檔](https://github.com/jsvine/pdfplumber)

---

## 📝 更新日誌

### Version 1.0 (2025-11-18)
- ✅ 初始發布
- ✅ 完整的自動化工作流程
- ✅ CLI 命令列介面
- ✅ 批次處理功能
- ✅ 完整的文檔和範例
- ✅ 測試工具

---

## 💬 支援和反饋

如有問題或建議，請：

1. 查看相關文檔
2. 查看範例程式
3. 運行測試工具
4. 檢查日誌檔案

---

**最後更新**: 2025-11-18
**版本**: 1.0
**作者**: Clinical Documentation Automation Team

---

**快速開始**: 閱讀 [`QUICKSTART_AUTOMATION.md`](#3-quickstart_automationmd-) 並運行您的第一個自動化任務！🚀
