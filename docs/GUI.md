# GUI

The GUI system is designed around explicit programmer-controlled components.

Planned syntax:

```text
make.ui():
    title("My App")
    size(600, 400)
    background("white")

    add.label("Enter your name"):
        position(50, 40)

    add.input("name"):
        position(50, 80)
        size(300, 35)

    add.button("Submit"):
        position(50, 140)
        size(150, 40)
```

Nurture should never automatically create an arbitrary demo GUI. The programmer defines what appears and where.
