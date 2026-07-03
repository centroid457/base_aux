// ============================================================
// 1. СОЗДАНИЕ SET
// ============================================================

// 1.1 Пустой Set (самый частый)
const empty = new Set();
console.log('empty size:', empty.size); // 0

// 1.2 Из массива (дубликаты игнорируются)
const fromArray = new Set([1, 2, 3, 3, 4]); // {1,2,3,4}
console.log('fromArray:', [...fromArray]); // [1,2,3,4]

// 1.3 Из строки (разбивается на символы)
const fromString = new Set('hello'); // {'h','e','l','o'} (две 'l' схлопнуты)
console.log('fromString:', [...fromString]); // ['h','e','l','o']

// 1.4 Из другого Set (клонирование)
const original = new Set([1,2,3]);
const cloned = new Set(original);
console.log('cloned:', [...cloned]); // [1,2,3]

// 1.5 Из любого итерируемого объекта (генератор)
function* gen() { yield 'a'; yield 'b'; yield 'a'; }
const fromGen = new Set(gen()); // {'a','b'}
console.log('fromGen:', [...fromGen]);

// 1.6 Из объекта (только значения, ключи теряются)
const obj = { a: 1, b: 2, c: 1 };
const fromObjValues = new Set(Object.values(obj)); // {1,2}
console.log('fromObjValues:', [...fromObjValues]);

// 1.7 Из Map (только значения, ключи теряются)
const map = new Map([['a',1], ['b',2], ['c',1]]);
const fromMapValues = new Set(map.values()); // {1,2}
// или new Set(map) – тогда будут пары [key,value] – не то
console.log('fromMapValues:', [...fromMapValues]);

// 1.8 Через добавление по одному (после создания)
const set = new Set();
set.add(1);
set.add(2);
set.add(2); // игнорируется
console.log('set:', [...set]); // [1,2]

// ============================================================
// 2. ОСНОВНЫЕ СВОЙСТВА И МЕТОДЫ
// ============================================================
const s = new Set([10, 20, 30]);

// 2.1 Размер
console.log('size:', s.size); // 3

// 2.2 Добавление (цепочка)
s.add(40).add(50);
console.log('after add:', [...s]); // [10,20,30,40,50]

// 2.3 Проверка наличия
console.log('has(20):', s.has(20));  // true
console.log('has(99):', s.has(99));  // false

// 2.4 Удаление одного элемента
const deleted = s.delete(20);
console.log('deleted 20:', deleted); // true
console.log('after delete:', [...s]); // [10,30,40,50]

// 2.5 Очистка всех
s.clear();
console.log('after clear size:', s.size); // 0

// ============================================================
// 3. ОСОБЕННОСТИ РАВЕНСТВА (NaN и объекты)
// ============================================================
const spec = new Set();
spec.add(NaN);
spec.add(NaN);      // второй NaN игнорируется – они считаются равными
console.log('NaN size:', spec.size); // 1

// Объекты сравниваются по ссылке
const a = {};
const b = {};
spec.add(a);
spec.add(b);        // два разных объекта – разные
spec.add(a);        // тот же объект – игнорируется
console.log('objects size:', spec.size); // 3 (NaN + a + b)

// ============================================================
// 4. ИТЕРАЦИЯ
// ============================================================
const data = new Set(['x', 'y', 'z']);

// 4.1 for...of (значения)
console.log('for...of:');
for (const item of data) {
    console.log(item);
}

// 4.2 forEach (с индексом, но индекс = значение)
console.log('forEach:');
data.forEach((value, valueAgain, set) => {
    console.log(value, valueAgain); // одинаковые
});

// 4.3 keys() – синоним values() (для совместимости с Map)
console.log('keys():', [...data.keys()]); // ['x','y','z']

// 4.4 values() – то же самое
console.log('values():', [...data.values()]); // ['x','y','z']

// 4.5 entries() – возвращает пары [значение, значение]
console.log('entries():', [...data.entries()]); // [['x','x'], ['y','y'], ['z','z']]

// ============================================================
// 5. ПРЕОБРАЗОВАНИЯ
// ============================================================
const set2 = new Set([1,2,3]);

// 5.1 В массив (два способа)
const arr1 = Array.from(set2);
const arr2 = [...set2];
console.log('array:', arr1); // [1,2,3]

// 5.2 В строку (через join)
console.log('join:', [...set2].join(', ')); // "1, 2, 3"

// 5.3 В объект (если нужны ключи – только если ключи строковые)
const objFromSet = Object.fromEntries([...set2].map(v => [v, v]));
console.log('object:', objFromSet); // {1:1, 2:2, 3:3}

// ============================================================
// 6. ОПЕРАЦИИ НАД МНОЖЕСТВАМИ (не встроены, но легко сделать)
// ============================================================
const A = new Set([1,2,3]);
const B = new Set([2,3,4]);

// 6.1 Объединение
const union = new Set([...A, ...B]); // {1,2,3,4}

// 6.2 Пересечение
const intersection = new Set([...A].filter(x => B.has(x))); // {2,3}

// 6.3 Разность (A \ B)
const difference = new Set([...A].filter(x => !B.has(x))); // {1}

console.log('union:', [...union]);
console.log('intersection:', [...intersection]);
console.log('difference:', [...difference]);

// ============================================================
// 7. WEAKSET (кратко)
// ============================================================
// WeakSet – только объекты, нет size, не итерируется, автоматическое удаление
const ws = new WeakSet();
let obj1 = {};
ws.add(obj1);
console.log('WeakSet has obj1:', ws.has(obj1)); // true
obj1 = null; // после сборки мусора элемент может исчезнуть

// ============================================================
// 8. ПРОВЕРКА ТИПА
// ============================================================
console.log('typeof set:', typeof set2);              // 'object'
console.log('instanceof Set:', set2 instanceof Set);  // true
console.log('toString:', Object.prototype.toString.call(set2)); // '[object Set]'


// =====================================================================================================================
