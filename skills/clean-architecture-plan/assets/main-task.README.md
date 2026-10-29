# {{MAIN_TASK_CODE}} — {{ชื่อ main task}}

{{ผลลัพธ์และประโยชน์ต่อผู้ใช้แบบสั้น เหมาะสำหรับ Trello}}

- **ขอบเขต:** {{Web / Backend / Database และสิ่งที่จะทำ}}
- **รูปแบบการทำงาน:** {{ตามลำดับ (ค่าเริ่มต้น) หรือ ขนานที่ผู้ใช้เลือกชัดเจน พร้อมหลักฐานการเลือก}}
- **เริ่มได้เมื่อ:** {{งานย่อย producer และ contract/artifact ที่ต้องพร้อม ไม่รอ main task ทั้งก้อน}}
- **ก่อนเชื่อมระบบจริงต้องมี:** {{งาน integration และ real collaborators}}
- **ถือว่าเสร็จเมื่อ:** {{เกณฑ์ยอมรับและระดับหลักฐาน}}

## สัญญาและสิทธิ์

{{ลิงก์งานออกแบบเจ้าของ code blocks สำหรับ entity/repository/use case/service/permission/API และงาน catalog/default grants/seed; ระบุสิ่งที่ยังรอข้อสรุป}}

## Parallel map และลำดับที่เลือก

{{แทน node ด้วยรหัสงานจริง แสดง dependencies และจุดพร้อมเริ่มงานข้ามส่วน ระบุว่าโอกาสขนานเป็นข้อมูลประกอบเท่านั้นจนผู้ใช้เลือก ไม่ใช่สิทธิ์เรียก agent หรือเริ่ม execute}}

```mermaid
flowchart LR
    C[{{CONTRACT_TASK}}: Domain and permission contracts] --> S[{{SDK_TASK}}: Spec and generated client]
    C --> B[{{BACKEND_TASK}}: Implement backend]
    S --> W[{{WEB_TASK}}: Client hooks and forms]
    B --> H[{{HTTP_TASK}}: Real HTTP integration]
    S --> H
    H --> V[{{VERIFY_TASK}}: Browser integration]
    W --> V
```

- **ลำดับ/ช่วงงานที่เลือก:** {{ลำดับที่เคารพ dependencies; ถ้าขนานให้ระบุ waves/gates ที่ผู้ใช้เลือก}}
- **ส่วนที่อาจทำพร้อมกันได้:** {{งานและ artifact gates; ในโหมดตามลำดับให้ระบุว่ายังไม่จัดให้ทำพร้อมกัน}}
- **ไฟล์ร่วมและผู้รับผิดชอบ:** {{single writer/ส่งต่องานตามลำดับสำหรับ exports/codegen/migrations/catalogs/composition}}
- **ระดับพร้อมส่งต่อ:** {{แยก contract-ready, SDK-ready, HTTP-ready และตรวจระบบจริง}}

## งานย่อย

- [ ] [{{MAIN_TASK_CODE}}-01 {{ชื่องานย่อยภาษาไทย}}](tasks/{{MAIN_TASK_CODE}}-01-{{task-slug}}.md)
- [ ] [{{MAIN_TASK_CODE}}-02 {{ชื่องานย่อยภาษาไทย}}](tasks/{{MAIN_TASK_CODE}}-02-{{task-slug}}.md)
