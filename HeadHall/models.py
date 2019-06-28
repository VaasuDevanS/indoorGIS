# Django import
from django.db import models

# Project import
from indoorGIS.settings import STATIC_ROOT as static

# Module imports
import geopandas as gpd
import os

HeadHall = os.path.join(static, "HeadHall", "SHPs")


class ELevel(models.Model):

    class Meta:
        verbose_name_plural = "ELevel"

    OBJECTID = models.IntegerField(primary_key=True, editable=False)
    PlaceNode = models.IntegerField()
    PlaceName = models.CharField(max_length=50, null=True, blank=True)
    PersonName = models.CharField(max_length=50, null=True, blank=True)
    Contact = models.CharField(max_length=20, null=True, blank=True)
    Email = models.CharField(max_length=20, null=True, blank=True)
    Details = models.CharField(max_length=200, null=True, blank=True)
    geometry = models.TextField(editable=False)

    # Read the blks file once and reuse
    blks = gpd.read_file(os.path.join(HeadHall, "E_Level_Blocks"))


    def save(self, *args, **kwargs):
        """
        Overriding the Django's default save mechanism to update shp
        """

        # Save the GeoPandas OBJECTID for quicker calculations
        oID = self.blks.OBJECTID

        # Get the record from eBlocks
        flds = ["PlaceNode", "PlaceName", "PersonName",
                "Contact", "Email", "Details"]
        eBlkRcrd = self.blks[oID==self.OBJECTID][flds]

        # Construct a new dataframe from the passed object
        tmpRcrd = gpd.GeoDataFrame({f:[getattr(self,f)] for f in flds})

        # If values are updated, update the SHP as well
        if not (eBlkRcrd.values==tmpRcrd.values).all():
            for f in flds:
                self.blks.loc[ (oID==self.OBJECTID), f ] = getattr(self, f)
            self.blks.to_file(os.path.join(HeadHall, "E_Level_Blocks"))

        # Save the model
        super().save(*args, **kwargs)

# EOF