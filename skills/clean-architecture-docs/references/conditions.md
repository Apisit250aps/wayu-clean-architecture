# Thai JSDoc for conditions

เมื่อเขียนหรือแก้ JavaScript/TypeScript ต้องเพิ่มหรือปรับ Thai JSDoc `/** ... */` ให้ครบทุก condition ในขอบเขตนั้น รวมเงื่อนไขสั้นและเงื่อนไขที่ไม่ใช้ `if` หากเป็นคำขอเพิ่มเอกสารให้โค้ดเดิม ให้ตรวจทุก condition ในขอบเขตที่ผู้ใช้ระบุ ไม่ขยายไปแก้ทั้ง repository โดยไม่ได้ขอ

JSDoc ของ method อย่างเดียวไม่แทนคำอธิบายเงื่อนไขภายใน วางบล็อกใกล้ condition, branch, predicate, property หรือ statement ที่มี expression นั้น ถ้า expression ฝังอยู่ใน JSX/object/query ให้เลือกตำแหน่งที่ syntax เดิมรองรับ โดยไม่แทรกข้อความเป็น JSX output หรือเปลี่ยน evaluation order เพื่อวาง comment

แต่ละเงื่อนไขต้องบอกว่า **ตรวจข้อเท็จจริงอะไร เพราะเหตุใด และเมื่อเข้า/ไม่เข้าเงื่อนไขเกิดอะไร** ระบุ source/tenant/permission/status/time boundary ที่เกี่ยวข้องตาม source จริง อธิบายผลเป็น return/throw/skip/continue/query/fallback/state transition ตามที่โค้ดทำ ไม่เขียนเพียง “ตรวจ if” หรือแปลชื่อตัวแปรซ้ำ

| รูปแบบ | สิ่งที่ต้องอธิบาย |
| --- | --- |
| `if`/`else`, guards, `switch`/`case`/`default` | เหตุผลและผลแต่ละทาง รวม return/throw/break/continue และ fallthrough |
| Ternary และ conditional rendering | เงื่อนไขเลือกค่า/UI รวม hidden, disabled และ empty state |
| AND/OR/NOT, comparisons, membership, narrowing, optional chaining | เงื่อนไขย่อยและ short-circuit; optional chaining หยุดที่ null/undefined |
| Nullish/logical assignment และ fallback/default expressions | fallback ทำงานเมื่อใด; แยก null/undefined จาก falsy และ default parameter ไม่ทำงานเมื่อรับ null |
| Loops, recursion termination, callback predicates | ขอบเขตการทำซ้ำ/หยุด และการรับหรือคัดรายการใน filter/find/some/every |
| Schema refinements, assertions, validation/authorization/integrity/concurrency | สิ่งที่ผ่าน/ไม่ผ่าน ขอบเขต หน่วย error จริง และข้อจำกัดของการรับประกัน |
| SQL/ORM predicates, JOIN/CASE/exists/conflict conditions | tenant, active/deleted, relationship, revision, ช่วงเวลา และผล query; JSDoc อยู่นอก SQL string |
| Error/result discriminants และ async branches | เงื่อนไขเลือกผลสำเร็จ/ล้มเหลว การแปลง error และหน้าที่ caller |

หนึ่งบล็อกอธิบาย compound condition ที่อยู่ติดกันได้เมื่ออธิบายทุกส่วนและทุกทางครบ ไม่ใช้ comment กว้างหนึ่งบล็อกครอบหลายเงื่อนไขที่มีหน้าที่ต่างกัน ไม่สร้าง helper/variable หรือปรับ logic เพียงเพื่อให้ใส่ JSDoc ได้ และไม่เพิ่ม tags ที่ไม่ตรงกับ syntax เช่น `@returns` ให้ statement `if`

ตัวอย่างต่อไปเป็น contract สมมติ ต้องตรวจ implementation จริงก่อนนำไปใช้:

```ts
/**
 * ปฏิเสธเมื่อไม่พบสมาชิก หรือสมาชิกเป็นขององค์กรอื่น เพื่อไม่ให้คำขอนี้ข้าม tenant;
 * ใช้ short-circuit จึงไม่อ่าน organizationId จาก null และเมื่อผ่านจะทำงานขั้นถัดไป
 */
if (!member || member.organizationId !== organizationId) {
  throw new ForbiddenError();
}

/** คืนผลว่างทันทีเมื่อไม่มี IDs; เมื่อมี IDs จึงส่ง batch lookup ต่อ โดยยังไม่ได้รับรองว่า IDs ทุกตัวมีอยู่ */
if (ids.length === 0) return [];

/** ใช้ limit ที่ caller ส่งมา; เฉพาะ null/undefined จึงใช้ defaultLimit ส่วน 0 จะถูกส่งต่อให้ validation ตรวจ */
const limit = requestedLimit ?? defaultLimit;

/** แสดงปุ่มเฉพาะเมื่อมีสิทธิ์และรายการยัง PENDING; เงื่อนไขหนึ่งไม่ผ่านจะซ่อนปุ่ม และ UI นี้ไม่แทน server authorization */
const showApprove = canApprove && status === "PENDING";

/** ส่งช่วงที่มีวันงานให้ตรวจต่อ มิฉะนั้นใช้รายการว่าง; ไม่มีการอ่านฐานข้อมูลใน expression นี้ */
const scopes = hasWorkDates ? requestedScopes : [];

/**
 * จำกัดผลอ่านไว้ในองค์กรนี้ เฉพาะรายการที่ยังไม่ถูกลบ และวันที่อยู่ใน [startsOn, endsBefore);
 * แต่ละ predicate ต้องผ่านทั้งหมด แถวที่ไม่ผ่านจะไม่อยู่ในผลลัพธ์ และ query นี้ไม่ได้ตรวจสิทธิ์ของ actor
 */
const where = and(
  eq(records.organizationId, organizationId),
  isNull(records.deletedAt),
  gte(records.workDate, startsOn),
  lt(records.workDate, endsBefore),
);
```

หาก condition เรียก helper/schema/SQL expression ให้เปิดอ่านสัญญานั้นก่อนอธิบาย เช่น `exists` ไม่รับรอง authorization, query เช็คซ้ำไม่รับรอง uniqueness ภายใต้ concurrency และ `FOR UPDATE` ไม่คุ้มครอง write ที่อยู่นอก transaction หากไม่ทราบเหตุผลทางธุรกิจ ให้บอกสิ่งที่ source ตรวจได้และรายงานช่องว่าง ไม่แต่ง policy ขึ้นเอง

ตรวจทาน coverage จาก conditions ที่อยู่ใน diff/ขอบเขตที่ขอจริง รวม shorthand, callbacks และ query builders ไม่ใช้การนับ `if` หรือการมี JSDoc ของ method เป็นหลักฐานว่าครบทุกเงื่อนไข
