# Django import
from django.db import models

# Project import
from indoorGIS.settings import STATIC_ROOT as static

# Module imports
import geopandas as gpd
from os.path import join


class Level(models.Model):

    OBJECTID = models.IntegerField(primary_key=True, editable=False)
    PlaceNode = models.IntegerField()
    PlaceName = models.CharField(max_length=50, null=True, blank=True)
    PersonName = models.CharField(max_length=50, null=True, blank=True)
    Contact = models.CharField(max_length=20, null=True, blank=True)
    Email = models.CharField(max_length=50, null=True, blank=True)
    Details = models.CharField(max_length=200, null=True, blank=True)
    geometry = models.TextField(editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Overriding the Django's default save mechanism to update shp
        """

        # Save the GeoPandas OBJECTID for quicker calculations
        oID = self.blks.OBJECTID

        # Get the record from eBlocks
        flds = ["PlaceNode", "PlaceName", "PersonName",
                "Contact", "Email", "Details"]
        eBlkRcrd = self.blks[oID == self.OBJECTID][flds]

        # Construct a new dataframe from the passed object
        tmpRcrd = gpd.GeoDataFrame({f: [getattr(self, f)] for f in flds})

        # If values are updated, update the SHP as well
        if not (eBlkRcrd.values == tmpRcrd.values).all():
            for f in flds:
                self.blks.loc[(oID == self.OBJECTID), f] = getattr(self, f)
            self.blks.to_file(self.blkFile)

        # Save the model
        super().save(*args, **kwargs)


class ELevel(Level):

    class Meta:
        verbose_name_plural = "ELevel"

    blkFile = join(static, "HeadHall", "SHPs", "E_Level_Blocks")
    blks = gpd.read_file(blkFile)


class DLevel(Level):

    class Meta:
        verbose_name_plural = "DLevel"

    blkFile = join(static, "HeadHall", "SHPs", "D_Level_Blocks")
    blks = gpd.read_file(blkFile)


class CLevel(Level):

    class Meta:
        verbose_name_plural = "CLevel"

    blkFile = join(static, "HeadHall", "SHPs", "C_Level_Blocks")
    blks = gpd.read_file(blkFile)


class BLevel(Level):

    class Meta:
        verbose_name_plural = "BLevel"

    blkFile = join(static, "HeadHall", "SHPs", "B_Level_Blocks")
    blks = gpd.read_file(blkFile)


# EOF
