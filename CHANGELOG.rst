###########
 Changelog
###########

*********************
 v2.1.0 (2025-03-18)
*********************

-  Fix `ValueError`` for mutable default when one dataclass is the
   default for a field in another (by `@FrankPortman
   <https://github.com/FrankPortman>`_)

*********************
 v2.0.0 (2025-02-19)
*********************

**BREAKING CHANGES**

-  Use type aliases for primitive types. Essentially all primitive types
   are now wrapped in Annotation and provide some meta information into
   original thrift type

*********************
 v1.2.0 (2024-12-25)
*********************

-  Correctly reference constants values from external modules (`#50
   <https://github.com/unmade/thrift-pyi/issues/50>`_)

*********************
 v1.1.0 (2024-12-17)
*********************

-  Correctly handle mutable defaults for structs

*********************
 v1.0.0 (2024-10-20)
*********************

**BREAKING CHANGES**

-  Drop python 3.7 and python 3.8 support * Arguments of type enum
   annotated as enum instead of 'int' (by `@N0I0C0K
   <https://github.com/N0I0C0K>`_)

-  Enum members are not annotated anymore (by `@N0I0C0K
   <https://github.com/N0I0C0K>`_)

*********************
 v0.9.0 (2024-04-27)
*********************

-  Dump constants after structures (`#47
   <https://github.com/unmade/thrift-pyi/issues/47>`_)

*********************
 v0.8.0 (2023-11-02)
*********************

-  Use sys.executable to run linters (contributed by `@FrankPortman
   <https://github.com/FrankPortman>`_)

*********************
 v0.7.0 (2023-08-17)
*********************

-  Support const (`#42
   <https://github.com/unmade/thrift-pyi/issues/42>`_)

v0.6.0 (2023-07-27)

-  Include fields on Exceptions (thanks to `@mjpizz
   <https://github.com/mjpizz>`_)

*********************
 v0.5.0 (2022-12-12)
*********************

-  Support `TTYPE.Binary`

*********************
 v0.4.0 (2022-08-29)
*********************

-  Generate stubs using ast instead of Jinja
-  Unpin black and autoflake dependencies
-  Support python 3.9 and python 3.10

*********************
 v0.3.0 (2022-01-22)
*********************

-  Allow to instantiate exceptions with arguments(bug reported by
   `@mjpizz <https://github.com/mjpizz>`_)

*********************
 v0.2.1 (2021-11-03)
*********************

-  Fix bug when empty exceptions could generate invalid python (`#27
   <https://github.com/unmade/thrift-pyi/issues/27>`_)

*********************
 v0.2.0 (2020-10-29)
*********************

-  Add `TType.Binary` support

*********************
 v0.1.0 (2019-05-28)
*********************

-  Release stable version
-  Add py38 stage to test matrix in travis

****************************
 v0.1.0-beta.4 (2019-05-28)
****************************

-  Add `--strict-optional` parameter - if not specified, all fields will
   be optional with default to None
-  Handle correctly default string values

****************************
 v0.1.0-beta.3 (2019-05-25)
****************************

-  Add `--async` flag to mark methods with `async` prefix
-  Add `-o` shortcut for `--output` option
-  Refactor codebase

****************************
 v0.1.0-beta.2 (2019-05-23)
****************************

-  Update badges link

****************************
 v0.1.0-beta.1 (2019-05-23)
****************************

-  First release on PyPI.
