// =====================================================================================================================
// type_reference__CLASS – Полный справочник по классам в JavaScript

// =====================================================================================================================
// ФООРМЫ ЗАПИСИ
// ---------------------------------------------------------------------------------------------------------------------
// -------- 1. LAMBDA КЛАССЫ КАК ВЫРАЖЕНИЯ (анонимные классы) --------
console.log('\n=== 7. Классы как выражения ===');

const Rectangle = class {
    constructor(width, height) {
        this.width = width;
        this.height = height;
    }
    area() {
        return this.width * this.height;
    }
};
const rect = new Rectangle(10, 5);
console.log(rect.area()); // 50

// ---------------------------------------------------------------------------------------------------------------------
// -------- 2. БАЗОВОЕ ОБЪЯВЛЕНИЕ КЛАССА --------
console.log('=== 1. Базовое объявление класса ===');

class Person {
    // Конструктор
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    // Метод
    greet() {
        console.log(`Hello, I'm ${this.name}, ${this.age} years old.`);
    }

    // Ещё один метод
    celebrateBirthday() {
        this.age += 1;
        console.log(`Happy birthday! Now ${this.age}.`);
    }
}

const alice = new Person('Alice', 30);
alice.greet();                // Hello, I'm Alice, 30 years old.
alice.celebrateBirthday();    // Happy birthday! Now 31.

// =====================================================================================================================
// СВОЙСТВА И МЕТОДЫ
// ---------------------------------------------------------------------------------------------------------------------
// -------- 1. СВОЙСТВА И МЕТОДЫ - СТАТИЧЕСКИЕ  --------
console.log('\n=== 3. Статические свойства и методы ===');

class MathHelper {
    static PI = 3.14159;
    static square(x) {
        return x * x;
    }
    static cube(x) {
        return x * x * x;
    }
}

console.log(MathHelper.PI);              // 3.14159
console.log(MathHelper.square(4));       // 16
console.log(MathHelper.cube(3));         // 27

// ---------------------------------------------------------------------------------------------------------------------
// -------- 2. СВОЙСТВА И МЕТОДЫ - ПРИВАТНЫЕ (#) --------
console.log('\n=== 4. Приватные поля и методы ===');
// нельзя обращаться снаружи - только внутри методов

class BankAccount {
    #balance = 0;           // приватное поле

    constructor(initialBalance) {
        this.#balance = initialBalance;
    }

    // Публичный метод
    deposit(amount) {
        this.#add(amount);
    }

    withdraw(amount) {
        if (amount > this.#balance) {
            console.log('Insufficient funds');
        } else {
            this.#add(-amount);
        }
    }

    get balance() {
        return this.#balance;
    }

    // Приватный метод
    #add(amount) {
        this.#balance += amount;
    }
}

const account = new BankAccount(100);
console.log(account.balance);          // 100
account.deposit(50);
console.log(account.balance);          // 150
account.withdraw(30);
console.log(account.balance);          // 120
account.withdraw(200);                 // Insufficient funds
// console.log(account.#balance);      // SyntaxError
// account.#add(10);                  // SyntaxError

// ---------------------------------------------------------------------------------------------------------------------
// -------- 2. ГЕТТЕРАМИ И СЕТТЕРАМИ --------
console.log('\n=== 2. Геттеры и сеттеры ===');

class User {
    constructor(firstName, lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    // Геттер
    get fullName() {
        return `${this.firstName} ${this.lastName}`;
    }

    // Сеттер
    set fullName(name) {
        const parts = name.split(' ');
        this.firstName = parts[0];
        this.lastName = parts[1] || '';
    }
}

const user = new User('John', 'Doe');
console.log(user.fullName);          // John Doe
user.fullName = 'Jane Smith';
console.log(user.firstName);         // Jane
console.log(user.lastName);          // Smith

// ---------------------------------------------------------------------------------------------------------------------
// -------- 11. СВОЙСТВА КЛАССА (статические и экземпляра) --------

console.log('\n=== 11. Свойства класса ===');

class Car {
    static wheels = 4;
    constructor(model) {
        this.model = model;
    }
    get info() {
        return `${this.model} has ${Car.wheels} wheels.`;
    }
}
const car = new Car('Tesla');
console.log(car.info); // Tesla has 4 wheels.
console.log(Car.wheels); // 4

// =====================================================================================================================
// НАСЛЕДОВАНИЕ
// ---------------------------------------------------------------------------------------------------------------------
// -------- 5. НАСЛЕДОВАНИЕ (extends) --------
console.log('\n=== 5. Наследование ===');

class Animal {
    constructor(name) {
        this.name = name;
    }
    speak() {
        console.log(`${this.name} makes a sound.`);
    }
}

class Dog extends Animal {
    constructor(name, breed) {
        super(name);          // вызов конструктора родителя
        this.breed = breed;
    }
    speak() {
        console.log(`${this.name} (${this.breed}) barks!`);
    }
    fetch() {
        console.log(`${this.name} is fetching.`);
    }
}

const dog = new Dog('Rex', 'Labrador');
dog.speak();      // Rex (Labrador) barks!
dog.fetch();      // Rex is fetching.

// ---------------------------------------------------------------------------------------------------------------------
// -------- 9. АБСТРАКТНЫЕ МЕТОДЫ (симуляция) --------
console.log('\n=== 9. Абстрактные методы (имитация) ===');

class Shape {
    constructor(name) {
        if (this.constructor === Shape) {
            throw new Error('Shape is abstract');
        }
        this.name = name;
    }
    area() {
        throw new Error('Method area() must be implemented');
    }
}

class Circle extends Shape {
    constructor(radius) {
        super('Circle');
        this.radius = radius;
    }
    area() {
        return Math.PI * this.radius * this.radius;
    }
}
const circle = new Circle(3);
console.log(circle.area()); // ~28.27
// const shape = new Shape(); // Error: Shape is abstract

// ---------------------------------------------------------------------------------------------------------------------
// -------- 10. МИКСИНЫ (композиция) = ОБЬЕДИНЕНИЕ THIS в разных классов --------
console.log('\n=== 10. Миксины ===');

const LoggerMixin = {
    log() {
        console.log(`[LOG] ${this.name}`);
    }
};

class Service {
    constructor(name) {
        this.name = name;
    }
}
// Примешиваем методы
Object.assign(Service.prototype, LoggerMixin);

const service = new Service('API');
service.log('Service started'); // [LOG] Service started


// =====================================================================================================================
// ПРОВЕРКИ
// ---------------------------------------------------------------------------------------------------------------------
// -------- 6. ПРОВЕРКА ЭКЗЕМПЛЯРА (instanceof) --------
console.log('\n=== 6. Проверка instanceof ===');
console.log(dog instanceof Dog);      // true
console.log(dog instanceof Animal);   // true
console.log(dog instanceof Object);   // true
console.log(account instanceof BankAccount); // true


// ---------------------------------------------------------------------------------------------------------------------
// -------- 14. ПРОВЕРКА ТИПА КЛАССА --------

console.log('\n=== 14. Проверка типа класса ===');

console.log(typeof Person);               // "function"
console.log(Person.prototype.constructor === Person); // true
console.log(Object.getPrototypeOf(alice) === Person.prototype); // true


// =====================================================================================================================
// ДАНДЕРНЫЕ МЕТОДЫ
// ---------------------------------------------------------------------------------------------------------------------
// -------- 8. ВЫЧИСЛЯЕМЫЕ ИМЕНА МЕТОДОВ --------
console.log('\n=== 8. Вычисляемые имена свойств/методов ===');

const methodName = 'getArea';
class Square {
    constructor(side) {
        this.side = side;
    }
    [methodName]() {
        return this.side * this.side;
    }
}
const sq = new Square(4);
console.log(sq[methodName]()); // 16


// ---------------------------------------------------------------------------------------------------------------------
// -------- 12. ИТЕРИРУЕМЫЙ КЛАСС (Symbol.iterator) --------
console.log('\n=== 12. Итерируемый класс ===');

class Range {
    constructor(start, end) {
        this.start = start;
        this.end = end;
    }
    *[Symbol.iterator]() {
        for (let i = this.start; i <= this.end; i++) {
            yield i;
        }
    }
}
const range = new Range(1, 3);
for (const num of range) {
    console.log(num); // 1, 2, 3
}

// =====================================================================================================================
// РАЗНОЕ
// ---------------------------------------------------------------------------------------------------------------------
// -------- 13. ПРИВЯЗКА КОНТЕКСТА (bind) --------
console.log('\n=== 13. Привязка контекста ===');

class ClickHandler {
    constructor(name) {
        this.name = name;
    }
    handleClick() {
        console.log(`Clicked by ${this.name}`);
    }
}
const handler = new ClickHandler('Bob');
const btn = document.createElement('button');
// Привязываем контекст
btn.addEventListener('click', handler.handleClick.bind(handler));
// Или стрелочная функция
btn.addEventListener('click', () => handler.handleClick());

// ---------------------------------------------------------------------------------------------------------------------
// -------- 15. КРАТКИЙ СПРАВОЧНИК ПО СИНТАКСИСУ --------
console.log('\n=== 15. Краткий справочник ===');
console.log(`
Класс:
  class MyClass {
    constructor() { ... }
    method() { ... }
    get prop() { ... }
    set prop(val) { ... }
    static staticMethod() { ... }
    static staticProperty = value;
    #privateField = 0;
    #privateMethod() { ... }
  }

Наследование:
  class Child extends Parent {
    constructor(...args) {
      super(...args);
      ...
    }
    overrideMethod() { ... }
  }

Проверка:
  obj instanceof Class
  Object.getPrototypeOf(obj) === Class.prototype

Методы класса (встроенные):
  Object.assign(Child.prototype, mixin) – примешивание
  class MyClass { [computedName]() { ... } } – вычисляемые имена
`);

console.log('✅ Справочник по классам загружен.');


// =====================================================================================================================
