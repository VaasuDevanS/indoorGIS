# indoorGIS

[University of New Brunswick, Fredericton](https://www.unb.ca/) | [Web-App Link](https://indoorgis.pythonanywhere.com/)

Directed Research Project - Summer (2019) <br />
Study Area: HeadHall - [Link](https://www.google.com/maps/place/Head+Hall,+NB-1,+Fredericton,+NB/@45.9496034,-66.6424096,18.75z/data=!4m5!3m4!1s0x4ca4220f063c4685:0xd90a16a19db56df7!8m2!3d45.949433!4d-66.6421681 "View in Google Maps")

**Short description:** WebApp for finding Faculties, Facilities, Routing and more <br />
**Supervisor:** [Shabnam Jabari](https://www.unb.ca/faculty-staff/directory/engineering-geomatics/jabari-shabnam.html)


| Package     | Reference                                                                               | Version                |
| ----------- | --------------------------------------------------------------------------------------- | ---------------------- |
| Django      | [https://www.djangoproject.com/](https://www.djangoproject.com/)                        | 2.1                    |
| Networkx    | [https://networkx.github.io/](https://networkx.github.io/)                              | 2.1                    |
| Geopandas   | [https://geopandas.org/](http://geopandas.org/)                                         | 0.5.0 (pandas: 0.24.2) |
| Leaflet     | [https://leafletjs.com](https://leafletjs.com)                                          | 1.5.1                  |
| Jquery      | [https://jquery.com/](https://jquery.com/)                                              | 3.3.1                  |
| Bootstrap   | [https://getbootstrap.com/](https://getbootstrap.com/)                                  | 3.3.7                  |
| Metismenu   | [https://mm.onokumus.com/](https://mm.onokumus.com/)                                    | 3.0.4                  |
| FontAwesome | [https://fontawesome.com/](https://fontawesome.com/)                                    | 5.9.0                  |
| W3          | [https://www.w3schools.com/w3css/](https://www.w3schools.com/w3css/w3css_downloads.asp) | 4.13                   |

### Georeferencing
To obtain geo-referenced tiff with the Plan images, the following [gdal_translate](https://gdal.org/programs/gdal_translate.html) command was used
```console
gdal_translate -of GTiff -a_ullr 0 90 180 0 -a_srs EPSG:4326 x_Level.jpg x_Level.tiff
```

### Commit log
***

**v4.0 (Aug 27, 2019)** [Video](https://raw.githubusercontent.com/VaasuDevanS/indoorGIS/master/log/HeadHall/IndoorGIS-Mobile.mp4)
* Statistics Model for understanding the app usage (50% done)
* CSS for Mobile screen sizes ([template](https://www.w3schools.com/w3css/tryit.asp?filename=tryw3css_examples_home2))
* Replaced Slick Carousel with Bootstrap Carousel because of mobile display issues

***

**Commit 4 - v3.1 (July 5, 2019)** [Video](https://raw.githubusercontent.com/VaasuDevanS/indoorGIS/master/log/HeadHall/IndoorGIS-v3.1.mp4)
* Categories menu for Facilities, Faculties and more using MetisMenu JS and FontAwesome CSS
* Fixed null value display, zoom and other bugs

***known issues***
* Shortest path through the blocks

***

**Commit 3 - v3.0 (July 3, 2019)** [Video](https://raw.githubusercontent.com/VaasuDevanS/indoorGIS/master/log/HeadHall/IndoorGIS-v3.0.mp4)
* Added the remaining levels (B, C, D); Displayed using Slick JS Carousel
* Search functionality and editable model for all the levels
* Removed onClick routing functionality and modified to open popup
* Added the 'about' modal

***known issues***
* Shortest path through the blocks

***

**Commit 2 - v2.0 (June 28, 2019)** [Video](https://raw.githubusercontent.com/VaasuDevanS/indoorGIS/master/log/HeadHall/IndoorGIS-v2.0.mp4)
* Created commit log and superuser for the admin portal
* Editable model for the Blocks in admin page (\<URL>/admin will create model objects)
* Added Tab-Icon,Field clear (X) and button images (Clear, Search and Routing)
* Search / Directions within the Web App
* JSON and Fields via JQuery-Ajax and python
* Fixed the incorrect network on the South-East side

***known issues***
* Shortest path through the blocks

***

**Commit 1 - v1.0 (June 18, 2019)** [Video](https://raw.githubusercontent.com/VaasuDevanS/indoorGIS/master/log/HeadHall/IndoorGIS-v1.0.mp4)

* Div showing E-Level, Blocks and Route for GGE side
* Display routes and zoom to extent for the selected two blocks and route
* Clear button to clear the route and selected blocks, default extent

***known issues***
* Incorrect Network on the South-East side
* Shortest path through the blocks

***