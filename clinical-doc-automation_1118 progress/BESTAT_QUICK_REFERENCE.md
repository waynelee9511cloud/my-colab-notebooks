# Bestat樣式分析器快速參考

## 30秒快速開始

```python
from modules.bestat_style_analyzer import BestatStyleAnalyzer
from docx import Document

# 建立文件
doc = Document()
doc.add_paragraph("您的內容")

# 套用Bestat樣式
analyzer = BestatStyleAnalyzer()
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 儲存
styled_doc.save("output.docx")
```

## 常用功能速查

### 1. 提取樣式
```python
styles = analyzer.extract_styles_from_document("template.docx")
analyzer.save_style_config("styles.json", styles)
```

### 2. 套用樣式
```python
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="標題",
    protocol_number="編號",
    version="版本"
)
```

### 3. 驗證規範
```python
validation = analyzer.validate_bestat_compliance(doc)
print(f"符合: {validation['compliant']}")
```

### 4. 比較文件
```python
comparison = analyzer.compare_styles("doc1.docx", "doc2.docx")
print(f"差異: {comparison['total_differences']}")
```

### 5. 載入配置
```python
analyzer.load_style_config("config.json")
```

## Word Formatter 整合

```python
from modules.word_formatter import WordFormatter

formatter = WordFormatter()
formatter.create_document()

# 添加內容
formatter.apply_title_style("標題", level=1)
formatter.apply_body_style("內文")

# 套用Bestat樣式
formatter.apply_bestat_style(
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 驗證並儲存
validation = formatter.validate_bestat_compliance()
if validation['compliant']:
    formatter.save_document("output.docx")
```

## 便利函數

```python
from modules.bestat_style_analyzer import (
    analyze_document_style,
    apply_bestat_style_to_document,
    validate_document_compliance
)

# 快速分析
analyze_document_style("input.docx", "styles.json")

# 快速套用
apply_bestat_style_to_document(
    "input.docx", "output.docx",
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
)

# 快速驗證
validation = validate_document_compliance("document.docx")
```

## 自訂配置範例

```python
custom_config = {
    "company_info": {
        "name": "自訂公司名稱"
    },
    "fonts": {
        "title": {
            "name": "Arial",
            "size": 20,
            "color": {"r": 0, "g": 102, "b": 204}
        }
    },
    "page_setup": {
        "margins": {
            "top_inches": 1.5,
            "bottom_inches": 1.5
        }
    }
}

analyzer = BestatStyleAnalyzer(config=custom_config)
```

## 錯誤處理

```python
try:
    doc = Document("input.docx")
    styled_doc = analyzer.apply_bestat_style(doc, ...)

    validation = analyzer.validate_bestat_compliance(styled_doc)
    if validation['compliant']:
        styled_doc.save("output.docx")
    else:
        for issue in validation['issues']:
            print(f"問題: {issue}")

except FileNotFoundError:
    print("找不到檔案")
except Exception as e:
    print(f"錯誤: {e}")
```

## Bestat標準樣式

### 頁面設定
- 紙張：A4 (8.27" × 11.69")
- 方向：直向
- 邊距：1.0" (上下左右)

### 字體
- 標題：Arial 18pt 粗體 藍色(0,51,153)
- 一級標題：Arial 16pt 粗體 藍色
- 二級標題：Arial 14pt 粗體 亮藍(0,102,204)
- 內文：Calibri 11pt 黑色

### 顏色
- 主色：RGB(0, 51, 153) - 深藍
- 輔色：RGB(0, 102, 204) - 亮藍
- 強調：RGB(255, 153, 0) - 橙色
- 機密：RGB(255, 0, 0) - 紅色

## 常見問題

**Q: 如何處理沒有Logo的情況？**
```python
# 不提供logo_path參數即可
styled_doc = analyzer.apply_bestat_style(
    doc,
    document_title="Protocol",
    protocol_number="PRO-2025-001",
    version="1.0"
    # logo_path省略
)
```

**Q: 如何批次處理？**
```python
from pathlib import Path

input_dir = Path("./input")
for docx_file in input_dir.glob("*.docx"):
    doc = Document(docx_file)
    styled_doc = analyzer.apply_bestat_style(doc, ...)
    styled_doc.save(f"./output/{docx_file.name}")
```

**Q: 驗證失敗怎麼辦？**
```python
validation = analyzer.validate_bestat_compliance(doc)
if not validation['compliant']:
    # 查看具體問題
    for issue in validation['issues']:
        print(f"問題: {issue}")
    # 根據問題修正後重新套用樣式
```

## 運行測試

```bash
# 運行完整測試套件
cd clinical-doc-automation/modules
python test_bestat_style_analyzer.py

# 運行範例
cd clinical-doc-automation/examples
python bestat_style_example.py
```

## 更多資訊

完整文件：`BESTAT_STYLE_GUIDE.md`
