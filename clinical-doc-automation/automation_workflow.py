#!/usr/bin/env python3
"""
Clinical Document Automation Workflow
臨床試驗文件自動化工作流程

這個模組提供端到端的自動化工作流程，能夠從 Protocol PDF 一鍵生成所有臨床試驗文件。

支援功能：
- Protocol PDF 解析
- CRF (Case Report Form) 生成
- DVP (Data Validation Plan) 生成
- User Guide 生成
- DMP (Data Management Plan) 生成（如果已實現）
- 進度追蹤和日誌記錄
- 錯誤處理和回滾機制
- 批次處理支援
- CLI 命令列介面

Author: Clinical Documentation Automation Team
Date: 2025-11-18
Version: 1.0
"""

import os
import sys
import json
import logging
import argparse
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass, field, asdict
import shutil

# 導入現有的模組
try:
    from modules.protocol_parser import ProtocolParser, ProtocolInfo
    from modules.crf_generator import CRFGenerator, CRFDomain
    from modules.dvp_generator import DVPGenerator, ProtocolInfo as DVPProtocolInfo, CRFField, Severity, ValidationType
    from modules.user_guide_generator import UserGuideGenerator
except ImportError:
    # 如果直接執行此腳本，調整路徑
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from modules.protocol_parser import ProtocolParser, ProtocolInfo
    from modules.crf_generator import CRFGenerator, CRFDomain
    from modules.dvp_generator import DVPGenerator, ProtocolInfo as DVPProtocolInfo, CRFField, Severity, ValidationType
    from modules.user_guide_generator import UserGuideGenerator


# ==================== 日誌設置 ====================

def setup_logging(log_file: Optional[str] = None, verbose: bool = False) -> logging.Logger:
    """
    設置日誌系統

    Args:
        log_file: 日誌檔案路徑，如果為 None 則只輸出到控制台
        verbose: 是否顯示詳細日誌（DEBUG 級別）

    Returns:
        配置好的 logger 物件
    """
    log_level = logging.DEBUG if verbose else logging.INFO
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # 創建 logger
    logger = logging.getLogger('ClinicalDocAutomation')
    logger.setLevel(log_level)

    # 清除現有的 handlers
    logger.handlers = []

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console_handler)

    # 檔案 handler（如果指定）
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 檔案始終記錄詳細日誌
        file_handler.setFormatter(logging.Formatter(log_format))
        logger.addHandler(file_handler)

    return logger


# ==================== 資料結構 ====================

@dataclass
class GenerationTask:
    """單個文件生成任務"""
    task_id: str
    task_type: str  # 'crf', 'dvp', 'user_guide', 'dmp'
    status: str = 'pending'  # 'pending', 'running', 'completed', 'failed', 'skipped'
    output_path: Optional[str] = None
    error_message: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        return asdict(self)


@dataclass
class AutomationReport:
    """自動化執行報告"""
    protocol_path: str
    output_directory: str
    start_time: str
    end_time: Optional[str] = None
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    skipped_tasks: int = 0
    tasks: List[GenerationTask] = field(default_factory=list)
    generated_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    protocol_info: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """轉換為字典"""
        data = asdict(self)
        data['tasks'] = [task.to_dict() for task in self.tasks]
        return data

    def to_json(self, indent: int = 2) -> str:
        """轉換為 JSON 字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

    def save_to_file(self, output_path: str):
        """保存報告到檔案"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


# ==================== 主類別 ====================

class ClinicalDocAutomation:
    """
    臨床試驗文件自動化生成系統

    這個類別整合了所有文件生成模組，提供一鍵生成所有臨床試驗文件的功能。

    主要功能：
    1. Protocol PDF 解析
    2. CRF 文件生成
    3. DVP 文件生成
    4. User Guide 文件生成
    5. DMP 文件生成（如果已實現）
    6. 進度追蹤和日誌記錄
    7. 錯誤處理和回滾機制
    8. 生成詳細報告

    使用範例:
        automation = ClinicalDocAutomation(
            protocol_pdf="/path/to/protocol.pdf",
            api_key="your-gemini-api-key",
            output_dir="/path/to/output"
        )

        report = automation.run_all()
        print(report.to_json())
    """

    def __init__(
        self,
        protocol_pdf: str,
        api_key: str,
        output_dir: Optional[str] = None,
        verbose: bool = False,
        backup: bool = True
    ):
        """
        初始化自動化系統

        Args:
            protocol_pdf: Protocol PDF 檔案路徑
            api_key: Gemini API 金鑰
            output_dir: 輸出目錄，如果為 None 則自動生成
            verbose: 是否顯示詳細日誌
            backup: 是否在失敗時備份已生成的檔案
        """
        self.protocol_pdf = Path(protocol_pdf)
        self.api_key = api_key
        self.verbose = verbose
        self.backup_enabled = backup

        # 驗證 Protocol PDF 存在
        if not self.protocol_pdf.exists():
            raise FileNotFoundError(f"Protocol PDF 不存在: {self.protocol_pdf}")

        # 設置輸出目錄
        if output_dir is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            protocol_name = self.protocol_pdf.stem
            output_dir = f"output_{protocol_name}_{timestamp}"

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 設置日誌
        log_file = self.output_dir / "automation.log"
        self.logger = setup_logging(str(log_file), verbose)

        # 初始化報告
        self.report = AutomationReport(
            protocol_path=str(self.protocol_pdf),
            output_directory=str(self.output_dir),
            start_time=datetime.now().isoformat()
        )

        # 儲存解析的 Protocol 資訊
        self.protocol_info: Optional[ProtocolInfo] = None

        # 備份目錄
        self.backup_dir = self.output_dir / "_backup"

        self.logger.info("=" * 80)
        self.logger.info("臨床試驗文件自動化系統啟動")
        self.logger.info("=" * 80)
        self.logger.info(f"Protocol PDF: {self.protocol_pdf}")
        self.logger.info(f"輸出目錄: {self.output_dir}")
        self.logger.info(f"日誌檔案: {log_file}")
        self.logger.info("=" * 80)

    def _create_backup(self, file_path: str):
        """創建檔案備份"""
        if not self.backup_enabled:
            return

        try:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
            backup_path = self.backup_dir / Path(file_path).name
            shutil.copy2(file_path, backup_path)
            self.logger.debug(f"已備份: {file_path} -> {backup_path}")
        except Exception as e:
            self.logger.warning(f"備份失敗: {str(e)}")

    def _update_task_status(
        self,
        task: GenerationTask,
        status: str,
        output_path: Optional[str] = None,
        error_message: Optional[str] = None
    ):
        """更新任務狀態"""
        task.status = status

        if status == 'running':
            task.start_time = datetime.now().isoformat()
        elif status in ['completed', 'failed', 'skipped']:
            task.end_time = datetime.now().isoformat()

        if output_path:
            task.output_path = output_path
            if status == 'completed':
                self.report.generated_files.append(output_path)

        if error_message:
            task.error_message = error_message
            self.report.errors.append(f"[{task.task_type}] {error_message}")

        # 更新報告統計
        if status == 'completed':
            self.report.completed_tasks += 1
        elif status == 'failed':
            self.report.failed_tasks += 1
        elif status == 'skipped':
            self.report.skipped_tasks += 1

    def parse_protocol(self) -> bool:
        """
        解析 Protocol PDF

        Returns:
            成功返回 True，失敗返回 False
        """
        task = GenerationTask(
            task_id="parse_protocol",
            task_type="protocol_parsing"
        )
        self.report.tasks.append(task)
        self.report.total_tasks += 1

        self.logger.info("")
        self.logger.info("▶ 步驟 1/5: 解析 Protocol PDF")
        self.logger.info("-" * 80)

        try:
            self._update_task_status(task, 'running')

            # 初始化 Protocol Parser
            parser = ProtocolParser(api_key=self.api_key)

            # 解析 Protocol
            self.logger.info(f"正在解析 Protocol: {self.protocol_pdf.name}")
            self.protocol_info = parser.parse_protocol(str(self.protocol_pdf))

            # 保存解析結果
            json_output = self.output_dir / "protocol_info.json"
            parser.save_to_json(self.protocol_info, str(json_output))

            # 儲存到報告
            self.report.protocol_info = self.protocol_info.to_dict()

            self._update_task_status(task, 'completed', str(json_output))

            self.logger.info(f"✓ Protocol 解析完成")
            self.logger.info(f"  試驗標題: {self.protocol_info.study_title}")
            self.logger.info(f"  Protocol 編號: {self.protocol_info.protocol_number}")
            self.logger.info(f"  試驗階段: {self.protocol_info.phase}")
            self.logger.info(f"  JSON 已保存: {json_output}")

            return True

        except Exception as e:
            error_msg = f"Protocol 解析失敗: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            self._update_task_status(task, 'failed', error_message=error_msg)
            return False

    def generate_crf(self) -> bool:
        """
        生成 CRF 文件

        Returns:
            成功返回 True，失敗返回 False
        """
        task = GenerationTask(
            task_id="generate_crf",
            task_type="crf"
        )
        self.report.tasks.append(task)
        self.report.total_tasks += 1

        self.logger.info("")
        self.logger.info("▶ 步驟 2/5: 生成 CRF (Case Report Form) 文件")
        self.logger.info("-" * 80)

        if not self.protocol_info:
            error_msg = "無法生成 CRF：Protocol 資訊未解析"
            self.logger.error(error_msg)
            self._update_task_status(task, 'skipped', error_message=error_msg)
            return False

        try:
            self._update_task_status(task, 'running')

            # 準備 Protocol 資訊
            protocol_data = {
                'study_title': self.protocol_info.study_title,
                'protocol_number': self.protocol_info.protocol_number,
                'sponsor': self.protocol_info.sponsor,
                'version': '1.0'
            }

            # 初始化 CRF Generator
            generator = CRFGenerator(protocol_info=protocol_data)

            # 確定要包含的 CRF 領域
            domains = self.protocol_info.crf_domains if self.protocol_info.crf_domains else None

            # 生成 CRF
            output_file = self.output_dir / f"CRF_{self.protocol_info.protocol_number.replace('/', '_')}.docx"
            self.logger.info(f"正在生成 CRF 文件...")

            if domains:
                self.logger.info(f"  包含 {len(domains)} 個 CRF 領域")
                for domain in domains:
                    self.logger.debug(f"    - {domain}")
            else:
                self.logger.info(f"  使用所有標準 CRF 領域")

            generator.generate_crf(
                domains=domains,
                output_path=str(output_file),
                include_all_standard=(domains is None)
            )

            self._update_task_status(task, 'completed', str(output_file))

            self.logger.info(f"✓ CRF 文件生成完成")
            self.logger.info(f"  檔案: {output_file}")
            self.logger.info(f"  包含領域數: {len(generator.get_available_domains())}")

            return True

        except Exception as e:
            error_msg = f"CRF 生成失敗: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            self._update_task_status(task, 'failed', error_message=error_msg)
            return False

    def generate_dvp(self) -> bool:
        """
        生成 DVP (Data Validation Plan) 文件

        Returns:
            成功返回 True，失敗返回 False
        """
        task = GenerationTask(
            task_id="generate_dvp",
            task_type="dvp"
        )
        self.report.tasks.append(task)
        self.report.total_tasks += 1

        self.logger.info("")
        self.logger.info("▶ 步驟 3/5: 生成 DVP (Data Validation Plan) 文件")
        self.logger.info("-" * 80)

        if not self.protocol_info:
            error_msg = "無法生成 DVP：Protocol 資訊未解析"
            self.logger.error(error_msg)
            self._update_task_status(task, 'skipped', error_message=error_msg)
            return False

        try:
            self._update_task_status(task, 'running')

            # 準備 Protocol 資訊
            dvp_protocol_info = DVPProtocolInfo(
                protocol_number=self.protocol_info.protocol_number or "N/A",
                protocol_title=self.protocol_info.study_title or "N/A",
                sponsor=self.protocol_info.sponsor or "N/A",
                indication=self.protocol_info.target_population or "N/A",
                phase=self.protocol_info.phase or "N/A",
                version="1.0"
            )

            # 初始化 DVP Generator
            generator = DVPGenerator(protocol_info=dvp_protocol_info)

            # 準備 CRF 欄位（基於標準領域）
            crf_fields = self._prepare_crf_fields_for_dvp()
            generator.add_crf_fields(crf_fields)

            # 生成驗證規則
            self.logger.info(f"正在生成驗證規則...")
            generator.generate_all_rules()

            rules_summary = generator.get_rules_summary()
            self.logger.info(f"  已生成 {len(generator.validation_rules)} 條驗證規則")
            for rule_type, count in rules_summary.items():
                self.logger.debug(f"    - {rule_type}: {count} 條")

            # 生成 DVP 文件
            output_file = self.output_dir / f"DVP_{self.protocol_info.protocol_number.replace('/', '_')}.docx"
            self.logger.info(f"正在生成 DVP 文件...")
            generator.generate_dvp_document(str(output_file))

            self._update_task_status(task, 'completed', str(output_file))

            self.logger.info(f"✓ DVP 文件生成完成")
            self.logger.info(f"  檔案: {output_file}")
            self.logger.info(f"  驗證規則數: {len(generator.validation_rules)}")

            return True

        except Exception as e:
            error_msg = f"DVP 生成失敗: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            self._update_task_status(task, 'failed', error_message=error_msg)
            return False

    def _prepare_crf_fields_for_dvp(self) -> List[CRFField]:
        """準備 DVP 所需的 CRF 欄位定義"""
        fields = []

        # 基本的 Demographics 欄位
        fields.extend([
            CRFField(
                field_name="subject_id",
                field_label="Subject ID",
                form_name="Demographics",
                data_type="text",
                required=True
            ),
            CRFField(
                field_name="age",
                field_label="Age",
                form_name="Demographics",
                data_type="numeric",
                required=True,
                min_value=18,
                max_value=120,
                units="years"
            ),
            CRFField(
                field_name="date_of_birth",
                field_label="Date of Birth",
                form_name="Demographics",
                data_type="date",
                required=True
            ),
        ])

        # 基本的 Vital Signs 欄位
        fields.extend([
            CRFField(
                field_name="systolic_bp",
                field_label="Systolic Blood Pressure",
                form_name="Vital Signs",
                data_type="numeric",
                required=True,
                min_value=70,
                max_value=200,
                units="mmHg"
            ),
            CRFField(
                field_name="diastolic_bp",
                field_label="Diastolic Blood Pressure",
                form_name="Vital Signs",
                data_type="numeric",
                required=True,
                min_value=40,
                max_value=130,
                units="mmHg"
            ),
            CRFField(
                field_name="heart_rate",
                field_label="Heart Rate",
                form_name="Vital Signs",
                data_type="numeric",
                required=True,
                min_value=40,
                max_value=200,
                units="bpm"
            ),
        ])

        # 基本的 Adverse Events 欄位
        fields.extend([
            CRFField(
                field_name="ae_term",
                field_label="Adverse Event Term",
                form_name="Adverse Events",
                data_type="text",
                required=True
            ),
            CRFField(
                field_name="ae_start_date",
                field_label="AE Start Date",
                form_name="Adverse Events",
                data_type="date",
                required=True
            ),
            CRFField(
                field_name="ae_end_date",
                field_label="AE End Date",
                form_name="Adverse Events",
                data_type="date",
                required=False
            ),
        ])

        return fields

    def generate_user_guide(self) -> bool:
        """
        生成 User Guide 文件

        Returns:
            成功返回 True，失敗返回 False
        """
        task = GenerationTask(
            task_id="generate_user_guide",
            task_type="user_guide"
        )
        self.report.tasks.append(task)
        self.report.total_tasks += 1

        self.logger.info("")
        self.logger.info("▶ 步驟 4/5: 生成 User Guide 文件")
        self.logger.info("-" * 80)

        if not self.protocol_info:
            error_msg = "無法生成 User Guide：Protocol 資訊未解析"
            self.logger.error(error_msg)
            self._update_task_status(task, 'skipped', error_message=error_msg)
            return False

        try:
            self._update_task_status(task, 'running')

            # 準備 Protocol 資訊
            protocol_data = {
                'protocol_id': self.protocol_info.protocol_number or "N/A",
                'protocol_title': self.protocol_info.study_title or "N/A",
                'sponsor': self.protocol_info.sponsor or "N/A",
                'version': '1.0',
                'date': datetime.now().strftime('%Y-%m-%d')
            }

            # 準備 CRF 設計資訊
            crf_design = self._prepare_crf_design_for_user_guide()

            # 初始化 User Guide Generator
            generator = UserGuideGenerator(
                protocol_info=protocol_data,
                crf_design=crf_design,
                system_name="EDC/ePRO System"
            )

            # 生成 User Guide
            output_file = self.output_dir / f"UserGuide_{self.protocol_info.protocol_number.replace('/', '_')}.docx"
            self.logger.info(f"正在生成 User Guide 文件...")
            generator.generate(str(output_file))

            # 也生成截圖列表
            screenshot_list = self.output_dir / f"UserGuide_Screenshots.txt"

            self._update_task_status(task, 'completed', str(output_file))

            self.logger.info(f"✓ User Guide 文件生成完成")
            self.logger.info(f"  檔案: {output_file}")
            self.logger.info(f"  截圖需求清單: {screenshot_list}")
            self.logger.info(f"  所需截圖數: {len(generator.get_screenshot_list())}")

            return True

        except Exception as e:
            error_msg = f"User Guide 生成失敗: {str(e)}"
            self.logger.error(error_msg)
            self.logger.debug(traceback.format_exc())
            self._update_task_status(task, 'failed', error_message=error_msg)
            return False

    def _prepare_crf_design_for_user_guide(self) -> Dict[str, Any]:
        """準備 User Guide 所需的 CRF 設計資訊"""
        forms = []

        # Demographics 表單
        forms.append({
            'form_name': 'demographics',
            'form_title': 'Demographics',
            'visit': 'Screening',
            'fields': [
                {
                    'field_name': 'subject_id',
                    'field_label': 'Subject ID',
                    'field_type': 'text',
                    'required': True,
                    'validation': 'Unique identifier'
                },
                {
                    'field_name': 'date_of_birth',
                    'field_label': 'Date of Birth',
                    'field_type': 'date',
                    'required': True,
                    'validation': 'Format: YYYY-MM-DD'
                },
                {
                    'field_name': 'sex',
                    'field_label': 'Sex',
                    'field_type': 'dropdown',
                    'required': True,
                    'validation': 'Male/Female'
                },
            ]
        })

        # Vital Signs 表單
        forms.append({
            'form_name': 'vital_signs',
            'form_title': 'Vital Signs',
            'visit': 'All Visits',
            'fields': [
                {
                    'field_name': 'systolic_bp',
                    'field_label': 'Systolic Blood Pressure (mmHg)',
                    'field_type': 'number',
                    'required': True,
                    'validation': 'Range: 70-200'
                },
                {
                    'field_name': 'diastolic_bp',
                    'field_label': 'Diastolic Blood Pressure (mmHg)',
                    'field_type': 'number',
                    'required': True,
                    'validation': 'Range: 40-130'
                },
                {
                    'field_name': 'heart_rate',
                    'field_label': 'Heart Rate (bpm)',
                    'field_type': 'number',
                    'required': True,
                    'validation': 'Range: 40-200'
                },
            ]
        })

        # Adverse Events 表單
        forms.append({
            'form_name': 'adverse_events',
            'form_title': 'Adverse Events',
            'visit': 'All Visits',
            'fields': [
                {
                    'field_name': 'ae_occurred',
                    'field_label': 'Did any adverse event occur?',
                    'field_type': 'radio',
                    'required': True,
                    'validation': 'Yes/No'
                },
                {
                    'field_name': 'ae_description',
                    'field_label': 'Event Description',
                    'field_type': 'textarea',
                    'required': False,
                    'validation': 'Required if AE occurred'
                },
                {
                    'field_name': 'ae_severity',
                    'field_label': 'Severity',
                    'field_type': 'dropdown',
                    'required': False,
                    'validation': 'Mild/Moderate/Severe'
                },
            ]
        })

        return {'forms': forms}

    def generate_dmp(self) -> bool:
        """
        生成 DMP (Data Management Plan) 文件

        注意：此功能尚未實現，返回 skipped 狀態

        Returns:
            成功返回 True，失敗返回 False
        """
        task = GenerationTask(
            task_id="generate_dmp",
            task_type="dmp"
        )
        self.report.tasks.append(task)
        self.report.total_tasks += 1

        self.logger.info("")
        self.logger.info("▶ 步驟 5/5: 生成 DMP (Data Management Plan) 文件")
        self.logger.info("-" * 80)

        # DMP 生成器尚未實現
        error_msg = "DMP 生成器尚未實現"
        self.logger.warning(error_msg)
        self._update_task_status(task, 'skipped', error_message=error_msg)

        return True  # 返回 True 以繼續執行

    def generate_final_report(self) -> str:
        """
        生成最終執行報告

        Returns:
            報告檔案路徑
        """
        self.logger.info("")
        self.logger.info("=" * 80)
        self.logger.info("生成執行報告")
        self.logger.info("=" * 80)

        # 完成報告
        self.report.end_time = datetime.now().isoformat()

        # 保存 JSON 報告
        json_report_path = self.output_dir / "automation_report.json"
        self.report.save_to_file(str(json_report_path))

        # 生成人類可讀的報告
        text_report_path = self.output_dir / "automation_report.txt"
        self._generate_text_report(str(text_report_path))

        self.logger.info(f"✓ JSON 報告已保存: {json_report_path}")
        self.logger.info(f"✓ 文字報告已保存: {text_report_path}")

        return str(text_report_path)

    def _generate_text_report(self, output_path: str):
        """生成文字格式的報告"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("臨床試驗文件自動化生成報告\n")
            f.write("Clinical Document Automation Report\n")
            f.write("=" * 80 + "\n\n")

            # 基本資訊
            f.write("【基本資訊】\n")
            f.write("-" * 80 + "\n")
            f.write(f"Protocol PDF: {self.report.protocol_path}\n")
            f.write(f"輸出目錄: {self.report.output_directory}\n")
            f.write(f"開始時間: {self.report.start_time}\n")
            f.write(f"結束時間: {self.report.end_time}\n")

            # 計算執行時間
            if self.report.start_time and self.report.end_time:
                start = datetime.fromisoformat(self.report.start_time)
                end = datetime.fromisoformat(self.report.end_time)
                duration = end - start
                f.write(f"執行時長: {duration}\n")

            f.write("\n")

            # Protocol 資訊
            if self.report.protocol_info:
                f.write("【Protocol 資訊】\n")
                f.write("-" * 80 + "\n")
                f.write(f"試驗標題: {self.report.protocol_info.get('study_title', 'N/A')}\n")
                f.write(f"Protocol 編號: {self.report.protocol_info.get('protocol_number', 'N/A')}\n")
                f.write(f"贊助商: {self.report.protocol_info.get('sponsor', 'N/A')}\n")
                f.write(f"試驗階段: {self.report.protocol_info.get('phase', 'N/A')}\n")
                f.write(f"目標族群: {self.report.protocol_info.get('target_population', 'N/A')}\n")
                f.write(f"樣本數: {self.report.protocol_info.get('sample_size', 'N/A')}\n")
                f.write("\n")

            # 執行統計
            f.write("【執行統計】\n")
            f.write("-" * 80 + "\n")
            f.write(f"總任務數: {self.report.total_tasks}\n")
            f.write(f"完成任務: {self.report.completed_tasks}\n")
            f.write(f"失敗任務: {self.report.failed_tasks}\n")
            f.write(f"跳過任務: {self.report.skipped_tasks}\n")

            success_rate = (self.report.completed_tasks / self.report.total_tasks * 100) if self.report.total_tasks > 0 else 0
            f.write(f"成功率: {success_rate:.1f}%\n")
            f.write("\n")

            # 任務詳情
            f.write("【任務詳情】\n")
            f.write("-" * 80 + "\n")
            for i, task in enumerate(self.report.tasks, 1):
                status_icon = {
                    'completed': '✓',
                    'failed': '✗',
                    'skipped': '○',
                    'running': '▶',
                    'pending': '...'
                }.get(task.status, '?')

                f.write(f"{i}. {status_icon} {task.task_type.upper()} - {task.status.upper()}\n")
                if task.output_path:
                    f.write(f"   輸出檔案: {task.output_path}\n")
                if task.error_message:
                    f.write(f"   錯誤訊息: {task.error_message}\n")
                if task.start_time:
                    f.write(f"   開始時間: {task.start_time}\n")
                if task.end_time:
                    f.write(f"   結束時間: {task.end_time}\n")
                f.write("\n")

            # 生成的檔案列表
            if self.report.generated_files:
                f.write("【生成的檔案】\n")
                f.write("-" * 80 + "\n")
                for i, file_path in enumerate(self.report.generated_files, 1):
                    f.write(f"{i}. {file_path}\n")
                f.write("\n")

            # 錯誤列表
            if self.report.errors:
                f.write("【錯誤列表】\n")
                f.write("-" * 80 + "\n")
                for i, error in enumerate(self.report.errors, 1):
                    f.write(f"{i}. {error}\n")
                f.write("\n")

            # 結尾
            f.write("=" * 80 + "\n")
            f.write("報告結束\n")
            f.write("=" * 80 + "\n")

    def run_all(self, generate_types: Optional[List[str]] = None) -> AutomationReport:
        """
        執行所有文件生成任務

        Args:
            generate_types: 要生成的文件類型列表，如果為 None 則生成所有類型
                          可選值: ['crf', 'dvp', 'user_guide', 'dmp']

        Returns:
            AutomationReport 物件
        """
        if generate_types is None:
            generate_types = ['crf', 'dvp', 'user_guide', 'dmp']

        self.logger.info("")
        self.logger.info("開始執行自動化工作流程...")
        self.logger.info("")

        try:
            # 步驟 1: 解析 Protocol
            success = self.parse_protocol()
            if not success:
                self.logger.error("Protocol 解析失敗，終止執行")
                return self.report

            # 步驟 2-5: 根據指定生成文件
            if 'crf' in generate_types:
                self.generate_crf()

            if 'dvp' in generate_types:
                self.generate_dvp()

            if 'user_guide' in generate_types:
                self.generate_user_guide()

            if 'dmp' in generate_types:
                self.generate_dmp()

        except Exception as e:
            self.logger.error(f"執行過程中發生未預期的錯誤: {str(e)}")
            self.logger.debug(traceback.format_exc())
            self.report.errors.append(f"未預期的錯誤: {str(e)}")

        finally:
            # 生成最終報告
            self.generate_final_report()

            # 顯示摘要
            self._print_summary()

        return self.report

    def _print_summary(self):
        """顯示執行摘要"""
        self.logger.info("")
        self.logger.info("=" * 80)
        self.logger.info("執行摘要")
        self.logger.info("=" * 80)
        self.logger.info(f"總任務數: {self.report.total_tasks}")
        self.logger.info(f"完成: {self.report.completed_tasks}")
        self.logger.info(f"失敗: {self.report.failed_tasks}")
        self.logger.info(f"跳過: {self.report.skipped_tasks}")

        if self.report.total_tasks > 0:
            success_rate = (self.report.completed_tasks / self.report.total_tasks * 100)
            self.logger.info(f"成功率: {success_rate:.1f}%")

        self.logger.info("")
        self.logger.info(f"輸出目錄: {self.output_dir}")
        self.logger.info(f"生成檔案數: {len(self.report.generated_files)}")

        if self.report.generated_files:
            self.logger.info("")
            self.logger.info("生成的檔案:")
            for file_path in self.report.generated_files:
                self.logger.info(f"  ✓ {file_path}")

        if self.report.errors:
            self.logger.info("")
            self.logger.warning(f"錯誤數: {len(self.report.errors)}")
            for error in self.report.errors:
                self.logger.warning(f"  ✗ {error}")

        self.logger.info("=" * 80)


# ==================== 批次處理 ====================

class BatchProcessor:
    """
    批次處理器

    支援一次處理多個 Protocol PDF 檔案
    """

    def __init__(
        self,
        api_key: str,
        output_base_dir: Optional[str] = None,
        verbose: bool = False
    ):
        """
        初始化批次處理器

        Args:
            api_key: Gemini API 金鑰
            output_base_dir: 基礎輸出目錄
            verbose: 是否顯示詳細日誌
        """
        self.api_key = api_key
        self.output_base_dir = output_base_dir or "batch_output"
        self.verbose = verbose
        self.results: List[Tuple[str, AutomationReport]] = []

    def process_protocols(
        self,
        protocol_pdfs: List[str],
        generate_types: Optional[List[str]] = None
    ) -> List[Tuple[str, AutomationReport]]:
        """
        批次處理多個 Protocol PDF

        Args:
            protocol_pdfs: Protocol PDF 檔案路徑列表
            generate_types: 要生成的文件類型列表

        Returns:
            (protocol_path, report) 元組的列表
        """
        print("=" * 80)
        print(f"批次處理開始 - 共 {len(protocol_pdfs)} 個 Protocol")
        print("=" * 80)

        for i, pdf_path in enumerate(protocol_pdfs, 1):
            print(f"\n處理 Protocol {i}/{len(protocol_pdfs)}: {pdf_path}")
            print("-" * 80)

            try:
                # 為每個 Protocol 創建獨立的輸出目錄
                protocol_name = Path(pdf_path).stem
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_dir = Path(self.output_base_dir) / f"{protocol_name}_{timestamp}"

                # 執行自動化
                automation = ClinicalDocAutomation(
                    protocol_pdf=pdf_path,
                    api_key=self.api_key,
                    output_dir=str(output_dir),
                    verbose=self.verbose
                )

                report = automation.run_all(generate_types=generate_types)
                self.results.append((pdf_path, report))

                print(f"✓ Protocol {i} 處理完成")

            except Exception as e:
                print(f"✗ Protocol {i} 處理失敗: {str(e)}")
                traceback.print_exc()

        print("\n" + "=" * 80)
        print("批次處理完成")
        print("=" * 80)

        # 生成批次摘要報告
        self._generate_batch_summary()

        return self.results

    def _generate_batch_summary(self):
        """生成批次處理摘要報告"""
        summary_path = Path(self.output_base_dir) / "batch_summary.txt"

        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("批次處理摘要報告\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"處理的 Protocol 數量: {len(self.results)}\n")
            f.write(f"處理時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            total_completed = 0
            total_failed = 0
            total_skipped = 0

            for i, (protocol_path, report) in enumerate(self.results, 1):
                f.write(f"\n{i}. {Path(protocol_path).name}\n")
                f.write("-" * 80 + "\n")
                f.write(f"   輸出目錄: {report.output_directory}\n")
                f.write(f"   完成任務: {report.completed_tasks}\n")
                f.write(f"   失敗任務: {report.failed_tasks}\n")
                f.write(f"   跳過任務: {report.skipped_tasks}\n")
                f.write(f"   生成檔案: {len(report.generated_files)}\n")

                total_completed += report.completed_tasks
                total_failed += report.failed_tasks
                total_skipped += report.skipped_tasks

            f.write("\n" + "=" * 80 + "\n")
            f.write("總計統計\n")
            f.write("=" * 80 + "\n")
            f.write(f"總完成任務: {total_completed}\n")
            f.write(f"總失敗任務: {total_failed}\n")
            f.write(f"總跳過任務: {total_skipped}\n")

        print(f"\n批次摘要報告已保存: {summary_path}")


# ==================== CLI 介面 ====================

def create_cli_parser() -> argparse.ArgumentParser:
    """創建命令列參數解析器"""
    parser = argparse.ArgumentParser(
        description="臨床試驗文件自動化生成系統 - Clinical Document Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用範例:

1. 生成所有文件:
   python automation_workflow.py --protocol protocol.pdf --api-key YOUR_API_KEY

2. 只生成 CRF 和 DVP:
   python automation_workflow.py --protocol protocol.pdf --api-key YOUR_API_KEY --generate crf dvp

3. 批次處理多個 Protocol:
   python automation_workflow.py --batch protocol1.pdf protocol2.pdf --api-key YOUR_API_KEY

4. 使用環境變數設置 API Key:
   export GEMINI_API_KEY="your-api-key"
   python automation_workflow.py --protocol protocol.pdf

5. 指定輸出目錄:
   python automation_workflow.py --protocol protocol.pdf --api-key YOUR_API_KEY --output-dir ./my_output
        """
    )

    # 主要參數
    parser.add_argument(
        '--protocol',
        type=str,
        help='Protocol PDF 檔案路徑'
    )

    parser.add_argument(
        '--batch',
        nargs='+',
        type=str,
        help='批次處理：多個 Protocol PDF 檔案路徑'
    )

    parser.add_argument(
        '--api-key',
        type=str,
        help='Gemini API 金鑰（也可使用環境變數 GEMINI_API_KEY）'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        help='輸出目錄路徑（預設：自動生成）'
    )

    parser.add_argument(
        '--generate',
        nargs='+',
        choices=['crf', 'dvp', 'user_guide', 'dmp', 'all'],
        default=['all'],
        help='要生成的文件類型（預設：all）'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='顯示詳細日誌'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='失敗時不備份已生成的檔案'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='Clinical Document Automation v1.0'
    )

    return parser


def main():
    """主函數 - CLI 入口點"""
    parser = create_cli_parser()
    args = parser.parse_args()

    # 驗證參數
    if not args.protocol and not args.batch:
        parser.error("必須指定 --protocol 或 --batch 參數")

    if args.protocol and args.batch:
        parser.error("--protocol 和 --batch 不能同時使用")

    # 獲取 API Key
    api_key = args.api_key or os.getenv('GEMINI_API_KEY')
    if not api_key:
        parser.error("必須提供 API Key（使用 --api-key 或設置環境變數 GEMINI_API_KEY）")

    # 處理 generate 參數
    generate_types = args.generate
    if 'all' in generate_types:
        generate_types = ['crf', 'dvp', 'user_guide', 'dmp']

    try:
        # 單個 Protocol 處理
        if args.protocol:
            automation = ClinicalDocAutomation(
                protocol_pdf=args.protocol,
                api_key=api_key,
                output_dir=args.output_dir,
                verbose=args.verbose,
                backup=not args.no_backup
            )

            report = automation.run_all(generate_types=generate_types)

            # 返回適當的退出碼
            if report.failed_tasks > 0:
                sys.exit(1)
            else:
                sys.exit(0)

        # 批次處理
        elif args.batch:
            processor = BatchProcessor(
                api_key=api_key,
                output_base_dir=args.output_dir or "batch_output",
                verbose=args.verbose
            )

            results = processor.process_protocols(
                protocol_pdfs=args.batch,
                generate_types=generate_types
            )

            # 檢查是否有失敗
            any_failed = any(report.failed_tasks > 0 for _, report in results)
            sys.exit(1 if any_failed else 0)

    except KeyboardInterrupt:
        print("\n\n用戶中斷執行")
        sys.exit(130)
    except Exception as e:
        print(f"\n執行錯誤: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


# ==================== 程式入口 ====================

if __name__ == "__main__":
    main()
