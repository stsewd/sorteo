Sorteo
======

Script usado para realizar sorteos usando los asistentes de un evento de `Meetup <https://www.meetup.com/>`__.

.. note::

   Uso enfocado en la comunidad de `Python Ecuador <https://pythonecuador.org/>`__.
   Pero es extensible para ser usado de manera general.

.. contents:: Contenidos
   :local:

Uso
---

.. argparse::
   :module: sorteo.main
   :func: get_argparser
   :prog: sorteo

   evento
       Si sólo es dado el id del evento,
       por defecto se buscará eventos de `Python Ecuador <https://www.meetup.com/es/python-ecuador/>`__


Ejemplos
--------

Para hacer un sorteo de `este evento <https://www.meetup.com/es/python-ecuador/events/254871518/>`__
con 3 ganadores:

.. code:: bash
  
  sorteo -n 3 https://www.meetup.com/es/python-ecuador/events/254871518/

o

.. code:: bash

  sorteo -n 3 254871518

Contribuir
----------

- Haz un fork
- Crea una nueva rama
- Escribe tus cambios y agrega tests
- Envía un Pull Requests

Índices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
