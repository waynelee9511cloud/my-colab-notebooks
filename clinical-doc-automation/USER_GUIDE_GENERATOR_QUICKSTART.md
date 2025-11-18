# EDC/ePRO User Guide Generator - 快速入門

## 安裝

```bash
pip install python-docx
```

## 5分鐘快速開始

### 1. 基本使用

```python
from modules.user_guide_generator import (
    UserGuideGenerator,
    create_sample_protocol_info,
    create_sample_crf_design
)

# 使用範例資料快速生成
protocol_info = create_sample_protocol_info()
crf_design = create_sample_crf_design()

generator = UserGuideGenerator(
    protocol_info=protocol_info,
    crf_design=crf_design,
    system_name="My EDC System"
)

generator.generate("my_user_guide.docx")
```

### 2. 自訂 Protocol 資訊

```python
protocol_info = {
    'protocol_id': 'STUDY-2025-001',
    'protocol_title': '您的研究標題',
    'sponsor': '贊助商名稱',
    'version': '1.0',
    'date': '2025-11-18'
}
```

### 3. 定義 CRF 設計

```python
crf_design = {
    'forms': [
        {
            'form_name': 'demographics',        # 表單識別名稱
            'form_title': '受試者基本資料',      # 顯示標題
            'visit': '篩選訪視',                # 訪視時間點
            'fields': [                         # 欄位清單
                {
                    'field_name': 'subject_id',
                    'field_label': '受試者編號',
                    'field_type': 'text',       # 欄位類型
                    'required': True,           # 是否必填
                    'validation': '格式: XXX-001'  # 驗證規則
                },
                # 更多欄位...
            ]
        },
        # 更多表單...
    ]
}
```

### 4. 生成並管理截圖

```python
# 生成文件
generator.generate("user_guide.docx")

# 查看所有截圖需求
screenshots = generator.get_screenshot_list()
print(f"需要 {len(screenshots)} 張截圖")

# 匯出截圖清單
generator.export_screenshot_list("screenshots_needed.txt")
```

## 支援的欄位類型

| 類型 | 說明 | 範例 |
|------|------|------|
| `text` | 文字輸入 | 姓名、編號 |
| `number` | 數字 | 年齡、劑量 |
| `decimal` | 小數 | 體重、身高 |
| `date` | 日期 | 出生日期 |
| `dropdown` | 下拉選單 | 性別、種族 |
| `radio` | 單選 | 是/否 |
| `checkbox` | 多選 | 症狀 |
| `textarea` | 長文字 | 備註、說明 |

## 輸出檔案

執行後會生成：

1. **user_guide.docx** - 完整的使用者指南（Word格式）
2. **user_guide_screenshots.txt** - 截圖需求清單

## 文件內容

自動生成的使用者指南包含：

1. **封面頁** - Protocol 資訊和版本
2. **簡介** - 目的和適用對象
3. **系統登入** - 登入步驟和疑難排解
4. **系統導航** - 介面說明和操作方式
5. **資料輸入說明** - 每個 CRF 的詳細步驟
6. **疑問管理** - Query 處理流程
7. **報表產生** - 報表類型和操作
8. **附錄** - 聯絡資訊、縮寫表、修訂歷史

## 範例程式

```bash
# 執行所有範例
cd clinical-doc-automation
python examples/example_user_guide_generation.py

# 執行特定範例
python examples/example_user_guide_generation.py 1  # 基本使用
python examples/example_user_guide_generation.py 2  # 自訂Protocol
python examples/example_user_guide_generation.py 3  # 截圖管理
```

## 進階選項

### 不包含附錄

```python
generator.generate("user_guide.docx", include_appendix=False)
```

### 自訂系統名稱

```python
generator = UserGuideGenerator(
    protocol_info=protocol_info,
    crf_design=crf_design,
    system_name="MyCompany Clinical Data Platform v2.0"
)
```

## 完整文件

詳細資訊請參閱：
- **模組文件**: `modules/USER_GUIDE_GENERATOR_README.md`
- **範例代碼**: `examples/example_user_guide_generation.py`
- **原始碼**: `modules/user_guide_generator.py`

## 常見問題

**Q: 如何修改文件樣式？**
A: 繼承 `UserGuideGenerator` 類別並覆寫 `_setup_document_styles()` 方法

**Q: 可以自訂章節內容嗎？**
A: 可以，繼承類別並新增自訂方法，在 `generate()` 中呼叫

**Q: 如何插入實際截圖？**
A: 生成文件後，在 Word 中找到紅色的截圖佔位符，替換為實際圖片

**Q: 支援多語言嗎？**
A: 目前章節標題為英文，但可以在 protocol_info 和 crf_design 中使用任何語言

## 技術支援

如有問題，請參考：
1. 詳細文件：`modules/USER_GUIDE_GENERATOR_README.md`
2. 範例代碼：`examples/example_user_guide_generation.py`
3. 測試輸出：`output/test_user_guide.docx`

---

**版本**: 1.0.0
**更新日期**: 2025-11-18
**作者**: Clinical Documentation Automation Team
