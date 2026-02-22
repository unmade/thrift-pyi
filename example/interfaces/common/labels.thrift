enum LabelColor {
    RED = 1,
    GREEN = 2,
    BLUE = 3,
}

struct Label {
    1: required string name
    2: required i32 color
}

const Label DEFAULT_LABEL = {"name": "default", "color": LabelColor.BLUE }
