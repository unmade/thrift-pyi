namespace * dates

struct DateTime {
    1: required i16 year,
    2: required byte month,
    3: required byte day
    4: required i16 hour,
    5: required byte minute,
    6: required byte second,
    7: optional i64 microsecond
}

struct Date {

}

const DateTime EPOCH = {
    "year": 1970,
    "month": 1,
    "day": 1,
    "hour": 0,
    "minute": 0,
    "second": 0,
    "microsecond": 0
}
