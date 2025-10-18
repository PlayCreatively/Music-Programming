class Graph {
  ArrayList<Node> nodes = new ArrayList<Node>();
  ArrayList<Connection> conns = new ArrayList<Connection>();

  Port draggingFrom = null; // must be OUTPUT
  PVector dragPos = new PVector();

  Connection hoverConn = null;

  void add(Node n) { nodes.add(n); }

  void update() {
    // Update z-order dragging: bring active nodes to front (done in press)
    // Track hover connection
    hoverConn = null;
    // Check nearest connection within threshold
    float bestD = 10e9;
    for (Connection c : conns) {
      float d = c.distanceTo(worldMouseX, worldMouseY);
      if (d < 12 && d < bestD) { bestD = d; hoverConn = c; }
    }
  }

  void draw() {
    // Connections first (under nodes)
    stroke(40);
    strokeWeight(2.5);
    noFill();
    for (Connection c : conns) {
      if (c == hoverConn) {
        strokeWeight(3.5);
        stroke(20, 140, 255);
      } else {
        strokeWeight(2.5);
        stroke(40, 120);
      }
      c.draw();
    }

    // Pending wire
    if (draggingFrom != null) {
      stroke(20, 140, 255);
      strokeWeight(3);
      noFill();
	  PVector mw = mouseWorld(); 
      drawBezier(draggingFrom.screenPos(), new PVector(mw.x, mw.y));
      noStroke();
      fill(20, 140, 255, 180);
      ellipse(mw.x, mw.y, 8, 8);
    }

    // Nodes on top
    for (Node n : nodes) n.draw();
  }

  void mousePressed(float mx, float my) {
    // Try ports first (outputs start a wire; inputs finish one if dragging)
    Port p = findPortAt(mx, my);
    if (p != null) {
      if (p.kind == PortKind.OUTPUT) {
        draggingFrom = p;
        dragPos.set(mx, my);
        return;
      } else if (p.kind == PortKind.INPUT && draggingFrom != null) {
        tryConnect(draggingFrom, p);
        draggingFrom = null;
        return;
      }
    }

    // Start dragging a node by title bar
    for (int i = nodes.size()-1; i >= 0; --i) { // top-most first
      Node n = nodes.get(i);
      if (n.hitTitle(mx, my)) {
        n.beginDrag(mx, my);
        // bring to front
        nodes.remove(i);
        nodes.add(n);
        return;
      }
    }
  }

  void mouseDragged(float mx, float my) {
    for (Node n : nodes) n.drag(mx, my);
    dragPos.set(mx, my);
  }

  void mouseReleased(float mx, float my) {
    // Release node drags
    for (Node n : nodes) n.endDrag();

    // If we were dragging a wire and released over an input, connect
    if (draggingFrom != null) {
      Port p = findPortAt(mx, my);
      if (p != null && p.kind == PortKind.INPUT) {
        tryConnect(draggingFrom, p);
      }
      draggingFrom = null;
    }
  }

  void keyPressed(char k, int keyCode) {
    if ((keyCode == DELETE || keyCode == BACKSPACE) && hoverConn != null) {
      conns.remove(hoverConn);
      hoverConn = null;
    }
    if (keyCode == ESC) { // cancel pending wire without quitting sketch
      key = 0;
      draggingFrom = null;
    }
  }

  void tryConnect(Port out, Port in) {
    if (out == null || in == null) return;
    if (out.kind != PortKind.OUTPUT || in.kind != PortKind.INPUT) return;
    if (out.node == in.node) return; // no self-looping a single node side
    // One connection per input: remove existing into 'in'
    for (int i = conns.size()-1; i >= 0; --i) {
      if (conns.get(i).in == in) conns.remove(i);
    }
    conns.add(new Connection(out, in));
  }

  Port findPortAt(float mx, float my) {
    for (int i = nodes.size()-1; i >= 0; --i) {
      Node n = nodes.get(i);
      Port p = n.portAt(mx, my);
      if (p != null) return p;
    }
    return null;
  }
}
