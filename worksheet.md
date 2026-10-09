# Worksheet - FixIt

**Phạm Hương Giang · 2A202602359 · 09/10/2026**

> Chưa có khách thương mại/baseline. Số `[MH]` là giả định lab. `[TB]` là guardrail thử nghiệm, chưa phải baseline; khóa lại sau hai chu kỳ.

## Trạm 1 - Loại mô hình

**FixIt là B2B** vì công ty quản lý vận hành chung cư trả phí, BQL trực tiếp dùng hệ thống giám sát nhà cung cấp; cư dân chỉ gửi phản ánh và không trả tiền.

| Đèn B2B | Trạng thái | Số nằm ở đâu / cần gì để đo |
|---|---:|---|
| TTFV | 🔧 | Log bắt đầu pilot và ca đầu có SLA + bằng chứng + kết luận. |
| Pipeline coverage | ❌ | Cần CRM và target doanh thu quý. |
| Deal chết ở security/procurement | ❌ | Cần deal và lý do đóng trong CRM. |
| POC → paid | ❌ | Cần POC kết thúc và hợp đồng trả phí. |
| Sales cycle | ❌ | Cần ngày qualified và ngày ký. |
| Usage depth | 🔧 | Event tạo ca, nộp bằng chứng, hậu kiểm, xác minh. |
| Chi phí triển khai / ACV | 🔧 | Giờ triển khai × đơn giá + tích hợp, chia ACV. |
| Tập trung doanh thu | ❌ | Cần doanh thu theo khách. |
| NRR | ❌ | Cần doanh thu cohort qua kỳ. |
| Gross Margin | ❌ | Cần doanh thu và COGS thật. |
| CAC payback | ❌ | Hiện chỉ có giả định mô hình. |

## Trạm 2 - Cây ba tầng

**North Star:** ca vệ sinh được BQL xác minh có căn cứ/tuần - hiện **chưa đo** - mục tiêu pilot **≥80/100 ca đến hạn**. Chỉ tính ca có công việc, SLA, bằng chứng và kết luận; loại ca test/nháp/chỉ đánh dấu hoàn thành.

| # | Tầng | Đèn | Định nghĩa và công thức | Nhịp · owner | Báo trước cho |
|---:|:---:|---|---|---|---|
| 1 | L | TTFV | Ngày từ bắt đầu pilot đến ca giá trị đầu tiên; loại cài đặt/ca test. `verified_at đầu - pilot_started_at` | Mỗi pilot · Product Ops | Usage → retention |
| 2 | L | Ca đủ bằng chứng | Ca đến hạn đủ ảnh/thời gian/người theo SLA; loại bằng chứng thiếu/nộp sau hậu kiểm. `đủ / đến hạn` | Tuần · Supervisor | Xác minh thành công |
| 3 | L | Phát hiện trước phản ánh | Cảnh báo trước phản ánh và được BQL xác nhận; loại cảnh báo sau phản ánh/chưa xác nhận. `báo trước / bất thường xác nhận` | Tuần · Product Ops | Thời gian xử lý |
| 4 | O | Ca xác minh thành công | Ca đến hạn có SLA, bằng chứng, kết luận hợp lệ; loại test/nháp. `hợp lệ / đến hạn` | Tuần · BQL lead | Retention |
| 5 | O | Median xử lý bất thường | Giờ từ cảnh báo đến kết luận; loại ca mở/test, báo backlog riêng. Median thời gian | Tuần · BQL lead | Retention |
| 6 | O | Chi phí AI/ca | Token/API/inference production; loại R&D, test, triển khai. `AI cost / ca hợp lệ` | Tuần · FinOps | Gross Margin |
| 7 | G | Khách tiếp tục dùng M3 | Khách đầu kỳ còn ≥1 ca hợp lệ ở M3; loại khách mới/test. `active M3 / đầu kỳ` | Tháng · CS | NRR/LTV |
| 8 | G | Gross Margin sau AI | Doanh thu trừ AI, hosting, triển khai phân bổ; loại R&D/sales. `(Revenue-COGS)/Revenue` | Tháng · Finance | Runway |

Đèn chi phí AI: **#6**.

## Trạm 3 - Ngưỡng

| # | Đèn | 🟢 | 🟡 | 🔴 | Nguồn và lý do |
|---:|---|---:|---:|---:|---|
| 1 | TTFV | ≤14d | 15-30d | >30d | `[TB]` Phải tạo giá trị trong chu kỳ 30 ngày để còn thời gian FIX; khóa sau ≥2 pilot, 08/12/26. |
| 2 | Ca đủ bằng chứng | ≥90% | 80-89% | <80% | `[TB]` Dưới 80% khiến >1/5 ca không xác minh được; đo 2 tuần, khóa 23/10/26. |
| 3 | Phát hiện trước phản ánh | ≥60% | 30-59% | <30% | `[TB]` Giả thuyết giá trị chủ động; đo 2 tuần, khóa 23/10/26. |
| 4 | Ca xác minh thành công | ≥80% | 60-79% | <60% | `[TB]` Pilot cần ≥4/5 ca tạo kết luận; đo 2 tuần, khóa 23/10/26. |
| 5 | Median xử lý bất thường | ≤24h | 25-48h | >48h | `[TB]` Guardrail theo nhịp BQL hằng ngày; đo 2 tuần, khóa 23/10/26. |
| 6 | Chi phí AI/ca | ≤128đ | 129-160đ | >160đ | `[MH-01]` 160đ là trần; xanh có đệm biến động 20%. |
| 7 | Khách tiếp tục M3 | ≥80% | 60-79% | <60% | `[MH-03]` Payback 5 tháng; rời trước M3 đe dọa thu hồi CAC. |
| 8 | Gross Margin | ≥60% | 50-59% | <50% | `[MH-02]` 60% là mục tiêu; dưới 50% hụt ≥200.000đ lãi gộp/khách/tháng. |

### Phụ lục `[MH]`

**MH-01 - AI/ca:** COGS tối đa = 2.000.000 × (1-60%) = 800.000đ; ngân sách AI = 800.000 × 20% = 160.000đ; 1.000 ca → trần = **160đ/ca**; đệm 20% → xanh ≤128đ, vàng 129-160đ, đỏ >160đ.

**MH-02 - GM và CAC:** lãi gộp = 2.000.000 × 60% = **1.200.000đ/tháng**; CAC tối đa = 1.200.000 × 12 = **14.400.000đ**; CAC giả định 6.000.000đ → payback **5 tháng**. GM 50% chỉ cho 1.000.000đ, hụt 200.000đ/tháng → xanh ≥60%, vàng 50-59%, đỏ <50%.

**MH-03 - Retention M3:** CAC 6.000.000 / lãi gộp 1.200.000 = **5 tháng** hoàn vốn. Nếu M3 <60%, phần lớn cohort rời trước hoàn vốn; đặt mục tiêu pilot có đệm ở ≥80% → xanh ≥80%, vàng 60-79%, đỏ <60%.

## Trạm 4 - 5 luật

1. **⏹ R-01 NẾU** TTFV >30d **TRÊN** 2 pilot **VÀ** ≥100 ca/pilot **THÌ** dừng pilot mới 14d, cắt còn 1 tòa + 1 nhóm SLA **KHÔNG THÌ** không tuyển sales/giảm giá để che tắc nghẽn.
2. **⏹ R-02 NẾU** ca đủ bằng chứng <80% **TRONG** 2 tuần **VÀ** ≥100 ca/tuần **THÌ** đóng băng mở tòa mới, sửa checklist + trường bắt buộc **KHÔNG THÌ** không dùng AI suy đoán bằng chứng thiếu.
3. **R-03 NẾU** xác minh <60% **TRONG** 2 tuần **VÀ** ≥100 ca/tuần **THÌ** mã hóa lỗi 20 ca và sửa nguyên nhân lớn nhất sprint tới **KHÔNG THÌ** không tăng volume/thêm dashboard.
4. **R-04 NẾU** AI >160đ/ca **TRONG** 2 tuần **VÀ** ≥100 ca hợp lệ/tuần **THÌ** giới hạn call, rút context, dùng rule-based cho ca rủi ro thấp **KHÔNG THÌ** không bỏ QA/chuyển phí âm thầm.
5. **R-05 NẾU** median xử lý >48h **TRONG** 2 tuần **VÀ** ≥20 bất thường đóng/tuần **THÌ** gán một owner/ca + SLA 24h trong 14d **KHÔNG THÌ** không gửi thêm cảnh báo hàng loạt.

## Cổng gác 90 ngày

| Mốc | Metric duy nhất | Ngưỡng | Bằng chứng | Nếu trượt |
|---|---|---|---|---|
| 08/11/26 | Ca xác minh hợp lệ lũy kế | ≥100 | `verified_cases.csv` | FIX một điểm nghẽn |
| 08/12/26 | Median TTFV | ≤30d trên ≥2 pilot | `pilot_ttfv_report.csv` | PIVOT use case/user |
| 07/01/27 | BQL pilot tiếp tục dùng M3 | ≥60% trên ≥5 BQL | Cohort activity log | KILL nếu đạt tiêu chí |

**KILL:** Đến **07/01/2027**, dừng hướng hiện tại nếu **<3/5 BQL pilot** tạo ≥1 ca xác minh hợp lệ ở M3 sau một vòng FIX onboarding.

**CHƯA ĐO:** 8/8 đèn chưa có số production. Cần event log, AI-cost log và sổ revenue/COGS; baseline tuần 23/10/26, TTFV 08/12/26, retention M3 và GM sơ bộ 07/01/27.
