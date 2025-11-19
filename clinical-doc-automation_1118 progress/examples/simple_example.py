#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
最簡單的 DVP 生成範例
這是使用 DVP Generator 最簡單的方式
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.dvp_generator import create_dvp, ProtocolInfo, CRFField


# 步驟 1: 定義試驗書資訊
protocol = ProtocolInfo(
    protocol_number="ABC-2025-001",
    protocol_title="高血壓藥物第三期臨床試驗",
    sponsor="ABC 製藥公司",
    indication="原發性高血壓",
    phase="Phase III"
)

# 步驟 2: 定義 CRF 欄位
fields = [
    # 人口統計學表單
    CRFField("subject_id", "受試者編號", "人口統計學", "text", required=True),
    CRFField("age", "年齡", "人口統計學", "numeric", required=True, min_value=18, max_value=75, units="歲"),
    CRFField("weight", "體重", "人口統計學", "numeric", required=True, min_value=40, max_value=150, units="公斤"),

    # 生命徵象表單
    CRFField("systolic_bp", "收縮壓", "生命徵象", "numeric", required=True, min_value=90, max_value=200, units="mmHg"),
    CRFField("diastolic_bp", "舒張壓", "生命徵象", "numeric", required=True, min_value=50, max_value=130, units="mmHg"),
    CRFField("heart_rate", "心率", "生命徵象", "numeric", required=True, min_value=40, max_value=150, units="次/分"),

    # 不良事件表單
    CRFField("ae_start_date", "不良事件開始日期", "不良事件", "date"),
    CRFField("ae_end_date", "不良事件結束日期", "不良事件", "date"),
]

# 步驟 3: 生成 DVP（一行完成！）
create_dvp(
    protocol_info=protocol,
    crf_fields=fields,
    output_path="../output/simple_dvp.docx"
)

print("✓ DVP 已成功生成: ../output/simple_dvp.docx")
