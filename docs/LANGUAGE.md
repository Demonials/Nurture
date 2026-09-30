# Nurture Language

## Core syntax

```usd
name = "Udit"
age = int(input("Age: "))
write(name)
```

### Conditions

```usd
if age >= 18:
    write("Adult")
elif age >= 13:
    write("Teenager")
else:
    write("Child")
```

### While

```usd
x = 1
while x <= 5:
    write(x)
    x = x + 1
```

### Loops

Legacy-compatible syntax:

```usd
loop i in 1..10:
    write(i)
```

Preferred compact syntax:

```usd
loop(1, 10)->write("hello")
```

or:

```usd
loop(1, 10)->
    write(i)
```

`loop(start, end)` is inclusive. A third argument sets the step.

```usd
loop(10, 1, -1)->write(i)
```

The automatic loop variable is `i`.

### Functions

```usd
function add(a, b):
    return a + b

write(add(2, 3))
```

### Input

```usd
name = input("Name: ")
age = int(input("Age: "))
height = float(input("Height: "))
```

Built-ins: `input`, `int`, `float`, `str`, `bool`, `len`, `type`, `write`.

### Modules

Use `link` before module access:

```usd
link math
link file
link web
link net
link crypto
link system
link process
link time
```
