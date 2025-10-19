// for SuperCollider integration
import supercollider.*;
import oscP5.*;
import netP5.*;

import processing.javafx.*; // for FX2D renderer

// to run .bat file
import java.io.*;
import java.util.concurrent.*;

// --- Minimal Visual Node Graph ---
// Controls:
//  - Drag nodes by their title bar.
//  - Click an OUTPUT, then an INPUT to connect.
//  - ESC to stop dragging a pending wire.
//  - Hover a wire and press DELETE/BACKSPACE to remove it.

Graph graph;
PShape svg;
Camera2D cam;

float worldMouseX, worldMouseY;

SynthNode osc;

void runBatOnce() throws Exception {
  ProcessBuilder pb = new ProcessBuilder(
    "cmd.exe", "/c", "C:\\Users\\lexi-\\Documents\\Porstmouth University\\Music-Programming\\Final Project - Processing\\SC_processing\\run.bat"
  );
  pb.directory(new File("C:\\Users\\lexi-\\Documents\\Porstmouth University\\Music-Programming\\Final Project - Processing\\SC_processing"));  // optional working dir
  pb.redirectErrorStream(true);            // merge stderr→stdout

  Process p = pb.start();

  try (BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream(), "UTF-8"))) {
    String line;
    while ((line = r.readLine()) != null) {
      System.out.println("[bat] " + line);
    }
  }

  // Optional timeout
  boolean done = p.waitFor(30, TimeUnit.SECONDS);
  if (!done) {
    p.destroyForcibly();
    throw new RuntimeException("SuperCollider timed out");
  }
  if (p.exitValue() != 0) {
    throw new RuntimeException("SuperCollider failed with code " + p.exitValue());
  }
}

void setup() {
  // try{
  //   runBatOnce();

  // } catch (Exception e) {
  //   e.printStackTrace();
  // }
  
    // Use P2D or FX2D (FX2D = nicest AA + HiDPI text, a bit heavier)
  size(1200, 800, FX2D);      // or: size(1200, 800, FX2D);

  // Make the canvas scale to your display's pixel ratio (e.g., 2 on Retina)
  pixelDensity(displayDensity());

  smooth();

  // Optional niceties
  hint(ENABLE_STROKE_PURE);     // crisper 1px lines on the pixel grid
  textFont(createFont("Inter", 14, true)); // native font for sharper text
  
  svg = loadShape("mario.svg");
  
  graph = new Graph();

  cam = new Camera2D();

  // Demo nodes
  osc = new SynthNode("sine", 120, 160);
  osc.addInput("freq", 80);
  osc.addInput("amp", 0.001);
  osc.addOutput("signal");

  graph.add(new SliderNode("slider", 190, 160));

  Node env = new Node("Envelope", 460, 120);
  env.addInput("Gate");
  env.addOutput("Env");

  Node filter = new Node("Filter", 460, 360);
  filter.addInput("In");
  filter.addInput("Cutoff");
  filter.addInput("Res");
  filter.addOutput("Out");

  Node out = new Node("Output", 760, 260);
  out.addInput("L");
  out.addInput("R");

  graph.add(osc);
  graph.add(env);
  graph.add(filter);
  graph.add(out);
}

void draw() {
  PVector worldMouse = cam.screenToWorld(mouseX, mouseY);
  worldMouseX = worldMouse.x;
  worldMouseY = worldMouse.y;

  background(255, 239, 216);

// --- WORLD ---
  pushMatrix();
  cam.apply();          // translate/scale world to screen
  
  graph.update();
  graph.draw();
  shape(svg, 100, 100, 200, 200);  // Draw it at position (100,100)
  
  popMatrix();

  // --- UI OVERLAY ---
  drawHud();
}

void mousePressed()  { 
  PVector m = mouseWorld();
  graph.mousePressed(m.x, m.y); cam.mousePressed(mouseButton, mouseX, mouseY); 
}
void mouseDragged()  { 
  PVector m = mouseWorld();
  graph.mouseDragged(m.x, m.y); 
  cam.mouseDragged(mouseX, mouseY); 
}
void mouseReleased() { 
  PVector m = mouseWorld();
  graph.mouseReleased(m.x, m.y); 
  cam.mouseReleased(); 
}
void mouseWheel(processing.event.MouseEvent e) { cam.mouseWheel(e); }
void keyPressed()    { graph.keyPressed(key, keyCode); }


void mouseMoved ()
{
    osc.set("freq", 40 + (mouseX * 3)); 
}

PVector mouseWorld() { 
  return cam.screenToWorld(mouseX, mouseY); 
}

void exit ()
{
    for (Node n : graph.nodes) if(n instanceof SynthNode) ((SynthNode) n).free();
    super.exit();
}

void drawHud() {
  
}
