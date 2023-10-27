/*
 * $Id: Tab.java,v 1.3 1996/02/11 14:19:24 toshok Exp $
 *
 * Thumb tabs for web pages.
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

package hungry.tabs;

import java.applet.Applet;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.FontMetrics;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.net.URL;

public class Tab {
  /**
   * The name displayed in the tab
   */
  String myName;

  /**
   * The URL to go to when we're activated
   */
  URL myUrl;

  /**
   * The netscape frame in which open up the new document
   */
  String myFrame;

  /**
   * The applet containing this tab
   */
  TabApplet myApplet;

  /**
   * The font used to draw the text
   */
  Font myFont;
  
  /** 
   * The metrics for my font
   */
  FontMetrics metrics;

  /**
   * The color of the tab
   */
  Color bgcolor;

  /**
   * The color of the tab's text when it isn't armed.
   */
  Color textcolor;

  /**
   * The color of the tab's text when it is armed.
   */
  Color selcolor;

  /**
   * Whether or not we're armed presently.
   */
  boolean selected;

  /**
   * Either TabApplet.VERTICAL or TabApplet.HORIZONTAL
   */
  int myOrientation;

  /**
   * My bounding box
   */
  Rectangle bounds;

  /**
   * Creates a new Tab.
   * @param name the name to use for this tab.
   * @param url the url to associate with this tab.
   * @param frame the frame in which to open the url.
   * @param background the color of the tab.
   * @param text the normal text color.
   * @param select the selected <i>(armed)</i> text color.
   * @param font the font used to draw the text.
   * @param orientation the orientation of this tab.
   * @param applet the applet containing this tab.
   */
  public Tab(String name, 
	     String url,
	     String frame,
	     Color background,
	     Color text,
	     Color select,
	     Font font,
	     int orientation,
	     TabApplet applet) {
    myName = name;
    
    try {
      myUrl = new URL(((Applet)applet).getDocumentBase(),
		      url);
    }
    catch (Exception e) {
      myUrl = null;
    }

    myFrame = frame;
    bgcolor = background;
    textcolor = text;
    selcolor = select;
    myFont = font;
    myApplet = applet;
    myOrientation = orientation;
    bounds = new Rectangle();
    selected = false;

    metrics = Toolkit.getDefaultToolkit().getFontMetrics(myFont);
    
    if (myOrientation == TabApplet.HORIZONTAL) {
      resize(metrics.stringWidth(myName) + 15,
	     metrics.getHeight() + 5);
    }
    else {
      resize(metrics.stringWidth(myName) + 15,
	     metrics.getHeight() + 10);
    }
  }

  /**
   * Creates a new Tab
   * @param name the text displayed in this tab
   * @param url the url to open when we're activated
   * @param frame the frame in which we open the url
   * @param applet the applet containing this tab
   */
  public Tab(String name,
	     String url,
	     String frame,
	     TabApplet applet) {
    this(name, url, frame, Color.lightGray, Color.black, Color.red, 
	 new Font("helvetica", Font.BOLD, 14), 
	 TabApplet.HORIZONTAL, applet);
  }

  /**
   * Erases the tab.
   * @param g the graphics object used to erase the tab
   */
  public void erase(Graphics g) {
    g.clearRect(bounds.x, bounds.y,
		bounds.width, bounds.height);
  }

  /**
   * Paints the tab.
   * @param g the graphics object used to paint the tab.
   */
  public void paint(Graphics g) {

    if (myOrientation == TabApplet.HORIZONTAL) {

      // fill in the tab
      g.setColor(bgcolor);
      g.fillRect(bounds.x, bounds.y,
		 bounds.width - 5,
		 bounds.height);

      // draw the border 
      g.setColor(Color.black);
      g.drawLine(bounds.x, bounds.y,
		 bounds.x + bounds.width - 5, bounds.y);
      g.drawLine(bounds.x, bounds.y,
		 bounds.x, bounds.y + bounds.height);
      g.drawLine(bounds.x + bounds.width - 5, bounds.y,
		 bounds.x + bounds.width - 5, bounds.y + bounds.height);
    
      // draw the shadow
      for (int i = 1; i < 5; i++) {
	Color bg = ((Applet)myApplet).getBackground();
	int new_red = bg.getRed() - (int)((5-i) / 5.0 * bg.getRed());
	int new_green = bg.getGreen() - (int)((5-i) / 5.0 * bg.getGreen());
	int new_blue = bg.getBlue() - (int)((5-i) / 5.0 * bg.getBlue());

	g.setColor(new Color(new_red < 0 ? 0 : new_red,
			     new_green < 0 ? 0 : new_green,
			     new_blue < 0 ? 0 : new_blue));

	g.drawLine(bounds.x + bounds.width - 5 + i, bounds.y + 3,
		   bounds.x + bounds.width - 5 + i, bounds.y + bounds.height);
      }
      
    }
    else { // vertical

      // fill in the tab.
      g.setColor(bgcolor);
      g.fillRect(bounds.x, bounds.y,
		 bounds.width - 5,
		 bounds.height - 5);

      // draw the border.
      g.setColor(Color.black);
      g.drawLine(bounds.x, bounds.y,
		 bounds.x + bounds.width - 5, bounds.y);
      g.drawLine(bounds.x, bounds.y + bounds.height - 5,
		 bounds.x + bounds.width - 5, bounds.y + bounds.height - 5);
      g.drawLine(bounds.x + bounds.width - 5, bounds.y,
		 bounds.x + bounds.width - 5, bounds.y + bounds.height - 5);

      // draw the shadow
      for (int i = 1; i < 5; i++) {
	Color bg = ((Applet)myApplet).getBackground();
	int new_red = bg.getRed() - (int)((5-i) / 5.0 * bg.getRed());
	int new_green = bg.getGreen() - (int)((5-i) / 5.0 * bg.getGreen());
	int new_blue = bg.getBlue() - (int)((5-i) / 5.0 * bg.getBlue());

	g.setColor(new Color(new_red < 0 ? 0 : new_red,
			     new_green < 0 ? 0 : new_green,
			     new_blue < 0 ? 0 : new_blue));

	g.drawLine(bounds.x + bounds.width - 5 + i, bounds.y + 3,
		   bounds.x + bounds.width - 5 + i, bounds.y + bounds.height - 5 + i);
	g.drawLine(bounds.x, bounds.y + bounds.height - 5 + i,
		   bounds.x + bounds.width - 5 + i, bounds.y + bounds.height - 5 + i);
      }      
    }

    // now draw the text.
    if (selected) {
      g.setColor(selcolor);
    }
    else {
      g.setColor(textcolor);
    }
    
    g.setFont(myFont);

    if (myOrientation == TabApplet.HORIZONTAL) {
      g.drawString(myName, bounds.x + 5,
		   bounds.y + metrics.getHeight());
    }
    else {
      g.drawString(myName, bounds.x + (selected ? 10 : 5),
		   bounds.y + metrics.getHeight());
    }
    
  }

  /**
   * Moves the tab to a new position within the applet.
   * @param x the new x position.
   * @param y the new y position.
   */
  public void move(int x, int y) {
    bounds.x = x;
    bounds.y = y;
  }

  /**
   * Resizes the tab to a new width and height.
   * @param width the new width.
   * @param height the new height.
   */
  public void resize(int width, int height) {
    bounds.width = width;
    bounds.height = height;
  }

  /**
   * Returns the bounding box for this tab.
   */
  public Rectangle getBounds() {
    return bounds;
  }

  /**
   * Sets whether or not this tab is selected
   * @param flag whether or not this tab is selected.
   */
  public void setSelected(boolean flag) {
    selected = flag;
  }

  /**
   * Activates the tab, by opening the URL into the frame
   * specified when the tab was created.
   */
  public void activate() {
    if (myUrl != null) {
      if (myFrame != null) {
	((Applet)myApplet).getAppletContext().showDocument(myUrl,
							   myFrame);
      }
      else {
	((Applet)myApplet).getAppletContext().showDocument(myUrl);
      }
    } 
  }

  /**
   * Returns the URL associated with this tab.
   */
  public String getURL() {
    if (myUrl != null) {
      return myUrl.toString();
    }
    else {
      return "";
    }
  }
}
