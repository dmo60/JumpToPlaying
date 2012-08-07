# original author: Steven Brown
# Rhythmbox3 port: Timo Loewe

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import GObject
from gi.repository import Peas
from gi.repository import Gio
from gi.repository import PeasGtk
from gi.repository import Gtk


ui_toolbar_button = """
<ui>
  <toolbar name="ToolBar">
    <placeholder name="PluginPlaceholder">
      <toolitem name="ToolBarJumpToPlaying" action="ViewJumpToPlaying"/>
    </placeholder>
  </toolbar>
</ui>

"""


ui_context_menu = """
<ui>

  <popup name="BrowserSourceViewPopup">
     <placeholder name="PluginPlaceholder">
         <menuitem name="BrowserPopupJumpToPlaying" action="ViewJumpToPlaying"/>
     </placeholder>
  </popup>

  <popup name="PlaylistViewPopup">
     <placeholder name="PluginPlaceholder">
         <menuitem name="BrowserPopupJumpToPlaying" action="ViewJumpToPlaying"/>
     </placeholder>
  </popup>


  <popup name="QueuePlaylistViewPopup">
     <placeholder name="PluginPlaceholder">
         <menuitem name="BrowserPopupJumpToPlaying" action="ViewJumpToPlaying"/>
     </placeholder>
  </popup>

  <popup name="PodcastViewPopup">
     <placeholder name="PluginPlaceholder">
         <menuitem name="BrowserPopupJumpToPlaying" action="ViewJumpToPlaying"/>
     </placeholder>
  </popup>

</ui>

"""

DCONF_DIR = 'org.gnome.rhythmbox.plugins.jumptoplaying'


class JumpToPlaying(GObject.Object, Peas.Activatable, PeasGtk.Configurable):
    __gtype_name = 'JumpToPlaying'
    object = GObject.property(type=GObject.Object)

    def __init__(self):
        GObject.Object.__init__(self)
        self.settings = Gio.Settings(DCONF_DIR)


    def do_activate(self):
        self.shell = self.object
        self.first_run = True

        rb_settings = Gio.Settings("org.gnome.rhythmbox")
        
        uim = self.shell.props.ui_manager    

        self.ui_tb = None
        self.ui_cm = None
        self.update_ui()
        
        # Watch for setting changes
        self.skc_id = self.settings.connect('changed', self.settings_changed)

        # hide the button in Small Display mode
        # Since Rhythmbox 2.97 there is no longer a SmallDisplayMode, but for now we keep it for compatibility 
        try:
            small_display_toggle = uim.get_widget ("/MenuBar/ViewMenu/ViewSmallDisplayMenu")
            tb_widget = uim.get_widget ("/ToolBar/PluginPlaceholder/ToolBarJumpToPlaying")
            self.tb_conn_id = small_display_toggle.connect ('toggled', self.hide_if_active, tb_widget)

            # start hidden if in small_display
            is_small = rb_settings["small-display"]
            if (is_small):
                tb_widget.hide()
        except:
            #print "No SmallDisplayMode anymore (since Rhythmbox 2.97)"
            pass

    
    def do_deactivate(self):
        
        uim = self.shell.props.ui_manager
        self.settings.disconnect(self.skc_id)
        
        if (self.ui_tb != None):
            uim.remove_ui(self.ui_tb)
            del self.ui_tb
        if (self.ui_cm != None):
            uim.remove_ui(self.ui_cm)
            del self.ui_cm
        try:
            small_display_toggle = uim.get_widget ("/MenuBar/ViewMenu/ViewSmallDisplayMenu")
            small_display_toggle.disconnect(self.tb_conn_id)
        except:
            pass
        uim.ensure_update()
        
    
    def update_ui(self):

        uim = self.shell.props.ui_manager

        self.ui_tb = uim.add_ui_from_string(ui_toolbar_button)        
        self.ui_cm = uim.add_ui_from_string(ui_context_menu)
        
        tb_widget = uim.get_widget ("/ToolBar/PluginPlaceholder/ToolBarJumpToPlaying")
        
        if self.first_run:
            self.default_label = tb_widget.get_label()
            self.first_run = False
                
        if self.settings["use-custom-label"]:
            tb_widget.set_label(self.settings["label-text"])
        else:
            tb_widget.set_label(self.default_label)
        
        uim.ensure_update()
        
    
    def settings_changed(self, settings, key):
        self.update_ui()


    def hide_if_active(self, toggle_widget, ui_element):
        "Hides ui_element if toggle_widget is active."
        
        if (toggle_widget.get_active()):
            ui_element.hide()
        else:
            ui_element.show()
    
    
    def do_create_configure_widget(self):
        dialog = Gtk.VBox()
        
        # switch for use-custom-label
        hbox = Gtk.HBox()
        switch = Gtk.Switch()
        switch.set_active(self.settings["use-custom-label"])
        switch.connect("notify::active", self.switch_toggled)
        
        label = Gtk.Label()
        label.set_text("Use custom label")
        
        hbox.pack_start(label, False, False, 5)
        hbox.pack_start(switch, False, False, 5)
        dialog.pack_start(hbox, False, False, 5)
        
        # entry for label-text
        hbox = Gtk.HBox()
        entry = Gtk.Entry()
        entry_buffer = Gtk.EntryBuffer()
        entry_buffer.set_text(self.settings["label-text"], len(self.settings["label-text"]))
        entry_buffer.connect("inserted-text", self.label_edited)
        entry_buffer.connect("deleted-text", self.label_edited)
        entry.set_buffer(entry_buffer)
        
        
        label = Gtk.Label()
        label.set_text("Label text")
        
        hbox.pack_start(label, False, False, 5)
        hbox.pack_start(entry, False, False, 5)
        dialog.pack_start(hbox, False, False, 5)
        
        dialog.set_size_request(300, -1)
        
        return dialog
    
    
    def switch_toggled(self, switch, active):
        self.settings["use-custom-label"] = switch.get_active()
        
    
    def label_edited(self, entry_buffer, *args):
        self.settings["label-text"] = entry_buffer.get_text()
    
    
        
