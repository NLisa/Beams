#!/usr/bin/env python

#import sys
#import scipy as S
#import scipy.misc.pilutil
#import matplotlib.cm
from traits.api import HasTraits, Instance, DelegatesTo, Button, Enum, Str
from traitsui.api import View, HSplit, Tabbed, HGroup, VGroup, Item, Label

from Camera import *
from DummyGaussian import *
#from CameraImage import *
#from AwesomeColorMaps import awesome, isoluminant
#from ColorMapIndicator import *
#from CameraDialog import *
#from DeltaDetector import *
#from MinMaxDisplay import *
#from BeamProfiler import *

class MainWindow(HasTraits):
    '''The main window for the Beams application.'''

    # Current folder for file dialog
    _current_folder = None

    camera = Instance(Camera)
    id_string = DelegatesTo('camera')
    resolution = DelegatesTo('camera')
    frame_rate = DelegatesTo('camera')
    color_scale = Enum('a', 'b')
    rotation_angle = Enum(0, 90, 180, 270)
    status = Str()

    find_resolution = Button()
    view = View(
        VGroup(
            HSplit(
                Tabbed(
                    VGroup(
                        Item('id_string', style='readonly', show_label=False),
                        HGroup(
                            Item('resolution'),
                            Item('find_resolution', show_label=False)),
                        HGroup(
                            Item('frame_rate', style='custom'),
                            Label('fps')),
                        label='Camera'
                    ),
                    VGroup(
                        Item('color_scale'),
                        label='Video'
                    ),
                    VGroup(
                        Item('rotation_angle'),
                        label='Transform'
                    ),
                    VGroup(label='Math'),
                    VGroup(label='Cross-section')
                )
            ),
            Item('status', style='readonly', show_label=False)
        )
    )

    def __init__(self):
        self.camera = DummyGaussian()

#    # Signal handlers
#    def action_about(self, action, data=None):
#        self.about_window.present()
#    
#    def action_save(self, action, data=None):
#        # First make a copy of the frame we will save
#        save_frame = self.webcam.frame.copy()
#        
#        # Then find out where to save it
#        dialog = gtk.FileChooserDialog('Save Image', self.main_window,
#            gtk.FILE_CHOOSER_ACTION_SAVE,
#            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
#            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
#        try:
#            dialog.set_current_folder(self._current_folder)
#        except TypeError:
#            pass  # thrown if current folder is None
#        response = dialog.run()
#        path = dialog.get_filename()
#        
#        # Store the directory for the next time
#        self._current_folder = dialog.get_current_folder()
#        
#        dialog.destroy()
#        if response != gtk.RESPONSE_ACCEPT:
#            return
#        
#        # Default is PNG
#        if '.' not in path:
#            path += '.png'

#        # Save it
#        S.misc.imsave(path, save_frame)
#    
#    def action_choose_camera(self, action, data=None):
#        self.cameras_dialog.show()
#    
#    def action_configure_camera(self, action, data=None):
#        self.webcam.configure()
 
    def _find_resolution_fired(self):
        pass

#    def action_take_video(self, action, data=None):
#        # Set the 'Take Photo' action insensitive if 'Take Video' is on
#        self.actiongroup.get_action('take_photo').set_sensitive(not action.get_active())
#        
#        if action.get_active():
#            self.idle_id = glib.idle_add(self.image_capture)
#        else:
#            glib.source_remove(self.idle_id)
#    
#    def action_take_photo(self, action, data=None):
#        self.image_capture()
#    
#    def action_quit(self, action, data=None):
#        gtk.main_quit()
#    
#    def on_rotate_box_changed(self, combo, data=None):
#        self.screen.rotate = combo.props.active
#    
#    def on_detect_toggle_toggled(self, box, data=None):
#        self.delta.active = box.props.active

#    def on_minmax_toggle_toggled(self, box, data=None):
#        self.minmax.active = box.props.active

#    def on_profiler_toggle_toggled(self, box, data=None):
#        self.profiler.active = box.props.active
#    
#    def on_delta_threshold_value_changed(self, spin, data=None):
#        self.delta.threshold = spin.props.value

#    available_colormaps = {
#        0: None,
#        1: matplotlib.cm.gray,
#        2: matplotlib.cm.bone,
#        3: matplotlib.cm.pink,
#        4: matplotlib.cm.jet,
#        5: isoluminant,
#        6: awesome
#    }

#    def on_colorscale_box_changed(self, combo, data=None):
#        cmap_index = self.available_colormaps[combo.props.active]
#        self.screen.cmap = cmap_index
#        self.cmap_sample.cmap = cmap_index

#    def on_cameras_response(self, dialog, response_id, data=None):
#        self.cameras_dialog.hide()
#        
#        if response_id == gtk.RESPONSE_CLOSE:
#            info = self.cameras_dialog.get_plugin_info()
#            self.select_plugin(*info)
#    
#    # Image capture timeout
#    def image_capture(self):
#        try:
#            self.webcam.query_frame()
#        except CameraError:
#            errmsg = gtk.MessageDialog(parent=self.main_window, 
#                flags=gtk.DIALOG_MODAL, 
#                type=gtk.MESSAGE_ERROR,
#                buttons=gtk.BUTTONS_CLOSE,
#                message_format='There was an error reading from the camera.')
#            errmsg.run()
#            sys.exit()
#            
#        self.screen.data = self.webcam.frame
#        
#        # Send the frame to the processing components
#        if self.delta.active:
#            self.delta.send_frame(self.webcam.frame)
#        if self.minmax.active:
#            self.minmax.send_frame(self.webcam.frame)
#        if self.profiler.active:
#            self.profiler.send_frame(self.webcam.frame)

#        return True  # keep the idle function going
#    
#    # Select camera plugin
#    def select_plugin(self, module_name, class_name):
#        self._camera_module = __import__(module_name)
#        self._camera_class = getattr(self._camera_module, class_name)

#        # Set up image capturing
#        self.webcam = self._camera_class(cam=0) # index of camera to be used
#        try:
#            self.webcam.open()
#        except CameraError:
#            errmsg = gtk.MessageDialog(parent=self.main_window, 
#                flags=gtk.DIALOG_MODAL, 
#                type=gtk.MESSAGE_ERROR,
#                buttons=gtk.BUTTONS_CLOSE,
#                message_format='No camera was detected. Did you forget to plug it in?')
#            errmsg.run()
#            sys.exit()
#        
#        # Set up resolution box
#        self.resolutions.clear()
#        for (w, h) in self.webcam.find_resolutions():
#            it = self.resolutions.append(['{0} x {1}'.format(w, h), w, h])
#        self.resolution_box.props.active = 0
#        
#        # Change camera info label
#        self.camera_label.props.label = \
#            'Camera: {}'.format(self.webcam.id_string)

#    def __init__(self):
#        # Load our user interface definition
#        builder = gtk.Builder()
#        builder.add_from_file('../data/Beams.ui')

#        # Load our menu/toolbar definition
#        manager = gtk.UIManager()
#        manager.add_ui_from_file('../data/menus.xml')

#        # Add all the actions to an action group for the menu and toolbar
#        self.actiongroup = builder.get_object('actiongroup')
#        manager.insert_action_group(self.actiongroup)

#        # Build the window
#        self.main_window = builder.get_object('main_window')
#        self.main_window.get_child().pack_start(manager.get_widget('/menubar'), expand=False)
#        self.main_window.get_child().pack_start(manager.get_widget('/toolbar'), expand=False)
#        
#        self.screen = CameraImage()
#        self.screen.set_size_request(640, 480)
#        builder.get_object('main_hbox').pack_start(self.screen)
#        
#        self.cmap_sample = ColorMapIndicator()
#        self.cmap_sample.set_size_request(128, 10)
#        builder.get_object('colorscale_vbox').pack_start(self.cmap_sample)

#        # Build the camera selection dialog box
#        self.cameras_dialog = CameraDialog()
#        self.cameras_dialog.connect('response', self.on_cameras_response)
#        
#        # Build the beam profiler
#        self.profiler = BeamProfiler(self.screen)
#        builder.get_object('profiler_toggle').props.active = self.profiler.active

#        # Build the min-max display
#        self.minmax = MinMaxDisplay(self.screen)
#        builder.get_object('minmax_toggle').props.active = self.minmax.active

#        # Build the delta detector
#        self.delta = DeltaDetector(self.screen)
#        builder.get_object('detect_toggle').props.active = self.delta.active
#        builder.get_object('delta_threshold').props.value = self.delta.threshold

#        # Save pointers to other widgets
#        self.about_window = builder.get_object('about_window')
#        self.colorscale_box = builder.get_object('colorscale_box')
#        self.resolution_box = builder.get_object('resolution_box')
#        self.resolutions = builder.get_object('resolutions')
#        self.camera_label = builder.get_object('camera_label')
#        self.current_delta = builder.get_object('current_delta')

#        # Open the default plugin
#        info = self.cameras_dialog.get_plugin_info()
#        try:
#            self.select_plugin(*info)
#        except ImportError:
#            # some module was not available, select the dummy
#            self.cameras_dialog.select_fallback()
#            info = self.cameras_dialog.get_plugin_info()
#            self.select_plugin(*info)

#        # Connect the signals last of all
#        builder.connect_signals(self, self)

if __name__ == '__main__':
    mainwin = MainWindow()
    mainwin.configure_traits()
