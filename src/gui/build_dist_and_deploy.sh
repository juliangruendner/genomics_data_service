npm run env -s && ng build --prod --base-href=/
rm gemini_gui.zip
zip -r gemini_gui.zip dist/
cp gemini_gui.zip ../gui_server