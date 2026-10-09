from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "dashboard.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
styles = getSampleStyleSheet()
base = ParagraphStyle("base", fontName="Arial", fontSize=7.2, leading=9, textColor=colors.HexColor("#172033"))
small = ParagraphStyle("small", parent=base, fontSize=6.4, leading=7.7)
h1 = ParagraphStyle("h1", parent=base, fontName="Arial-Bold", fontSize=17, leading=20, textColor=colors.HexColor("#0B5D4B"), alignment=TA_CENTER)
h2 = ParagraphStyle("h2", parent=base, fontName="Arial-Bold", fontSize=9.5, leading=11, textColor=colors.white, backColor=colors.HexColor("#0B5D4B"), spaceBefore=5, spaceAfter=3, leftIndent=3)
bold = ParagraphStyle("bold", parent=base, fontName="Arial-Bold")

def P(x, sty=base): return Paragraph(x, sty)
def tbl(data, widths, header=True):
    t = Table([[P(str(c), bold if header and r == 0 else small) for c in row] for r, row in enumerate(data)], colWidths=widths, repeatRows=1 if header else 0)
    cmd=[("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#AAB4C0")),("LEFTPADDING",(0,0),(-1,-1),3),("RIGHTPADDING",(0,0),(-1,-1),3),("TOPPADDING",(0,0),(-1,-1),2.5),("BOTTOMPADDING",(0,0),(-1,-1),2.5)]
    if header: cmd += [("BACKGROUND",(0,0),(-1,0),colors.HexColor("#DDEFEA")),("TEXTCOLOR",(0,0),(-1,0),colors.HexColor("#0B5D4B"))]
    t.setStyle(TableStyle(cmd)); return t

doc=SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=10*mm,rightMargin=10*mm,topMargin=9*mm,bottomMargin=9*mm)
S=[]
S += [P("OPERATING DASHBOARD - FIXIT", h1), P("B2B · 09/10/2026 · Phạm Hương Giang - 2A202602359", ParagraphStyle("meta",parent=base,alignment=TA_CENTER)), Spacer(1,3), P("<b>NORTH STAR:</b> ca được BQL xác minh có căn cứ/tuần · hiện <b>chưa đo</b> · pilot <b>≥80/100 ca đến hạn</b>"), P("[MH] = mô hình giả định · [TB] = guardrail thử nghiệm, khóa sau 2 chu kỳ; không phải số đã đo.", small), P("CÂY ĐÈN 3 TẦNG",h2)]
metrics=[["Tầng","Đèn","Hiện","Xanh / Vàng / Đỏ","Nguồn","Báo trước · luật"],["L","TTFV","Chưa đo","≤14d / 15-30d / >30d","[TB] 08/12","Usage→retention · R-01"],["L","Ca đủ bằng chứng","Chưa đo","≥90 / 80-89 / <80%","[TB] 23/10","Xác minh · R-02"],["L","Phát hiện trước phản ánh","Chưa đo","≥60 / 30-59 / <30%","[TB] 23/10","Xử lý · theo dõi"],["O","Ca xác minh thành công","Chưa đo","≥80 / 60-79 / <60%","[TB] 23/10","Retention · R-03"],["O","Median xử lý bất thường","Chưa đo","≤24 / 25-48 / >48h","[TB] 23/10","Retention · R-05"],["O","Chi phí AI/ca","Chưa đo","≤128 / 129-160 / >160đ","[MH-01]","GM · R-04"],["G","Khách tiếp tục M3","Chưa đo","≥80 / 60-79 / <60%","[MH-03]","NRR/LTV"],["G","Gross Margin sau AI","Chưa đo","≥60 / 50-59 / <50%","[MH-02]","Runway"]]
S.append(tbl(metrics,[9*mm,39*mm,20*mm,39*mm,23*mm,60*mm])); S.append(P("5 LUẬT QUYẾT ĐỊNH ([DỪNG] = LUẬT DỪNG)",h2))
rules=["<b>[DỪNG] R-01:</b> TTFV >30d trên 2 pilot, ≥100 ca/pilot → dừng pilot mới 14d, cắt còn 1 tòa + 1 nhóm SLA; cấm tuyển sales/giảm giá.","<b>[DỪNG] R-02:</b> bằng chứng <80% trong 2 tuần, ≥100 ca/tuần → đóng băng mở tòa mới, sửa checklist; cấm AI suy đoán dữ liệu thiếu.","<b>R-03:</b> xác minh <60% trong 2 tuần, ≥100 ca/tuần → mã hóa lỗi 20 ca, sửa nguyên nhân lớn nhất; cấm tăng volume/thêm dashboard.","<b>R-04:</b> AI >160đ/ca trong 2 tuần, ≥100 ca/tuần → giới hạn call, rút context, rule-based ca ít rủi ro; cấm bỏ QA/chuyển phí âm thầm.","<b>R-05:</b> xử lý >48h trong 2 tuần, ≥20 ca đóng/tuần → gán owner + SLA 24h; cấm gửi thêm cảnh báo hàng loạt."]
for x in rules: S.append(P(x,small)); S.append(Spacer(1,1))
S.append(P("CỔNG GÁC 90 NGÀY",h2)); gates=[["Ngày","Một metric","Ngưỡng","Bằng chứng","Nếu trượt"],["08/11/26","Ca xác minh lũy kế","≥100","verified_cases.csv","FIX một điểm nghẽn"],["08/12/26","Median TTFV","≤30d, ≥2 pilot","pilot_ttfv_report.csv","PIVOT use case/user"],["07/01/27","BQL tiếp tục M3","≥60%, ≥5 BQL","Cohort activity log","KILL theo tiêu chí"]]
S.append(tbl(gates,[22*mm,42*mm,35*mm,50*mm,41*mm])); S += [Spacer(1,3),P("<b>KILL:</b> Đến 07/01/27, dừng hướng hiện tại nếu <3/5 BQL pilot tạo ≥1 ca hợp lệ ở M3 sau một vòng FIX onboarding.",small),P("<b>CHƯA ĐO:</b> 8/8 đèn. Cần event log, AI-cost log, revenue/COGS; baseline tuần 23/10/26, TTFV 08/12/26, M3/GM 07/01/27.",small),PageBreak(),P("PHỤ LỤC [MH] - FIXIT",h1),P("Toàn bộ đầu vào dưới đây là giả định phục vụ lab, không phải dữ liệu kinh doanh thực tế.",base),P("MH-01 · CHI PHÍ AI/CA",h2),P("ARPU 2.000.000đ; GM 60% → COGS tối đa = 800.000đ. AI = 20% COGS = 160.000đ/tháng. Với 1.000 ca: trần = <b>160đ/ca</b>. Đệm 20% → xanh ≤128đ · vàng 129-160đ · đỏ >160đ."),P("MH-02 · GROSS MARGIN VÀ CAC",h2),P("Lãi gộp = 2.000.000 × 60% = <b>1.200.000đ/tháng</b>. CAC tối đa = 1.200.000 × 12 = <b>14.400.000đ</b>. CAC giả định 6.000.000đ → payback = <b>5 tháng</b>. GM 50% hụt 200.000đ/khách/tháng → xanh ≥60% · vàng 50-59% · đỏ <50%."),P("MH-03 · DUY TRÌ KHÁCH M3",h2),P("CAC 6.000.000 / lãi gộp 1.200.000 = <b>5 tháng</b> hoàn vốn. Nếu retention M3 <60%, phần lớn cohort rời trước hoàn vốn; mục tiêu pilot có đệm ≥80% → xanh ≥80% · vàng 60-79% · đỏ <60%."),P("NGUỒN VÀ GIỚI HẠN",h2),P("Nguồn nội bộ: mô tả FixIt và giả định tài chính do nhóm cung cấp ngày 09/10/2026. Phương pháp: HANDBOOK.md Day 23, mục B2B. Không dùng benchmark ngoài trong ngưỡng; [TB] sẽ được thay bằng baseline thật sau hai chu kỳ. TTFV hiện tính từ lúc bắt đầu pilot; khi có hợp đồng thương mại sẽ đổi mốc đầu thành ngày ký.")]
doc.build(S)
print(OUT)
