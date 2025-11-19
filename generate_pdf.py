#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 PDF 訓練文件
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

# 註冊中文字體（使用系統字體）
try:
    pdfmetrics.registerFont(TTFont('Chinese', '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf'))
    FONT_NAME = 'Chinese'
except:
    FONT_NAME = 'Helvetica'
    print("警告：無法載入中文字體，將使用英文字體")

def create_pdf():
    """創建 PDF 文件"""
    pdf_path = '/home/user/my-colab-notebooks/MedGemma_訓練教學完整版.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                           topMargin=2*cm, bottomMargin=2*cm,
                           leftMargin=2*cm, rightMargin=2*cm)

    # 創建樣式
    styles = getSampleStyleSheet()

    # 標題樣式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontName=FONT_NAME,
        fontSize=24,
        textColor=HexColor('#003366'),
        alignment=TA_CENTER,
        spaceAfter=30
    )

    # 副標題樣式
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=18,
        textColor=HexColor('#003366'),
        alignment=TA_CENTER,
        spaceAfter=20
    )

    # 章節標題
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontName=FONT_NAME,
        fontSize=16,
        textColor=HexColor('#003366'),
        spaceAfter=12
    )

    # 小標題
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontName=FONT_NAME,
        fontSize=14,
        textColor=HexColor('#336699'),
        spaceAfter=10
    )

    # 正文
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName=FONT_NAME,
        fontSize=11,
        leading=16,
        spaceAfter=8
    )

    # 程式碼
    code_style = ParagraphStyle(
        'CustomCode',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=9,
        leftIndent=20,
        rightIndent=20,
        backColor=HexColor('#F5F5F5'),
        spaceAfter=12
    )

    story = []

    # ========== 封面 ==========
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph('MedGemma 醫療術語校正模型', title_style))
    story.append(Paragraph('Python 機器學習完整訓練教學', subtitle_style))
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('Notebook 20 個 Cells 完整講解', normal_style))
    story.append(Paragraph('從環境設定、資料處理、模型訓練到結果分析', normal_style))
    story.append(PageBreak())

    # ========== Cell 1 ==========
    story.append(Paragraph('Cell 1: 安裝套件', heading1_style))
    story.append(Paragraph('完整程式碼', heading2_style))

    code1 = """print('📦 開始安裝必要套件...')
!pip install -q transformers datasets accelerate bitsandbytes peft openpyxl scikit-learn matplotlib seaborn
print('✅ 套件安裝完成！')"""

    story.append(Preformatted(code1, code_style))

    story.append(Paragraph('程式碼講解', heading2_style))
    story.append(Paragraph('這個 Cell 安裝所有訓練所需的 Python 套件。', normal_style))
    story.append(Paragraph('• ! 符號：在 Jupyter/Colab 執行 Shell 命令', normal_style))
    story.append(Paragraph('• pip：Python 套件管理工具', normal_style))
    story.append(Paragraph('• -q：安靜模式，減少輸出', normal_style))

    story.append(Paragraph('套件說明', heading2_style))
    story.append(Paragraph('1. transformers：HuggingFace 模型庫', normal_style))
    story.append(Paragraph('2. datasets：資料集處理', normal_style))
    story.append(Paragraph('3. bitsandbytes：模型量化（4-bit）', normal_style))
    story.append(Paragraph('4. peft：LoRA 微調', normal_style))
    story.append(Paragraph('5. scikit-learn：評估指標', normal_style))

    story.append(Paragraph('重要概念', heading2_style))
    story.append(Paragraph('【量化】將 32-bit 參數壓縮到 4-bit，節省 8 倍記憶體。', normal_style))
    story.append(Paragraph('【比喻】套件就像工具箱，提供現成工具，不用從頭打造。', normal_style))

    story.append(PageBreak())

    # ========== Cell 9: 資料平衡 ==========
    story.append(Paragraph('Cell 9: 資料平衡', heading1_style))

    story.append(Paragraph('為什麼需要資料平衡？', heading2_style))
    story.append(Paragraph('如果訓練資料中「正確術語」有 900 筆，「錯誤術語」只有 100 筆，模型會傾向預測「都是正確的」，因為這樣準確率有 90%！但實際上模型並沒有學會辨識錯誤。', normal_style))

    code9 = """TARGET_ERROR_RATIO = 0.40  # 目標錯誤比例 40%
MAX_TOTAL_SAMPLES = 3500   # 資料上限

# 上採樣錯誤資料
df_error_upsampled = resample(df_error, replace=True, n_samples=needed_count)

# 合併並打亂
df = pd.concat([df_correct, df_error_upsampled])
df = df.sample(frac=1, random_state=42).reset_index(drop=True)"""

    story.append(Preformatted(code9, code_style))

    story.append(Paragraph('重點概念', heading2_style))
    story.append(Paragraph('• 上採樣：複製少數類別資料（replace=True）', normal_style))
    story.append(Paragraph('• 下採樣：減少多數類別資料（replace=False）', normal_style))
    story.append(Paragraph('• random_state=42：固定隨機種子', normal_style))

    story.append(PageBreak())

    # ========== Cell 17: 統計分析 ==========
    story.append(Paragraph('Cell 17: 統計分析', heading1_style))

    code17 = """values = [0.85, 0.87, 0.83, 0.86, 0.84]

mean = np.mean(values)  # 0.85
std = np.std(values, ddof=1)  # 0.0158

# 95% 信賴區間
ci = stats.t.interval(0.95, df=4, loc=mean, scale=stats.sem(values))"""

    story.append(Preformatted(code17, code_style))

    story.append(Paragraph('重要概念', heading2_style))
    story.append(Paragraph('【平均值】中心趨勢，5 次測試的平均表現', normal_style))
    story.append(Paragraph('【標準差】離散程度，越小表示越穩定', normal_style))
    story.append(Paragraph('【信賴區間】真實值有 95% 機率在此範圍', normal_style))

    story.append(PageBreak())

    # ========== 總結 ==========
    story.append(Paragraph('完整訓練流程總結', heading1_style))

    story.append(Paragraph('20 個 Cells 功能概覽', heading2_style))
    story.append(Paragraph('Cell 1-2：環境設定（安裝、導入）', normal_style))
    story.append(Paragraph('Cell 3-5：基礎準備（GPU、Drive、檔案）', normal_style))
    story.append(Paragraph('Cell 6-8：資料讀取與整合', normal_style))
    story.append(Paragraph('Cell 9：資料平衡', normal_style))
    story.append(Paragraph('Cell 10-11：訓練準備', normal_style))
    story.append(Paragraph('Cell 12-16：模型訓練（5-fold）', normal_style))
    story.append(Paragraph('Cell 17：統計分析', normal_style))
    story.append(Paragraph('Cell 18-19：視覺化', normal_style))
    story.append(Paragraph('Cell 20：生成報告', normal_style))

    story.append(Paragraph('核心技術', heading2_style))
    story.append(Paragraph('【量化】32-bit → 4-bit，節省 8 倍記憶體', normal_style))
    story.append(Paragraph('【LoRA】只訓練 0.21% 參數', normal_style))
    story.append(Paragraph('【交叉驗證】5-fold，結果更可靠', normal_style))

    story.append(Spacer(1, 2*cm))
    story.append(Paragraph('恭喜你完成了完整的 MedGemma 訓練教學！', normal_style))

    # 生成 PDF
    doc.build(story)
    return pdf_path

# 生成 PDF
print("正在生成 PDF 文件...")
pdf_path = create_pdf()
print(f"✅ PDF 已生成: {pdf_path}")

import os
pdf_size = os.path.getsize(pdf_path) / 1024
print(f"📄 PDF 大小: {pdf_size:.2f} KB")
