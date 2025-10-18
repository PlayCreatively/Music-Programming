// -------------- Nodes, Ports, Connections ----------------

enum PortKind { INPUT, OUTPUT }

class Node {
  String title;
  float x, y, w, h;
  boolean dragging = false;
  PVector dragOff = new PVector();

  ArrayList<Port> inputs = new ArrayList<Port>();
  ArrayList<Port> outputs = new ArrayList<Port>();

  Node(String title, float x, float y) {
    this.title = title;
    this.x = x; this.y = y;
    this.w = 200; this.h = 120; // height grows with ports too
  }

  void addInput(String label, Listener listener) 
  {
    inputs.add(new Port(this, PortKind.INPUT, label, listener));
    autoSize();
  }

  void addInput(String label, Listener listener, float defaultValue) {
    addInput(label, listener);
    set(label, defaultValue);
  }

  void addOutput(String label, Listener listener) {
    outputs.add(new Port(this, PortKind.OUTPUT, label, listener));
    autoSize();
  }

  void set(String label, float value) 
  {
      for (Port p : inputs)
        if (p.label.equals(label)) 
        {
          p.set(value);
          return;
        }
  }

  void autoSize() {
    int rows = max(inputs.size(), outputs.size());
    float bodyRows = max(1, rows);
    h = 42 + 22 * bodyRows + 18;
    w = max(160, textWidth(title) + 60);
  }

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
    textSize(12);
    int rows = max(inputs.size(), outputs.size());
    for (int i = 0; i < rows; i++) {
      float py = y + 48 + i * 22;
      // input label
      if (i < inputs.size()) {
        Port in = inputs.get(i);
        in.slotIndex = i;
        PVector p = in.screenPos();
        fill(40, 160, 255);
        circle(p.x, p.y, 10);
        fill(20);
        textAlign(LEFT, CENTER);
        
        text(in.label + " : " + nf(in.value, 0, 0), x + 18, py);
      }
      // output label
      if (i < outputs.size()) {
        Port out = outputs.get(i);
        out.slotIndex = i;
        PVector p = out.screenPos();
        fill(255, 150, 60);
        circle(p.x, p.y, 10);
        fill(20);
        textAlign(RIGHT, CENTER);
        text(out.label, x + w - 18, py);
      }
    }
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

  void free() {
    synth.free();
  }

  void addInput(String label, float defaultValue) {
    addInput(label);
    set(label, defaultValue);
  }

  void addInput(String label) {
    inputs.add(new Port(this, PortKind.INPUT, label, new Listener() {
      public void set(float v) {
        synth.set(label, v);
      }
    }));
    autoSize();
  }
}

class SliderNode extends Node {
  float min, max;

  SliderNode(String title, float x, float y) {
    super(title, x, y);
    this.min = 0.0;
    this.max = 1.0;

    addOutput("value", new Listener() {
      public void set(float v) {
        // no-op
      }
    });
  }



  void setRange(float min, float max) {
    this.min = min;
    this.max = max;
  }

}

class Port implements Listener {
  Node node;
  PortKind kind;
  String label;
  float value = 0.0;
  int slotIndex = 0; // row within its side
  ArrayList<Port> connections = null;

  Port(Node n, PortKind k, String label) {
    this.node = n;
    this.kind = k;
    this.label = label;
    this.listener = null;
  }

  void set(float v) {
    value = v;
    if (listener != null) listener.set(v);
  }

  PVector screenPos() {
    float py = node.y + 48 + slotIndex * 22;
    float px = (kind == PortKind.INPUT) ? node.x + 10 : node.x + node.w - 10;
    return new PVector(px, py);
  }

  boolean hit(float mx, float my) {
    PVector p = screenPos();
    return dist(mx, my, p.x, p.y) <= 7;
  }
}

class Connection {
  Port out, in;
  Connection(Port o, Port i) { out = o; in = i; }

  void draw() {
    PVector a = out.screenPos();
    PVector b = in.screenPos();
    drawBezier(a, b);
  }

  // Distance from mouse to the curve (sampled polyline)
  float distanceTo(float mx, float my) {
    PVector a = out.screenPos();
    PVector b = in.screenPos();
    // Sample 24 points along the cubic
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

  PVector bezPoint(PVector a, PVector b, float t) {
    // Handles 100% of horizontal distance along X, fixed at endpoints' Y
    float dx = b.x - a.x;
    float h = 1.0 * dx;
    PVector c1 = new PVector(a.x + h, a.y);
    PVector c2 = new PVector(b.x - h, b.y);
    // Cubic Bézier interpolation
    float u = 1 - t;
    float bx = u*u*u*a.x + 3*u*u*t*c1.x + 3*u*t*t*c2.x + t*t*t*b.x;
    float by = u*u*u*a.y + 3*u*u*t*c1.y + 3*u*t*t*c2.y + t*t*t*b.y;
    return new PVector(bx, by);
  }
}
