// -------------- Nodes, Ports, Connections ----------------

enum PortKind { INPUT, OUTPUT }

class Node {
  String title;
  float x, y, w, h;
  boolean dragging = false;
  PVector dragOff = new PVector();

  ArrayList<PortInInteractive> inputs = new ArrayList<PortInInteractive>();
  ArrayList<PortOut> outputs = new ArrayList<PortOut>();

  Node(String title, float x, float y) {
    this.title = title;
    this.x = x; this.y = y;
    this.w = 200; this.h = 120; // height grows with ports too
  }

  PortInInteractive addInput(String label) 
  {
    PortInInteractive port = new PortInInteractive(this, label);
    port.slotIndex = inputs.size();
    inputs.add(port);
    autoSize();
    return port;
  }

  PortInInteractive addInput(String label, float defaultValue) {
    PortInInteractive port = addInput(label);
    port.set(defaultValue);
    return port;
  }

  PortOut addOutput(String label) {
    PortOut port = new PortOut(this, label);
    port.slotIndex = outputs.size();
    outputs.add(port);
    autoSize();
    return port;
  }

  PortIn set(String label, float value) 
  {
    for (PortIn p : inputs)
      if (p.label.equals(label)) 
      {
        p.set(value);
        return p;
      }
    return null;
  }

  void autoSize() {
    int rows = max(inputs.size(), outputs.size());
    float bodyRows = max(1, rows);
    h = 42 + 22 * bodyRows + 18;
    w = max(160, textWidth(title) + 60);
  }

  void update() {
    // override in subclasses
  }

  boolean onMousePressed(float mx, float my, Graph g) 
  {
    for( PortInInteractive p : inputs) 
      if (p.onMousePressed(mx, my)) 
        return true; // captured
    return false;
  }
  void onMouseDragged(float mx, float my)
  {
    for( PortInInteractive p : inputs) 
      p.onMouseDragged(mx, my);
  }
  void onMouseReleased(float mx, float my)
  {
    for( PortInInteractive p : inputs) 
      p.onMouseReleased(mx, my);
  }

  void onKeyPressed(char k, int keyCode) {}

  void beginDrag(float mx, float my) {
    dragging = true;
    dragOff.set(mx - x, my - y);
  }
  void drag(float mx, float my) {
    if (dragging) {
      x = mx - dragOff.x;
      y = my - dragOff.y;
    }
  }
  void endDrag() { dragging = false; }

  boolean hitTitle(float mx, float my) {
    return (mx >= x && mx <= x+w && my >= y && my <= y+32);
  }

  Port portAt(float mx, float my) {
    for (Port p : inputs)  if (p.hit(mx, my))  return p;
    for (Port p : outputs) if (p.hit(mx, my)) return p;
    return null;
  }

  void draw() {
    // Body
    noStroke();
    // drop shadow
    fill(0, 20);
    rect(x+3, y+4, w, h, 16);
    // panel
    fill(255);
    rect(x, y, w, h, 16);

    // Title bar
    fill(30);
    rect(x, y, w, 32, 16, 16, 0, 0);
    fill(255);
    textAlign(LEFT, CENTER);
    textSize(13);
    text(title, x+10, y+16);

    // Port rows
    int yOff = 2; // fine-tune port vertical alignment
    textSize(12);
    for (int i = 0; i < outputs.size(); i++) {
      float py = y + 48 + i * 22;
      // output label
      Port out = outputs.get(i);
      out.slotIndex = i;
      PVector p = out.screenPos();
      fill(255, 150, 60);
      circle(p.x, p.y + yOff, 10);
      fill(20);
      textAlign(RIGHT, CENTER);
      text(out.label, x + w - 18, py);
    }
    for (int i = 0; i < inputs.size(); i++)
      inputs.get(i).draw();

    // border last
    noFill();
    stroke(0, 60);
    strokeWeight(1.5);
    rect(x, y, w, h, 16);
  }
}

interface Listener {
  void set(float x);
}

class SynthNode extends Node {
  Synth synth;

  SynthNode(String title, float x, float y) {
    super(title, x, y);
    this.synth = new Synth(title);
    synth.create();
  }

  PortInInteractive addInput(String label, float defaultValue) {
    PortInInteractive port = super.addInput(label, defaultValue);
    synth.set(label, defaultValue);
    port.listener = (float value) -> {
      synth.set(label, value);
    };
    return port;
  }

  void free() {
    synth.free();
  }
}

class SliderNode extends Node {
  float min = 0.0;
  float max = 1.0;

  // current value the slider holds (and publishes to outputs[0])
  float value = 0.5;

  // interaction
  boolean draggingKnob = false;
  float sliderPadding = 20;     // left/right space
  float knobHalfW = 6;          // half width of knob rect
  float knobH = 16;
  float sliderYOffset = 30;     // distance from bottom to slider line

  SliderNode(String title, float x, float y) {
    super(title, x, y);
    addOutput("");
  }

  void setRange(float min, float max) {
    if (min == max) max = min + 1e-6f;
    this.min = min;
    this.max = max;
    value = constrain(value, min, max);
  }

  // Helpers ---------------------------------------------------------
  float sliderY() { return y + h - sliderYOffset; }
  float trackLeft() { return x + sliderPadding; }
  float trackRight() { return x + w - sliderPadding; }
  float trackWidth() { return trackRight() - trackLeft(); }

  float valueToX(float v) {
    float t = (v - min) / (max - min);
    return trackLeft() + constrain(t, 0, 1) * trackWidth();
  }

  float xToValue(float px) {
    float t = (px - trackLeft()) / max(1e-6f, trackWidth());
    return constrain(lerp(min, max, constrain(t, 0, 1)), min, max);
  }

  boolean knobHit(float mx, float my) {
    float kx = valueToX(value);
    float ky = sliderY();
    return (mx >= kx - knobHalfW && mx <= kx + knobHalfW &&
            my >= ky - knobH*0.5f && my <= ky + knobH*0.5f);
  }

  boolean trackHit(float mx, float my) {
    float ky = sliderY();
    // generous 8px hit thickness around the line to allow clicking track to jump
    return (mx >= trackLeft() && mx <= trackRight() &&
            abs(my - ky) <= 8);
  }

  // Node lifecycle ---------------------------------------------------
  void update() {
    // publish held value each frame
    outputs.get(0).set(value);
  }

  void draw() {
    super.draw();

    // track
    float ky = sliderY();
    stroke(0, 60);
    strokeWeight(1.5);
    line(trackLeft(), ky, trackRight(), ky);

    // knob
    noStroke();
    fill(100, 200, 100);
    float kx = valueToX(value);
    rect(kx - knobHalfW, ky - knobH*0.5f, knobHalfW*2, knobH, 4);

    // value text
    fill(20);
    textAlign(CENTER, TOP);
    text(nf(value, 0, 2), kx, ky + knobH*0.5f);

  }

  // Scalable mouse contract (see section 2):
  // Return true on press if we capture the mouse.
  boolean onMousePressed(float mx, float my) {
    // prefer knob; fall back to clicking track to jump-to and capture
    if (knobHit(mx, my) || trackHit(mx, my)) {
      value = xToValue(mx);      // jump-to on click anywhere on track
      draggingKnob = true;
      return true;
    }
    return false;
  }

  void onMouseDragged(float mx, float my) {
    if (draggingKnob) {
      value = xToValue(mx);
    }
  }

  void onMouseReleased(float mx, float my) {
    draggingKnob = false;
  }
}



class Port {
  Node node;
  PortKind kind;
  String label;
  int slotIndex = 0; // row within its side

  Port(Node n, PortKind k, String label) {
    this.node = n;
    this.kind = k;
    this.label = label;
  }
  
  boolean hit(float mx, float my) {
    PVector p = screenPos();
    return dist(mx, my, p.x, p.y) <= 7;
  }

  boolean hitLabel(float mx, float my) {
    float tx, ty;
    if (kind == PortKind.INPUT) {
      tx = node.x + 18;
      ty = node.y + 48 + slotIndex * 22;
      return (mx >= tx && mx <= tx + textWidth(label) + 40 &&
              my >= ty - 8 && my <= ty + 8);
    } else {
      tx = node.x + node.w - 18 - textWidth(label);
      ty = node.y + 48 + slotIndex * 22;
      return (mx >= tx - 40 && mx <= tx + textWidth(label) &&
              my >= ty - 8 && my <= ty + 8);
    }
  }

  PVector screenPos() {
    float py = node.y + 48 + slotIndex * 22;
    float px = (kind == PortKind.INPUT) ? node.x + 10 : node.x + node.w - 10;
    return new PVector(px, py);
  }
}

class PortIn extends Port
{
  float value = 0.0;
  Listener listener = null;
  boolean connected = false;

  PortIn(Node n, String label) { super(n, PortKind.INPUT, label); }

  void set(float v) {
    value = v;
    if (listener != null)
      listener.set(v);
  }
}

class PortInInteractive extends PortIn
{
  PortInInteractive(Node n, String label) { super(n, label); }
  float minV = 0;
  float maxV = 1;
  float step = 0;        // 0 means continuous (no stepping)
  int decimals = 2;      // display precision
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

  void setRange(float minV, float maxV) {
    if (minV == maxV) maxV += 1e-6f;
    this.minV = minV;
    this.maxV = maxV;
    value = constrain(value, minV, maxV);
  }

  void set(float v) {
    value = clampAndStep(v);
    if (listener != null) listener.set(value);
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
    hovered = hitLabel(worldMouseX, worldMouseY);

    int yOff = 2; // fine-tune port vertical alignment
    textSize(12);
    float py = node.y + 48 + slotIndex * 22;
    PVector p = screenPos();
    fill(40, 160, 255);
    circle(p.x, p.y + yOff, 10);
    textAlign(LEFT, CENTER);
    String vStr = nf(value, 0, decimals) + (unit.length() > 0 ? " " + unit : "");
    if(hovered || dragging) {fill(255, 150, 60); cursor(loadImage("vertical-resize.png")); }
    else                    fill(20);
    text(label + " : " + vStr, node.x + 18, py);
  }

  // ----- Mouse contract (call from your graph/sketch) -----
  boolean onMousePressed(float mx, float my) {
    if (!hitLabel(mx, my)) return false;
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
      if (listener != null) listener.set(value);
    }
  }

  void onMouseReleased(float mx, float my) {
    dragging = false;
  }

  // ----- Internals -----

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

class PortOut extends Port
{
  ArrayList<PortIn> connections = new ArrayList<PortIn>();

  PortOut(Node n, String label) { super(n, PortKind.OUTPUT, label); }

  void set(float v) {
    for (PortIn in : connections)
      in.set(v);
  }
}

class Connection {
  PortOut out;
  PortIn in;

  Connection(PortOut out, PortIn in) {
    this.out = out;
    this.in = in;

    in.connected = true; 
    out.connections.add(in);
  }

  void disconnect() {
    in.connected = false;
    out.connections.remove(in);
  }

  void draw() {
    drawBezier(out.screenPos(), in.screenPos());
  }

  // Distance from mouse to the curve (sampled polyline)
  float distanceTo(float mx, float my) {
    // Sample 24 points along the cubic
    PVector a = out .screenPos();
    PVector b = in  .screenPos();
    
    float best = 10e9;
    PVector prev = bezPoint(a, b, 0);
    for (int i = 1; i <= 24; i++) {
      float t = i/24.0;
      PVector cur = bezPoint(a, b, t);
      float d = distToSegment(mx, my, prev.x, prev.y, cur.x, cur.y);
        if (d < best) best = d;
          prev = cur;
      }
    return best;
  }
}