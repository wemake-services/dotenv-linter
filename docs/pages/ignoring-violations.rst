Ignoring violations
===================

You can suppress specific violations directly in your ``.env`` file
using special ignore comments.

Syntax
------

Add a comment above the line you want to ignore:

.. code-block:: text

   # dotenv:ignore[ViolationName]
   KEY=VALUE

You can also ignore multiple violations at once:

.. code-block:: text

   # dotenv:ignore[IncorrectNameViolation, SpacedValueViolation]
   KEY=VALUE

And you can stack multiple ignore comments:

.. code-block:: text

   # dotenv:ignore[IncorrectNameViolation]
   # dotenv:ignore[SpacedValueViolation]
   KEY=VALUE

Example
-------

.. code-block:: text

   # dotenv:ignore[IncorrectNameViolation]
   wemake=DOTENV

   # dotenv:ignore[UnreadableNameViolation]
   MY_1I_VAR=VALUE

   # dotenv:ignore[SpacedAssignViolation]
   KEY =

   # dotenv:ignore[ReservedNameViolation]
   DJANGO_ENV=1

   # dotenv:ignore[DuplicateNameViolation]
   KEY=VALUE
   # dotenv:ignore[DuplicateNameViolation]
   KEY=VALUE