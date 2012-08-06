# install schema
sudo cp ./org.gnome.rhythmbox.plugins.jumptoplaying.gschema.xml /usr/share/glib-2.0/schemas/
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

# install plugin
mkdir -p ~/.local/share/rhythmbox/plugins/
rm -r -f ~/.local/share/rhythmbox/plugins/JumpToPlaying/
cp -r ./JumpToPlaying/ ~/.local/share/rhythmbox/plugins/
