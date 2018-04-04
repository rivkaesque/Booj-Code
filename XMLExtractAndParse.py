import urllib2
import xml.etree.ElementTree as ET
import pandas as pd

def xmltoDataframe(Columns,MultiValueColumns, XMLURL,SortBy):
    file= urllib2.urlopen(XMLurl)
    data = file.read()
    file.close()
    tree = ET.fromstring(data)
    DF=pd.DataFrame(columns=Columns)
    
    for child in tree.iter('Listing'):
            #for each child, createa a series to be added to the response dataframe
            row={}
             #iterate through the tags of each child
            for desc in child.iter():
                if desc.tag in Columns:
                    tag= desc.tag
                    if tag in MultiValueColumns:
                       #use tostring to allow for all multivalue columns to be automatically stripped
                       val=ET.tostring(desc,method='text').strip().replace('\n        ',',')
                    else:
                        val=desc.text
                    #multiple versions of description exist, so concatenate them.
                    test=''
                    if tag  in row:
                        test=row[tag]
                    row[tag]=test+str(val)
            if len(row)>1:
                #add the row to the dataframe
                DF=DF.append(row,ignore_index=True )
    return(DF.sort_values(by=[SortBy]))


XMLurl='http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
Columns=['MlsId','MlsName','DateListed','StreetAddress','Price','Bedrooms','Bathrooms','Appliances','Rooms','Description']
MultiValueColumns=['Appliances','Rooms']
SortBy='DateListed'

DF=xmltoDataframe(Columns,MultiValueColumns, XMLurl,SortBy)


DF2=DF[(pd.DatetimeIndex(DF['DateListed']).year==2016) & (DF['Description'].str.contains(" and "))]
DF2['Description'][0:1]=DF2['Description'].str[:200]
DF2.to_csv('Test.csv') 
