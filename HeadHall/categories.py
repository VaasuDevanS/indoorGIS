# Module imports
import geopandas as gpd


# Common
university = "<span class='fas fa-university'></span>"

# Facilities
archive = "<span class='fas fa-archive'></span>"
fac = {"utensils": "<span class='fas fa-utensils'></span>",
       "male": "<span class='fas fa-male'></span>",
       "female": "<span class='fas fa-female'></span>",
       "tint": "<span class='fas fa-tint'></span>",
       "coffee": "<span class='fas fa-coffee'></span>",
       "book": "<span class='fas fa-book'></span>",
       }

# Faculties
user = "<span class='fas fa-user'></span>"
briefcase = "<span class='fas fa-briefcase'></span>"

# Classrooms
chalk_board_teacher = "<span class='fas fa-chalkboard-teacher'></span>"
chalk_board = "<span class='fas fa-chalkboard'></span>"

# Labs
server = "<span class='fas fa-server'></span>"
desktop = "<span class='fas fa-desktop'></span>"

# Offices
store = "<span class='fas fa-store'></span>"
stamp = "<span class='fas fa-stamp'></span>"


def categorize(blkFile, lvl_ix, lvl):

    def res_html(res, icon):

        nonlocal html
        result = res.itertuples(index=False, name=None)
        for oId, name in sorted(result, key=lambda x: x[1]):
            a = """<a href='#' onclick="searchFunc('%s')">""" % [oId, lvl_ix]
            html += "<li> %s %s &nbsp; %s </a> </li>" % (a, icon, name)
        html += "</ul> </li>"

    blk = gpd.read_file(blkFile)
    html = "<li> <a href='#'> %s %s </a> <ul>" % (university, lvl)

    # Facilities
    html += "<li> <a href='#'> %s Facilities </a> <ul>" % archive
    query_res = blk[blk.PlaceType.str.startswith("Facility", na=False)]
    result = query_res[["OBJECTID", "PlaceName", "PlaceType"]]

    for oId, name, facility in result.itertuples(index=False, name=None):
        icon = fac[facility.split(",")[1]]
        a = """<a href='#' onclick="searchFunc('%s')">""" % [oId, lvl_ix]
        html += "<li> %s %s &nbsp; %s </a> </li>" % (a, icon, name)
    html += "</ul> </li>"

    # Faculties
    html += "<li> <a href='#'> %s Faculties </a> <ul>" % user
    res = blk.query("PlaceType=='Faculty'")[["OBJECTID", "PersonName"]]
    res_html(res, briefcase)

    # ClassRooms
    html += "<li> <a href='#'> %s Classrooms </a> <ul>" % chalk_board_teacher
    res = blk.query("PlaceType=='Classroom'")[["OBJECTID", "PlaceName"]]
    res_html(res, chalk_board)

    # Labs
    html += "<li> <a href='#'> %s Labs </a> <ul>" % server
    res = blk.query("PlaceType=='Lab'")[["OBJECTID", "PlaceName"]]
    res_html(res, desktop)

    # Offices
    html += "<li> <a href='#'> %s Offices </a> <ul>" % store
    res = blk.query("PlaceType=='Office'")[["OBJECTID", "PlaceName"]]
    res_html(res, stamp)

    html += "</ul> </li>"
    return html


# EOF
