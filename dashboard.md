# OPERATING DASHBOARD - FIXIT

**B2B · 09/10/2026 · Phạm Hương Giang - 2A202602359**  
**NORTH STAR:** ca được BQL xác minh có căn cứ/tuần · hiện **chưa đo** · pilot **≥80/100 ca đến hạn**

`[MH]` = mô hình giả định · `[TB]` = guardrail thử nghiệm, khóa sau 2 chu kỳ; không phải số đã đo.

| Tầng | Đèn | Hiện | 🟢 / 🟡 / 🔴 | Nguồn | Báo trước · luật |
|---|---|---:|---|---|---|
| L | TTFV | Chưa đo | ≤14d / 15-30d / >30d | `[TB]` 08/12 | Usage → retention · R-01 |
| L | Ca đủ bằng chứng | Chưa đo | ≥90 / 80-89 / <80% | `[TB]` 23/10 | Xác minh · R-02 |
| L | Phát hiện trước phản ánh | Chưa đo | ≥60 / 30-59 / <30% | `[TB]` 23/10 | Xử lý · theo dõi |
| O | Ca xác minh thành công | Chưa đo | ≥80 / 60-79 / <60% | `[TB]` 23/10 | Retention · R-03 |
| O | Median xử lý bất thường | Chưa đo | ≤24 / 25-48 / >48h | `[TB]` 23/10 | Retention · R-05 |
| O | Chi phí AI/ca | Chưa đo | ≤128 / 129-160 / >160đ | `[MH-01]` | GM · R-04 |
| G | Khách tiếp tục M3 | Chưa đo | ≥80 / 60-79 / <60% | `[MH-03]` | NRR/LTV |
| G | Gross Margin sau AI | Chưa đo | ≥60 / 50-59 / <50% | `[MH-02]` | Runway |

### 5 luật (⏹ = dừng)

1. **⏹ R-01:** TTFV >30d trên 2 pilot, ≥100 ca/pilot → dừng pilot mới 14d, cắt còn 1 tòa + 1 nhóm SLA; cấm tuyển sales/giảm giá.
2. **⏹ R-02:** bằng chứng <80% trong 2 tuần, ≥100 ca/tuần → đóng băng mở tòa mới, sửa checklist; cấm AI suy đoán dữ liệu thiếu.
3. **R-03:** xác minh <60% trong 2 tuần, ≥100 ca/tuần → mã hóa lỗi 20 ca, sửa nguyên nhân lớn nhất; cấm tăng volume/thêm dashboard.
4. **R-04:** AI >160đ/ca trong 2 tuần, ≥100 ca/tuần → giới hạn call, rút context, rule-based ca ít rủi ro; cấm bỏ QA/chuyển phí âm thầm.
5. **R-05:** xử lý >48h trong 2 tuần, ≥20 ca đóng/tuần → gán owner + SLA 24h; cấm gửi thêm cảnh báo hàng loạt.

### Cổng gác 90 ngày

| Ngày | Một metric | Ngưỡng | Bằng chứng | Nếu trượt |
|---|---|---|---|---|
| 08/11/26 | Ca xác minh lũy kế | ≥100 | `verified_cases.csv` | FIX một điểm nghẽn |
| 08/12/26 | Median TTFV | ≤30d, ≥2 pilot | `pilot_ttfv_report.csv` | PIVOT use case/user |
| 07/01/27 | BQL tiếp tục M3 | ≥60%, ≥5 BQL | Cohort activity log | KILL theo tiêu chí |

**KILL:** Đến 07/01/27, dừng hướng hiện tại nếu <3/5 BQL pilot tạo ≥1 ca hợp lệ ở M3 sau một vòng FIX onboarding.  
**CHƯA ĐO:** 8/8 đèn. Cần event log, AI-cost log, revenue/COGS; baseline tuần 23/10/26, TTFV 08/12/26, M3/GM 07/01/27.
