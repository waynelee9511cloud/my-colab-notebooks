# Bestat公司文件樣式分析器使用指南

## 目錄

1. [簡介](#簡介)
2. [安裝與設定](#安裝與設定)
3. [核心功能](#核心功能)
4. [快速開始](#快速開始)
5. [進階使用](#進階使用)
6. [API參考](#api參考)
7. [最佳實踐](#最佳實踐)
8. [常見問題](#常見問題)

---

## 簡介

Bestat樣式分析器是一個專門為Bestat公司設計的Word文件樣式管理工具，提供以下核心功能：

### 主要特色

- **樣式提取**：從現有Word文件提取完整的樣式設定
- **樣式套用**：自動套用Bestat公司標準樣式到文件
- **規範驗證**：驗證文件是否符合Bestat公司規範
- **樣式比較**：比較兩個文件的樣式差異
- **配置管理**：支援JSON格式的樣式配置檔案
- **Word Formatter整合**：無縫整合到現有的Word Formatter模組

### Bestat標準樣式規範

Bestat公司的文件樣式規範包含：

#### 頁面設定
- **紙張大小**：A4 (8.27" × 11.69")
- **方向**：直向 (Portrait)
- **邊距**：上下左右各 1.0 英寸
- **頁首距離**：0.5 英寸
- **頁尾距離**：0.5 英寸

#### 字體規範
- **標題字體**：Arial, 18pt, 粗體, Bestat藍色 (RGB: 0, 51, 153)
- **一級標題**：Arial, 16pt, 粗體, Bestat藍色
- **二級標題**：Arial, 14pt, 粗體, 亮藍色 (RGB: 0, 102, 204)
- **三級標題**：Arial, 12pt, 粗體, 亮藍色
- **內文**：Calibri, 11pt, 常規, 黑色, 兩端對齊
- **表格標題**：Arial, 10pt, 粗體, 白色字 + 藍色背景
- **表格內文**：Calibri, 10pt, 常規, 黑色

#### 顏色方案
- **主色（深藍）**：RGB(0, 51, 153) - 用於標題和重點
- **輔色（亮藍）**：RGB(0, 102, 204) - 用於次要標題
- **強調色（橙色）**：RGB(255, 153, 0) - 用於特殊標記
- **機密標記（紅色）**：RGB(255, 0, 0) - 用於機密聲明

#### 段落格式
- **行距**：1.15
- **段前間距**：0pt
- **段後間距**：10pt
- **首行縮排**：無

#### 頁首內容
- **位置**：Logo在左，文件資訊在右
- **Logo尺寸**：寬1.5"，高0.6"
- **包含資訊**：文件標題、Protocol編號、版本、日期
- **底部分隔線**：80個底線符號

#### 頁尾內容
- **三欄式佈局**：
  - 左：機密聲明 (CONFIDENTIAL, 紅色粗體)
  - 中：日期
  - 右：頁碼 (Page X of Y)
- **頂部分隔線**：80個底線符號

---

## 安裝與設定

### 系統需求

- Python 3.7 或更高版本
- python-docx 套件
- Pillow 套件（用於處理圖片）

### 安裝步驟

```bash
# 1. 安裝必要套件
pip install python-docx pillow

# 2. 確認檔案結構
clinical-doc-automation/
├── modules/
│   ├── bestat_style_analyzer.py  # 主模組
│   ├── word_formatter.py          # Word Formatter（已整合）
│   └── test_bestat_style_analyzer.py  # 測試套件
├── examples/
│   └── bestat_style_example.py    # 使用範例
└── output/                         # 輸出目錄
```

### 驗證安裝

```python
# 測試導入
from modules.bestat_style_analyzer import BestatStyleAnalyzer

# 建立實例
analyzer = BestatStyleAnalyzer()
print("安裝成功！")
```

---

## 核心功能

### 1. 樣式提取

從現有Word文件提取所有樣式設定：

```python
from modules.bestat_style_analyzer import BestatStyleAnalyzer

analyzer = BestatStyleAnalyzer()
styles = analyzer.extract_styles_from_document("template.docx")

# styles 包含以下內容：
# - page_setup: 頁面設定
# - fonts: 字體樣式
# - colors: 顏色方案
# - paragraph_spacing: 段落格式
# - header: 頁首設定
# - footer: 頁尾設定
# - table_style: 表格樣式
# - logo_info: Logo資訊
# - metadata: 文件元數據
```

### 2. 樣式套用

套用Bestat標準樣式到文件：

```python
from docx import Document

analyzer = BestatStyleAnalyzer()
doc = Document("input.docx")

# 套用Bestat樣式
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="臨床試驗Protocol",
    protocol_number="PRO-2025-001",
    version="1.0",
    logo_path="bestat_logo.png"  # 可選
)

styled_doc.save("output.docx")
```

### 3. 規範驗證

驗證文件是否符合Bestat規範：

```python
doc = Document("document.docx")
validation = analyzer.validate_bestat_compliance(doc)

print(f"符合規範: {validation['compliant']}")
print(f"問題數: {validation['total_issues']}")
print(f"警告數: {validation['total_warnings']}")

# 顯示具體問題
for issue in validation['issues']:
    print(f"問題: {issue}")

for warning in validation['warnings']:
    print(f"警告: {warning}")
```

### 4. 樣式比較

比較兩個文件的樣式差異：

```python
comparison = analyzer.compare_styles("doc1.docx", "doc2.docx")

print(f"總差異數: {comparison['total_differences']}")

# 查看各類別的差異
for category, differences in comparison['differences'].items():
    if differences:
        print(f"\n{category} 差異:")
        for diff in differences:
            print(f"  - {diff}")
```

### 5. 配置管理

#### 儲存配置到JSON

```python
# 儲存預設配置
analyzer.save_style_config("bestat_default.json")

# 儲存提取的樣式
styles = analyzer.extract_styles_from_document("template.docx")
analyzer.save_style_config("my_style.json", styles)
```

#### 載入配置

```python
# 從JSON載入配置
analyzer.load_style_config("my_style.json")

# 或在初始化時指定自訂配置
custom_config = {
    "company_info": {
        "name": "Bestat Taiwan"
    },
    "fonts": {
        "title": {
            "size": 20
        }
    }
}

analyzer = BestatStyleAnalyzer(config=custom_config)
```

---

## 快速開始

### 範例1：建立標準Bestat文件

```python
from docx import Document
from modules.bestat_style_analyzer import BestatStyleAnalyzer

# 初始化
analyzer = BestatStyleAnalyzer()

# 建立文件並添加內容
doc = Document()
doc.add_paragraph("第一章 研究背景")
doc.add_paragraph("本研究旨在評估新藥的療效...")

# 套用Bestat樣式
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="第三期臨床試驗Protocol",
    protocol_number="PRO-2025-PHASE3",
    version="2.0",
    logo_path="bestat_logo.png"
)

# 驗證規範
validation = analyzer.validate_bestat_compliance(styled_doc)
if validation['compliant']:
    print("✓ 文件符合Bestat規範")
    styled_doc.save("protocol.docx")
else:
    print("✗ 發現問題，請修正:")
    for issue in validation['issues']:
        print(f"  - {issue}")
```

### 範例2：使用Word Formatter整合

```python
from modules.word_formatter import WordFormatter

# 建立Word Formatter實例
formatter = WordFormatter()
formatter.create_document()

# 添加內容
formatter.apply_title_style("臨床試驗Protocol", level=1)
formatter.apply_body_style("研究目的：評估新藥安全性和有效性。")

# 套用Bestat樣式
formatter.apply_bestat_style(
    document_title="臨床試驗Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 驗證
validation = formatter.validate_bestat_compliance()
print(f"符合規範: {validation['compliant']}")

# 儲存
formatter.save_document("protocol_formatted.docx")
```

### 範例3：從範本提取並套用

```python
# 步驟1：從公司範本提取樣式
analyzer = BestatStyleAnalyzer()
styles = analyzer.extract_styles_from_document("bestat_template.docx")
analyzer.save_style_config("bestat_extracted.json", styles)

# 步驟2：套用到新文件
new_analyzer = BestatStyleAnalyzer()
new_analyzer.load_style_config("bestat_extracted.json")

doc = Document("draft.docx")
styled_doc = new_analyzer.apply_bestat_style(
    doc,
    document_title="新Protocol",
    protocol_number="PRO-2025-NEW",
    version="1.0"
)

styled_doc.save("final.docx")
```

---

## 進階使用

### 自訂Bestat樣式

```python
# 定義自訂配置（Taiwan分公司範例）
taiwan_config = {
    "company_info": {
        "name": "Bestat Taiwan Branch",
        "full_name": "Bestat Clinical Research - Taiwan Office",
        "website": "www.bestat.com.tw"
    },
    "fonts": {
        "title": {
            "name": "微軟正黑體",  # 使用中文字體
            "size": 20,
            "color": {"r": 0, "g": 102, "b": 204}
        },
        "body": {
            "name": "新細明體",
            "size": 12
        }
    },
    "colors": {
        "primary": {"r": 0, "g": 102, "b": 204}  # 亮藍色
    },
    "page_setup": {
        "margins": {
            "top_inches": 1.2,  # 稍大的上邊距
            "bottom_inches": 1.2
        }
    }
}

# 使用自訂配置
analyzer = BestatStyleAnalyzer(config=taiwan_config)
```

### 批次處理文件

```python
import os
from pathlib import Path

def batch_apply_bestat_style(input_dir, output_dir):
    """批次套用Bestat樣式到所有Word文件"""

    analyzer = BestatStyleAnalyzer()
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 處理所有.docx檔案
    for docx_file in input_path.glob("*.docx"):
        print(f"處理: {docx_file.name}")

        # 載入文件
        doc = Document(docx_file)

        # 套用樣式
        styled_doc = analyzer.apply_bestat_style(
            doc,
            document_title=docx_file.stem,
            protocol_number=f"PRO-2025-{docx_file.stem}",
            version="1.0"
        )

        # 儲存
        output_file = output_path / docx_file.name
        styled_doc.save(str(output_file))

        print(f"  ✓ 已儲存: {output_file}")

# 使用範例
batch_apply_bestat_style("./input", "./output")
```

### 生成樣式分析報告

```python
# 生成詳細報告
analyzer.generate_style_report(
    doc_path="protocol.docx",
    output_path="protocol_analysis.json"
)

# 讀取報告
import json
with open("protocol_analysis.json", "r", encoding="utf-8") as f:
    report = json.load(f)

print("樣式分析報告:")
print(f"文件: {report['document']}")
print(f"分析日期: {report['analysis_date']}")
print(f"\n驗證結果:")
print(f"  符合規範: {report['validation_results']['compliant']}")
print(f"\n建議:")
for rec in report['recommendations']:
    print(f"  - {rec}")
```

### 使用便利函數

```python
from modules.bestat_style_analyzer import (
    analyze_document_style,
    apply_bestat_style_to_document,
    validate_document_compliance
)

# 快速分析
styles = analyze_document_style("template.docx", "output.json")

# 快速套用
apply_bestat_style_to_document(
    input_doc_path="draft.docx",
    output_doc_path="final.docx",
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 快速驗證
validation = validate_document_compliance("final.docx")
print(f"符合規範: {validation['compliant']}")
```

---

## API參考

### BestatStyleAnalyzer 類別

#### 初始化

```python
analyzer = BestatStyleAnalyzer(config=None)
```

**參數：**
- `config` (dict, optional): 自訂配置字典，會與預設配置合併

#### 主要方法

##### extract_styles_from_document()

從Word文件提取樣式設定。

```python
styles = analyzer.extract_styles_from_document(document_path)
```

**參數：**
- `document_path` (str): Word文件路徑

**返回：**
- `dict`: 包含所有樣式資訊的字典

**提取內容：**
- `page_setup`: 頁面設定
- `fonts`: 字體樣式
- `colors`: 顏色方案
- `paragraph_spacing`: 段落格式
- `header`: 頁首設定
- `footer`: 頁尾設定
- `table_style`: 表格樣式
- `logo_info`: Logo資訊
- `metadata`: 文件元數據

##### apply_bestat_style()

套用Bestat樣式到文件。

```python
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="",
    protocol_number="",
    version="",
    logo_path=None
)
```

**參數：**
- `doc` (Document): python-docx Document物件
- `document_title` (str): 文件標題
- `protocol_number` (str): Protocol編號
- `version` (str): 版本號
- `logo_path` (str, optional): Logo圖片路徑

**返回：**
- `Document`: 套用樣式後的Document物件

##### validate_bestat_compliance()

驗證文件是否符合Bestat規範。

```python
validation = analyzer.validate_bestat_compliance(doc)
```

**參數：**
- `doc` (Document): python-docx Document物件

**返回：**
- `dict`: 驗證結果字典

**返回結構：**
```python
{
    "compliant": bool,           # 是否符合規範
    "total_issues": int,         # 問題總數
    "total_warnings": int,       # 警告總數
    "issues": [str],            # 問題清單
    "warnings": [str],          # 警告清單
    "validation_date": str      # 驗證日期
}
```

##### compare_styles()

比較兩個文件的樣式差異。

```python
comparison = analyzer.compare_styles(doc1_path, doc2_path)
```

**參數：**
- `doc1_path` (str): 第一個文件路徑
- `doc2_path` (str): 第二個文件路徑

**返回：**
- `dict`: 包含差異資訊的字典

##### save_style_config()

儲存樣式配置到JSON檔案。

```python
analyzer.save_style_config(output_path, style_config=None)
```

**參數：**
- `output_path` (str): 輸出JSON檔案路徑
- `style_config` (dict, optional): 樣式配置字典，None則使用當前配置

##### load_style_config()

從JSON檔案載入樣式配置。

```python
config = analyzer.load_style_config(config_path)
```

**參數：**
- `config_path` (str): JSON配置檔案路徑

**返回：**
- `dict`: 載入的樣式配置

##### generate_style_report()

生成詳細的樣式分析報告。

```python
analyzer.generate_style_report(doc_path, output_path)
```

**參數：**
- `doc_path` (str): 要分析的文件路徑
- `output_path` (str): 報告輸出路徑（JSON格式）

### 便利函數

#### analyze_document_style()

快速分析文件樣式並儲存為JSON。

```python
from modules.bestat_style_analyzer import analyze_document_style

styles = analyze_document_style(document_path, output_json_path)
```

#### apply_bestat_style_to_document()

快速套用Bestat樣式到文件。

```python
from modules.bestat_style_analyzer import apply_bestat_style_to_document

apply_bestat_style_to_document(
    input_doc_path,
    output_doc_path,
    config_path=None,
    document_title="",
    protocol_number="",
    version="",
    logo_path=None
)
```

#### validate_document_compliance()

快速驗證文件規範。

```python
from modules.bestat_style_analyzer import validate_document_compliance

validation = validate_document_compliance(document_path, config_path=None)
```

---

## 最佳實踐

### 1. 建立公司範本庫

```python
# 為不同類型的文件建立範本配置
templates = {
    "protocol": "bestat_protocol_template.json",
    "report": "bestat_report_template.json",
    "presentation": "bestat_presentation_template.json"
}

def create_document(doc_type, title, protocol, version):
    analyzer = BestatStyleAnalyzer()
    analyzer.load_style_config(templates[doc_type])

    doc = Document()
    # ... 添加內容 ...

    return analyzer.apply_bestat_style(doc, title, protocol, version)
```

### 2. 建立驗證流程

```python
def validate_and_save(doc, output_path):
    """驗證文件並根據結果決定是否儲存"""

    analyzer = BestatStyleAnalyzer()
    validation = analyzer.validate_bestat_compliance(doc)

    if validation['compliant']:
        doc.save(output_path)
        print(f"✓ 文件已通過驗證並儲存: {output_path}")
        return True
    else:
        print("✗ 文件未通過驗證，請修正以下問題:")
        for issue in validation['issues']:
            print(f"  - {issue}")
        return False
```

### 3. 版本控制樣式配置

```python
# 使用日期標記樣式版本
from datetime import datetime

def save_versioned_config(analyzer, base_name):
    version = datetime.now().strftime("%Y%m%d")
    filename = f"{base_name}_v{version}.json"
    analyzer.save_style_config(filename)
    print(f"配置已儲存: {filename}")
```

### 4. 錯誤處理

```python
def safe_apply_bestat_style(doc_path, output_path):
    """安全地套用Bestat樣式，包含完整錯誤處理"""

    try:
        analyzer = BestatStyleAnalyzer()
        doc = Document(doc_path)

        styled_doc = analyzer.apply_bestat_style(
            doc,
            document_title="Protocol",
            protocol_number="PRO-2025-001",
            version="1.0"
        )

        validation = analyzer.validate_bestat_compliance(styled_doc)

        if validation['compliant']:
            styled_doc.save(output_path)
            return True, "成功"
        else:
            return False, validation['issues']

    except FileNotFoundError:
        return False, "找不到輸入檔案"
    except Exception as e:
        return False, f"發生錯誤: {str(e)}"
```

---

## 常見問題

### Q1: 如何處理中文字體？

A: 在自訂配置中指定中文字體：

```python
custom_config = {
    "fonts": {
        "title": {
            "name": "微軟正黑體"
        },
        "body": {
            "name": "新細明體"
        }
    }
}

analyzer = BestatStyleAnalyzer(config=custom_config)
```

### Q2: 如何處理沒有Logo的情況？

A: 不提供 `logo_path` 參數即可：

```python
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
    # logo_path 省略
)
```

### Q3: 驗證失敗時如何修正？

A: 查看詳細的問題清單並逐一修正：

```python
validation = analyzer.validate_bestat_compliance(doc)

if not validation['compliant']:
    print("問題清單:")
    for issue in validation['issues']:
        print(f"  - {issue}")

    # 根據問題類型修正
    # 例如：頁面設定問題 → 重新套用樣式
    # 字體問題 → 檢查字體安裝
```

### Q4: 如何批次處理大量文件？

A: 使用批次處理函數：

```python
def batch_process(file_list):
    analyzer = BestatStyleAnalyzer()
    results = []

    for file_path in file_list:
        try:
            doc = Document(file_path)
            styled_doc = analyzer.apply_bestat_style(doc, ...)
            output_path = file_path.replace(".docx", "_bestat.docx")
            styled_doc.save(output_path)
            results.append((file_path, "成功"))
        except Exception as e:
            results.append((file_path, f"失敗: {e}"))

    return results
```

### Q5: 樣式配置如何在團隊間共享？

A: 將JSON配置檔案存放在共享位置：

```python
# 1. 匯出標準配置
analyzer = BestatStyleAnalyzer()
analyzer.save_style_config("//shared/bestat_standard.json")

# 2. 團隊成員載入配置
team_analyzer = BestatStyleAnalyzer()
team_analyzer.load_style_config("//shared/bestat_standard.json")
```

### Q6: 如何處理不同國家/地區的樣式差異？

A: 為每個地區建立獨立配置：

```python
# 台灣配置
taiwan_config = {...}
analyzer_tw = BestatStyleAnalyzer(config=taiwan_config)

# 日本配置
japan_config = {...}
analyzer_jp = BestatStyleAnalyzer(config=japan_config)

# 或動態載入
def get_regional_analyzer(region):
    config_map = {
        "TW": "bestat_taiwan.json",
        "JP": "bestat_japan.json",
        "US": "bestat_us.json"
    }

    analyzer = BestatStyleAnalyzer()
    analyzer.load_style_config(config_map[region])
    return analyzer
```

---

## 附錄

### A. JSON配置檔案範例

```json
{
  "company_info": {
    "name": "Bestat Inc.",
    "full_name": "Bestat Clinical Research Organization",
    "website": "www.bestat.com"
  },
  "page_setup": {
    "size": "A4",
    "width_inches": 8.27,
    "height_inches": 11.69,
    "orientation": "portrait",
    "margins": {
      "top_inches": 1.0,
      "bottom_inches": 1.0,
      "left_inches": 1.0,
      "right_inches": 1.0
    }
  },
  "fonts": {
    "title": {
      "name": "Arial",
      "size": 18,
      "bold": true,
      "color": {"r": 0, "g": 51, "b": 153}
    }
  }
}
```

### B. 驗證結果範例

```json
{
  "compliant": false,
  "total_issues": 2,
  "total_warnings": 1,
  "issues": [
    "頁面寬度不符: 期望 8.27\"，實際 8.50\"",
    "缺少頁首"
  ],
  "warnings": [
    "使用了非標準字體: Times New Roman"
  ],
  "validation_date": "2025-11-18T10:30:00"
}
```

### C. 完整工作流程範例

```python
"""完整的Bestat文件處理工作流程"""

from docx import Document
from modules.bestat_style_analyzer import BestatStyleAnalyzer
from modules.word_formatter import WordFormatter

# 步驟1：建立文件內容
formatter = WordFormatter()
formatter.create_document()

formatter.apply_title_style("臨床試驗Protocol", level=1)
formatter.apply_title_style("1. 研究背景", level=2)
formatter.apply_body_style("本研究評估新藥的安全性和有效性...")

# 步驟2：套用Bestat樣式
formatter.apply_bestat_style(
    document_title="第三期臨床試驗Protocol",
    protocol_number="PRO-2025-PHASE3",
    version="2.0",
    logo_path="bestat_logo.png"
)

# 步驟3：驗證規範
validation = formatter.validate_bestat_compliance()

if validation['compliant']:
    # 步驟4：通過驗證，儲存最終文件
    formatter.save_document("protocol_final.docx")
    print("✓ 文件已通過驗證並儲存")

    # 步驟5：生成樣式報告（可選）
    analyzer = BestatStyleAnalyzer()
    analyzer.generate_style_report(
        "protocol_final.docx",
        "protocol_report.json"
    )
else:
    # 驗證失敗，顯示問題並修正
    print("文件需要修正以下問題:")
    for issue in validation['issues']:
        print(f"  - {issue}")
```

---

## 聯絡資訊

如有問題或建議，請聯絡：

- **開發團隊**：Clinical Document Automation Team
- **版本**：1.0.0
- **更新日期**：2025-11-18

---

**版權所有 © 2025 Bestat Inc. 保留所有權利。**
