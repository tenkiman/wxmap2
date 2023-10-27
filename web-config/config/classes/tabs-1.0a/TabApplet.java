/*
 * $Id: TabApplet.java,v 1.2 1996/02/07 11:23:23 toshok Exp $
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

public interface TabApplet {
  /**
   * Vertical orientation for tab layout.
   */
  static int VERTICAL = 0;

  /**
   * Horizontal orientation for tab layout.
   */
  static int HORIZONTAL = 1;
}
