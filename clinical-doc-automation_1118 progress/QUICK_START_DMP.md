# Data Management Plan (DMP) Generator - 快速开始指南

## 🚀 60 秒快速开始

### 最简单的方式 - 只需 3 行代码！

```python
from modules.dmp_generator import create_dmp_with_defaults

create_dmp_with_defaults(
    protocol_number="PROTO-2025-001",
    protocol_title="我的临床试验",
    sponsor="制药公司名称",
    indication="适应症",
    phase="Phase III",
    output_path="output/DMP.docx"
)
```

**完成！** 您已经生成了一个完整的、符合法规要求的 Data Management Plan！

---

## 📋 生成的文档包含什么？

### 10 个完整章节：
1. ✅ Introduction（简介 + 法规合规性）
2. ✅ Study Overview（试验概述表格）
3. ✅ Data Management Responsibilities（3个默认角色 + 职责）
4. ✅ Data Flow（10步骤流程图）
5. ✅ CRF Design（开发流程 + 设计惯例）
6. ✅ Data Validation（验证策略 + 4种检查类型）
7. ✅ Data Quality Control（QC活动 + 品质指标）
8. ✅ Database Lock（9项标准 + 6步骤流程）
9. ✅ Data Security（存取控制 + 稽核轨迹 + GDPR）
10. ✅ Archive（存档要求 + 保存期限）

### 附录：
- ✅ 缩写词汇表（15个常用缩写）
- ✅ 项目时程表（如提供里程碑）

### 法规合规性：
- ✅ ICH GCP E6(R2)
- ✅ FDA 21 CFR Part 11
- ✅ GDPR（适用时）

---

## 🎯 三种使用方式

### 方式 1: 超级快速（推荐初学者）
```python
from modules.dmp_generator import create_dmp_with_defaults

create_dmp_with_defaults(
    protocol_number="PROTO-2025-001",
    protocol_title="My Study",
    sponsor="My Company",
    indication="Disease X",
    phase="Phase III",
    output_path="DMP.docx"
)
```

### 方式 2: 基本使用（推荐大多数用户）
```python
from modules.dmp_generator import DMPGenerator, ProtocolInfo

protocol_info = ProtocolInfo(
    protocol_number="PROTO-2025-001",
    protocol_title="A Phase III Study",
    sponsor="Pharma Inc.",
    indication="Diabetes",
    phase="Phase III"
)

generator = DMPGenerator(protocol_info)
generator.generate_dmp_document("DMP.docx")
```

### 方式 3: 完整定制（推荐进阶用户）
```python
from modules.dmp_generator import (
    DMPGenerator, ProtocolInfo, CRFDomain, Milestone
)

# 详细的 Protocol 信息
protocol_info = ProtocolInfo(
    protocol_number="PROTO-2025-001",
    protocol_title="A Phase III Study",
    sponsor="Pharma Inc.",
    indication="Diabetes",
    phase="Phase III",
    study_design="Randomized, Double-Blind",
    sample_size="300 subjects",
    study_duration="24 months"
)

generator = DMPGenerator(protocol_info)

# 添加 CRF 领域
generator.add_crf_domain(CRFDomain(
    domain_name="Demographics",
    description="Subject demographics",
    visit_schedule=["Screening"],
    is_critical=True,
    validation_rules=8
))

# 添加里程碑
generator.add_milestone(Milestone(
    name="Database Lock",
    description="Lock clinical database",
    planned_date="31-Dec-2025",
    responsible="Data Manager"
))

# 生成文档
generator.generate_dmp_document("DMP_Full.docx")
```

---

## 🧪 测试验证

### 运行快速测试
```bash
python examples/quick_test_dmp.py
```

**预期输出：**
```
✓ Test 1: 基本 DMP 生成 - 成功
✓ Test 2: 快速创建函数 - 成功
✓ Test 3: 导出配置 - 成功
✓ All tests passed!
```

### 运行完整测试套件
```bash
python -m modules.test_dmp_generator
```

**预期输出：**
```
Ran 25 tests in 0.6s
OK
Tests run: 25
Successes: 25
Failures: 0
```

---

## 📚 查看示例

### 运行所有示例
```bash
python examples/dmp_generator_example.py all
```

### 运行特定示例
```bash
# 示例 1: 基础 DMP
python examples/dmp_generator_example.py 1

# 示例 2: 完整 DMP（含12个CRF领域、11个里程碑）
python examples/dmp_generator_example.py 2

# 示例 3: 快速建立
python examples/dmp_generator_example.py 3

# 示例 4: 自定义角色
python examples/dmp_generator_example.py 4

# 示例 5: 肿瘤学研究（含RECIST 1.1）
python examples/dmp_generator_example.py 5
```

---

## 📖 详细文档

查看完整文档：
```bash
# 方法 1: 直接阅读
cat modules/README_DMP.md

# 方法 2: 查看快速开始指南
python -m modules.dmp_generator

# 方法 3: 查看项目总结
cat DMP_GENERATOR_SUMMARY.md
```

---

## 💡 常见问题

### Q: 生成的文档在哪里？
A: 在您指定的 `output_path` 位置。例如：
```python
generator.generate_dmp_document("output/DMP.docx")
# 文档保存在: output/DMP.docx
```

### Q: 如何打开生成的文档？
A: 使用 Microsoft Word 或 LibreOffice Writer 打开 .docx 文件。

### Q: 可以自定义内容吗？
A: 可以！您可以：
- 添加自定义 CRF 领域
- 添加项目里程碑
- 添加自定义验证规则
- 添加自定义章节
- 自定义角色和职责

### Q: 是否符合法规要求？
A: 是的！生成的 DMP 符合：
- ICH GCP E6(R2)
- FDA 21 CFR Part 11
- GDPR（适用时）

### Q: 可以修改默认内容吗？
A: 可以！所有默认值都可以覆盖。例如：
```python
# 清除默认角色，使用自定义角色
generator.dm_roles = []
generator.add_dm_role(my_custom_role)
```

---

## 🎨 自定义示例

### 添加 CRF 领域
```python
from modules.dmp_generator import CRFDomain

generator.add_crf_domain(CRFDomain(
    domain_name="Vital Signs",
    description="BP, HR, Temperature",
    visit_schedule=["Screening", "Week 4", "Week 8"],
    is_critical=False,
    validation_rules=12
))
```

### 添加里程碑
```python
from modules.dmp_generator import Milestone

generator.add_milestone(Milestone(
    name="First Subject In",
    description="First subject enrolled",
    planned_date="01-Mar-2025",
    responsible="Clinical Operations"
))
```

### 添加验证规则
```python
from modules.dmp_generator import ValidationCheck

generator.add_validation_check(ValidationCheck(
    check_type="HbA1c Range Check",
    description="Verify HbA1c between 7.0% and 10.0%",
    severity="Critical",
    implementation="Real-time"
))
```

### 添加自定义角色
```python
from modules.dmp_generator import DataManagementRole

generator.add_dm_role(DataManagementRole(
    role="Medical Coder",
    organization="Coding Services Inc.",
    responsibilities=[
        "Code AEs using MedDRA",
        "Code medications using WHO Drug"
    ],
    contact_person="Jane Smith",
    contact_email="jane@coding.com"
))
```

### 添加自定义章节
```python
from modules.dmp_generator import DMPSection

generator.add_custom_section(DMPSection(
    section_number="11",
    title="Study-Specific Procedures",
    content="This study has unique requirements...",
    subsections=[
        {
            'title': 'CGM Data',
            'content': 'CGM devices will be used...'
        }
    ]
))
```

---

## 🔧 实用技巧

### 技巧 1: 在文件名中包含版本号
```python
generator.generate_dmp_document(
    f"DMP_{protocol_info.protocol_number}_v{protocol_info.version}.docx"
)
```

### 技巧 2: 设置 EDC 系统名称
```python
generator.set_edc_system("Medidata Rave v2023.1")
```

### 技巧 3: 导出配置供其他程序使用
```python
config_dict = generator.export_to_dict()
# 可以保存为 JSON 或传递给其他模块
```

### 技巧 4: 使用 WordFormatter 获得专业格式
```python
generator.generate_dmp_document(
    "DMP.docx",
    use_word_formatter=True  # 使用专业格式
)
```

---

## 📁 文件位置

所有相关文件位于：
```
clinical-doc-automation/
├── modules/
│   ├── dmp_generator.py          # 核心模块
│   ├── test_dmp_generator.py     # 测试套件
│   └── README_DMP.md             # 完整文档
├── examples/
│   ├── dmp_generator_example.py  # 5个示例
│   └── quick_test_dmp.py         # 快速测试
├── DMP_GENERATOR_SUMMARY.md      # 项目总结
└── QUICK_START_DMP.md            # 本文档
```

---

## 🎓 学习路径

### 初学者
1. ✅ 阅读本快速开始指南
2. ✅ 运行快速测试：`python examples/quick_test_dmp.py`
3. ✅ 使用 `create_dmp_with_defaults()` 生成第一个 DMP
4. ✅ 在 Word 中查看生成的文档

### 中级用户
1. ✅ 阅读 `modules/README_DMP.md`
2. ✅ 运行示例 1-3
3. ✅ 尝试添加 CRF 领域和里程碑
4. ✅ 自定义验证规则

### 进阶用户
1. ✅ 阅读 `DMP_GENERATOR_SUMMARY.md`
2. ✅ 运行所有示例（特别是示例 5：肿瘤学）
3. ✅ 创建自定义角色和章节
4. ✅ 整合到现有工作流程

---

## 🆘 需要帮助？

### 查看文档
- **快速开始**: 本文档
- **完整文档**: `modules/README_DMP.md`
- **项目总结**: `DMP_GENERATOR_SUMMARY.md`

### 运行示例
```bash
python examples/dmp_generator_example.py all
```

### 查看内置帮助
```bash
python -m modules.dmp_generator
```

---

## ✨ 开始使用

**准备好了吗？只需3行代码：**

```python
from modules.dmp_generator import create_dmp_with_defaults

create_dmp_with_defaults(
    protocol_number="YOUR-PROTOCOL-001",
    protocol_title="Your Study Title",
    sponsor="Your Company",
    indication="Your Indication",
    phase="Phase III",
    output_path="output/DMP.docx"
)
```

**就是这么简单！** 🎉

---

*Clinical Document Automation Team*
*Making clinical data management easier, one document at a time.*
