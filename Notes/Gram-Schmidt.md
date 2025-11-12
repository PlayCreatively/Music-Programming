---
created: 2025-07-11
---
## Build a basis from **three points** (your “align to a plane”)

Given three _selected_ vectors `p1, p2, p3` in **unit space**:

``` python
def basis_from_three_points(p1, p2, p3):
    # All are (D,) in unit space.
    u = p2 - p1
    u /= np.linalg.norm(u) + 1e-12
    w = p3 - p1
    # Gram–Schmidt: v = w - (u·w)u
    v = w - np.dot(u, w) * u
    v /= np.linalg.norm(v) + 1e-12
    # Pack as columns
    return np.stack([u, v], axis=1)   # (D,2)
```

Drop `B` into your state and re-project: `Y = project(X, mins, maxs, B)`.

> why are you using Gram-Schmidt? Can't you just construct 2 basic vectors from the 3 and then create the 3rd with cross product?

Right, in 3D you’d totally just use a cross product — that’s the natural way to get a perpendicular vector.  
But the key is: you’re not guaranteed to live in 3D anymore.

Let’s unpack why Gram–Schmidt shows up instead of a cross product.

---

### 1\. The cross product only exists in 3D (and 7D)

Mathematically, the cross product is a quirky creature.  
It’s defined as a binary operation that takes two 3D vectors and returns a third vector perpendicular to both — and whose magnitude equals the area of the parallelogram they span.

It works *only* in **three dimensions** (and in a special, exotic sense, also in 7D via octonions).  
There’s no general cross product in 4D, 5D, etc. — there’s no unique perpendicular direction, because the space of “perpendicular directions” has more than one degree of freedom.

So in higher dimensions, the concept of “orthogonal complement” replaces the cross product, and Gram–Schmidt is the general way to compute that.

---

### 2\. Gram–Schmidt is the generalized “make orthogonal” procedure

If you start from two nonparallel vectors $a, b$ in D-dimensional space:

- First, normalize $a$ → gives you **u**, the first axis.
- Then subtract the component of $b$ that’s along **u** → gives a vector perpendicular to **u**.
- Normalize that → gives **v**, the second axis.

Formally:

$$
u = \frac{a}{||a||}, \quad
v = \frac{b - (a·b)u}{||b - (a·b)u||}
$$

That’s the two-step Gram–Schmidt.  
If you were in 3D and you happened to compute `v = normalize(cross(a,b))`, you’d get the same direction up to sign — Gram–Schmidt is the higher-dimensional generalization of that idea.

---

### 3\. In your “three points define a plane” case

You’ve got three D-dimensional points:  
$P_1, P_2, P_3$

You can think of:

- $a = P_2 - P_1$
- $b = P_3 - P_1$

Then run Gram–Schmidt:

$$
u = normalize(a)
$$
 
$$
v = normalize(b - (u·b)u)
$$

Now **u** and **v** are two orthonormal vectors that define the plane spanned by those points, regardless of how many dimensions your data has.

---

### 4\. Why orthonormalization matters

If you skip the orthogonalization and just pick two difference vectors:

- They might not be perpendicular.
- When you project onto them, your 2D coordinates get skewed and scaled weirdly.
- As a result, when you drag points in the 2D view, the lifted points in high-D space don’t move in the expected plane.

Gram–Schmidt ensures `u` and `v` are orthonormal → projections and inverse projections behave predictably.

---

So, the cross product is a special case of Gram–Schmidt that only happens to produce a unique perpendicular vector in 3D.  
In high-dimensional space, you use Gram–Schmidt because there are infinitely many perpendicular directions — and you just need one consistent, orthonormal pair.

Would you like a short visualization of what goes wrong if you skip the orthogonalization and just take raw `a` and `b` as your basis?