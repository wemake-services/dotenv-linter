Github Actions
--------------

.. image:: https://github.com/wemake-services/dotenv-linter/workflows/dotenv/badge.svg
  :alt: Github Action badge
  :target: https://github.com/wemake-services/dotenv-linter/actions

Good news: we ship pre-built Github Action with this project.

You can use it from the `Github Marketplace <https://github.com/marketplace/actions/dotenv-linter>`_:

.. code:: yaml

  - name: dotenv-linter
    uses: wemake-services/dotenv-linter

You can also specify any version
starting from ``0.1.5`` instead of the default ``latest`` tag.

Inputs
~~~~~~

.. rubric:: reporter

We support three reporting options:

- ``terminal`` (default one) when we just dump the output into Action's logs.
  Is the easiest one to setup, that's why we use it by default
- ``github-pr-review`` (recommended) when we use `inline comments <https://github.com/reviewdog/reviewdog#reporter-github-pullrequest-review-comment--reportergithub-pr-review>`_ inside code reviews
- ``github-pr-check`` when we use `Github Checks <https://github.com/reviewdog/reviewdog#reporter-github-checks--reportergithub-pr-check>`_ for the output

Take a note that ``github-pr-review`` and ``github-pr-check`` requires
``GITHUB_TOKEN`` environment variable to be set.

For example, that's how ``github-pr-reviews`` can be set up:

.. code:: yaml

  - name: dotenv-linter
    uses: wemake-services/dotenv-linter
    with:
      reporter: 'github-pr-review'
    env:
      GITHUB_TOKEN: ${{ secrets.github_token }}

.. rubric:: options

We also support custom CLI ``options`` to be specified,
they are exactly match anything
that can be provided to ``dotenv-linter`` itself:

.. code:: yaml

  - name: dotenv-linter
    uses: wemake-services/dotenv-linter
    with:
      options: './conf/.env ./conf/.env.docker'

Outputs
~~~~~~~

We also support ``outputs`` from the spec, so you can later
pass the output of ``dotenv-linter`` to somewhere else.

.. code:: yaml

  - name: dotenv-linter
    uses: wemake-services/dotenv-linter
  - name: Custom Action
    runs: echo "{{ steps.dotenv-linter.outputs.output }}"
