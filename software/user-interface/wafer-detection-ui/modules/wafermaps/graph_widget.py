""" MatplotFigure is based on https://github.com/jeysonmc/kivy_matplotlib 
and kivy scatter
"""

import math
import copy

import matplotlib
matplotlib.use('Agg')
from kivy.graphics.texture import Texture
from kivy.graphics.transformation import Matrix
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, BoundedNumericProperty, AliasProperty, \
    NumericProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import cbook
from matplotlib.colors import to_hex
from weakref import WeakKeyDictionary
from kivy.metrics import dp
import numpy as np
from kivy.utils import get_color_from_hex
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.collections import PathCollection

# This shouldn't be in  the widget class: TODO
from data.wfdata import load_stitch_data


class MatplotFigure(Widget):
    """Widget to show a matplotlib figure in kivy.
    The figure is rendered internally in an AGG backend then
    the rgba data is obtained and blitted into a kivy texture.
    """

    figure = ObjectProperty(None)
    _box_pos = ListProperty([0, 0])
    _box_size = ListProperty([0, 0])
    _img_texture = ObjectProperty(None)
    _alpha_box = NumericProperty(0)   
    _bitmap = None
    do_update=False
    figcanvas = ObjectProperty(None)
    translation_touches = BoundedNumericProperty(1, min=1)
    do_scale = BooleanProperty(True)
    scale_min = NumericProperty(0.01)
    scale_max = NumericProperty(1e20)
    transform = ObjectProperty(Matrix())
    _alpha_hor = NumericProperty(0)
    _alpha_ver = NumericProperty(0)
    pos_x_rect_hor=NumericProperty(0)
    pos_y_rect_hor=NumericProperty(0)
    pos_x_rect_ver=NumericProperty(0)
    pos_y_rect_ver=NumericProperty(0)  
    invert_rect_ver = BooleanProperty(False)
    invert_rect_hor = BooleanProperty(False)
    legend_instance = ObjectProperty(None, allownone=True)
    legend_do_scroll_x = BooleanProperty(True)
    legend_do_scroll_y = BooleanProperty(True)
    interactive_axis = BooleanProperty(False) 
    do_pan_x = BooleanProperty(True)
    do_pan_y = BooleanProperty(True)    
    do_zoom_x = BooleanProperty(True)
    do_zoom_y = BooleanProperty(True)  
    fast_draw = BooleanProperty(True) #True will don't draw axis
    xsorted = BooleanProperty(False) #to manage x sorted data
    minzoom = NumericProperty(dp(40))
    compare_xdata = BooleanProperty(False)   
    hover_instance = ObjectProperty(None, allownone=True)
    nearest_hover_instance = ObjectProperty(None, allownone=True)
    compare_hover_instance = ObjectProperty(None, allownone=True)
    disable_mouse_scrolling = BooleanProperty(False) 
    disable_double_tap = BooleanProperty(False) 

    def on_figure(self, obj, value):
        self.figcanvas = _FigureCanvas(self.figure, self)
        self.figcanvas._isDrawn = False
        l, b, w, h = self.figure.bbox.bounds
        w = int(math.ceil(w))
        h = int(math.ceil(h))
        self.width = w
        self.height = h

        if self.figure.axes[0]:
            #add copy patch
            ax=self.figure.axes[0]
            patch_cpy=copy.copy(ax.patch)
            patch_cpy.set_visible(False)
            for pos in ['right', 'top', 'bottom', 'left']:
                ax.spines[pos].set_zorder(10)
            patch_cpy.set_zorder(9)
            self.background_patch_copy= ax.add_patch(patch_cpy)
            
            #set xmin axes attribute
            self.axes = self.figure.axes[0]
            
            #set default xmin/xmax and ymin/ymax
            self.xmin,self.xmax = self.axes.get_xlim()
            self.ymin,self.ymax = self.axes.get_ylim()
            self.calculate_defects()
        
        if self.legend_instance:
            self.legend_instance.reset_legend()
            self.legend_instance=None
            
        # Texture
        self._img_texture = Texture.create(size=(w, h))

        #close last figure in memory (avoid max figure warning)
        matplotlib.pyplot.close()

    def __init__(self, **kwargs):
        super(MatplotFigure, self).__init__(**kwargs)
        
        #figure info
        self.figure = None
        self.axes = None
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        self.lines = []
        
        #option
        self.touch_mode='pan'
        self.hover_on = False
        self.cursor_xaxis_formatter=None #used matplotlib formatter to display x cursor value
        self.cursor_yaxis_formatter=None #used matplotlib formatter to display y cursor value

        #zoom box coordonnate
        self.x0_box = None
        self.y0_box = None
        self.x1_box = None
        self.y1_box = None
        
        #clear touches on touch up
        self._touches = []
        self._last_touch_pos = {}

        #background 
        self.background=None
        self.background_patch_copy=None        

        #manage adjust x and y
        self.anchor_x = None
        self.anchor_y = None 
        
        #trick to manage wrong canvas size on first call (compare_hover)
        self.first_call_compare_hover=False
        
        #manage hover data
        self.x_hover_data = None
        self.y_hover_data = None
        
        #pan management
        self.first_touch_pan = None
        
        #manage back and next event
        self._nav_stack = cbook.Stack()
        self.set_history_buttons()         
        
        self.bind(size=self._onSize)

    def register_lines(self,lines:list) -> None:
        """ register lines method
        
        Args:
            lines (list): list of matplolib line class
            
        Return:
            None        
        """ 
        
        #create cross hair cusor
        self.horizontal_line = self.axes.axhline(color='k', lw=0.8, ls='--', visible=False)
        self.vertical_line = self.axes.axvline(color='k', lw=0.8, ls='--', visible=False)
        
        #register lines
        self.lines=lines
                
        #cursor text
        self.text = self.axes.text(1.0, 1.01, '', 
                                      transform=self.axes.transAxes,
                                      ha='right')

    def set_cross_hair_visible(self, visible:bool) -> None:
        """ set curcor visibility
        
        Args:
            visible (bool): make cursor visble or not
            
        Return:
            None
        
        """       
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)

    def hover(self, event) -> None:
        """ hover cursor method (cursor to nearest value)
        
        Args:
            event: touch kivy event
            
        Return:
            None
        
        """
           
        #if cursor is set -> hover is on
        if self.hover_on:

            #transform kivy x,y touch event to x,y data
            trans = self.axes.transData.inverted()
            xdata, ydata = trans.transform_point((event.x - self.pos[0], event.y - self.pos[1]))

            #loop all register lines and find closest x,y data for each valid line
            distance=[]
            good_line=[]
            good_index=[]
            for line in self.lines:
                #get only visible lines
                if line.get_visible():  
                    #get line x,y datas
                    self.x_cursor, self.y_cursor = line.get_data()
                    
                    #check if line is not empty
                    if len(self.x_cursor)!=0:                        
                        
                        #find closest data index from touch (x axis)
                        if self.xsorted:
                            index = min(np.searchsorted(self.x_cursor, xdata), len(self.y_cursor) - 1)
                            
                        else:
                            index = np.argsort(abs(self.x_cursor - xdata))[0]

                        #get x data from index
                        x = self.x_cursor[index]
                        
                        if self.compare_xdata:
                            #get distance between line and touch (in pixels)
                            ax=line.axes 
                            #left axis
                            xy_pixels_mouse = ax.transData.transform([(xdata,ydata)])
                            xy_pixels = ax.transData.transform([(x,ydata)])
                            dx2 = (xy_pixels_mouse[0][0]-xy_pixels[0][0]) 
                            distance.append(dx2)
                        else:    
                            
                            #find ydata corresponding to xdata
                            y = self.y_cursor[index]
                                                   
                            #get distance between line and touch (in pixels)
                            ax=line.axes 
                            #left axis
                            xy_pixels_mouse = ax.transData.transform([(xdata,ydata)])
                            xy_pixels = ax.transData.transform([(x,y)])
                            dx2 = (xy_pixels_mouse[0][0]-xy_pixels[0][0])**2
                            dy2 = (xy_pixels_mouse[0][1]-xy_pixels[0][1])**2 
                            
                            #store distance
                            distance.append((dx2 + dy2)**0.5)
                        
                        #store all best lines and index
                        good_line.append(line)
                        good_index.append(index)
 
            #case if no good line
            if len(good_line)==0:
                return

            #if minimum distance if lower than 50 pixels, get line datas with 
            #minimum distance 
            if min(distance)<dp(50):
                #index of minimum distance
                if self.compare_xdata:
                    if not self.hover_instance or not hasattr(self.hover_instance,'children_list'):
                        return
                    
                    idx_best_list = np.flatnonzero(np.array(distance) == min(distance))
                    
                    #get datas from closest line
                    line=good_line[idx_best_list[0]]
                    self.x_cursor, self.y_cursor = line.get_data()
                    x = self.x_cursor[good_index[idx_best_list[0]]]
                    y = self.y_cursor[good_index[idx_best_list[0]]] 

                    xy_pos = ax.transData.transform([(x,y)]) 
                    self.x_hover_data = x
                    self.y_hover_data = y
                    self.hover_instance.x_hover_pos=float(xy_pos[0][0]) + self.x
                    self.hover_instance.y_hover_pos=float(xy_pos[0][1]) + self.y
                    self.hover_instance.y_touch_pos=float(xy_pixels[0][1]) + self.y
                    
                    if self.first_call_compare_hover:
                        self.hover_instance.show_cursor=True 
                    else:
                        self.first_call_compare_hover=True
                    
                    if len(idx_best_list)>0:
                        available_widget = self.hover_instance.children_list
                        nb_widget=len(available_widget)
                        index_list=list(range(nb_widget))
                        for i, current_idx_best in enumerate(idx_best_list):
                            if i > nb_widget-1:
                                break
                            else:
                                line=good_line[idx_best_list[i]]
                                line_label = line.get_label()
                                if line_label in self.hover_instance.children_names:
                                    index= self.hover_instance.children_names.index(line_label)                                   
                                    y_cursor = line.get_ydata()
                                    y = y_cursor[good_index[idx_best_list[i]]] 
                                    xy_pos = ax.transData.transform([(x,y)]) 
                                    available_widget[index].x_hover_pos=float(xy_pos[0][0]) + self.x
                                    available_widget[index].y_hover_pos=float(xy_pos[0][1]) + self.y
                                    available_widget[index].custom_color = get_color_from_hex(to_hex(line.get_color()))
                                    
                                    if self.cursor_yaxis_formatter:
                                        y = self.cursor_yaxis_formatter.format_data(y) 
                                    available_widget[index].label_y_value=f"{y}"
                                    available_widget[index].show_widget=True
                                    index_list.remove(index)
                                    
                        if i<nb_widget-1:
                            for ii in index_list:
                                available_widget[ii].show_widget=False

                        if self.cursor_xaxis_formatter:
                            x = self.cursor_xaxis_formatter.format_data(x) 
                            
                        self.hover_instance.label_x_value=f"{x}"
                    
                        self.hover_instance.ymin_line = float(ax.bbox.bounds[1])  + self.y
                        self.hover_instance.ymax_line = float(ax.bbox.bounds[1] + ax.bbox.bounds[3])  + self.y
                        
                        if self.hover_instance.x_hover_pos>self.x+self.axes.bbox.bounds[2] + self.axes.bbox.bounds[0] or \
                            self.hover_instance.x_hover_pos<self.x+self.axes.bbox.bounds[0] or \
                            self.hover_instance.y_hover_pos>self.y+self.axes.bbox.bounds[1] + self.axes.bbox.bounds[3] or \
                            self.hover_instance.y_hover_pos<self.y+self.axes.bbox.bounds[1]:               
                            self.hover_instance.hover_outside_bound=True
                        else:
                            self.hover_instance.hover_outside_bound=False                      
                        
                        return
                        
                
                else:
                    idx_best=np.argmin(distance)
                    
                    #get datas from closest line
                    line=good_line[idx_best]
                    self.x_cursor, self.y_cursor = line.get_data()
                    x = self.x_cursor[good_index[idx_best]]
                    y = self.y_cursor[good_index[idx_best]]  
                    
                    if not self.hover_instance:
                        self.set_cross_hair_visible(True)
                    
                    # update the cursor x,y data               
                    ax=line.axes
                    self.horizontal_line.set_ydata(y)
                    self.vertical_line.set_xdata(x)
    
                    #x y label
                    if self.hover_instance:                     
                        xy_pos = ax.transData.transform([(x,y)]) 
                        self.x_hover_data = x
                        self.y_hover_data = y
                        self.hover_instance.x_hover_pos=float(xy_pos[0][0]) + self.x
                        self.hover_instance.y_hover_pos=float(xy_pos[0][1]) + self.y
                        self.hover_instance.show_cursor=True
                            
                        if self.cursor_xaxis_formatter:
                            x = self.cursor_xaxis_formatter.format_data(x)
                        if self.cursor_yaxis_formatter:
                            y = self.cursor_yaxis_formatter.format_data(y) 
                        self.hover_instance.label_x_value=f"{x}"
                        self.hover_instance.label_y_value=f"{y}"
                
                        self.hover_instance.ymin_line = float(ax.bbox.bounds[1])  + self.y
                        self.hover_instance.ymax_line = float(ax.bbox.bounds[1] + ax.bbox.bounds[3])  + self.y
                        
                        self.hover_instance.custom_label = line.get_label()
                        self.hover_instance.custom_color = get_color_from_hex(to_hex(line.get_color()))
                        
                        if self.hover_instance.x_hover_pos>self.x+self.axes.bbox.bounds[2] + self.axes.bbox.bounds[0] or \
                            self.hover_instance.x_hover_pos<self.x+self.axes.bbox.bounds[0] or \
                            self.hover_instance.y_hover_pos>self.y+self.axes.bbox.bounds[1] + self.axes.bbox.bounds[3] or \
                            self.hover_instance.y_hover_pos<self.y+self.axes.bbox.bounds[1]:               
                            self.hover_instance.hover_outside_bound=True
                        else:
                            self.hover_instance.hover_outside_bound=False                      
                        
                        return
                    else:
                        if self.cursor_xaxis_formatter:
                            x = self.cursor_xaxis_formatter.format_data(x)
                        if self.cursor_yaxis_formatter:
                            y = self.cursor_yaxis_formatter.format_data(y) 
                        self.text.set_text(f"x={x}, y={y}")
    
                    #blit method (always use because same visual effect as draw)                  
                    if self.background is None:
                        self.set_cross_hair_visible(False)
                        self.axes.figure.canvas.draw_idle()
                        self.axes.figure.canvas.flush_events()                   
                        self.background = self.axes.figure.canvas.copy_from_bbox(self.axes.figure.bbox)
                        self.set_cross_hair_visible(True)  
    
                    self.axes.figure.canvas.restore_region(self.background)
                    self.axes.draw_artist(self.text)
    
                    self.axes.draw_artist(self.horizontal_line)
                    self.axes.draw_artist(self.vertical_line)  
    
                    #draw (blit method)
                    self.axes.figure.canvas.blit(self.axes.bbox)                 
                    self.axes.figure.canvas.flush_events()

            #if touch is too far, hide cross hair cursor
            else:
                self.set_cross_hair_visible(False)  
                if self.hover_instance:
                    self.hover_instance.x_hover_pos=self.x
                    self.hover_instance.y_hover_pos=self.y      
                    self.hover_instance.show_cursor=False
                    self.x_hover_data = None
                    self.y_hover_data = None

    def home(self) -> None:
        """ reset data axis
        
        Return:
            None
        """
        #do nothing is all min/max are not set
        if self.xmin is not None and \
            self.xmax is not None and \
            self.ymin is not None and \
            self.ymax is not None:
                
            ax = self.axes
            xleft,xright=ax.get_xlim()
            ybottom,ytop=ax.get_ylim() 
            
            #check inverted data
            inverted_x = False
            if xleft>xright:
                inverted_x=True
            inverted_y = False
            if ybottom>ytop:
                inverted_y=True         
            
            if inverted_x:
                ax.set_xlim(right=self.xmin,left=self.xmax)
            else:
                ax.set_xlim(left=self.xmin,right=self.xmax)
            if inverted_y:
                ax.set_ylim(top=self.ymin,bottom=self.ymax)
            else:
                ax.set_ylim(bottom=self.ymin,top=self.ymax)                              

            ax.figure.canvas.draw_idle()
            ax.figure.canvas.flush_events() 

            ax.set_title('Wafer Map with Defects [' + str(self.calculate_defects()) + ']')
            

    def back(self, *args):
        """
        Move back up the view lim stack.
        For convenience of being directly connected as a GUI callback, which
        often get passed additional parameters, this method accepts arbitrary
        parameters, but does not use them.
        """
        self._nav_stack.back()
        self.set_history_buttons()
        self._update_view()

    def forward(self, *args):
        """
        Move forward in the view lim stack.
        For convenience of being directly connected as a GUI callback, which
        often get passed additional parameters, this method accepts arbitrary
        parameters, but does not use them.
        """
        self._nav_stack.forward()
        self.set_history_buttons()
        self._update_view()
 
    def push_current(self):
       """Push the current view limits and position onto the stack."""
       self._nav_stack.push(
           WeakKeyDictionary(
               {ax: (ax._get_view(),
                     # Store both the original and modified positions.
                     (ax.get_position(True).frozen(),
                      ax.get_position().frozen()))
                for ax in self.figure.axes}))
       self.set_history_buttons()       

    def update(self):
        """Reset the Axes stack."""
        self._nav_stack.clear()
        self.set_history_buttons()
        
    def _update_view(self):
        """
        Update the viewlim and position from the view and position stack for
        each Axes.
        """
        nav_info = self._nav_stack()
        if nav_info is None:
            return
        # Retrieve all items at once to avoid any risk of GC deleting an Axes
        # while in the middle of the loop below.
        items = list(nav_info.items())
        for ax, (view, (pos_orig, pos_active)) in items:
            ax._set_view(view)
            # Restore both the original and modified positions
            ax._set_position(pos_orig, 'original')
            ax._set_position(pos_active, 'active')
        self.figure.canvas.draw_idle() 
        self.figure.canvas.flush_events()

    def set_history_buttons(self):
        """Enable or disable the back/forward button."""

    def reset_touch(self) -> None:
        """ reset touch
        
        Return:
            None
        """
        self._touches = []
        self._last_touch_pos = {}
        
    def _get_scale(self):
        """ kivy scatter _get_scale method """
        p1 = Vector(*self.to_parent(0, 0))
        p2 = Vector(*self.to_parent(1, 0))
        scale = p1.distance(p2)

        # XXX float calculation are not accurate, and then, scale can be
        # throwed again even with only the position change. So to
        # prevent anything wrong with scale, just avoid to dispatch it
        # if the scale "visually" didn't change. #947
        # Remove this ugly hack when we'll be Python 3 only.
        if hasattr(self, '_scale_p'):
            if str(scale) == str(self._scale_p):
                return self._scale_p

        self._scale_p = scale
        return scale

    def _set_scale(self, scale):
        """ kivy scatter _set_scale method """
        rescale = scale * 1.0 / self.scale
        self.apply_transform(Matrix().scale(rescale, rescale, rescale),
                             post_multiply=True,
                             anchor=self.to_local(*self.center))

    scale = AliasProperty(_get_scale, _set_scale, bind=('x', 'y', 'transform'))
    '''Scale value of the scatter.

    :attr:`scale` is an :class:`~kivy.properties.AliasProperty` and defaults to
    1.0.
    '''

    def _draw_bitmap(self):
        """ draw bitmap method. based on kivy scatter method"""
        if self._bitmap is None:
            print("No bitmap!")
            return
        self._img_texture = Texture.create(size=(self.bt_w, self.bt_h))
        self._img_texture.blit_buffer(
            bytes(self._bitmap), colorfmt="rgba", bufferfmt='ubyte')
        self._img_texture.flip_vertical()
        
        if self.hover_instance:
            #update hover pos if needed
            if self.hover_instance.show_cursor and self.x_hover_data and self.y_hover_data:        
                xy_pos = self.axes.transData.transform([(self.x_hover_data,self.y_hover_data)]) 
                self.hover_instance.x_hover_pos=float(xy_pos[0][0]) + self.x
                self.hover_instance.y_hover_pos=float(xy_pos[0][1]) + self.y
     
                # ymin,ymax=self.axes.get_ylim()
                # ylim_pos = self.axes.transData.transform([(ymin,ymax)])
                self.hover_instance.ymin_line = float(self.axes.bbox.bounds[1]) + self.y
                self.hover_instance.ymax_line = float(self.axes.bbox.bounds[1] + self.axes.bbox.bounds[3] )+ self.y
    
                if self.hover_instance.x_hover_pos>self.x+self.axes.bbox.bounds[2] + self.axes.bbox.bounds[0] or \
                    self.hover_instance.x_hover_pos<self.x+self.axes.bbox.bounds[0] or \
                    self.hover_instance.y_hover_pos>self.y+self.axes.bbox.bounds[1] + self.axes.bbox.bounds[3] or \
                    self.hover_instance.y_hover_pos<self.y+self.axes.bbox.bounds[1]:               
                    self.hover_instance.hover_outside_bound=True
                else:
                    self.hover_instance.hover_outside_bound=False            
        

    def transform_with_touch(self, event):
        """ manage touch behaviour. based on kivy scatter method"""
        # just do a simple one finger drag
        changed = False

        if len(self._touches) == self.translation_touches:
            
            if self.touch_mode=='pan':
                if self._nav_stack() is None:
                    self.push_current()                
                self.apply_pan(self.axes, event)
 
            if self.touch_mode=='pan_x' or self.touch_mode=='pan_y' \
                or self.touch_mode=='adjust_x' or self.touch_mode=='adjust_y':
                if self._nav_stack() is None:
                    self.push_current()                    
                self.apply_pan(self.axes, event, mode=self.touch_mode)                
 
            elif self.touch_mode=='drag_legend':
                if self.legend_instance:
                    self.apply_drag_legend(self.axes, event)
            
            elif self.touch_mode=='zoombox':
                if self._nav_stack() is None:
                    self.push_current()                
                real_x, real_y = event.x - self.pos[0], event.y - self.pos[1]
                self.draw_box(event, self.x_init,self.y_init, event.x, real_y)
                
            #mode cursor
            elif self.touch_mode=='cursor':
                self.hover_on=True
                self.hover(event)
                
            changed = True

        #note: avoid zoom in/out on touch mode zoombox
        if len(self._touches) == 1:#
            return changed
        
        # we have more than one touch... list of last known pos
        points = [Vector(self._last_touch_pos[t]) for t in self._touches
                  if t is not event]
        # add current touch last
        points.append(Vector(event.pos))

        # we only want to transform if the touch is part of the two touches
        # farthest apart! So first we find anchor, the point to transform
        # around as another touch farthest away from current touch's pos
        anchor = max(points[:-1], key=lambda p: p.distance(event.pos))

        # now we find the touch farthest away from anchor, if its not the
        # same as touch. Touch is not one of the two touches used to transform
        farthest = max(points, key=anchor.distance)
        if farthest is not points[-1]:
            return changed

        # ok, so we have touch, and anchor, so we can actually compute the
        # transformation
        old_line = Vector(*event.ppos) - anchor
        new_line = Vector(*event.pos) - anchor
        if not old_line.length():  # div by zero
            return changed

        if self.do_scale:
            #            scale = new_line.length() / old_line.length()
            scale = old_line.length() / new_line.length()
            new_scale = scale * self.scale
            if new_scale < self.scale_min:
                scale = self.scale_min / self.scale
            elif new_scale > self.scale_max:
                scale = self.scale_max / self.scale
                
            self.apply_zoom(scale, self.axes, anchor=anchor,new_line=new_line)

            changed = True
        return changed

    def on_motion(self,*args):
        '''Kivy Event to trigger mouse event on motion
           `enter_notify_event`.
        '''
        pos = args[1]
        newcoord = self.to_widget(pos[0], pos[1])
        x = newcoord[0]
        y = newcoord[1]
        inside = self.collide_point(x,y)
        if inside: 

            # will receive all motion events.
            if self.figcanvas and self.hover_instance:
                #avoid in motion if touch is detected
                if not len(self._touches)==0:
                    return
                FakeEvent.x=x
                FakeEvent.y=y
                self.hover(FakeEvent)

    def on_touch_down(self, event):
        """ Manage Mouse/touch press """
        x, y = event.x, event.y

        print('on_touch_down >>>' + str(x) + ' ' + str(y))

        if self.collide_point(x, y) and self.figure:
            if self.legend_instance:
                if self.legend_instance.box.collide_point(x, y):
                    if self.touch_mode!='drag_legend':
                        return False   
                    else:
                        event.grab(self)
                        self._touches.append(event)
                        self._last_touch_pos[event] = event.pos
                        if len(self._touches)>1:
                            #new touch, reset background
                            self.background=None
                            
                        return True 
                       
            if event.is_mouse_scrolling:
                if not self.disable_mouse_scrolling:
                    ax = self.axes
                    ax = self.axes
                    self.zoom_factory(event, ax, base_scale=1.2)
                return True

            elif event.is_double_tap:
                if not self.disable_double_tap:
                    self.home()
                return True
                  
            else:
                if self.touch_mode=='cursor':
                    self.hover_on=True
                    self.hover(event)                
                elif self.touch_mode=='zoombox':
                    real_x, real_y = x - self.pos[0], y - self.pos[1]
                    self.x_init=x
                    self.y_init=real_y
                   
                    self.draw_box(event, x, y, real_x, real_y) 
                 
                event.grab(self)
                self._touches.append(event)
                self._last_touch_pos[event] = event.pos
                if len(self._touches)>1:
                    #new touch, reset background
                    self.background=None
                    
                return True

        else:
            return False

    def on_touch_move(self, event):
        """ Manage Mouse/touch move while pressed """

        x, y = event.x, event.y

        if event.is_double_tap:
            if not self.disable_double_tap:
                self.home()               
            return True

        # scale/translate
        if event in self._touches and event.grab_current == self:

            if self.transform_with_touch(event):
                self.transform_with_touch(event)
            self._last_touch_pos[event] = event.pos

        # stop propagating if its within our bounds
        if self.collide_point(x, y):
            return True

    def on_touch_up(self, event):
        """ Manage Mouse/touch release """
        # remove it from our saved touches
        if event in self._touches and event.grab_state:
            event.ungrab(self)
            del self._last_touch_pos[event]
            self._touches.remove(event)
            if self.touch_mode=='pan' or self.touch_mode=='zoombox' or \
                self.touch_mode=='pan_x' or self.touch_mode=='pan_y' \
                or self.touch_mode=='adjust_x' or self.touch_mode=='adjust_y':   
                self.push_current()
                if self.interactive_axis:
                    if self.touch_mode=='pan_x' or self.touch_mode=='pan_y' \
                        or self.touch_mode=='adjust_x' or self.touch_mode=='adjust_y':
                        self.touch_mode='pan'
                    self.first_touch_pan=None

        x, y = event.x, event.y
        if abs(self._box_size[0]) > 1 or abs(self._box_size[1]) > 1 or self.touch_mode=='zoombox':
            self.reset_box()  
            if not self.collide_point(x, y) and self.do_update:
                #update axis lim if zoombox is used and touch outside widget
                self.update_lim()            
                
                ax=self.axes
                ax.figure.canvas.draw_idle()
                ax.figure.canvas.flush_events() 
                return True
            
        # stop propagating if its within our bounds
        if self.collide_point(x, y) and self.figure:

            if self.do_update:
                self.update_lim()      
                                             

            self.anchor_x=None
            self.anchor_y=None
            
            ax=self.axes
            self.background=None
            ax.figure.canvas.draw_idle()
            ax.figure.canvas.flush_events()                           
            
            self.calculate_defects()

            return True

    def apply_zoom(self, scale_factor, ax, anchor=(0, 0),new_line=None):
        """ zoom touch method """
                
        x = anchor[0]-self.pos[0]
        y = anchor[1]-self.pos[1]

        trans = ax.transData.inverted()
        xdata, ydata = trans.transform_point((x+new_line.x/2, y+new_line.y/2))        
        
        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim() 

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        if self.do_zoom_x:
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
        if self.do_zoom_y:
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])

        if self.fast_draw:   
            #use blit method            
            if self.background is None:
                self.background_patch_copy.set_visible(True)
                ax.figure.canvas.draw_idle()
                ax.figure.canvas.flush_events()                   
                self.background = ax.figure.canvas.copy_from_bbox(ax.figure.bbox)
                self.background_patch_copy.set_visible(False)  
            ax.figure.canvas.restore_region(self.background)
           
            for line in ax.lines:
                ax.draw_artist(line)
            ax.figure.canvas.blit(ax.bbox)
            ax.figure.canvas.flush_events()
        else:
            ax.figure.canvas.draw_idle()
            ax.figure.canvas.flush_events()           

    def apply_pan(self, ax, event, mode='pan'):
        """ pan method """
        
        trans = ax.transData.inverted()
        xdata, ydata = trans.transform_point((event.x-self.pos[0], event.y-self.pos[1]))
        xpress, ypress = trans.transform_point((self._last_touch_pos[event][0]-self.pos[0], self._last_touch_pos[event][1]-self.pos[1]))
        dx = xdata - xpress
        dy = ydata - ypress

        xleft,xright=self.axes.get_xlim()
        ybottom,ytop=self.axes.get_ylim()
        
        #check inverted data
        inverted_x = False
        if xleft>xright:
            inverted_x=True
            cur_xlim=(xright,xleft)
        else:
            cur_xlim=(xleft,xright)
        inverted_y = False
        if ybottom>ytop:
            inverted_y=True 
            cur_ylim=(ytop,ybottom)
        else:
            cur_ylim=(ybottom,ytop) 
        
        if self.interactive_axis and self.touch_mode=='pan' and not self.first_touch_pan=='pan':
            if (ydata < cur_ylim[0] and not inverted_y) or (ydata > cur_ylim[1] and inverted_y):
                left_anchor_zone= (cur_xlim[1] - cur_xlim[0])*.2 + cur_xlim[0]
                right_anchor_zone= (cur_xlim[1] - cur_xlim[0])*.8 + cur_xlim[0]
                if xdata < left_anchor_zone or xdata > right_anchor_zone:
                    mode = 'adjust_x'
                else:
                    mode = 'pan_x'
                self.touch_mode = mode
            elif (xdata < cur_xlim[0] and not inverted_x) or (xdata > cur_xlim[1] and inverted_x):
                bottom_anchor_zone=  (cur_ylim[1] - cur_ylim[0])*.2 + cur_ylim[0]
                top_anchor_zone= (cur_ylim[1] - cur_ylim[0])*.8 + cur_ylim[0]               
                if ydata < bottom_anchor_zone or ydata > top_anchor_zone:
                    mode = 'adjust_y'
                else:
                    mode= 'pan_y' 
                self.touch_mode = mode
            else:
                self.touch_mode = 'pan'

        if not mode=='pan_y' and not mode=='adjust_y':             
            if mode=='adjust_x':
                if self.anchor_x is None:
                    midpoint= (cur_xlim[1] + cur_xlim[0])/2
                    if xdata>midpoint:
                        self.anchor_x='left'
                    else:
                        self.anchor_x='right'
                if self.anchor_x=='left':                
                    if xdata> cur_xlim[0]:
                        cur_xlim -= dx/2
                        if inverted_x:
                            ax.set_xlim(cur_xlim[1],None)
                        else:
                            ax.set_xlim(None,cur_xlim[1])
                else:
                    if xdata< cur_xlim[1]:
                        cur_xlim -= dx/2
                        if inverted_x:
                            ax.set_xlim(None,cur_xlim[0])
                        else:
                            ax.set_xlim(cur_xlim[0],None)
            else:
                cur_xlim -= dx/2
                if inverted_x:
                    ax.set_xlim(cur_xlim[1],cur_xlim[0])
                else:
                    ax.set_xlim(cur_xlim)
                
        if not mode=='pan_x' and not mode=='adjust_x':
            if mode=='adjust_y':
                if self.anchor_y is None:
                    midpoint= (cur_ylim[1] + cur_ylim[0])/2
                    if ydata>midpoint:
                        self.anchor_y='top'
                    else:
                        self.anchor_y='bottom'               
                
                if self.anchor_y=='top':
                    if ydata> cur_ylim[0]:
                        cur_ylim -= dy/2 
                        if inverted_y:
                            ax.set_ylim(cur_ylim[1],None)
                        else:
                            ax.set_ylim(None,cur_ylim[1])
                else:
                    if ydata< cur_ylim[1]:
                        cur_ylim -= dy/2  
                        if inverted_y:
                            ax.set_ylim(None,cur_ylim[0]) 
                        else:
                            ax.set_ylim(cur_ylim[0],None)
            else:            
                cur_ylim -= dy/2
                if inverted_y:
                    ax.set_ylim(cur_ylim[1],cur_ylim[0])
                else:
                    ax.set_ylim(cur_ylim)

        if self.first_touch_pan is None:
            self.first_touch_pan=self.touch_mode

        if self.fast_draw: 
            #use blit method               
            if self.background is None:
                self.background_patch_copy.set_visible(True)
                ax.figure.canvas.draw_idle()
                ax.figure.canvas.flush_events()                   
                self.background = ax.figure.canvas.copy_from_bbox(ax.figure.bbox)
                self.background_patch_copy.set_visible(False)  
            ax.figure.canvas.restore_region(self.background)                
           
            for line in ax.lines:
                ax.draw_artist(line)
                
            ax.figure.canvas.blit(ax.bbox)
            ax.figure.canvas.flush_events() 
            
        else:
            ax.figure.canvas.draw_idle()
            ax.figure.canvas.flush_events()
            
    def apply_drag_legend(self, ax, event):
        """ drag legend method """
                        
        dx = event.x - self._last_touch_pos[event][0]
        if not self.legend_do_scroll_x:
            dx=0
        dy = event.y - self._last_touch_pos[event][1]      
        if not self.legend_do_scroll_y:
            dy=0        
        legend = ax.get_legend()
        if legend is not None:
        
            bbox = legend.get_window_extent()
            legend_x = bbox.xmin
            legend_y = bbox.ymin
               
            loc_in_canvas = legend_x +dx/2, legend_y+dy/2
            loc_in_norm_axes = legend.parent.transAxes.inverted().transform_point(loc_in_canvas)
            legend._loc = tuple(loc_in_norm_axes)
            
            #use blit method               
            if self.background is None:
                ax.get_legend().set_visible(False)
                ax.figure.canvas.draw_idle()
                ax.figure.canvas.flush_events()                   
                self.background = ax.figure.canvas.copy_from_bbox(ax.figure.bbox)
                ax.get_legend().set_visible(True)
            ax.figure.canvas.restore_region(self.background)   
    
            ax.draw_artist(legend)
                
            ax.figure.canvas.blit(ax.bbox)
            ax.figure.canvas.flush_events() 

            self.legend_instance.update_size()

    def zoom_factory(self, event, ax, base_scale=1.1):
        """ zoom with scrolling mouse method """

        newcoord = self.to_widget(event.x, event.y, relative=False)
        x = newcoord[0]
        y = newcoord[1]

        trans = ax.transData.inverted()
        xdata, ydata = trans.transform_point((x, y))     

        cur_xlim = ax.get_xlim()
        cur_ylim = ax.get_ylim()

        if event.button == 'scrolldown':
            # deal with zoom in
            scale_factor = 1 / base_scale
        elif event.button == 'scrollup':
            # deal with zoom out
            scale_factor = base_scale
        else:
            # deal with something that should never happen
            scale_factor = 1
            print(event.button)

        new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
        new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor

        relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
        rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

        if self.do_zoom_x:
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
        if self.do_zoom_y:
            ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])

        ax.figure.canvas.draw_idle()
        ax.figure.canvas.flush_events()    

    def _onSize(self, o, size):
        """ _onsize method """
        if self.figure is None:
            return
        # Create a new, correctly sized bitmap
        self._width, self._height = size
        self._isDrawn = False

        if self._width <= 1 or self._height <= 1:
            return

        dpival = self.figure.dpi
        winch = self._width / dpival
        hinch = self._height / dpival
        self.figure.set_size_inches(winch, hinch)
        self.figcanvas.resize_event()
        self.figcanvas.draw()  
        if self.legend_instance:
            self.legend_instance.update_size()
        if self.hover_instance:
            self.hover_instance.figwidth = self.width

    def update_lim(self):
        """ update axis lim if zoombox is used"""
        ax=self.axes

        self.do_update=False
        
        #check if inverted axis
        xleft,xright=self.axes.get_xlim()
        ybottom,ytop=self.axes.get_ylim()

        # print('x coordinates')
        # print(str(xleft) + ' ' + str(xright))
        # print('y coordinates')
        # print(str(ybottom) + ' ' + str(ytop))

        
        if xright>xleft:
            ax.set_xlim(left=min(self.x0_box,self.x1_box),right=max(self.x0_box,self.x1_box))
        else:
            ax.set_xlim(right=min(self.x0_box,self.x1_box),left=max(self.x0_box,self.x1_box))
        if ytop>ybottom:
            ax.set_ylim(bottom=min(self.y0_box,self.y1_box),top=max(self.y0_box,self.y1_box))
        else:
            ax.set_ylim(top=min(self.y0_box,self.y1_box),bottom=max(self.y0_box,self.y1_box))


    def calculate_defects(self):
        """ calculate total number of defects in the selected zoom area"""
       
        #check if inverted axis
        xleft,xright=self.axes.get_xlim()
        ybottom,ytop=self.axes.get_ylim()

        df = load_stitch_data()
        # print(df.head())

        # filter the DataFrame based on the input ranges
        subset = df.loc[(df['x'] >= xleft) & (df['x'] <= xright) & 
                        (df['y'] >= ybottom) & (df['y'] <= ytop)]
        
        # calculate the sum of the count of defects in the subset
        total_defects = subset['size'].count()

        print(f'Total defects for x range {xleft} to {xright} and y range {ybottom} to {ytop}: {total_defects}')
        self.axes.set_title('Wafer Map with Defects [' + str(total_defects) + ']')
        return total_defects
        


    def get_current_axes(self):
        return self.axes
        

    def reset_box(self):
        """ reset zoombox and apply zoombox limit if zoombox option if selected"""
        if min(abs(self._box_size[0]),abs(self._box_size[1]))>self.minzoom:
            trans = self.axes.transData.inverted()
            self.x0_box, self.y0_box = trans.transform_point((self._box_pos[0]-self.pos[0], self._box_pos[1]-self.pos[1])) 
            self.x1_box, self.y1_box = trans.transform_point((self._box_size[0]+self._box_pos[0]-self.pos[0], self._box_size[1]+self._box_pos[1]-self.pos[1]))
            self.do_update=True
            
        self._box_size = 0, 0
        self._box_pos = 0, 0
        self._alpha_box=0

        self._pos_x_rect_hor = 0
        self._pos_y_rect_hor = 0
        self._pos_x_rect_ver = 0
        self._pos_y_rect_ver = 0 
        self._alpha_hor=0 
        self._alpha_ver=0
        self.invert_rect_hor = False
        self.invert_rect_ver = False
        
    def draw_box(self, event, x0, y0, x1, y1) -> None:
        """ Draw zoombox method
        
        Args:
            event: touch kivy event
            x0: x coordonnate init
            x1: y coordonnate of move touch
            y0: y coordonnate init
            y1: x coordonnate of move touch
            
        Return:
            None
        """
        pos_x, pos_y = self.pos
        # Kivy coords
        y0 = pos_y + y0
        y1 = pos_y + y1
        
        if abs(y1-y0)>dp(5) or abs(x1-x0)>dp(5):
            self._alpha_box=0.3   
            self._alpha_rect=0
        
        trans = self.axes.transData.inverted()
        xdata, ydata = trans.transform_point((event.x-pos_x, event.y-pos_y)) 

        xleft,xright=self.axes.get_xlim()
        ybottom,ytop=self.axes.get_ylim()

         
        xmax = max(xleft,xright)
        xmin = min(xleft,xright)
        ymax = max(ybottom,ytop)
        ymin = min(ybottom,ytop)

        # print('Draw Box coordinates: Xleft-Xright ('+ str(xleft)+',' + str(xright) + ')' + ' Ybottom, Ytop ' + '('+ str(ybottom) +',' + str(ytop) + ')')
                
        #check inverted data
        inverted_x = False
        if xleft>xright:
            inverted_x=True
        inverted_y = False
        if ybottom>ytop:
            inverted_y=True        

        x0data, y0data = trans.transform_point((x0-pos_x, y0-pos_y)) 
         
        if x0data>xmax or x0data<xmin or y0data>ymax or y0data<ymin:
            return

        if xdata<xmin:
            x1_min = self.axes.transData.transform([(xmin,ymin)])
            if (x1<x0 and not inverted_x) or (x1>x0 and inverted_x):
                x1=x1_min[0][0]+pos_x
            else:
                x0=x1_min[0][0]

        if xdata>xmax:
            x0_max = self.axes.transData.transform([(xmax,ymin)])
            if (x1>x0 and not inverted_x) or (x1<x0 and inverted_x):
                x1=x0_max[0][0]+pos_x 
            else:
                x0=x0_max[0][0]                  

        if ydata<ymin:
            y1_min = self.axes.transData.transform([(xmin,ymin)])
            if (y1<y0 and not inverted_y) or (y1>y0 and inverted_y):
                y1=y1_min[0][1]+pos_y
            else:
                y0=y1_min[0][1]+pos_y

        if ydata>ymax:
            y0_max = self.axes.transData.transform([(xmax,ymax)])
            if (y1>y0 and not inverted_y) or (y1<y0 and inverted_y):
                y1=y0_max[0][1]+pos_y
            else:
                y0=y0_max[0][1]+pos_y
                
        if abs(x1-x0)<dp(20) and abs(y1-y0)>self.minzoom:
            self.pos_x_rect_ver=x0
            self.pos_y_rect_ver=y0   
            
            x1_min = self.axes.transData.transform([(xmin,ymin)])
            x0=x1_min[0][0]+pos_x

            x0_max = self.axes.transData.transform([(xmax,ymin)])
            x1=x0_max[0][0]+pos_x

            self._alpha_ver=1
            self._alpha_hor=0
                
        elif abs(y1-y0)<dp(20) and abs(x1-x0)>self.minzoom:
            self.pos_x_rect_hor=x0
            self.pos_y_rect_hor=y0  

            y1_min = self.axes.transData.transform([(xmin,ymin)])
            y0=y1_min[0][1]+pos_y
             
            y0_max = self.axes.transData.transform([(xmax,ymax)])
            y1=y0_max[0][1]+pos_y         

            self._alpha_hor=1
            self._alpha_ver=0
                        
        else:
            self._alpha_hor=0   
            self._alpha_ver=0

        if x1>x0:
            self.invert_rect_ver=False
        else:
            self.invert_rect_ver=True
        if y1>y0:
            self.invert_rect_hor=False
        else:
            self.invert_rect_hor=True
            
        self._box_pos = x0, y0
        self._box_size = x1 - x0, y1 - y0

class _FigureCanvas(FigureCanvasAgg):
    """Internal AGG Canvas"""

    def __init__(self, figure, widget, *args, **kwargs):
        self.widget = widget
        super(_FigureCanvas, self).__init__(figure, *args, **kwargs)

    def draw(self):
        """
        Render the figure using agg.
        """
        super(_FigureCanvas, self).draw()
        agg = self.get_renderer()
        w, h = agg.width, agg.height
        self._isDrawn = True

        self.widget.bt_w = w
        self.widget.bt_h = h
        self.widget._bitmap = agg.buffer_rgba()
        self.widget._draw_bitmap()

    def blit(self, bbox=None):
        """
        Render the figure using agg (blit method).
        """        
        agg = self.get_renderer()
        w, h = agg.width, agg.height
        self.widget._bitmap = agg.buffer_rgba()
        self.widget.bt_w = w
        self.widget.bt_h = h
        self.widget._draw_bitmap()

class FakeEvent:
    x:None
    y:None
    
from kivy.factory import Factory

Factory.register('MatplotFigure', MatplotFigure)

Builder.load_string('''
<MatplotFigure>
    canvas:
        Color:
            rgba: (1, 1, 1, 1)
        Rectangle:
            pos: self.pos
            size: self.size
            texture: self._img_texture
        Color:
            rgba: 0, 0, 1, self._alpha_box
        BorderImage:
            source: 'border.png'
            pos: self._box_pos
            size: self._box_size
            border:
                dp(1) if root.invert_rect_hor else -dp(1), \
                dp(1) if root.invert_rect_ver else -dp(1), \
                dp(1) if root.invert_rect_hor else -dp(1), \
                dp(1) if root.invert_rect_ver else -dp(1)
                
    canvas.after:            
        #horizontal rectangle left
		Color:
			rgba:0, 0, 0, self._alpha_hor
		Line:
			width: dp(1)
			rectangle:
				(self.pos_x_rect_hor+dp(1) if root.invert_rect_ver \
                 else self.pos_x_rect_hor-dp(4),self.pos_y_rect_hor-dp(20), dp(4),dp(40))            

        #horizontal rectangle right
		Color:
			rgba:0, 0, 0, self._alpha_hor
		Line:
			width: dp(1)
			rectangle:
				(self.pos_x_rect_hor-dp(4)+self._box_size[0] if root.invert_rect_ver \
                 else self.pos_x_rect_hor+dp(1)+self._box_size[0], self.pos_y_rect_hor-dp(20), dp(4),dp(40))             

        #vertical rectangle bottom
		Color:
			rgba:0, 0, 0, self._alpha_ver
		Line:
			width: dp(1)
			rectangle:
				(self.pos_x_rect_ver-dp(20),self.pos_y_rect_ver+dp(1) if root.invert_rect_hor else \
                 self.pos_y_rect_ver-dp(4), dp(40),dp(4))            

        #vertical rectangle top
		Color:
			rgba:0, 0, 0, self._alpha_ver
		Line:
			width: dp(1)
			rectangle:
				(self.pos_x_rect_ver-dp(20),self.pos_y_rect_ver-dp(4)+self._box_size[1] \
                 if root.invert_rect_hor else self.pos_y_rect_ver+dp(1)+self._box_size[1], \
                 dp(40),dp(4))
        ''')
