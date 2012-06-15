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

import gconf

from gi.repository import GObject, Peas

toolbar_button_key = 'toolbar_button'
context_menu_key = 'context_menu'

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



class JumpToPlaying(GObject.GObject, Peas.Activatable):
	__gtype_name = 'JumpToPlaying'
	object = GObject.property(type=GObject.GObject)

	def __init__(self):
		GObject.GObject.__init__(self)

		
	def update_ui (self):

		uim = self.shell.props.ui_manager

		self.ui_tb = uim.add_ui_from_string(ui_toolbar_button)		
		self.ui_cm = uim.add_ui_from_string(ui_context_menu)
		
		uim.ensure_update()


	def do_activate (self):
		self.shell = self.object
		
		uim = self.shell.props.ui_manager	

		self.ui_tb = None
		self.ui_cm = None
		self.update_ui()

		# hide the button in Small Display mode
		# Since Rhythmbox 2.97 there is no longer a SmallDisplayMode, but for now we keep it for compatibility 
		try:
				small_display_toggle = uim.get_widget ("/MenuBar/ViewMenu/ViewSmallDisplayMenu")
				tb_widget = uim.get_widget ("/ToolBar/PluginPlaceholder/ToolBarJumpToPlaying")
				self.tb_conn_id = small_display_toggle.connect ('toggled', self.hide_if_active, tb_widget)
		except:
			pass

		# start hidden if in small_display
		is_small = gconf.client_get_default().get_bool("/apps/rhythmbox/ui/small_display")
		if (is_small):
			tb_widget.hide()

	
	def do_deactivate (self):
		
		uim = self.shell.props.ui_manager
		
		if (self.ui_tb != None):
			uim.remove_ui(self.ui_tb)
			del self.ui_tb
		if (self.ui_cm != None):
			uim.remove_ui(self.ui_cm)
			del self.ui_cm
		try:
			small_display_toggle = uim.get_widget ("/MenuBar/ViewMenu/ViewSmallDisplayMenu")
			small_display_toggle.disconnect (self.tb_conn_id)
		except:
			pass
		uim.ensure_update()


	def hide_if_active (self, toggle_widget, ui_element):
		"Hides ui_element if toggle_widget is active."
		
		if (toggle_widget.get_active()):
			ui_element.hide()
			
		else:
			ui_element.show()
