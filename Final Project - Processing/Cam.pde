// ------------------------------------------------------------
// Camera2D: pan with RMB/Middle or hold Space + LMB; zoom with wheel
// ------------------------------------------------------------
class Camera2D {
  PVector pos = new PVector(0, 0); // world-space center
  float zoom = 1.0;
  float minZoom = 0.25, maxZoom = 6.0;

  boolean panning = false;
  PVector lastMouse = new PVector();

  void apply() {
    // Center screen, scale, then translate world so that pos is at center
    translate(width*0.5, height*0.5);
    scale(zoom);
    translate(-pos.x, -pos.y);
  }

  // Convert a screen pixel to world coords
  PVector screenToWorld(float sx, float sy) {
    float x = (sx - width*0.5) / zoom + pos.x;
    float y = (sy - height*0.5) / zoom + pos.y;
    return new PVector(x, y);
  }

  // Convert a world point to screen pixels (handy for hit-tests)
  PVector worldToScreen(float wx, float wy) {
    float x = (wx - pos.x) * zoom + width*0.5;
    float y = (wy - pos.y) * zoom + height*0.5;
    return new PVector(x, y);
  }

  void mousePressed(int button, float mx, float my) {
    boolean spacePanning = keyPressed && key == ' ';
    boolean grabPan = (button == RIGHT) || (button == CENTER) || (spacePanning && button == LEFT);
    if (grabPan) {
      panning = true;
      lastMouse.set(mx, my);
    }
  }

  void mouseDragged(float mx, float my) {
    if (!panning) return;
    // Move camera by the inverse of mouse delta in world units
    float dx = (mx - lastMouse.x) / zoom;
    float dy = (my - lastMouse.y) / zoom;
    pos.sub(dx, dy);
    lastMouse.set(mx, my);
  }

  void mouseReleased() {
    panning = false;
  }

  void mouseWheel(processing.event.MouseEvent e) {
    float steps = e.getCount() * .25; // +1 wheel down, -1 wheel up (usually)
    float newZoom = constrain(zoom -steps, minZoom, maxZoom);

    // Zoom to cursor: keep the world point under the mouse fixed on screen
    PVector before = screenToWorld(mouseX, mouseY);
    zoom = newZoom;
    PVector after = screenToWorld(mouseX, mouseY);
    PVector delta = PVector.sub(before, after);
    pos.add(delta);
  }
}