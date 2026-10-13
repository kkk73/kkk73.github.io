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

# Project 03: retain the original structure and update only the two bullet points.
c.setFillColor(white)
c.rect(39, 298, 518, 76, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 9.43)
c.drawString(42.5, 360, "多声部分离、自动扒谱与演奏纠错系统")
c.setFont("ResumeSong", 9.7)
c.drawRightString(552.8, 360, "2026.09--至今")
c.drawString(42.5, 346, "FPGA 大赛 · 安路赛道")
y = draw_wrapped(c, "-  系统方案：流式实现 Basic Pitch 自动扒谱及多声部分离系统，覆盖音符级转录、演奏纠错与谱面输出。", 45.5, 330, 507, size=10.1, leading=13.4)
draw_wrapped(c, "-  硬件方案：围绕 Conv2D、ReLU、Sigmoid 等核心算子进行 FPGA PL 侧定点化与流式实现。", 45.5, y - 1.0, 507, size=10.1, leading=13.4)

# Project 04 and the lower resume block, kept in the original line-oriented style.
c.setFillColor(white)
c.rect(39, 53, 518, 248, fill=1, stroke=0)
c.setFillColor(black)
c.setFont("ResumeBold", 9.43)
c.drawString(42.5, 286, "基于 M0 内核的 81 阶 FIR 滤波 SoC")
c.setFont("ResumeSong", 9.7)
c.drawRightString(552.8, 286, "2026")
c.drawString(42.5, 272, "四邮四电 ICT")
y = draw_wrapped(c, "-  基于 M0 内核构建 SoC 并集成 81 阶 FIR 滤波模块；完成包含功能验证、性能验证和计数器的验证系统。", 45.5, 256, 507, size=10.0, leading=13.0)
draw_wrapped(c, "-  FFA 与 DMA 实现启动后零空泡运行。", 45.5, y - 1.0, 507, size=10.0, leading=13.0)

c.setFont("ResumeBold", 10.78)
c.drawString(42.5, 205, "竞赛荣誉")
c.setLineWidth(0.45)
c.line(42.5, 198, 552.8, 198)

honors = [
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

c.line(42.5, 82, 552.8, 82)
c.save()

buffer.seek(0)
page.merge_page(PdfReader(buffer).pages[0])
writer = PdfWriter()
writer.add_page(page)
writer.add_metadata({"/Title": "尤钧个人简历", "/Author": "尤钧"})
with OUTPUT.open("wb") as stream:
    writer.write(stream)

print(OUTPUT)
