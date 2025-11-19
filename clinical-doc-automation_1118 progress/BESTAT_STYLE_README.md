# Bestat樣式分析器與範本生成器

## 概述

Bestat樣式分析器是一個強大的Word文件樣式管理工具，專為Bestat公司的臨床試驗文件設計，提供完整的樣式提取、套用、驗證和管理功能。

## 主要功能

### 1. 樣式提取 ✓
- 從現有Word範本提取完整樣式設定
- 包含頁面設定、字體、顏色、段落、頁首頁尾等
- 自動生成JSON配置檔案

### 2. 樣式套用 ✓
- 一鍵套用Bestat公司標準樣式
- 自動設定頁首（Logo、文件資訊）
- 自動設定頁尾（機密聲明、日期、頁碼）
- 支援自訂配置

### 3. 規範驗證 ✓
- 驗證文件是否符合Bestat規範
- 提供詳細的問題和警告清單
- 自動生成改進建議

### 4. 樣式比較 ✓
- 比較兩個文件的樣式差異
- 識別頁面、字體、顏色等方面的不同
- 生成詳細的差異報告

### 5. Word Formatter整合 ✓
- 無縫整合到現有WordFormatter模組
- 提供`apply_bestat_style()`便利方法
- 支援驗證和配置載入

## 檔案結構

```
clinical-doc-automation/
├── modules/
│   ├── bestat_style_analyzer.py       # 主模組（新）
│   ├── word_formatter.py              # Word Formatter（已整合）
│   └── test_bestat_style_analyzer.py  # 測試套件（新）
├── examples/
│   └── bestat_style_example.py        # 使用範例（新）
├── output/
│   ├── bestat_default_style.json      # 預設配置
│   └── bestat_examples/               # 範例輸出
├── BESTAT_STYLE_GUIDE.md              # 完整使用指南（新）
├── BESTAT_QUICK_REFERENCE.md          # 快速參考（新）
└── BESTAT_STYLE_README.md             # 本文件（新）
```

## 快速開始

### 安裝

```bash
pip install python-docx pillow
```

### 基本使用

```python
from modules.bestat_style_analyzer import BestatStyleAnalyzer
from docx import Document

# 初始化分析器
analyzer = BestatStyleAnalyzer()

# 建立或載入文件
doc = Document()
doc.add_paragraph("您的內容")

# 套用Bestat樣式
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="臨床試驗Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 驗證規範
validation = analyzer.validate_bestat_compliance(styled_doc)
if validation['compliant']:
    styled_doc.save("output.docx")
    print("✓ 文件符合Bestat規範")
```

### 與Word Formatter整合

```python
from modules.word_formatter import WordFormatter

formatter = WordFormatter()
formatter.create_document()

# 添加內容
formatter.apply_title_style("Protocol標題", level=1)
formatter.apply_body_style("Protocol內容...")

# 套用Bestat樣式
formatter.apply_bestat_style(
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 驗證並儲存
if formatter.validate_bestat_compliance()['compliant']:
    formatter.save_document("protocol.docx")
```

## 運行測試

```bash
# 運行完整測試套件
cd clinical-doc-automation/modules
python test_bestat_style_analyzer.py

# 運行使用範例
cd clinical-doc-automation/examples
python bestat_style_example.py
```

## Bestat標準樣式規範

### 頁面設定
- **紙張大小**：A4 (8.27" × 11.69")
- **方向**：直向
- **邊距**：上下左右各 1.0"

### 字體規範
| 元素 | 字體 | 大小 | 粗體 | 顏色 |
|------|------|------|------|------|
| 標題 | Arial | 18pt | ✓ | 深藍(0,51,153) |
| 一級標題 | Arial | 16pt | ✓ | 深藍 |
| 二級標題 | Arial | 14pt | ✓ | 亮藍(0,102,204) |
| 三級標題 | Arial | 12pt | ✓ | 亮藍 |
| 內文 | Calibri | 11pt | ✗ | 黑色 |
| 表格標題 | Arial | 10pt | ✓ | 白色/藍底 |
| 表格內文 | Calibri | 10pt | ✗ | 黑色 |

### 顏色方案
- **主色（深藍）**：RGB(0, 51, 153)
- **輔色（亮藍）**：RGB(0, 102, 204)
- **強調色（橙色）**：RGB(255, 153, 0)
- **機密標記（紅色）**：RGB(255, 0, 0)

### 頁首頁尾
- **頁首**：Logo（左）+ 文件資訊（右）+ 分隔線
- **頁尾**：機密聲明（左）+ 日期（中）+ 頁碼（右）+ 分隔線

## 核心API

### BestatStyleAnalyzer 類別

```python
# 初始化
analyzer = BestatStyleAnalyzer(config=None)

# 提取樣式
styles = analyzer.extract_styles_from_document("template.docx")

# 套用樣式
styled_doc = analyzer.apply_bestat_style(doc, title, protocol, version, logo_path)

# 驗證規範
validation = analyzer.validate_bestat_compliance(doc)

# 比較樣式
comparison = analyzer.compare_styles("doc1.docx", "doc2.docx")

# 儲存配置
analyzer.save_style_config("config.json", styles)

# 載入配置
analyzer.load_style_config("config.json")

# 生成報告
analyzer.generate_style_report("doc.docx", "report.json")
```

### 便利函數

```python
from modules.bestat_style_analyzer import (
    analyze_document_style,
    apply_bestat_style_to_document,
    validate_document_compliance
)

# 快速分析
analyze_document_style("input.docx", "styles.json")

# 快速套用
apply_bestat_style_to_document("input.docx", "output.docx", ...)

# 快速驗證
validate_document_compliance("document.docx")
```

### WordFormatter 整合方法

```python
formatter = WordFormatter()

# 套用Bestat樣式
formatter.apply_bestat_style(title, protocol, version, logo_path, config_path)

# 驗證規範
validation = formatter.validate_bestat_compliance()

# 提取樣式
styles = formatter.extract_bestat_styles(template_path, output_json)

# 載入配置
formatter.load_bestat_config(config_path)
```

## 使用場景

### 場景1：標準化新文件
```python
# 建立新Protocol文件並套用Bestat標準樣式
formatter = WordFormatter()
formatter.create_document()
# ... 添加內容 ...
formatter.apply_bestat_style(...)
formatter.save_document("protocol.docx")
```

### 場景2：從範本提取樣式
```python
# 從公司範本提取樣式並儲存為配置
analyzer = BestatStyleAnalyzer()
styles = analyzer.extract_styles_from_document("company_template.docx")
analyzer.save_style_config("company_style.json", styles)
```

### 場景3：批次處理文件
```python
# 批次套用Bestat樣式到多個文件
for file in document_list:
    doc = Document(file)
    styled_doc = analyzer.apply_bestat_style(doc, ...)
    styled_doc.save(f"bestat_{file}")
```

### 場景4：驗證文件規範
```python
# 驗證文件是否符合Bestat規範
validation = validate_document_compliance("protocol.docx")
if not validation['compliant']:
    print("需要修正的問題:")
    for issue in validation['issues']:
        print(f"  - {issue}")
```

### 場景5：自訂區域樣式
```python
# 為不同地區建立自訂樣式
taiwan_config = {
    "company_info": {"name": "Bestat Taiwan"},
    "fonts": {"title": {"name": "微軟正黑體"}}
}
analyzer = BestatStyleAnalyzer(config=taiwan_config)
```

## 測試覆蓋

測試套件包含以下測試：

1. ✓ 初始化測試
2. ✓ 預設配置測試
3. ✓ 樣式提取測試
4. ✓ 配置儲存與載入測試
5. ✓ Bestat樣式套用測試
6. ✓ 規範驗證測試
7. ✓ 樣式比較測試
8. ✓ 樣式報告生成測試
9. ✓ 便利函數測試
10. ✓ 自訂配置測試
11. ✓ 錯誤處理測試
12. ✓ Word Formatter整合測試

## 範例程式

範例程式包含9個完整範例：

1. 基本使用
2. 從範本提取樣式
3. 使用自訂配置
4. 驗證文件規範
5. 比較文件樣式
6. 生成樣式報告
7. Word Formatter整合
8. 批次處理
9. 使用便利函數

## 文件資源

- **完整指南**：`BESTAT_STYLE_GUIDE.md` - 詳細的功能說明和API參考
- **快速參考**：`BESTAT_QUICK_REFERENCE.md` - 常用功能速查表
- **使用範例**：`examples/bestat_style_example.py` - 完整的使用範例
- **測試套件**：`modules/test_bestat_style_analyzer.py` - 完整的測試程式

## 特色亮點

### 1. 完整的樣式管理
- 頁面設定（大小、邊距、方向）
- 字體樣式（名稱、大小、顏色、粗體、斜體）
- 顏色方案（主色、輔色、強調色）
- 段落格式（行距、間距、縮排）
- 頁首頁尾（Logo、文件資訊、頁碼）

### 2. 智能驗證系統
- 自動檢查頁面設定
- 驗證字體規範
- 確認頁首頁尾完整性
- 提供詳細的問題報告
- 給出改進建議

### 3. 靈活的配置管理
- JSON格式配置檔案
- 支援配置合併
- 版本控制友好
- 團隊共享方便

### 4. 無縫整合
- 完美整合Word Formatter
- 提供便利函數
- 支援批次處理
- 錯誤處理完善

## 最佳實踐

1. **使用版本控制**：將樣式配置JSON檔案納入版本控制
2. **建立範本庫**：為不同類型文件建立專用範本配置
3. **自動驗證**：在儲存前始終驗證文件規範
4. **團隊共享**：使用共享配置確保團隊樣式一致性
5. **錯誤處理**：使用try-except處理檔案操作錯誤

## 常見問題

**Q: 如何處理中文字體？**
A: 在配置中指定中文字體名稱，如"微軟正黑體"或"新細明體"。

**Q: 可以不使用Logo嗎？**
A: 可以，不提供logo_path參數即可。

**Q: 如何批次處理多個文件？**
A: 使用循環遍歷文件列表，逐一套用樣式。

**Q: 驗證失敗怎麼辦？**
A: 查看validation['issues']列表，根據具體問題修正。

**Q: 如何自訂樣式？**
A: 建立自訂配置字典，在初始化時傳入。

## 技術規格

- **Python版本**：3.7+
- **依賴套件**：python-docx, Pillow
- **支援格式**：.docx (Word 2007+)
- **配置格式**：JSON
- **編碼**：UTF-8

## 版本資訊

- **版本**：1.0.0
- **發布日期**：2025-11-18
- **作者**：Clinical Document Automation Team
- **授權**：Bestat Inc.

## 下一步

1. 查閱 `BESTAT_STYLE_GUIDE.md` 了解詳細功能
2. 運行 `test_bestat_style_analyzer.py` 進行測試
3. 執行 `bestat_style_example.py` 查看範例
4. 開始在您的專案中使用Bestat樣式分析器

---

**版權所有 © 2025 Bestat Inc. 保留所有權利。**
