# แนวทางเขียน JSDoc อธิบายโค้ด

เขียนให้ผู้อ่านเข้าใจว่าโค้ดมีหน้าที่อะไร ใช้เมื่อไหร่ รับข้อมูลอะไร คืนผลลัพธ์อะไร และมีข้อควรระวังอะไร โดยไม่ต้องอ่าน implementation ทั้งหมด ใช้ภาษาไทยและคงชื่อเทคนิค เช่น Repository, Session และ UUID เป็นภาษาอังกฤษ

## หลักการ

- วาง `/** ... */` เหนือ declaration ที่อธิบาย เริ่มด้วยหน้าที่สั้น ๆ แล้วเพิ่มกฎหรือข้อจำกัดที่ผู้เรียกต้องรู้ เน้น What และ Why มากกว่าลำดับ implementation
- อ่าน implementation, interface และ callers ก่อนเขียน อย่าเดาเรื่อง authorization, tenant scope, transaction, validation, soft delete หรือ error จากชื่อเพียงอย่างเดียว หาก contract กับ implementation ต่างกัน ให้รายงานความต่างแทนการเขียนรับรองพฤติกรรมที่ยังไม่มี
- Public Class, Method, Function และ Interface/Type ควรมีคำอธิบายหน้าที่ ส่วน constructor, private method และตัวแปรภายในเขียนเมื่อมีข้อมูลที่ชื่อหรือชนิดข้อมูลสื่อไม่ครบ
- `@param` และ `@returns` อธิบายความหมาย หน่วย ข้อจำกัด และกรณีไม่พบข้อมูล ไม่เขียนแค่ชนิดข้อมูลซ้ำกับ TypeScript
- ระบุ `@throws` เฉพาะ error ที่เกิดขึ้นจริงและผู้เรียกควรรู้ ถ้าใช้ typed result แทนการ throw ให้อธิบายผลสำเร็จ/ล้มเหลวใน `@returns`
- ระบุ side effects, ขอบเขต transaction และเงื่อนไขการเรียกซ้ำเมื่อเกี่ยวข้อง โดยอ้างอิงพฤติกรรมจริง
- ใช้ `@example` เมื่อช่วยให้เรียกใช้ถูกต้อง เลือกข้อมูลสมมติและห้ามใส่ credentials หรือข้อมูลส่วนบุคคลจริง
- ไม่ต้องใส่ทุก tag หรืออธิบายทุกบรรทัดที่ไม่มีการตัดสินใจ แต่ทุก condition ที่เขียนหรือแก้ต้องมี JSDoc ตามหัวข้อ [Conditions](#conditions) แม้เป็นเงื่อนไขสั้น ไม่ใช้คอมเมนต์เส้นคั่นตกแต่ง และไม่แก้ logic เพื่อให้ตรงกับคำอธิบาย

## โครงสร้างพื้นฐาน

```ts
/**
 * สรุปหน้าที่ของโค้ด
 *
 * @remarks
 * เงื่อนไขทางธุรกิจ ขอบเขต หรือผลกระทบที่ผู้เรียกต้องรู้
 *
 * @param input - ความหมายและข้อจำกัดของข้อมูลเข้า
 * @returns ความหมายของผลลัพธ์ รวมกรณีว่างหรือไม่พบข้อมูล
 * @throws {ActualError} เงื่อนไขที่ทำให้เกิดข้อผิดพลาดนี้
 *
 * @example
 * // ตัวอย่างการเรียกที่ตรงกับ signature จริง
 */
```

โครงสร้างนี้เป็นแม่แบบ เลือกใช้เฉพาะส่วนที่จำเป็นและแทนชื่อ error ด้วยชื่อจริง ตัวอย่างด้านล่างเป็น contract สมมติ ไม่ใช่การรับรองว่าโปรเจกต์มีพฤติกรรมเหล่านี้

## Class, Constructor และ Method / UseCase

Class อธิบายหน้าที่และขอบเขต ส่วน method อธิบายสัญญาที่ผู้เรียกต้องพึ่งพา Constructor อธิบาย dependencies เฉพาะเมื่อมีรายละเอียดที่ชื่อยังสื่อไม่ครบ

```ts
/**
 * ประสานงานสร้างผู้ใช้งาน โดยตรวจสอบอีเมลซ้ำและแฮชรหัสผ่าน
 * ก่อนส่งข้อมูลให้ Repository จัดเก็บ
 */
export class CreateUserUseCase {
  /**
   * @param repo - แหล่งจัดเก็บผู้ใช้ที่บังคับ uniqueness ของอีเมล
   * @param hasher - บริการแฮชรหัสผ่านทางเดียวก่อนจัดเก็บ
   */
  constructor(
    private readonly repo: UserRepository,
    private readonly hasher: PasswordHasher,
  ) {}

  /**
   * สร้างผู้ใช้งานใหม่จากข้อมูลที่ผ่านการตรวจสอบรูปแบบแล้ว
   *
   * @param input - อีเมล ชื่อที่แสดง และรหัสผ่านก่อนแฮช
   * @returns ผู้ใช้งานที่บันทึกแล้ว โดยไม่รวมรหัสผ่านหรือค่าแฮช
   * @throws {EmailAlreadyExistsError} เมื่ออีเมลถูกใช้งานแล้ว
   *
   * @example
   * const user = await useCase.execute({
   *   email: "user@example.com",
   *   displayName: "Demo",
   *   password: "example-password",
   * });
   */
  async execute(input: CreateUserInput): Promise<User> {
    // ... implementation ที่ต้องตรวจสอบก่อนนำคำอธิบายนี้ไปใช้
  }
}
```

อย่าอ้างว่า query ตรวจซ้ำเพียงอย่างเดียวป้องกันการสร้างพร้อมกันได้ ต้องตรวจข้อบังคับใน storage และการแปลง error ด้วยก่อนอธิบายการรับประกันนั้น

## Interface / Type และ Repository

อธิบายความหมายของ contract โดยไม่ผูก Domain กับ ORM ระบุ nullable, optional, หน่วย และ scope ของ field เมื่อมีผลต่อการใช้งาน เขียน contract ร่วมที่ interface และเพิ่มรายละเอียดเฉพาะ adapter ที่ implementation โดยไม่คัดลอกทั้งบล็อก

```ts
/** ข้อมูลสำหรับสร้างผู้ใช้ หลังตรวจสอบรูปแบบแล้ว */
interface CreateUserInput {
  /** อีเมลที่ใช้เข้าสู่ระบบ ต้องไม่ซ้ำตามนโยบายของระบบ */
  email: string;
  /** รหัสผ่านก่อนแฮช ห้ามบันทึกลง log */
  password: string;
  /** ชื่อที่แสดงให้ผู้ใช้งานอื่นเห็น */
  displayName: string;
}

/** สัญญาการอ่านข้อมูลผู้ใช้ของ Domain โดยไม่ผูกกับฐานข้อมูลหรือ ORM */
interface UserRepository {
  /**
   * ค้นหาผู้ใช้ที่ยังไม่ถูก soft delete ภายในองค์กรที่กำหนด
   *
   * @param organizationId - องค์กรจาก context ที่ผ่านการตรวจสอบสิทธิ์แล้ว
   * @param id - UUID ของผู้ใช้
   * @returns ผู้ใช้ในองค์กรนั้น หรือ null เมื่อไม่พบหรือถูก soft delete
   */
  findById(organizationId: string, id: string): Promise<User | null>;
}
```

ถ้าเป็น batch method ให้ระบุว่าผลลัพธ์เรียงตาม input หรือไม่ และ ID ที่ไม่พบถูกละออกหรือคืนค่าอย่างไรตาม source จริง

## Function และ Constant

ฟังก์ชันอธิบาย input/output และเงื่อนไขการคำนวณ ค่าคงที่อธิบายความหมาย หน่วย และเหตุผลที่เลือกค่าเมื่อทราบ ไม่ต้องอธิบายตัวแปรที่อ่านแล้วเข้าใจทันที เช่น `const total = items.length`

```ts
/**
 * คำนวณราคาหลังหักส่วนลด โดยยังไม่รวมภาษีและไม่มีการปัดเศษ
 *
 * @param price - ราคาเริ่มต้น (บาท) ผู้เรียกต้องตรวจว่าไม่ติดลบ
 * @param discount - ส่วนลดเป็นเปอร์เซ็นต์ ผู้เรียกต้องตรวจว่าอยู่ในช่วง 0–100
 * @returns ราคาหลังหักส่วนลด (บาท)
 * @example
 * calculateDiscount(1000, 10); // 900
 */
function calculateDiscount(price: number, discount: number): number {
  return price * (1 - discount / 100);
}

/** อายุสูงสุดของ Session ก่อนต้องเข้าสู่ระบบใหม่ (วินาที) */
const SESSION_MAX_AGE = 3600;
```

## Conditions

ทุก condition ที่เขียนหรือแก้ต้องมี Thai JSDoc อธิบายข้อเท็จจริง เหตุผล และผลแต่ละทาง รวม expression, callback, validation และ SQL/ORM predicates อ่าน [คู่มือ conditions](conditions.md) เมื่อทำงานส่วนนี้; JSDoc ของ method อย่างเดียวไม่แทนคำอธิบายเงื่อนไขภายใน

## Tags ที่เลือกใช้

| Tag                        | ใช้เมื่อ                                                                       |
| -------------------------- | ------------------------------------------------------------------------------ |
| `@param`                   | มีความหมายหรือข้อจำกัดของ parameter ที่ควรอธิบาย                               |
| `@returns`                 | ต้องระบุผลลัพธ์ รวม null, ค่าว่าง หรือ typed error result                      |
| `@throws`                  | มี error ที่ throw/reject จริงและผู้เรียกควรจัดการ                             |
| `@remarks`                 | มีกฎทางธุรกิจหรือข้อจำกัดเพิ่มเติม                                             |
| `@example`                 | ตัวอย่างช่วยลดความเข้าใจผิดในการเรียกใช้งาน                                    |
| `@deprecated`              | ต้องเลิกใช้ พร้อมเหตุผลและทางเลือกที่มีจริง                                    |
| `@see`                     | มี declaration หรือเอกสารที่เกี่ยวข้อง                                         |
| `@internal`                | เป็น API ภายในตาม convention/tooling ของโปรเจกต์ ไม่ใช่การควบคุมสิทธิ์ runtime |
| `@template` / `@typeParam` | ต้องอธิบาย generic parameter เลือกให้ตรงกับ JSDoc/TSDoc tooling เดิม           |

ไม่เพิ่ม `@type` หรือ `{Type}` ซ้ำใน `@param`/`@returns` ของ TypeScript ที่มี type annotation อยู่แล้ว ใช้ tags ที่ tooling เดิมรองรับโดยไม่เพิ่ม dependency เพื่องานเขียนคำอธิบาย

## ตรวจทานก่อนส่ง

- คำอธิบายเพิ่มข้อมูลจากชื่อ เช่น “ค้นหาผู้ใช้ที่ยังไม่ถูกลบในองค์กร” แทน “ค้นหาผู้ใช้”
- ชื่อ parameter, return, error, business rules และตัวอย่างตรงกับ source และ callers รวม null/empty และ async behavior
- ไม่รับรอง tenant isolation, validation, transaction หรือ concurrency ที่ยังไม่ได้ตรวจจาก source
- ทุก condition ในขอบเขตที่เขียน/แก้มี Thai JSDoc อธิบายข้อเท็จจริง เหตุผล และผลแต่ละทาง รวม expression, callback, schema และ query predicates ตาม [Conditions](#conditions)
- แก้เฉพาะเอกสารตามขอบเขตที่ขอ ไม่เปลี่ยน signature, exports หรือ logic และไม่แก้ไฟล์ generated โดยตรง
- ตรวจ diff และ formatting ที่โปรเจกต์มี รายงานว่าเป็นการตรวจ source; ไม่อ้างผล runtime จากการแก้ JSDoc
