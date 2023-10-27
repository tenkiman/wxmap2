/*
 * $Id: TabApp.java,v 1.3 1996/02/07 12:08:25 toshok Exp $
 *
 * Copyright (C) 1996 The Hungry Programmers
 *
 * This file is part of the Hungry Programmers Java ThumbTab library
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Library General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Library General Public License for more details.
 *
 * You should have received a copy of the GNU Library General Public
 * License along with this library; if not, write to the Free
 * Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
 *
 */

import hungry.tabs.Tab;
import hungry.tabs.TabApplet;
import java.applet.Applet;
import java.awt.Color;
import java.awt.Event;
import java.awt.Font;
import java.awt.Graphics;
import java.util.Vector;

public class TabApp extends Applet implements TabApplet {
  /**
   * Vertical orientation for tab layout.
   */
  static int VERTICAL = 0;

  /**
   * Horizontal orientation for tab layout.
   */
  static int HORIZONTAL = 1;

  /**
   * The tabs contained in this applet.
   */
  Vector children;

  /**
   * The tab that's currently armed.
   */
  Tab armedChild;

  /**
   * Either horizontal or vertical.
   */
  int myOrientation;

  /**
   * The color of the background for this applet (behind the tabs).
   */
  Color bgColor;

  /**
   * The color of the tabs for this applet.
   */
  Color tabColor;

  /**
   * The color of the normal text for the tabs in this applet.
   */
  Color textColor;

  /**
   * The color of the selected text for the tabs in this applet.
   */
  Color selColor;

  /**
   * The font to be used by the tabs in this applet.
   */
  Font font;

  /**
   * Constructs a new TabApp
   */
  public TabApp() {
    children = new Vector();
  }

  /**
   * Performs initialization for this applet, including reading the parameters
   * from the HTML.
   */
  public void init() {
    int num_children;
    String orient = getParameter("orientation");

    if (orient != null) {
      if (orient.equals("vertical")) {
 	myOrientation = VERTICAL;
      }
      else {
 	myOrientation = HORIZONTAL;
      }
    }
    else {
      myOrientation = HORIZONTAL; // if they didn't specify the parameter
    }
    
    try {
      font = new Font(getParameter("font"),
		      Font.BOLD,
		      (new Integer(getParameter("pointSize"))).intValue());
    }
    catch (Exception e) {
      font = new Font("helvetica",
		      Font.BOLD,
		      14);
    }

    try {
      textColor = new Color(Integer.valueOf(getParameter("textColor"),16).intValue());
    }
    catch (Exception e) {
      textColor = Color.black;
    }

    try {
      selColor = new Color(Integer.valueOf(getParameter("selectColor"),16).intValue());
    }
    catch (Exception e) {
      selColor = Color.red;
    }

    try {
      bgColor = new Color(Integer.valueOf(getParameter("bgColor"),16).intValue());
    }
    catch (Exception e) {
      bgColor = Color.white;
    }

    try {
      tabColor = new Color(Integer.valueOf(getParameter("tabColor"),16).intValue());
    }
    catch (Exception e) {
      tabColor = Color.lightGray;
    }

    setBackground(bgColor);

    try {
      num_children = (new Integer(getParameter("numChildren"))).intValue();
    }
    catch (Exception e) {
      e.printStackTrace();
      return;
    }

    for (int i = 0; i < num_children; i++) {
      String name = getParameter("name_" + i);
      String url = getParameter("url_" + i);
      String frame = getParameter("frame_" + i);

      if (name == null) {
        System.out.println("You must specify a name for all tabs.");
        return;
      }

      children.addElement(new Tab(name,
				  url,
				  frame,
				  tabColor,
				  textColor,
				  selColor,
				  font, 
				  myOrientation,
				  this));
    }
  }

  /**
   * Paints lines either across the bottom (if orientation is horizontal)
   * or the left hand side (if orientation is vertical).
   * @param g the graphics object used to paint the lines.
   */
  public void paintLines(Graphics g) {
    g.setColor(Color.black);

    if (myOrientation == HORIZONTAL) {
      if (armedChild != null) {
	g.drawLine(0, bounds().height - 1,
		   armedChild.getBounds().x, bounds().height - 1);
	g.drawLine(armedChild.getBounds().x + armedChild.getBounds().width - 5,
		   bounds().height - 1,
		   bounds().width - 1, bounds().height - 1);
      }
      else {
	g.drawLine(0, bounds().height - 1,
		   bounds().width - 1, bounds().height - 1);
      }
    }
    else { // vertical
      if (armedChild != null) {
	g.drawLine(0, 0,
		   0, armedChild.getBounds().y);
	g.drawLine(0, armedChild.getBounds().y + armedChild.getBounds().height - 5,
		   0, bounds().height - 1);
      }
      else {
	g.drawLine(0, 0,
		   0, bounds().height - 1);
      }      
    }
  }

  /**
   * Paints the applet by laying out and painting all the tab children.
   * @param g the graphics object used to paint the applet
   */
  public void paint(Graphics g) {
    int i;

    doLayout(g);

    for (i=0; i < children.size(); i++) {
      Tab child = (Tab)children.elementAt(i);

      child.paint(g);
    }

    paintLines(g);
  }

  /**
   * Lays out the tab children according to my orientation.
   * @param g the graphics object used to erase and repaint the children when I move them around.
   */
  public void doLayout(Graphics g) {
    int i;
    Tab child;

    if (!isShowing() || children.size() == 0) {
      return;
    }

    if (myOrientation == HORIZONTAL) {
      int current_x = 5;
      for (i=0; i < children.size(); i++) {
	child = (Tab)children.elementAt(i);

	child.erase(g);
	child.move(current_x, bounds().height - child.getBounds().height);
	child.paint(g);
	
	current_x += child.getBounds().width + 5;
      }
    }
    else { // vertical
      int current_y = 5;
      for (i=0; i < children.size(); i++) {
	child = (Tab)children.elementAt(i);
	
	child.erase(g);
	child.move(child.getBounds().x, current_y);
	child.paint(g);

	current_y += child.getBounds().height + 5;
      }
    }
  }

  /**
   * Selects (arms) a particular tab.
   * @param child the newly armed tab
   */
  public void selectChild(Tab child) {
    child.erase(getGraphics());

    if (myOrientation == HORIZONTAL) {
      child.resize(child.getBounds().width,
		   child.getBounds().height + 3);
      child.move(child.getBounds().x,
		 child.getBounds().y - 3);
    }
    else { // vertical
      child.resize(child.getBounds().width + 3,
		   child.getBounds().height);
    }

    child.setSelected(true);
    child.paint(getGraphics());
  }

  /**
   * Unselects (disarms) a particular tab.
   * @param child the (until recently) selected tab.
   */
  public void unselectChild(Tab child) {
    child.erase(getGraphics());

    if (myOrientation == HORIZONTAL) {
      child.resize(child.getBounds().width,
		   child.getBounds().height - 3);
      child.move(child.getBounds().x,
		 child.getBounds().y + 3);
    }
    else { // vertical
      child.resize(child.getBounds().width - 3,
		   child.getBounds().height);
    }

    child.setSelected(false);
    child.paint(getGraphics());
  }

  /**
   * Handles events for the applet.
   * @param e the event.
   */
  public boolean handleEvent(Event e) {
    Graphics g = getGraphics();

    if (e.id == Event.MOUSE_DRAG 
	|| e.id == Event.MOUSE_MOVE
	|| e.id == Event.MOUSE_DOWN
	|| e.id == Event.MOUSE_ENTER) {
      boolean inside = false;
      int i;

      for (i = 0; i < children.size(); i++) {

	Tab child = (Tab)children.elementAt(i);

	if (child.getBounds().inside(e.x, e.y)) {
	  if (child != armedChild) {

	    selectChild(child);

	    if (armedChild != null) {
	      unselectChild(armedChild);
	    }
	  }
	  inside = true;
	  armedChild = child;
	  
	  paintLines(g);
	  showStatus(armedChild.getURL());
	}
      }

      if (!inside && armedChild != null) {
	unselectChild(armedChild);
	armedChild = null;
	paintLines(g);
	showStatus("");
      }

      return true;
    }
    else if (e.id == Event.MOUSE_EXIT) {
      if (armedChild != null) {
	unselectChild(armedChild);
	armedChild = null;
	paintLines(g);
	showStatus("");
      }
    }
    else if (e.id == Event.MOUSE_UP) {
      if (armedChild != null) {
	armedChild.activate();
      }
    }

    return false;
  }
}
