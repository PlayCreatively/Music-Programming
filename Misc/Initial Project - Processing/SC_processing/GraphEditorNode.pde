import groovy.lang.Binding;
import groovy.lang.Closure;
import groovy.lang.GroovyShell;

interface FGet { float get(); }
interface FSet { void set(float v); }

class GraphFunctionNode extends Node {
  // --- UI layout ---
  float minW = 280, minH = 240;
  float pad = 10;
  float codeH = 24;
  float controlsH = 22;
  float footerH = 18;
  float knobR = 6;

  // --- function editing ---
  String code = "V(lerp(-1,1,t), 0)"; // default: line
  boolean editing = false;
  int caret = code.length();
  long lastEditMs = 0;
  boolean dirty = true;              // needs (re)compile

  // --- groovy eval ---
  GroovyShell shell = new GroovyShell(new Binding());
  Closure<?> fn = null;
  String err = null;

  // --- domains (editable) ---
  float tMin = 0, tMax = 1;
  float xMin = -1, xMax = 1;
  float yMin = -1, yMax = 1;

  // --- plot sampling ---
  int samples = 160;
  PVector[] pts = new PVector[samples];   // screen-space points
  float[]    ts = new float[samples];     // param per sample
  boolean showGrid = false;

  // --- knob & IO ---
  boolean draggingKnob = false;
  float tLocal = 0.25;    // current local t (when not driven by input)
  float tActive = 0.25;   // actual t in use (input or local)
  float tLastEmitted = Float.NaN;

  PortIn  inT;
  PortOut outX, outY, outT;

  GraphFunctionNode(String title, float x, float y) {
    super(title, x, y);
    inT  = addInput("t");           // don't set default (avoid listener fire)
    outX = addOutput("x");
    outY = addOutput("y");
    outT = addOutput("t");

    // react to t input
    inT.listener = (float v) -> {
      tLocal = v;
      // nothing else to do; we'll read inT.connected to disable knob
    };

    // init arrays
    for (int i=0;i<samples;i++){ pts[i]=new PVector(); ts[i]=0; }
  }

  // ---------- lifecycle ----------
  void update() {
    // recompile on idle (200ms after last edit)
    if (dirty && millis() - lastEditMs > 200) {
      compileFn();
      resample();
      dirty = false;
    }

    // choose active t
    boolean external = inT.connected;            // reliable (single-conn graph)
    tActive = external ? tLocal : tLocal;        // both store in tLocal, but knob is disabled when external

    // evaluate & emit on change
    if (fn != null) {
      PVector p = evalSafe(tActive);
      if (p != null && tActive != tLastEmitted) {
        outX.set(p.x);
        outY.set(p.y);
        outT.set(tActive);
        tLastEmitted = tActive;
      }
    }
  }

  void draw() {
    // ensure size for plot; Node.autoSize() already set base by ports
    w = max(w, minW);
    h = max(h, minH);

    // panel & title / ports
    super.draw();

    // regions
    float cx = x + pad, cy = y + 36;
    float codeY = cy;
    float controlsY = codeY + codeH + 6;
    float plotY = controlsY + controlsH + 6;
    float plotH = h - (plotY - y) - footerH - 6;
    float plotX = x + pad;
    float plotW = w - 2*pad;

    // code field
    drawCodeField(plotX, codeY, plotW, codeH);

    // controls: presets | grid toggle | ranges (tiny drags)
    drawControls(plotX, controlsY, plotW, controlsH);

    // plot
    drawPlot(plotX, plotY, plotW, plotH);

    // footer error
    if (err != null) {
      fill(200,40,40);
      textAlign(LEFT, CENTER);
      textSize(11);
      text(err, plotX, y + h - footerH*0.5);
    }
  }

  // ---------- code field ----------
  void drawCodeField(float rx, float ry, float rw, float rh) {
    // bg
    stroke(60);
    fill(editing ? color(35,35,50) : color(30,30,42));
    rect(rx, ry, rw, rh, 6);
    // text
    fill(230);
    textAlign(LEFT, CENTER);
    textSize(12);
    float padx=8;
    String left = code.substring(0, min(caret, code.length()));
    String right= code.substring(min(caret, code.length()));
    String shown = left + right; // simple; PDE text lacks caret render
    text(shown, rx+padx, ry+rh*0.5);
    // caret (simple)
    if (editing && (millis()/500)%2==0) {
      float cw = textWidth(left);
      stroke(255);
      line(rx+padx+cw, ry+4, rx+padx+cw, ry+rh-4);
    }
  }

  // ---------- controls ----------
  void drawControls(float rx, float ry, float rw, float rh) {
    // background
    noStroke(); fill(245); rect(rx, ry, rw, rh, 6);

    textAlign(LEFT, CENTER); fill(20); textSize(11);
    float xcur = rx + 8;

    // presets button
    float bx = xcur, bw = 64;
    drawButton(bx, ry+3, bw, rh-6, "Presets");
    xcur += bw + 8;

    // grid toggle
    float gx = xcur, gw = 54;
    drawToggle(gx, ry+3, gw, rh-6, "Grid", showGrid);
    xcur += gw + 10;

    // small drags: t, x, y ranges
    xcur += drawRangeDrag(xcur, ry, "t", ()->tMin, (v)->{ tMin=v; if (tMin>tMax) tMin=tMax-1e-6f; dirty=true; }, ()->tMax, (v)->{ tMax=v; if (tMax<tMin) tMax=tMin+1e-6f; dirty=true; });
    xcur += drawRangeDrag(xcur, ry, "x", ()->xMin, (v)->{ xMin=v; if (xMin>xMax) xMin=xMax-1e-6f; }, ()->xMax, (v)->{ xMax=v; if (xMax<xMin) xMax=xMin+1e-6f; });
    xcur += drawRangeDrag(xcur, ry, "y", ()->yMin, (v)->{ yMin=v; if (yMin>yMax) yMin=yMax-1e-6f; }, ()->yMax, (v)->{ yMax=v; if (yMax<yMin) yMax=yMin+1e-6f; });
  }

  // tiny widgets
  void drawButton(float x, float y, float w, float h, String label) {
    stroke(180); fill(255); rect(x, y, w, h, 5);
    fill(20); textAlign(CENTER,CENTER); textSize(11); text(label, x+w*0.5, y+h*0.5);
  }
  void drawToggle(float x, float y, float w, float h, String label, boolean on) {
    stroke(180); fill(on? color(220,255,220):255); rect(x, y, w, h, 5);
    fill(on? color(0,120,0):20); textAlign(CENTER,CENTER); textSize(11); text(label, x+w*0.5, y+h*0.5);
  }

  // "range: a..b" widget drawn inline: returns consumed width
  float drawRangeDrag(float x0, float y0, String name, FGet aGet, FSet aSet, FGet bGet, FSet bSet) {
    String s = name + ": [" + nf(aGet.get(),0,2) + " .. " + nf(bGet.get(),0,2) + "]";
    float wtxt = textWidth(s)+14;
    stroke(180); fill(255); rect(x0, y0+3, wtxt, 16, 4);
    fill(20); textAlign(LEFT, CENTER); textSize(11); text(s, x0+6, y0+11);
    return wtxt + 8;
  }

  // ---------- plot & knob ----------
  void drawPlot(float rx, float ry, float rw, float rh) {
    // bg
    stroke(200); fill(252); rect(rx, ry, rw, rh, 8);

    // grid & axes
    if (showGrid) {
      stroke(235); for (int i=1;i<10;i++) {
        float xi = rx + i*rw/10f; line(xi, ry, xi, ry+rh);
        float yi = ry + i*rh/10f; line(rx, yi, rx+rw, yi);
      }
    }
    // axes at 0
    float x0 = mapXtoPx(0, rx, rw);
    float y0 = mapYtoPx(0, ry, rh);
    stroke(180); line(x0, ry, x0, ry+rh); line(rx, y0, rx+rw, y0);

    // resample if needed (domain changed or function compiled)
    // (cheap guard: if first point is at 0,0 and fn exists, resample)
    if (fn != null && (pts[0].x == 0 && pts[0].y == 0 && ts[0]==0)) resample();

    // curve
    if (fn != null && err == null) {
      noFill(); stroke(30,140,220); strokeWeight(1.5);
      beginShape();
      for (int i=0;i<samples;i++) vertex(pts[i].x, pts[i].y);
      endShape();
    }

    // knob
    boolean external = inT.connected;
    PVector kp = pointAtT(tLocal);
    noStroke();
    if (external) { fill(160); } else { fill(30,140,220); }
    circle(kp.x, kp.y, knobR*2);
    stroke(255); noFill(); circle(kp.x, kp.y, knobR*2); // outline for contrast
  }

  // ---------- sampling & math ----------
  void resample() {
    if (fn == null) return;
    for (int i=0;i<samples;i++) {
      float tt = lerp(tMin, tMax, i/(samples-1.0));
      PVector p = evalSafe(tt);
      ts[i] = tt;
      if (p == null) { pts[i].set(0,0); continue; }
      pts[i].set(mapXtoPx(p.x, x+pad, w-2*pad), mapYtoPx(p.y, y+36+codeH+6+controlsH+6, h - (36+codeH+6+controlsH+6) - footerH - 6));
    }
  }

  PVector evalSafe(float t) {
    try {
      Object r = fn.call(t);
      if (r instanceof PVector) return (PVector)r;
      err = "Function must return PVector"; return null;
    } catch (Exception ex) {
      err = ex.getMessage();
      return null;
    }
  }

  float mapXtoPx(float xval, float rx, float rw){ return rx + (xval - xMin) / (xMax - xMin) * rw; }
  float mapYtoPx(float yval, float ry, float rh){ return ry + (1 - (yval - yMin) / (yMax - yMin)) * rh; }

  // find nearest param to pixel point
  float nearestT(float mx, float my) {
    float bestD = 1e9, bestT = tMin;
    for (int i=0;i<samples-1;i++) {
      PVector a = pts[i], b = pts[i+1];
      float u = proj01(mx, my, a.x, a.y, b.x, b.y);
      float px = lerp(a.x, b.x, u), py = lerp(a.y, b.y, u);
      float d2 = sq(mx-px) + sq(my-py);
      if (d2 < bestD) { bestD = d2; bestT = lerp(ts[i], ts[i+1], u); }
    }
    return bestT;
  }

  float proj01(float px,float py,float x1,float y1,float x2,float y2){
    float vx=x2-x1, vy=y2-y1;
    float wx=px-x1, wy=py-y1;
    float l2 = vx*vx+vy*vy; if (l2<=1e-9) return 0;
    float u = (wx*vx+wy*vy)/l2;
    return constrain(u,0,1);
  }

  PVector pointAtT(float tt) {
    // linear search; could binary by ts[] since monotonic in index
    int i = 0;
    for (; i<samples-1 && !(tt>=ts[i] && tt<=ts[i+1]); i++);
    if (i >= samples-1) i = samples-2;
    float u = (tt - ts[i]) / max(1e-9, (ts[i+1] - ts[i]));
    return PVector.lerp(pts[i], pts[i+1], u);
  }

  // ---------- compile ----------
  void compileFn() {
    err = null;
    String prelude =
      "import processing.core.PVector;\n" +
	  "import processing.core.PApplet;\n" +
      "float PI = 3.14159265359f;\n" +
      "float sin(v){ PApplet.sin((float)v) };\n" +
      "float cos(v){ PApplet.cos((float)v) };\n" +
      "float lerp(a,b,t){ PApplet.lerp((float)a, (float)b, (float)t) };\n" +
      "def V(x,y){ new PVector((float)x, (float)y) };\n";
    String script = prelude + "def f = t -> {" + code + "};\nreturn f;\n";
    try {
      Object o = shell.evaluate(script);
      if (!(o instanceof Closure)) { err = "Not a closure { t -> PVector }"; fn = null; return; }
      fn = (Closure<?>)o;
      // validate on a sample
      PVector test = evalSafe(lerp(tMin,tMax,0.5));
      if (test == null) { fn = null; }
    } catch (Exception ex) {
      err = ex.getMessage();
      fn = null;
    }
  }

  // ---------- interaction ----------
  boolean hitRect(float rx,float ry,float rw,float rh,float mx,float my){
    return mx>=rx && mx<=rx+rw && my>=ry && my<=ry+rh;
  }

  boolean onMousePressed(float mx, float my, Graph g) {
    // regions
    float rx = x+pad, ry = y+36, rw = w-2*pad;
    float codeY = ry;
    float controlsY = codeY + codeH + 6;
    float plotY = controlsY + controlsH + 6;
    float plotH = h - (plotY - y) - footerH - 6;

    // code field click: focus text
    if (hitRect(rx, codeY, rw, codeH, mx, my)) {
      editing = true; g.setKeyFocus(this);
      // place caret at end (simple). Optional: compute by textWidth for mx.
      caret = code.length();
      return true;
    }

    // controls: presets button
    float bx = rx+8, bw = 64, by = controlsY+3, bh = controlsH-6;
    if (hitRect(bx, by, bw, bh, mx, my)) {
      cyclePreset();
      return true;
    }
    // controls: grid toggle
    float gx = bx + bw + 8, gw = 54;
    if (hitRect(gx, by, gw, bh, mx, my)) {
      showGrid = !showGrid;
      return true;
    }
    // controls: ranges — detect which block and start 'virtual drag' by remembering anchor
    // (Keep simple: adjust ranges via mouse wheel would be nice; for now, only knob/fields)
    // Clicking the text doesn't capture; ranges are edited by keyboard shortcuts below.

    // plot/knob
    if (hitRect(rx, plotY, rw, plotH, mx, my)) {
      if (!inT.connected) {
        tLocal = nearestT(mx, my);
        draggingKnob = true;
        return true;
      }
      return false;
    }

    // clicking elsewhere removes focus
    editing = false;
    if (g.keyFocus == this) g.keyFocus = null;
    return false;
  }

  void onMouseDragged(float mx, float my) {
    if (draggingKnob && !inT.connected) {
      tLocal = nearestT(mx, my);
    }
  }

  void onMouseReleased(float mx, float my) {
    draggingKnob = false;
  }

  void onKeyPressed(char k, int keyCode) {
    if (!editing) return;

    // commit/compile on Enter
    if (keyCode == ENTER || keyCode == RETURN) {
      dirty = true; lastEditMs = millis();
      return;
    }

    if (keyCode == BACKSPACE) {
      if (caret>0 && code.length()>0) {
        code = code.substring(0, caret-1) + code.substring(caret);
        caret--;
        dirty = true; lastEditMs = millis();
      }
      return;
    }

    if (keyCode == DELETE) {
      if (caret < code.length()) {
        code = code.substring(0, caret) + code.substring(caret+1);
        dirty = true; lastEditMs = millis();
      }
      return;
    }

    // quick range edits with modifiers while focused:
    // Ctrl/Cmd + 1/2/3 cycles presets for t/x/y ranges; +/- zoom x/y ranges
    if (keyCode == java.awt.event.KeyEvent.VK_LEFT)  { caret = max(0, caret-1); return; }
    if (keyCode == java.awt.event.KeyEvent.VK_RIGHT) { caret = min(code.length(), caret+1); return; }

    // printable character
    if (k >= 32 && k != 127) {
      code = code.substring(0, caret) + k + code.substring(caret);
      caret++;
      dirty = true; lastEditMs = millis();
    }
  }

  void cyclePreset() {
    // rotate through a small bank
    String[] names = { "Line", "Circle", "Spiral", "Sine", "Quadratic", "Lissajous" };
    String next = names[(int)random(names.length)];
    if (next.equals("Line"))      code = "V(lerp(-1,1,t), 0)";
    if (next.equals("Circle"))    code = "float a = lerp(0, PI*PI, t); V(cos(a), sin(a))";
    if (next.equals("Spiral"))    code = "float a = 6*PI*t; float r = t; V(r*cos(a), r*sin(a))";
    if (next.equals("Sine"))      code = "float x = lerp(-1,1,t); V(x, sin(PI*x))";
    if (next.equals("Quadratic")) code = "float x = lerp(-1,1,t); V(x, x*x)";
    if (next.equals("Lissajous")) code = "float a = 2*PI*t; V(sin(3*a), sin(4*a + PI/2))";
    caret = code.length();
    dirty = true; lastEditMs = millis();
  }
}
