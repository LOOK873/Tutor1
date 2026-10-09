/* ตารางสอบ — แก้วันที่/ชื่อที่นี่ที่เดียว ใช้ทั้งหน้าแรกและหน้าเนื้อหา */
window.EXAMS = [
  { date: '2026-10-11', code: 'MTH2', name: 'MTH11102', note: 'ClassMarker (ออนไลน์)', kind: 'math' },
  { date: '2026-10-14', code: 'MTH1', name: 'MTH11101', note: 'ข้อเขียน · 13:00–16:00 น.', kind: 'math' },
  { date: '2026-10-15', code: 'PHY1', name: 'PHY ครั้งที่ 1', note: '', kind: 'phy' },
  { date: '2026-10-21', code: 'MTH2', name: 'MTH11102', note: 'สอบครั้งที่ 2', kind: 'math' },
  { date: '2026-10-22', code: 'PHY2', name: 'PHY ครั้งที่ 2', note: '', kind: 'phy' },
  { date: '2026-10-27', code: 'LAB PHY', name: 'LAB PHY', note: 'ปฏิบัติการฟิสิกส์', kind: 'phy' }
];
/* จำนวนวันจากวันนี้ (เวลาไทย) ถึงวันสอบ */
window.examDays = function (iso) {
  var t = new Date(Date.now() + 7 * 3600000);
  var today = Date.UTC(t.getUTCFullYear(), t.getUTCMonth(), t.getUTCDate());
  var p = iso.split('-');
  return Math.round((Date.UTC(+p[0], +p[1] - 1, +p[2]) - today) / 86400000);
};
window.examLabel = function (d) {
  return d < 0 ? 'สอบแล้ว' : d === 0 ? 'วันนี้!' : d === 1 ? 'พรุ่งนี้' : 'อีก ' + d + ' วัน';
};
window.nextExam = function () {
  for (var i = 0; i < EXAMS.length; i++) if (examDays(EXAMS[i].date) >= 0) return EXAMS[i];
  return null;
};
window.examChipText = function () {
  var e = nextExam();
  if (!e) return 'สอบครบแล้ว 🎉';
  return e.code + ' · ' + examLabel(examDays(e.date));
};
window.THAI_MONTH = ['', 'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
