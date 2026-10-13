from io import BytesIO
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "26921" / "尤钧个人简历.pdf"
OUTPUT = ROOT / "assets" / "resume-you-jun.pdf"

pdfmetrics.registerFont(TTFont("ResumeSong", r"C:\Windows\Fonts\STSONG.TTF"))
pdfmetrics.registerFont(TTFont("ResumeBold", r"C:\Windows\Fonts\msyhbd.ttc"))


def draw_wrapped(c, text, x, y, width, font="ResumeSong", size=10.2, leading=14.0):
    line = ""
    for char in text:
        candidate = line + char
        if pdfmetrics.stringWidth(candidate, font, size) <= width:
            line = candidate
        else:
            c.drawString(x, y, line)
            y -= leading
            line = char
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y


reader = PdfReader(str(SOURCE))
page = reader.pages[0]
page_width = float(page.mediabox.width)
page_height = float(page.mediabox.height)

buffer = BytesIO()
c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

# Header and education: keep the original one-page structure.
c.setFillColor(white)
c.rect(39, 673, 518, 141, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 20)
c.drawString(42.5, 792, "尤钧")
c.setFont("ResumeSong", 9.0)
c.drawString(42.5, 775, "电话：13771530261    邮箱：b24030711@njupt.edu.cn    出生日期：2006/06/23")
c.setLineWidth(0.8)
c.line(42.5, 768, 552.8, 768)
c.setFont("ResumeBold", 10.78)
c.drawString(42.5, 750, "教育背景")
c.setLineWidth(0.45)
c.line(42.5, 744, 552.8, 744)
c.setFont("ResumeSong", 10)
c.drawString(42.5, 728, "南京邮电大学")
c.drawRightString(552.8, 728, "预计 2028 年夏毕业")
c.drawString(42.5, 713, "集成电路设计与集成系统")
c.drawRightString(552.8, 713, "本科三年级")
c.drawString(42.5, 698, "绩点排名：第 28 名    综合测评排名：前 3%")
c.setFont("ResumeSong", 9.0)
c.drawString(42.5, 684, "课程成绩：电路分析基础 98；数字电路 95；Verilog HDL 91；电工电子 A/B 均学分替代为优秀。")

# Project 01: compact three-part description in the original project area.
c.setFillColor(white)
c.rect(39, 430, 518, 127, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 9.43)
c.drawString(42.5, 548, "面向蜂鸟 E203 SoC 的 Transformer 加速芯片")
c.setFont("ResumeSong", 9.7)
c.drawRightString(552.8, 548, "2025.08--11")
c.drawString(42.5, 534, "2025 全国大学生嵌入式芯片与系统设计竞赛 · 芯片设计赛道 · 国家一等奖")
c.setFont("ResumeSong", 8.2)
c.drawString(45.5, 518, "基于蜂鸟 E203 NICE 接口的 TPU 架构，完成 InstDecoder、Scratchpad、DMA 与脉动阵列协同设计。")
c.drawString(45.5, 506, "实现 E203 SoC 集成、UVM 验证、FPGA 部署及完整 ASIC 中后端流程。")
c.drawString(45.5, 494, "本人负责 DMA、脉动阵列 RTL 设计，独立完成综合、布局布线、时序、功耗及版图验证。")
c.drawString(45.5, 482, "SMIC 40 nm，150 MHz，6.018 TOPS/W；完成车牌识别应用验证。")

# Project 02: preserve the same short, segmented structure.
c.setFillColor(white)
c.rect(39, 375, 518, 66, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 9.43)
c.drawString(42.5, 425, "LoongArch32 双发射乱序 CPU")
c.setFont("ResumeSong", 9.7)
c.drawRightString(552.8, 425, "2026.06--08")
c.drawString(42.5, 411, "2026 龙芯杯团体赛")
draw_wrapped(c, "基于 LoongArch32 ISA 实现双发射乱序 CPU 核，通过全部功能测试并完成 U-Boot 启动，性能相对 OpenLA500 达到 2.5×。", 45.5, 396, 507, size=8.55, leading=10.5)
c.drawString(45.5, 384, "本人担任 CPU 核设计成员，完成处理器核整体设计、功能测试与系统启动验证。")

# Project 03: retain the original structure and update only the two bullet points.
c.setFillColor(white)
c.rect(39, 298, 518, 76, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 9.43)
c.drawString(42.5, 360, "多声部分离、自动扒谱与演奏纠错系统")
c.setFont("ResumeSong", 9.7)
c.drawRightString(552.8, 360, "2026.09--至今")
c.drawString(42.5, 346, "FPGA 大赛 · 安路赛道")
y = draw_wrapped(c, "-  基于 Basic Pitch 架构，创新性实现自动扒谱与多声部分离的流式硬件系统，完成音符级转录、演奏纠错及谱面输出。", 45.5, 330, 507, size=9.65, leading=12.2)
draw_wrapped(c, "-  本人担任 FPGA 算子与数据流设计成员，完成 Conv2D、ReLU、Sigmoid 等核心算子的 PL 侧定点化与流式实现。", 45.5, y - 1.0, 507, size=9.65, leading=12.2)

# Project 04 and the lower resume block, kept in the original line-oriented style.
c.setFillColor(white)
c.rect(39, 53, 518, 248, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 9.43)
c.drawString(42.5, 286, "基于 M0 内核的 81 阶 FIR 滤波 SoC")
c.setFont("ResumeSong", 9.7)
c.drawRightString(552.8, 286, "2026")
c.drawString(42.5, 272, "四邮四电 ICT")
y = draw_wrapped(c, "-  基于 M0 内核的 SoC 架构，创新性实现 81 阶 FIR 滤波模块、FFA 与 DMA 协同数据通路，实现启动后零空泡连续运行。", 45.5, 256, 507, size=9.55, leading=12.0)
draw_wrapped(c, "-  本人担任 SoC 验证与数据通路设计成员，完成覆盖功能、性能及计数器观测的验证系统。", 45.5, y - 1.0, 507, size=9.55, leading=12.0)

c.setFont("ResumeBold", 10.78)
c.drawString(42.5, 205, "竞赛荣誉")
c.setLineWidth(0.45)
c.line(42.5, 198, 552.8, 198)

honors = [
    "-  2026 校一等奖学金。",
    "-  2025 校二等奖学金。",
    "-  2025 嵌赛芯片设计大赛：国家一等奖，2 / 322。",
    "-  2025 嵌赛 FPGA 大赛（安路赛道）：国家一等奖。",
    "-  2026 西门子杯嵌入式设计赛道：国家一等奖，15 / 13524。",
    "-  2026 嵌赛芯片应用大赛（ST 赛道）：国家二等奖。",
    "-  2026 全国大学生电子设计竞赛嵌入式前沿专题挑战赛（瑞萨杯）：国家二等奖。",
    "-  2026 全国大学生电子设计竞赛 AI 前沿专题挑战赛（英特尔杯）：国家三等奖。",
]
c.setFont("ResumeSong", 9.7)
honor_y = 181
for item in honors:
    c.drawString(45.5, honor_y, item)
    honor_y -= 15.0

c.line(42.5, 52, 552.8, 52)
c.save()

buffer.seek(0)
page.merge_page(PdfReader(buffer).pages[0])
writer = PdfWriter()
writer.add_page(page)
writer.add_metadata({"/Title": "尤钧个人简历", "/Author": "尤钧"})
with OUTPUT.open("wb") as stream:
    writer.write(stream)

print(OUTPUT)
