Glossary
========

This glossary has informations about the data organized in pages.

Contour prime
-------------

The contour primes is the representation of a contour class that a
given contour belongs. For instance, a contour < 0 1 2 > belongs to
the same class of < 0 1 2 3 > and both are prime to < 0 1 >, the class
most contracted form.

Highest contour point
---------------------

A contour is a set of points enumbered from 0 to n - 1 - q, where n is
total number of contour points, and q is the number of non-adjacent
repeated contour points. The higher is the number of different contour
points, greater is the diversity of the contour. The contour higher
contour point of < 0 3 1 2 1 > is 3, meaning 4 different points. This
contour is more diversified than < 0 1 0 2 0 >, for instance.

Passing contour
---------------

The points of a contour can draw a zigzag, like in < 0 2 1 4 3 >, or
have "passing points", such as < 0 1 2 3 4 >. The "passing contour"
value defines if a contour has many "passing points". This value is
given by the quotient between the number of contour points in the
contour reduced by Bor window-3 algorithm and the total number of
points of the original contour, subtracted from 1. For instance, this
algorithm reduces < 0 2 3 1 4 > to < 0 3 1 4 >. The "passing contour"
value in this example is 1 - 4/5, or 0.2.

Oscillation index
-----------------

The oscillation index is related to direction changes. The higher is
this value, greater is the number of direction changes in a contour.


Contour first movement
----------------------

The movement between the first two contour points in a Music Unit. 1
for ascent, -1 for descent.

Contour last movement
---------------------

The movement between the last two contour points in a Music Unit. 1
for ascent, -1 for descent.
