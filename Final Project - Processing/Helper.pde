// --------------- Helpers -----------------

void drawBezier(PVector a, PVector b) {
  float dx = b.x - a.x;
  float h = 1.0 * dx; // 100% horizontal handles, as requested
  PVector c1 = new PVector(a.x + h, a.y);
  PVector c2 = new PVector(b.x - h, b.y);
  bezier(a.x, a.y, c1.x, c1.y, c2.x, c2.y, b.x, b.y);
}

// Point-line segment distance
float distToSegment(float px, float py, float x1, float y1, float x2, float y2) {
  float vx = x2 - x1, vy = y2 - y1;
  float wx = px - x1, wy = py - y1;
  float c1 = vx*wx + vy*wy;
  if (c1 <= 0) return dist(px, py, x1, y1);
  float c2 = vx*vx + vy*vy;
  if (c2 <= c1) return dist(px, py, x2, y2);
  float t = c1 / c2;
  float projx = x1 + t * vx, projy = y1 + t * vy;
  return dist(px, py, projx, projy);
}
