// Draggable label+value widget for Processing
// Vertical drag to change value. Designed to embed inside nodes.

class ValueDragDisplay {
  // placement
  float x, y, w, h;

  // data
  float value = 0;
  float minV = 0;
  float maxV = 1;
  float step = 0;        // 0 means continuous (no stepping)
  int decimals = 2;      // display precision
  String label = "";
  String unit = "";      // e.g. "Hz", "%"

  // interaction
  boolean hovered = false;
  boolean dragging = false;
  float dragStartY;
  float valueAtPress;

  // tuning
  // how many px of vertical drag to traverse full range (default ~200px)
  float pixelsForFullRange = 200;

  // state
  boolean changedThisFrame = false;

  ValueDragDisplay(String label) {
    this.label = label;
    setBounds(0, 0, 120, 24);
  }

  // ----- API -----
  void setBounds(float x, float y, float w, float h) {
    this.x = x; this.y = y; this.w = w; this.h = h;
  }

  void setRange(float minV, float maxV) {
    if (minV == maxV) maxV += 1e-6f;
    this.minV = minV;
    this.maxV = maxV;
    value = constrain(value, minV, maxV);
  }

  void set(float v) {
    value = clampAndStep(v);
  }

  float get() { return value; }

  void setStep(float step) { 
    this.step = max(0, step);
    value = clampAndStep(value);
  }

  void setDecimals(int d) { decimals = max(0, d); }

  void setUnit(String u) { unit = (u == null) ? "" : u; }

  void setPixelsForFullRange(float px) { pixelsForFullRange = max(8, px); }

  void setLabel(String s) { label = s == null ? "" : s; }

  boolean isDragging() { return dragging; }

  boolean wasChangedThisFrame() { 
    boolean c = changedThisFrame; 
    changedThisFrame = false; 
    return c; 
  }

  // ----- Drawing -----
  void draw() {
    // hover detection uses current mouse pos; feel free to move to onMouseMoved if you have it
    hovered = hit(mouseX, mouseY);

    // background pill
    noStroke();
    int bg = dragging ? color(30, 30, 40) : (hovered ? color(38, 38, 50) : color(32, 32, 45));
    fill(bg);
    rect(x, y, w, h, 6);

    // outline
    stroke(255, hovered ? 60 : 25);
    noFill();
    rect(x, y, w, h, 6);

    // text
    fill(230);
    textAlign(LEFT, CENTER);
    textSize(12);
    float pad = 8;
    text(label, x + pad, y + h * 0.5);

    // value text (right aligned)
    String vStr = nf(value, 0, decimals) + (unit.length() > 0 ? " " + unit : "");
    textAlign(RIGHT, CENTER);
    fill(hovered || dragging ? 255 : 210);
    text(vStr, x + w - pad, y + h * 0.5);
  }

  // ----- Mouse contract (call from your graph/sketch) -----
  boolean onMousePressed(float mx, float my) {
    if (!hit(mx, my)) return false;
    dragging = true;
    dragStartY = my;
    valueAtPress = value;
    return true; // capture
  }

  void onMouseDragged(float mx, float my) {
    if (!dragging) return;
    // vertical drag: moving up increases value
    float dy = dragStartY - my;
    float range = (maxV - minV);
    float sensitivity = range / pixelsForFullRange;

    // modifiers: Shift = fine, Ctrl/Cmd = coarse
    boolean fine = keyPressed && (keyCode == SHIFT);
    boolean coarse = keyPressed && (keyCode == CONTROL || keyCode == 157); // 157 ~ CMD on mac

    if (fine) sensitivity *= 0.2f;
    if (coarse) sensitivity *= 4.0f;

    float newV = valueAtPress + dy * sensitivity;
    float clamped = clampAndStep(newV);
    if (clamped != value) {
      value = clamped;
      changedThisFrame = true;
    }
  }

  void onMouseReleased(float mx, float my) {
    dragging = false;
  }

  // ----- Internals -----
  boolean hit(float mx, float my) {
    return mx >= x && mx <= x + w && my >= y && my <= y + h;
  }

  float clampAndStep(float v) {
    float c = constrain(v, minV, maxV);
    if (step > 0) {
      c = round(c / step) * step;
      // keep inside bounds after rounding
      c = constrain(c, minV, maxV);
    }
    return c;
  }
}
