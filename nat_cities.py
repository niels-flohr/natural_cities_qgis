#----------------------------------------------------------------------------------------
# Natural Cities Algorithm                                                              #
#                                                                                       #
# Creates Natural City polygons out of input point vector file                          #
# more Information on methodology:                                                      #
#   *jiang/miao 2014:  https://arxiv.org/pdf/1401.6756.pdf                              #
#   *jiang 2015: https://www.sciencedirect.com/science/article/pii/S026427511400198X    #
#                                                                                       #
#  requires saga and python-shapely                                                     #
#----------------------------------------------------------------------------------------

##natural_cities=name
##points=vector
##linelength=output vector
##natural_cities=output vector
##outputCRS=crs

# create tin
tin=processing.runalg('qgis:delaunaytriangulation', points,None)

# convert tin-polygons to lines
polygonToLines=processing.runalg('qgis:polygonstolines', tin['OUTPUT'],None)

# explode lines
explodeLines=processing.runalg('qgis:explodelines', polygonToLines['OUTPUT'],None)

# delete duplicates
deleteDup=processing.runalg('qgis:deleteduplicategeometries', explodeLines['OUTPUT'],None)

# reproject for statistics
reproj=processing.runalg('qgis:reprojectlayer', deleteDup['OUTPUT'],outputCRS,None)

#get lineproperties (requires saga geoalgorithms)
lineProp=processing.runalg('saga:lineproperties', reproj['OUTPUT'],False,False,True,linelength)

#calc basic statistics
basicStat=processing.runalg('qgis:basicstatisticsfornumericfields', lineProp['OUTPUT'],'length',None)

# extract mean (=cut-off-value)
extractbyAttribute=processing.runalg('qgis:extractbyattribute', lineProp['OUTPUT'],'length',4,basicStat['MEAN'],None)

# create polgons out of line (requires python-shapely)
polygonize=processing.runalg('qgis:polygonize',extractbyAttribute['OUTPUT'],False,True,None)

# dissolve 
diss=processing.runalg('qgis:dissolve', polygonize['OUTPUT'],True,None,None)

# multipartsToSingleParts
mtoSParts=processing.runalg('qgis:multiparttosingleparts', diss['OUTPUT'],natural_cities)

