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

def point_add(p1, p2):
   if p1 is None: return p2
   if p2 is None: return p1

   x1, y1 = p1
   x2, y2 = p2

   if x1 == x2 and y1 == y2:
      num = (3 * x1**2 + A)
      den = (2 * y1)
   else:
      num = (y2 - y1)
      den = (x2 - x1)

   s = (num * mod_invert(den, P_MOD)) % P_MOD

   qx = (s**2 - x1 - x2) % P_MOD
   qy = (s * (x1 - qx) - y1) % P_MOD

   return (qx, qy)

def double_add(k, point):
   result = None
   current = point

   while k > 0:
      if k % 2 == 1:
         result = point_add(result, current)

      current = point_add(current, current)
      k //= 2

   return result
