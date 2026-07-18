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


Ignore violations for blocks
----------------------------

You can also suppress violations across a block of lines:

.. code-block:: text

   # dotenv:disable[IncorrectNameViolation, SpacedNameViolation]
   # This and the following lines are not checked for ``SpacedNameViolation`` and ``IncorrectNameViolation``
   KEY=VALUE
   SOME_KEY=VALUE

If you need to ignore all violations, you can use the ``# dotenv:disable`` comment:

.. code-block:: text

   # dotenv:disable
   # This and the following lines are not checked for all violations
   KEY=VALUE
   SOME_KEY=VALUE

Then if you need to enable all violations, you can use the ``# dotenv:enable`` comment:

.. code-block:: text

   # dotenv:disable
   # This and the following lines are not checked for all violations
   KEY=VALUE
   SOME_KEY=VALUE
   # dotenv:enable
   # This and the following lines are checked for all violations
   DJANGO_ENV=VALUE
   API_KEY=VALUE

If you need to ignore some lines, you can use the ``# dotenv:ignore`` comment:

.. code-block:: text

   # dotenv:enable
   KEY1=VALUE
   KEY2=VALUE
   # dotenv:ignore[IncorrectNameViolation]
   KEY3=VALUE

You can also enable only specific violations:

.. code-block:: text

   # dotenv:disable
   KEY=VALUE
   SOME_KEY=VALUE
   # dotenv:enable[IncorrectNameViolation]
   SOME_OTHER_KEY=VALUE
