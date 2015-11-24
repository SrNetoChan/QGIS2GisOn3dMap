#QGIS2GisOn3dMap

##Description
QGIS Python Plugin that works as a client for gison3dmap projection system.
Sends layers definitions writen in gison3dmap syntax and XML to a remote host, allowing to project QGIS map canvas
layers into a 3d scale model.

##Installation

###Linux
On linux machines, use the terminal to the local repository root directory and run:

`Make deploy`
 
This will automaticly copy all needed files into the user's QGIS Plugin folder
(~/.qgis2/python/plugins/gison3dmap).

###Windows
Copy all files into the user's QGIS Plugin folder on a folder called gison3dmap
(c:\users\name_of_user\.qgis2\python\plugins\gison3dmap)

**Note**: After instalation, make sure that the plugin is active in QGIS. Use `Plugin > Install and manage Plugins`
Search for gison3dmap and check the corresponding checkbox.

**Note 2**: To make installation easier and equal to all users, it's recommended the creation of a QGIS Plugins Repository.

##Usage

Once the plugin is installed, there will be a toolbar with all gison3dmap tools. If not visible, activate it in `View > Toolbars > gison3dmap`.

## Plugin Structure and functionality

### Structure
The plugin main structure is as explained below.  
```
gison3dmap/
|-- icons/
|-- tools/
```
Other subfolders were created automaticly by QGIS Plugin Builder to provide support, but were not
fully implemented. They are useless for now, but were kept for future developing

```
gison3dmap/
|-- help/     --To build help files and documentation
|-- i18n/     --To allow translations
|-- scripts/  --Several script for deploying and publish the plugin
|-- test/     --Unit tests
```

### Current functionality and limitations

The plugin is able to project the following QGIS **Vector Layers Renderers**:
- singleSymbol;
- categorizedSymbol;
- graduatedSymbol.

Which symbols are within the following group:
- simpleMarker;
- simpleLine;
- simpleFill.

**Note**: Although QGIS allow combining several symbols layer to draw a layer, gison3dmap only accpets one symbol. Therefore, in multi layered symbols, only the top one is used. 

The plugin is able to project the following QGIS **Raster Layers Renderers**:
- singlebandpseudocolor
- singlebandgray

#### Know Issues
- Dash patterns were not implemented;
- Vector data provider is hardcoded as Shapefiles, no other providers were implemented (e.g. PostgreSQL);
- Labels, labels buffers and labels background colors are are coded and cannot be set;
- QGIS Hatches are designed differently from gison3dmap hatches (while one prints a color with black patterns on top, the other prints the colored patterns). Therefore, symbols using hatches probably won't  look the same when projected;
