# Лаб 9: Автомат төлөвлөлт, PDDL

Хавтасны бүтэц:

```
lab9/
  pddl/        domain, problem, .soln файлууд
  sim.py       төлөвлөгөө шалгах симулятор
  sim_output.txt
  report.md
```

Ашигласан орчин: Python 3.12, pyperplan 2.1 (`pip install pyperplan`). Бүх .pddl файлыг VS Code дээр бичсэн.

---

## Алхам 1: pyperplan анх ажиллуулах

`pyperplan --help` дээр гарсан сонголтууд:

- хайлт (`-s`): astar, wastar, gbf, bfs, ehs, ids, sat
- heuristic (`-H`): blind, landmark, lmcut, hadd, hff, hmax, hsa
- log (`-l`): debug, info, warning, error

`pyperplan light_domain.pddl light_problem.pddl` ажиллуулахад `light_problem.pddl.soln` дотор нэг мөр гарсан:

```
(turn-on lamp)
```

Дараа нь `:init`-ийг `(on lamp)` болгож (`light_problem_on.pddl`) ажиллуулахад `Plan length: 0` гарч .soln файл хоосон үүссэн. Учир нь эхний төлөвт зорилго аль хэдийн биелсэн байгаа тул ямар ч үйлдэл хийх шаардлагагүй.

---

## Алхам 2: Blocksworld цаасан загвар

| Үйлдэл | Параметр | Precondition | Add | Delete |
|---|---|---|---|---|
| pick-up | x | (clear x) (ontable x) (handempty) | (holding x) | (ontable x) (clear x) (handempty) |
| put-down | x | (holding x) | (ontable x) (clear x) (handempty) | (holding x) |
| stack | x, y | (holding x) (clear y) | (on x y) (clear x) (handempty) | (holding x) (clear y) |
| unstack | x, y | (on x y) (clear x) (handempty) | (holding x) (clear y) | (on x y) (clear x) (handempty) |

Тоогоор нь (pre / add / del): pick-up 3/1/3, put-down 1/3/1, stack 2/3/2, unstack 3/2/3.

p01-ийг гараар шийдсэн нь:

| Алхам | Үйлдэл | Үйлдлийн дараах төлөв |
|---|---|---|
| 0 | Эхний төлөв | ontable a, ontable b, ontable c, clear a, clear b, clear c, handempty |
| 1 | pick-up b | ontable a, ontable c, clear a, clear c, holding b |
| 2 | stack b c | ontable a, ontable c, clear a, clear b, on b c, handempty |
| 3 | pick-up a | ontable c, clear b, on b c, holding a |
| 4 | stack a b | ontable c, on b c, on a b, clear a, handempty |

Төгсгөлд (on a b), (on b c) хоёулаа байгаа. Үйлдэл бүрийн өмнө precondition-ыг шалгасан.

**Яагаад a-г эхэлж авбал болохгүй вэ:** a-г авч b дээр тавьчихвал b-ийн дээд хаалттай болно (clear b алга болно). Тэгвэл b-г c дээр тавихын тулд a-г буцааж авах хэрэгтэй болж 2 илүү үйлдэл гарна. Тиймээс цамхгийг доороос нь босгох ёстой, эхлээд b-г c дээр, дараа нь a-г b дээр.

---

## Алхам 3, 4: Blocksworld domain ба problem

`pddl/blocks_domain.pddl` дээр 5 predicate (on, ontable, clear, holding, handempty), 4 үйлдэл бичсэн. "Гар хоосон" гэдгийг `(not (holding ...))` биш `(handempty)` гэж эерэг predicate-аар илэрхийлсэн, учир нь pyperplan сөрөг precondition дэмждэггүй.

Үр дүн (`pyperplan blocks_domain.pddl pXX.pddl`, default нь bfs):

| Problem | Урт | Төлөвлөгөө |
|---|---|---|
| p01 | 4 | (pick-up b) (stack b c) (pick-up a) (stack a b) |
| p02 | 6 | (unstack c a) (put-down c) (pick-up b) (stack b c) (pick-up a) (stack a b) |
| p03 | 8 | (unstack a b) (put-down a) (unstack b c) (stack b a) (unstack c d) (stack c b) (pick-up d) (stack d c) |

p01-ийн гарсан төлөвлөгөө миний гараар гаргасантай яг ижил байсан.

p02 (Sussman anomaly) дээр сонирхолтой нь, хэрвээ эхлээд (on a b)-г биелүүлэх гэвэл дараа нь b-г c дээр тавихын тулд a-г буцааж буулгах хэрэгтэй болдог. Төлөвлөгч энийг хоёр зорилгыг тусад нь биш хамтад нь харж шийдсэн.

p03 дээр төлөвлөгч "бүгдийг буулгаад дахин босгох" биш, a-г ширээнд тавиад дараагийн блокуудыг шууд a дээр өрж эхэлсэн. Тэгэхээр a нь шинэ цамхгийн суурь болж байгаа.

---

## Алхам 5: Симулятор

`sim.py` дотор:

- `applicable(state, pre)`: `pre <= state` (дэд олонлог эсэх)
- `apply(state, add, delete)`: `(state - delete) | add`, эхлээд хасаад дараа нь нэмнэ
- `make_action(name, args)`: Blocksworld, Logistics, Hanoi гурвын үйлдлийг үүсгэнэ
- `parse_plan(path)`: .soln файлыг уншина
- `check(init, goal, plan)`: алхам бүрийг шалгаж, алдаатай бол хэддэх алхамд, ямар баримт дутсаныг хэвлэнэ

init болон goal-ийг гараар бичихгүйн тулд problem файлаас нь уншдаг жижиг parser (`parse_problem`) нэмсэн.

Ажиллуулах: `python sim.py` (бүгдийг шалгана) эсвэл `python sim.py p03.pddl p03.pddl.soln` (нэгийг алхам алхмаар).

Гаралт (`sim_output.txt`):

```
===== pyperplan-ын төлөвлөгөөнүүд =====
p01.pddl + p01.pddl.soln
  ЗӨВ: 4 алхамтай төлөвлөгөө зорилгод хүрлээ
p02.pddl + p02.pddl.soln
  ЗӨВ: 6 алхамтай төлөвлөгөө зорилгод хүрлээ
p03.pddl + p03.pddl.soln
  ЗӨВ: 8 алхамтай төлөвлөгөө зорилгод хүрлээ
p04.pddl + p04.pddl.soln
  ЗӨВ: 10 алхамтай төлөвлөгөө зорилгод хүрлээ
lp01.pddl + lp01.pddl.soln
  ЗӨВ: 10 алхамтай төлөвлөгөө зорилгод хүрлээ
lp02.pddl + lp02.pddl.soln
  ЗӨВ: 18 алхамтай төлөвлөгөө зорилгод хүрлээ
lp03.pddl + lp03.pddl.soln
  ЗӨВ: 26 алхамтай төлөвлөгөө зорилгод хүрлээ
hanoi3.pddl + hanoi3.pddl.soln
  ЗӨВ: 7 алхамтай төлөвлөгөө зорилгод хүрлээ
hanoi4.pddl + hanoi4.pddl.soln
  ЗӨВ: 15 алхамтай төлөвлөгөө зорилгод хүрлээ

===== Гараар өгсөн буруу төлөвлөгөө (p01) =====
(stack a b) ганцаараа:
  БУРУУ: 0-р алхамд (stack a b) precondition биелээгүй. Дутуу: [('holding', 'a')]
(pick-up a), (pick-up b):
  БУРУУ: 1-р алхамд (pick-up b) precondition биелээгүй. Дутуу: [('handempty',)]
```

`(stack a b)` нэг мөртэй төлөвлөгөөг 0-р алхамд, хоёр блок зэрэг авах төлөвлөгөөг 1-р алхамд няцааж байгаа.

---

## Алхам 6: Хайлт ба heuristic-ийн харьцуулалт

Эхлээд `Measure-Command { pyperplan ... }`-аар хэмжихэд бүх тохиргоо ойролцоогоор 0.12 сек гарсан. Энэ нь ихэнхдээ Python асах, файл parse хийх хугацаа учраас ялгаа харагдахгүй байсан. Log дээрх "Search time" нь Windows дээр 0.0 эсвэл 0.016 л гардаг (нарийвчлал муу). Тиймээс pyperplan-ыг Python дотроос нь дуудаж зөвхөн хайлтын хугацааг `time.perf_counter()`-аар 5 удаа хэмжиж хамгийн багыг нь авсан. Зангилааны тоо нь log-ийн "Nodes expanded" мөрөөс.

| Хайлт | Heuristic | p03 урт | p03 хугацаа | p04 урт | p04 хугацаа | Зангилаа (p03 / p04) |
|---|---|---|---|---|---|---|
| bfs | | 8 | 0.31 ms | 10 | 1.56 ms | 48 / 185 |
| astar | blind | 8 | 0.26 ms | 10 | 1.07 ms | 28 / 96 |
| astar | hmax | 8 | 2.03 ms | 10 | 6.73 ms | 14 / 26 |
| astar | lmcut | 8 | 5.60 ms | 10 | 10.71 ms | 9 / 11 |
| astar | hff | 8 | 1.23 ms | 10 | 1.88 ms | 9 / 11 |
| gbf | hff | 8 | 1.09 ms | 10 | 1.90 ms | 9 / 11 |

**Дүгнэлт.** bfs ба зөвшөөрөгдөх heuristic-тэй astar бүгд p03 дээр 8, p04 дээр 10 гаргасан. Оновчтой урт нэг л байдаг тул оновчтой гэж баталгаатай алгоритмууд заавал ижил урт гаргах ёстой. Зангилааны тоогоор lmcut хамгийн нарийн (p04 дээр 11, hmax 26, blind 96), гэхдээ нэг зангилаанд heuristic бодох нь үнэтэй тул ийм жижиг бодлого дээр хугацаагаар хамгийн удаан нь болсон. gbf+hff ба astar+hff хурдан, бас энэ удаа оновчтой урт гаргасан, гэхдээ hff зөвшөөрөгдөхгүй тул үүнийг баталгаа гэж үзэж болохгүй. p03-аас p04 болоход bfs-ийн хугацаа ойролцоогоор 5 дахин, зангилаа 3.9 дахин өссөн. 9.5-ын хүснэгтэд 4 блокоос 5 блок болоход төлөвийн тоо 125-аас 866 буюу 7 дахин өсдөг. bfs бүх төлөвийг биш зөвхөн зорилго хүртэлх давхаргуудыг тэлдэг учраас 7-оос арай бага өсөлт гарсан нь тохирч байна.

---

## Алхам 7: Domain-д алдаа оруулах

Файлууд: `broken1.pddl` ... `broken4.pddl`. Эвдэрсэн domain-оос гарсан төлөвлөгөөг `brokenN_pXX.soln` гэж хадгалаад жинхэнэ дүрмээр (sim.py) шалгасан.

| Өөрчлөлт | Problem | Урт | Төлөвлөгөө | Симуляторын дүгнэлт |
|---|---|---|---|---|
| 1. pick-up, unstack-аас (handempty) pre хассан | p01 | 4 | (pick-up b) (pick-up a) (stack b c) (stack a b) | БУРУУ: 1-р алхам (pick-up a), дутуу (handempty) |
| 2. stack-аас (clear ?y) pre хассан | p02 | 6 | (pick-up b) (stack b a) (unstack b a) (stack b c) (pick-up a) (stack a b) | БУРУУ: 1-р алхам (stack b a), дутуу (clear a) |
| 3. put-down, stack-аас (handempty) add хассан | p01, p02, p03 | олдсонгүй | "No operators left. Task unsolvable" | шалгах төлөвлөгөө байхгүй |
| 4. unstack-аас (clear ?x) pre хассан | p03 | 6 | (unstack b c) (stack b a) (unstack c d) (stack c b) (pick-up d) (stack d c) | БУРУУ: 0-р алхам (unstack b c), дутуу (clear b) |

Өөрчлөлт 1: урт 4 хэвээр учраас хараад л буруу гэж хэлэх аргагүй, гэхдээ гар b-г барьж байхад a-г авчихсан.

Өөрчлөлт 2: урт 6 нь оновчтой урттай яг ижил. Гэтэл 1-р алхамд b-г a дээр тавьсан, a дээр c байгаа (clear биш). Урт зөв харагдсан ч төлөвлөгөө буруу байна.

Өөрчлөлт 3: гар нэг удаа блок авсны дараа хэзээ ч хоосон болдоггүй тул нэгээс илүү блок хөдөлгөх боломжгүй. pyperplan relevance analysis хийхэд л бодлого шийдэлгүй гэдгийг олсон.

Өөрчлөлт 4: урт 6 нь оновчтой 8-аас богино, энэ нь өөрөө алдааны шинж. Симулятор 0-р алхамд `(unstack b c)` үйлдлийн `(clear b)` precondition биелээгүй гэж гаргасан, учир нь b дээр a байсаар байна. Өөрөөр хэлбэл төлөвлөгч a-г огт хөдөлгөлгүйгээр доор нь байгаа b-г "сугалж" авсан.

**Дүгнэлт.** Оновчтойгоос богино төлөвлөгөө гарвал domain-д нөхцөл дутуу байгаа гэж бараг шууд хэлж болно. Харин урт зөв гарсан нь зөв гэсэн үг биш (өөрчлөлт 1, 2). Тиймээс төлөвлөгөөг заавал тусдаа симулятороор шалгах хэрэгтэй. Шалгасны дараа domain-уудыг буцааж засаагүй, эх `blocks_domain.pddl` огт өөрчлөгдөөгүй, зөвхөн хуулбар дээр туршсан.

---

## Алхам 8: Logistics, lp01

`pddl/logistics_domain.pddl`: төрлийн удамшил (`truck airplane - vehicle`, `vehicle package - physobj` г.м.), 3 predicate, 6 үйлдэл. `pddl/lp01.pddl`-д бүх in-city баримтыг (a1, a2-ыг оруулаад) бичсэн.

Үр дүн: **10 үйлдэл**

```
(load-truck pkg1 t1 c1-1)
(drive-truck t1 c1-1 a1 city1)
(unload-truck pkg1 t1 a1)
(drive-truck t2 c2-1 a2 city2)
(load-airplane pkg1 plane1 a1)
(fly-airplane plane1 a1 a2)
(unload-airplane pkg1 plane1 a2)
(load-truck pkg1 t2 a2)
(drive-truck t2 a2 c2-1 city2)
(unload-truck pkg1 t2 c2-1)
```

Ачааны зам: t1 машин pkg1-ийг c1-1-ээс city1-ийн агаарын буудал a1 хүртэл зөөсөн. plane1 онгоц a1-ээс a2 руу нисэж ачааг city2-т авчирсан. Энэ хооронд t2 машин c2-1-ээс хоосон a2 руу очиж хүлээсэн, тэгээд ачааг a2-оос c2-1 хүртэл хүргэсэн. Симулятор дээр зөв гарсан.

---

## Алхам 9: lp02

Урт: **18 үйлдэл** (bfs, astar+lmcut хоёулаа 18).

```
(load-truck pkg2 t2 c2-1)
(load-truck pkg1 t1 c1-1)
(drive-truck t2 c2-1 a2 city2)
(unload-truck pkg2 t2 a2)
(drive-truck t1 c1-1 a1 city1)
(unload-truck pkg1 t1 a1)
(load-airplane pkg1 plane1 a1)
(fly-airplane plane1 a1 a2)
(load-airplane pkg2 plane1 a2)
(unload-airplane pkg1 plane1 a2)
(load-truck pkg1 t2 a2)
(drive-truck t2 a2 c2-1 city2)
(unload-truck pkg1 t2 c2-1)
(fly-airplane plane1 a2 a1)
(unload-airplane pkg2 plane1 a1)
(load-truck pkg2 t1 a1)
(drive-truck t1 a1 c1-2 city1)
(unload-truck pkg2 t1 c1-2)
```

**1. Яагаад 20 биш вэ?** pkg2-ыг ганцаар нь зөөвөл 11 үйлдэл болно (машин c2-1 -> a2, онгоц эхлээд хоосон a1 -> a2 нисэх, буцаж нисэх, t1 хоосон c1-1 -> a1 очих гэх мэт). Тэгэхээр тусдаа хийвэл 10 + 11 = 21. Хамтад нь хийхэд гурван үйлдэл хоёр ачаанд зэрэг хэрэглэгдсэн:

- `(drive-truck t2 c2-1 a2 city2)`: pkg2-ыг буудал руу авчирсан, бас t2-ыг pkg1-ийг тосохоор a2 дээр очуулсан.
- `(drive-truck t1 c1-1 a1 city1)`: pkg1-ийг буудал руу авчирсан, бас t1-ийг pkg2-ыг тосохоор a1 дээр үлдээсэн.
- `(fly-airplane plane1 a1 a2)`: pkg1-ийг зөөсөн, бас онгоцыг pkg2-ыг авахаар a2 дээр авчирсан.

21 - 3 = 18.

**2. Хугацаа.** bfs: lp01 0.59 ms (82 зангилаа), lp02 8.41 ms (727 зангилаа), ойролцоогоор 14 дахин өссөн. astar+lmcut: lp01 8.36 ms (13 зангилаа), lp02 165 ms (65 зангилаа), 20 дахин өссөн. lmcut зангилааг 11 дахин цөөн тэлсэн ч нэг зангилаа бүрт LM-cut бодох нь Python дээр удаан тул нийт хугацаагаар bfs-ээс удаан байсан.

| Problem | Хайлт | Урт | Зангилаа | Хугацаа |
|---|---|---|---|---|
| lp01 | bfs | 10 | 82 | 0.59 ms |
| lp01 | astar lmcut | 10 | 13 | 8.36 ms |
| lp01 | gbf hff | 10 | 13 | 1.78 ms |
| lp02 | bfs | 18 | 727 | 8.41 ms |
| lp02 | astar lmcut | 18 | 65 | 165.36 ms |
| lp02 | gbf hff | 18 | 23 | 6.17 ms |

**3. Онгоц хэдэн удаа нисэв?** 2 удаа (a1 -> a2, a2 -> a1). Нэг удаа нисэх боломжгүй, учир нь хоёр ачаа эсрэг чиглэлд явж байгаа: pkg1 city1-ээс city2 руу, pkg2 city2-оос city1 руу.

---

## Нэмэлт 1: Hanoi цамхаг

`pddl/hanoi_domain.pddl`, `hanoi3.pddl`, `hanoi4.pddl`. Төрөл: `place - object`, `peg disk - place`. `smaller` нь статик баримт, peg бүх дискнээс том, d1 хамгийн жижиг.

| Problem | Хайлт | Урт | Зангилаа | Хугацаа |
|---|---|---|---|---|
| hanoi3 | bfs | 7 | 20 | 0.17 ms |
| hanoi3 | astar lmcut | 7 | 13 | 8.08 ms |
| hanoi4 | bfs | 15 | 81 | 0.93 ms |
| hanoi4 | astar lmcut | 15 | 46 | 57.73 ms |
| hanoi4 | gbf hff | 15 | 33 | 7.41 ms |

3 диск 7 нүүдэл, 4 диск 15 нүүдэл, хоёулаа 2^n - 1 томъёотой тохирч байна.

**Тулгарсан асуудал:** эхэндээ `(:types place peg disk - place)` гэж бичсэн. pyperplan үүнийг "place, peg, disk гурвуулаа place-ийн хүүхэд" гэж уншаад place өөрөө өөрийнхөө эцэг болж, pyperplan гацаад 2 минут юу ч гаргаагүй. `(:types place - object peg disk - place)` болгож засахад шууд ажилласан.

## Нэмэлт 2: Гурван ачаатай Logistics (lp03)

city2-т c2-2 нэмсэн. Оновчтой урт **26**.

| Хайлт | Heuristic | Урт | Зангилаа | Хугацаа |
|---|---|---|---|---|
| bfs | | 26 | 12924 | 0.22 s |
| astar | blind | 26 | 12750 | 0.29 s |
| astar | hmax | 26 | 10537 | 6.36 s |
| astar | lmcut | 26 | 340 | 3.12 s |
| astar | hff | 26 | 341 | 0.21 s |
| gbf | hff | 26 | 32 | 0.019 s |

1. Оновчтой урт 26. bfs 0.22 сек-д олсон.
2. bfs 12924 зангилаа тэлсэн. Зөвшөөрөгдөх heuristic-тэй хайлтаас lmcut ердөө 340 зангилаа тэлсэн ч 3.1 сек болсон, hmax бүр 6.4 сек. Энэ хэмжээнд Python дээр heuristic бодох зардал зангилаа хэмнэснээс илүү гарч байна. Бодлого томрох тусам bfs-ийн зангилаа экспоненциалаар өсөх тул энэ харьцаа эргэх байх.
3. gbf+hff 26 гаргасан, оновчтойгоос 0-ээр илүү. Хамгийн хурдан (19 ms, 32 зангилаа) байсан.

---

## Хэлэлцүүлгийн асуултууд

**1. Хаалттай ертөнцийн таамаглал.** Төлөвт бичигдээгүй бүх баримт худал гэж үздэг тул init-д зөвхөн үнэн баримтуудыг бичихэд хангалттай. Жишээ нь p01-д `(on a b)` худал гэдгийг тусад нь бичих шаардлагагүй. Энэ нь domain, problem хоёрыг маш богино болгодог. Сул тал нь "ямар нэг зүйл биш" гэдгийг шууд илэрхийлэх боломжгүй (pyperplan сөрөг precondition дэмжихгүй). Тиймээс "гар хоосон" гэдгийг `(not (holding ?x))` гэж бичиж чадахгүй, оронд нь `handempty` гэсэн тусдаа predicate нэмж, түүнийг үйлдэл бүрт гараар нэмж хасах ёстой болсон. Үүнийг нэг газар мартвал (Алхам 7, өөрчлөлт 3) бодлого бүхэлдээ шийдэлгүй болдог.

**3. Admissible heuristic.** Зөвшөөрөгдөх heuristic гэдэг нь зорилго хүртэлх жинхэнэ зардлаас хэзээ ч их үнэлдэггүй heuristic. A* ийм heuristic-тэй бол илүү урт замыг богино гэж андуурч эрт дуусахгүй тул оновчтой шийдэл баталгаатай. hmax нь relaxed бодлогын хамгийн үнэтэй нэг дэд зорилгын зардлыг авдаг тул доод хязгаар болно. lmcut нь заавал хийх ёстой үйлдлийн бүлгүүдийн (landmark) зардлыг давхардуулахгүйгээр нэмдэг тул мөн доод хязгаар, гэхдээ hmax-аас том буюу нарийн (p04 дээр 11 vs 26 зангилаа). hff нь relaxed төлөвлөгөөний уртыг авдаг ба relaxed төлөвлөгөө оновчтой биш байж болох тул жинхэнэ зардлаас их гарах боломжтой. Тиймээс hff-тэй A* оновчтойг баталгаажуулахгүй, гэхдээ манай туршилтуудад бүгд оновчтой урт гарсан.

---

## Дүгнэлт

Энэ лабораторид Blocksworld, Logistics, Hanoi бодлогуудыг PDDL-ээр бичиж pyperplan-аар шийдүүлсэн. Бүх төлөвлөгөөг өөрийн бичсэн симулятороор шалгахад зөв гарсан. Хамгийн их ойлгосон зүйл бол төлөвлөгч domain-д бичсэнийг л мэддэг, нэг precondition дутвал урт нь зөв ч гэсэн буруу төлөвлөгөө гаргадаг (Алхам 7). Мөн heuristic нь зангилааны тоог маш их багасгадаг ч, жижиг бодлого дээр түүнийг бодох зардал нь хугацааг бүр нэмэгдүүлж болохыг харсан (lp03 дээр lmcut 3.1 сек, bfs 0.22 сек).
