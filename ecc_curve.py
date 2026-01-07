"""
Gestion des opérations mathématiques sur la courbe elliptique.
Courbe : Y^2 = X^3 + 35X + 3 (modulo 101)
Point de départ : P(2, 9)
"""

A = 35
B = 3
P_MOD = 101

P = (2, 9)

def mod_invert(a, p):
   return pow(a, -1, p)

def point_add(P1, P2):
   if P1 is None:
      return P2
   if P2 is None:
      return P1

   x1, y1 = P1
   x2, y2 = P2

   if x1 == x2 and (y1 + y2) % P_MOD == 0:
      return None

   if P1 == P2:
      m = (3 * x1 * x1 + A) * mod_invert(2 * y1, P_MOD)
   else:
      m = (y2 - y1) * mod_invert(x2 - x1, P_MOD)

   m %= P_MOD

   x3 = (m * m - x1 - x2) % P_MOD
   y3 = (m * (x1 - x3) - y1) % P_MOD

   return (x3, y3)


def double_add(k, point):
   result = None
   current = point

   while k > 0:
      if k % 2 == 1:
         result = point_add(result, current)

      current = point_add(current, current)
      k //= 2

   return result
